"""
Extract GPS data burned into VIOFO dashcam overlay using OCR.

Samples one frame every 5 seconds, crops the bottom 10% where the overlay lives,
runs EasyOCR on the raw RGB crop, parses speed/lat/lon/timestamp, and saves to CSV.

Output: data/gps_logs/<video_stem>_gps.csv
Columns: filename, timestamp, latitude, longitude, speed_mph

Usage:
  python extract_gps_ocr.py                          # all sessions under data/raw_footage/
  python extract_gps_ocr.py data/raw_footage/session_2026_0418/   # one session folder
  python extract_gps_ocr.py path/to/clip.MP4         # single file
"""

import csv
import logging
import multiprocessing
import re
import sys
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

try:
    import easyocr
except ImportError:
    sys.exit("easyocr not installed. Run: pip install easyocr")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── paths ──────────────────────────────────────────────────────────────────────
ROOT    = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_footage"
OUT_DIR = ROOT / "data" / "gps_logs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Seconds between sampled frames — 5× faster than 1 fps, still captures every GPS fix
SAMPLE_INTERVAL_SEC = 5

# Parallel workers — 4 clips processed simultaneously
NUM_WORKERS = 4

# ── per-worker EasyOCR reader (initialised once per process) ──────────────────
_worker_reader: "easyocr.Reader | None" = None


def _init_worker() -> None:
    """Initialise the EasyOCR reader inside each pool worker (avoids pickle issues)."""
    global _worker_reader
    log.info("Worker PID %d: loading EasyOCR model…", multiprocessing.current_process().pid)
    _worker_reader = easyocr.Reader(["en"], gpu=False, verbose=False)


# ── regex patterns for VIOFO overlay text ──────────────────────────────────────
# Sessions 1-2 format: "010MPH  N:32.7302  W:117.1667  17/04/2026 11:41:41"
# Session 3+ format:   "010MPH  N:32.7302  W:117.1667  2026-04-19 09:09:10"  (ISO after camera fix)
_RE_LAT = re.compile(r"N[:\s]?(\d{1,3}\.\d+)", re.IGNORECASE)
# EasyOCR sometimes splits "W:117.1667" → "W:117 1667" or "W:117 . 1667"
# No \b at end: \b fails when decimal is followed by another digit (OCR noise adds 5th digit)
# or when the next field starts with a letter (no space between fields). (\d{4}) stops
# naturally at the first non-digit, so no boundary assertion is needed.
_RE_LON = re.compile(r"W[:\s]?(\d{1,3})\s*\.?\s*(\d{4})", re.IGNORECASE)
_RE_SPD = re.compile(r"(\d{1,3})\s*MPH", re.IGNORECASE)
# Legacy: DD/MM/YYYY HH:MM[:SS] [AM/PM]
_RE_TS     = re.compile(r"(\d{2}/\d{2}/\d{4})\s*(\d{2}[:.]\d{2})(?:[:.]\d{2})?(?:\s*([AaPp][Mm]))?", re.IGNORECASE)
# ISO: YYYY-MM-DD HH:MM[:SS] — OCR may insert a space before seconds, hence \s* before SS
_RE_TS_ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2})[:.]\s*(\d{2})", re.IGNORECASE)


def _parse_overlay(text: str) -> dict:
    """Parse OCR text into structured GPS fields. Returns None values for misses."""
    text = re.sub(r"\.{2,}", ".", text)   # collapse consecutive dots (OCR artifact)

    lat_m      = _RE_LAT.search(text)
    lon_m      = _RE_LON.search(text)
    spd_m      = _RE_SPD.search(text)
    ts_m       = _RE_TS.search(text)
    ts_iso_m   = _RE_TS_ISO.search(text)

    timestamp = None
    if ts_iso_m:
        # ISO format: YYYY-MM-DD HH:MM (Session 3+)
        year_s, month_s, day_s = ts_iso_m.group(1), ts_iso_m.group(2), ts_iso_m.group(3)
        hour, minute = int(ts_iso_m.group(4)), int(ts_iso_m.group(5))
        if (1 <= int(day_s) <= 31 and 1 <= int(month_s) <= 12 and 2020 <= int(year_s) <= 2035
                and 0 <= hour <= 23 and 0 <= minute <= 59):
            timestamp = f"{year_s}-{month_s}-{day_s} {hour:02d}:{minute:02d}"
    elif ts_m:
        # Legacy DD/MM/YYYY HH:MM [AM/PM] format (Sessions 1-2)
        day_s, month_s, year_s = ts_m.group(1).split("/")
        time_s = ts_m.group(2).replace(".", ":")   # normalise dot separator
        ampm   = (ts_m.group(3) or "").upper()
        day, month, year = int(day_s), int(month_s), int(year_s)
        hour, minute     = int(time_s[:2]), int(time_s[3:5])

        # 12-hour → 24-hour conversion when AM/PM token is present
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        # Reject impossible dates/times produced by OCR digit misreads (e.g. day=78)
        if (1 <= day <= 31 and 1 <= month <= 12 and 2020 <= year <= 2035
                and 0 <= hour <= 23 and 0 <= minute <= 59):
            timestamp = f"{year_s}-{month_s}-{day_s} {hour:02d}:{minute:02d}"

    lat = float(lat_m.group(1)) if lat_m else None
    lon = -float(f"{lon_m.group(1)}.{lon_m.group(2)}") if lon_m else None

    # Reject coordinates outside the San Diego study area (catches OCR digit misreads)
    if lat is not None and not (31.0 <= lat <= 34.0):
        lat = None
    if lon is not None and not (-119.0 <= lon <= -115.0):
        lon = None

    return {
        "timestamp": timestamp,
        "latitude":  lat,
        "longitude": lon,
        "speed_mph": int(spd_m.group(1)) if spd_m else None,
    }


def _ocr_crop(crop: np.ndarray) -> str:
    """Run EasyOCR on the overlay crop and return all detected text as one string.

    EasyOCR handles cyan text natively from the raw RGB image. A binary cyan mask
    was tested but degrades character detail (W→M, digit dropout), lowering parse rates.
    """
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    results = _worker_reader.readtext(
        rgb,
        detail=0,
        allowlist="0123456789NWnw:./-MPHmph ",
        paragraph=False,
    )
    return " ".join(results)


def extract_gps_from_video(video_path: Path) -> "Path | None":
    """
    Extract GPS overlay data from a single MP4 file at 1 frame per SAMPLE_INTERVAL_SEC.

    Returns the output CSV path, or None if the video could not be opened.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        log.warning("Cannot open %s — skipping", video_path.name)
        return None

    fps          = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step   = max(1, int(round(fps * SAMPLE_INTERVAL_SEC)))
    total_secs   = max(1, total_frames // frame_step)

    out_path   = OUT_DIR / f"{video_path.stem}_gps.csv"
    fieldnames = ["filename", "timestamp", "latitude", "longitude", "speed_mph"]

    rows_written = 0
    frame_idx    = 0

    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()

        with tqdm(total=total_secs, desc=video_path.name, unit="s",
                  position=multiprocessing.current_process()._identity[0]
                  if multiprocessing.current_process()._identity else 0,
                  leave=True) as pbar:
            while True:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ok, frame = cap.read()
                if not ok:
                    break

                try:
                    h    = frame.shape[0]
                    crop = frame[int(h * 0.90):, :]
                    text = _ocr_crop(crop)
                    parsed = _parse_overlay(text)
                    parsed["filename"] = video_path.name
                    writer.writerow(parsed)
                    rows_written += 1
                except Exception as exc:
                    log.debug("Frame %d in %s — OCR error: %s", frame_idx, video_path.name, exc)
                    writer.writerow({"filename": video_path.name,
                                     "timestamp": None, "latitude": None,
                                     "longitude": None, "speed_mph": None})

                frame_idx += frame_step
                pbar.update(1)

    cap.release()

    if rows_written == 0:
        log.warning("%s — no rows extracted; OCR may have failed entirely", video_path.name)
    else:
        log.info("%s → %s  (%d rows)", video_path.name, out_path.name, rows_written)

    return out_path


def _parse_rates(csv_path: Path) -> dict:
    """Return per-field parse rates for a completed GPS CSV."""
    rows = []
    with open(csv_path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return {"total": 0, "timestamp": 0, "latitude": 0, "longitude": 0, "speed_mph": 0}
    n = len(rows)
    return {
        "total":     n,
        "timestamp": sum(1 for r in rows if r["timestamp"] not in ("", "None", None)),
        "latitude":  sum(1 for r in rows if r["latitude"]  not in ("", "None", None)),
        "longitude": sum(1 for r in rows if r["longitude"] not in ("", "None", None)),
        "speed_mph": sum(1 for r in rows if r["speed_mph"] not in ("", "None", None)),
    }


def _process_clip(video_path_str: str) -> "dict | None":
    """Worker entry point: extract GPS from one clip and return parse-rate dict."""
    video_path = Path(video_path_str)
    out_csv    = extract_gps_from_video(video_path)
    if out_csv is None or not out_csv.exists():
        return None
    rates = _parse_rates(out_csv)
    rates["clip"]     = video_path.name
    rates["csv_path"] = str(out_csv)
    return rates


def main() -> None:
    """Process front-camera MP4s or a single file / session folder passed as argv[1]."""
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        if arg.is_dir():
            targets = sorted(arg.rglob("*F.MP4")) + sorted(arg.rglob("*f.mp4"))
        else:
            targets = [arg]
    else:
        targets = sorted(RAW_DIR.rglob("*F.MP4")) + sorted(RAW_DIR.rglob("*f.mp4"))

    if not targets:
        log.error("No front-camera MP4 files found under %s", RAW_DIR)
        sys.exit(1)

    log.info(
        "Found %d front-camera clip(s) — sampling every %ds, %d parallel workers",
        len(targets), SAMPLE_INTERVAL_SEC, NUM_WORKERS,
    )

    results: list[dict] = []
    with multiprocessing.Pool(processes=NUM_WORKERS, initializer=_init_worker) as pool:
        with tqdm(total=len(targets), desc="Clips completed", unit="clip") as pbar:
            for result in pool.imap_unordered(_process_clip, [str(p) for p in targets]):
                if result:
                    results.append(result)
                pbar.update(1)

    log.info("Done. CSVs saved to %s", OUT_DIR)

    if not results:
        return

    results.sort(key=lambda r: r["clip"])

    # ── summary table ──────────────────────────────────────────────────────────
    print("\n" + "=" * 78)
    print(f"{'Clip':<42} {'rows':>5}  {'ts%':>4}  {'lat%':>4}  {'lon%':>4}  {'spd%':>4}  {'all4%':>5}")
    print("-" * 78)
    totals = {"total": 0, "timestamp": 0, "latitude": 0, "longitude": 0, "speed_mph": 0}
    for r in results:
        n = r["total"] or 1
        with open(r["csv_path"], newline="") as fh:
            all4 = sum(
                1 for row in csv.DictReader(fh)
                if all(row[f] not in ("", "None", None)
                       for f in ("timestamp", "latitude", "longitude", "speed_mph"))
            )
        print(
            f"{r['clip']:<42} {n:>5}  "
            f"{100*r['timestamp']//n:>3}%  "
            f"{100*r['latitude']//n:>3}%  "
            f"{100*r['longitude']//n:>3}%  "
            f"{100*r['speed_mph']//n:>3}%  "
            f"{100*all4//n:>4}%"
        )
        for k in totals:
            totals[k] += r[k]
    print("-" * 78)
    tn = totals["total"] or 1
    print(
        f"{'TOTAL':<42} {totals['total']:>5}  "
        f"{100*totals['timestamp']//tn:>3}%  "
        f"{100*totals['latitude']//tn:>3}%  "
        f"{100*totals['longitude']//tn:>3}%  "
        f"{100*totals['speed_mph']//tn:>3}%"
    )
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()
