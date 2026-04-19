"""
Tag each GPS session clip with a weather condition using Open-Meteo historical API.

Makes ONE API call per clip (session start lat/lon/date), fetches hourly weather
data for that day, matches the session hour, then stamps every row in that clip
with the same weather_condition_tag.

Output: data/weather_tags/<source_csv_stem>_weather.csv
Columns: filename, timestamp, latitude, longitude, speed_mph, weather_condition_tag

Auto-detected tags (in priority order):
  wet_pavement  — any measurable precipitation (>= 0.1 mm/h)
  marine_layer  — high cloud cover + low solar radiation, no rain
  glare         — high direct solar radiation + clear sky
  clear         — everything else

Manual-only tag (use --override-tag):
  overcast      — partial/heavy cloud cover, flat diffuse light, reduced road contrast;
                  Open-Meteo cannot reliably distinguish overcast from clear at hourly resolution
"""

import argparse
import csv
import logging
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError
import json
import re

from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
GPS_DIR = ROOT / "data" / "gps_logs"
OUT_DIR = ROOT / "data" / "weather_tags"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = ROOT / "results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Open-Meteo config ───────────────────────────────────────────────────────
OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY_VARS = [
    "precipitation",        # mm — any value >= 0.1 = wet_pavement
    "cloud_cover",          # % — high + low radiation = marine_layer
    "shortwave_radiation",  # W/m² — proxy for diffuse vs. direct sunlight
    "direct_radiation",     # W/m² — direct beam; high = potential glare
]
TIMEZONE = "America/Los_Angeles"

# ── tagging thresholds ──────────────────────────────────────────────────────
PRECIP_THRESH_MM        = 0.1   # wet_pavement: >= this much rain per hour
MARINE_CLOUD_PCT        = 60    # marine_layer: cloud cover must be at least this %
MARINE_SW_THRESH_WM2    = 150   # marine_layer: shortwave radiation must be < this
GLARE_SW_THRESH_WM2     = 400   # glare: shortwave radiation must be >= this
GLARE_CLOUD_MAX_PCT     = 30    # glare: cloud cover must be < this


def _fetch_hourly_weather(
    lat: float,
    lon: float,
    date_str: str,          # "YYYY-MM-DD"
    retries: int = 3,
) -> Optional[dict]:
    """
    Fetch Open-Meteo hourly weather for one day at a given coordinate.

    Returns a dict keyed by hour (0-23) → {variable: value}, or None on failure.
    """
    params = {
        "latitude":   lat,
        "longitude":  lon,
        "start_date": date_str,
        "end_date":   date_str,
        "hourly":     ",".join(HOURLY_VARS),
        "timezone":   TIMEZONE,
    }
    url = f"{OPEN_METEO_URL}?{urlencode(params)}"

    for attempt in range(1, retries + 1):
        try:
            with urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except URLError as exc:
            log.warning("API attempt %d/%d failed: %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(2 ** attempt)
            continue

        if "hourly" not in data:
            log.warning("Unexpected API response: 'hourly' key missing")
            return None

        hourly = data["hourly"]
        # hourly["time"] is a list like ["2026-04-17T00:00", ...]
        hours_by_index = {
            datetime.fromisoformat(t).hour: i
            for i, t in enumerate(hourly["time"])
        }

        result: dict[int, dict[str, float]] = {}
        for hour, idx in hours_by_index.items():
            result[hour] = {
                var: (hourly[var][idx] if hourly[var][idx] is not None else 0.0)
                for var in HOURLY_VARS
            }
        return result

    log.error("All %d API attempts failed for %s on %s", retries, (lat, lon), date_str)
    return None


def _apply_tag(weather_at_hour: dict) -> str:
    """
    Assign a single weather_condition_tag from hourly weather metrics.

    Priority: wet_pavement > marine_layer > glare > clear
    """
    precip  = weather_at_hour.get("precipitation", 0.0)
    cloud   = weather_at_hour.get("cloud_cover", 0.0)
    sw_rad  = weather_at_hour.get("shortwave_radiation", 0.0)

    if precip >= PRECIP_THRESH_MM:
        return "wet_pavement"
    if cloud >= MARINE_CLOUD_PCT and sw_rad < MARINE_SW_THRESH_WM2:
        return "marine_layer"
    if sw_rad >= GLARE_SW_THRESH_WM2 and cloud < GLARE_CLOUD_MAX_PCT:
        return "glare"
    return "clear"


def _first_valid_row(rows: list[dict]) -> Optional[dict]:
    """Return the first CSV row with non-null lat, lon, and timestamp."""
    for row in rows:
        if (
            row.get("latitude") not in ("", "None", None)
            and row.get("longitude") not in ("", "None", None)
            and row.get("timestamp") not in ("", "None", None)
        ):
            return row
    return None


def tag_csv(gps_csv: Path, override_tag: Optional[str] = None) -> Optional[Path]:
    """
    Tag all rows of one GPS CSV with a weather_condition_tag.

    If override_tag is set, skips the API and stamps every row with that tag.
    Returns the output CSV path, or None if the file could not be processed.
    """
    rows: list[dict] = []
    try:
        with open(gps_csv, newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError as exc:
        log.error("Cannot read %s: %s", gps_csv.name, exc)
        return None

    if not rows:
        log.warning("%s is empty — skipping", gps_csv.name)
        return None

    if override_tag:
        log.info("%s → manual override: all rows tagged '%s'", gps_csv.name, override_tag)
        out_fields = ["filename", "timestamp", "latitude", "longitude", "speed_mph",
                      "weather_condition_tag"]
        out_path = OUT_DIR / f"{gps_csv.stem}_weather.csv"
        with open(out_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                row["weather_condition_tag"] = override_tag
                writer.writerow(row)
        log.info("%s → %s  (%d rows)  tags: %s=%d",
                 gps_csv.name, out_path.name, len(rows), override_tag, len(rows))
        return out_path

    anchor = _first_valid_row(rows)
    if anchor is None:
        # Fallback: infer session date/hour from the filename (2026_MMDD_HHMMSS_...)
        # Used when OCR fails to parse any timestamps (e.g. overlay format change).
        fn_match = re.match(r"(\d{4})_(\d{2})(\d{2})_(\d{2})", gps_csv.stem)
        coord_row = next(
            (r for r in rows
             if r.get("latitude") not in ("", "None", None)
             and r.get("longitude") not in ("", "None", None)),
            None,
        )
        if fn_match and coord_row:
            year, month, day = fn_match.group(1), fn_match.group(2), fn_match.group(3)
            fn_hour = int(fn_match.group(4))
            session_date = f"{year}-{month}-{day}"
            lat = float(coord_row["latitude"])
            lon = float(coord_row["longitude"])
            log.info(
                "%s → no timestamps; inferring date %s hour %02d from filename",
                gps_csv.name, session_date, fn_hour,
            )
            hourly_data = _fetch_hourly_weather(lat, lon, session_date)
            anchor = {"timestamp": f"{session_date} {fn_hour:02d}:00",
                      "latitude": coord_row["latitude"],
                      "longitude": coord_row["longitude"]}
        else:
            log.warning("%s has no valid GPS rows — all rows will be tagged 'unknown'", gps_csv.name)
            hourly_data = None
            session_date = None
    else:
        lat = float(anchor["latitude"])
        lon = float(anchor["longitude"])
        ts  = anchor["timestamp"]   # "YYYY-MM-DD HH:MM"
        try:
            ts_norm      = ts.replace(".", ":", 1) if re.search(r"\d{2}\.\d{2}$", ts) else ts
            session_dt   = datetime.strptime(ts_norm, "%Y-%m-%d %H:%M")
            session_date = session_dt.strftime("%Y-%m-%d")
        except ValueError:
            log.warning("Cannot parse timestamp '%s' in %s", ts, gps_csv.name)
            hourly_data  = None
            session_date = None
        else:
            log.info(
                "%s  →  anchor: %s  %.4f, %.4f  →  fetching %s",
                gps_csv.name, ts, lat, lon, session_date,
            )
            hourly_data = _fetch_hourly_weather(lat, lon, session_date)

    # Build a lookup: row-timestamp hour → tag (computed once, shared across rows)
    tag_cache: dict[int, str] = {}

    def _row_tag(row: dict) -> str:
        """Resolve the tag for a single row."""
        if hourly_data is None:
            return "unknown"
        raw_ts = row.get("timestamp")
        if raw_ts in ("", "None", None):
            # Fall back to the session-level anchor hour
            anchor_ts = anchor["timestamp"] if anchor else None
            if anchor_ts is None:
                return "unknown"
            raw_ts = anchor_ts
        try:
            # EasyOCR sometimes reads "HH:MM" as "HH.MM" — normalise before parsing
            normalised = raw_ts.replace(".", ":", 1) if re.search(r"\d{2}\.\d{2}$", raw_ts) else raw_ts
            hour = datetime.strptime(normalised, "%Y-%m-%d %H:%M").hour
        except ValueError:
            return "unknown"
        if hour not in tag_cache:
            weather = hourly_data.get(hour)
            tag_cache[hour] = _apply_tag(weather) if weather else "unknown"
        return tag_cache[hour]

    out_fields = ["filename", "timestamp", "latitude", "longitude", "speed_mph",
                  "weather_condition_tag"]
    out_path = OUT_DIR / f"{gps_csv.stem}_weather.csv"

    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            row["weather_condition_tag"] = _row_tag(row)
            writer.writerow(row)

    tag_counts: dict[str, int] = {}
    for row in rows:
        t = row["weather_condition_tag"]
        tag_counts[t] = tag_counts.get(t, 0) + 1

    log.info(
        "%s → %s  (%d rows)  tags: %s",
        gps_csv.name, out_path.name, len(rows),
        "  ".join(f"{k}={v}" for k, v in sorted(tag_counts.items())),
    )
    return out_path


def _write_run_log(summary: list[dict]) -> None:
    """Persist a per-clip summary CSV to results/logs/ for traceability."""
    if not summary:
        return
    log_path = LOG_DIR / f"weather_tagging_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    fields = ["clip", "session_date", "rows", "wet_pavement", "marine_layer", "glare",
              "clear", "overcast", "unknown"]
    with open(log_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(summary)
    log.info("Run log → %s", log_path)


def main() -> None:
    """Process GPS CSVs in data/gps_logs/ — optionally filtered to one session folder.

    Positional argument (optional):
      path  — a GPS CSV file, a raw_footage session folder, or omitted for all CSVs

    Optional flags:
      --override-tag TAG  — skip API and stamp every row with TAG (e.g. overcast)
    """
    parser = argparse.ArgumentParser(description="Tag GPS session CSVs with weather conditions.")
    parser.add_argument("path", nargs="?", help="GPS CSV, session folder, or omit for all")
    parser.add_argument(
        "--override-tag",
        metavar="TAG",
        help="Skip API and force all rows to this tag (e.g. --override-tag overcast)",
    )
    args = parser.parse_args()

    if args.path:
        arg = Path(args.path)
        if arg.is_dir():
            clip_stems = {p.stem for p in arg.rglob("*F.MP4")} | {p.stem for p in arg.rglob("*f.mp4")}
            if not clip_stems:
                log.error("No front-camera MP4s found in session folder %s", arg)
                sys.exit(1)
            targets = sorted(
                GPS_DIR / f"{stem}_gps.csv"
                for stem in sorted(clip_stems)
                if (GPS_DIR / f"{stem}_gps.csv").exists()
            )
        else:
            targets = [arg]
    else:
        targets = sorted(GPS_DIR.glob("*_gps.csv"))

    if not targets:
        log.error("No GPS CSVs found in %s", GPS_DIR)
        log.error("Run extract_gps_ocr.py first to generate them.")
        sys.exit(1)

    override_tag: Optional[str] = args.override_tag
    if override_tag:
        log.info("Override tag active: '%s' — API calls skipped", override_tag)
    log.info("Found %d GPS CSV(s) to tag", len(targets))

    summary: list[dict] = []
    for gps_csv in tqdm(targets, desc="Clips", unit="clip"):
        out_path = tag_csv(gps_csv, override_tag=override_tag)
        if out_path is None:
            continue

        # Gather stats for the run log
        tag_counts: dict[str, int] = {k: 0 for k in
                                       ("wet_pavement", "marine_layer", "glare",
                                        "clear", "overcast", "unknown")}
        session_date = "unknown"
        with open(out_path, newline="") as fh:
            rows = list(csv.DictReader(fh))
        for row in rows:
            t = row.get("weather_condition_tag", "unknown")
            tag_counts[t] = tag_counts.get(t, 0) + 1
            if session_date == "unknown" and row.get("timestamp") not in ("", "None", None):
                try:
                    session_date = row["timestamp"][:10]
                except (IndexError, TypeError):
                    pass

        entry = {"clip": gps_csv.name, "session_date": session_date, "rows": len(rows)}
        entry.update(tag_counts)
        summary.append(entry)

        # Rate-limit: be respectful to the free API (skip when overriding)
        if len(targets) > 1 and not override_tag:
            time.sleep(1)

    _write_run_log(summary)

    # ── terminal summary ─────────────────────────────────────────────────────
    if not summary:
        return
    total = sum(r["rows"] for r in summary)
    print("\n" + "=" * 84)
    print(f"{'Clip':<40} {'rows':>5}  {'wet':>4}  {'marine':>6}  {'glare':>5}  {'ovcst':>5}  {'clear':>5}")
    print("-" * 84)
    for r in summary:
        print(
            f"{r['clip']:<40} {r['rows']:>5}  "
            f"{r['wet_pavement']:>4}  {r['marine_layer']:>6}  "
            f"{r['glare']:>5}  {r.get('overcast', 0):>5}  {r['clear']:>5}"
        )
    print("-" * 84)
    print(
        f"{'TOTAL':<40} {total:>5}  "
        f"{sum(r['wet_pavement'] for r in summary):>4}  "
        f"{sum(r['marine_layer'] for r in summary):>6}  "
        f"{sum(r['glare'] for r in summary):>5}  "
        f"{sum(r.get('overcast', 0) for r in summary):>5}  "
        f"{sum(r['clear'] for r in summary):>5}"
    )
    print("=" * 84 + "\n")
    log.info("Weather-tagged CSVs saved to %s", OUT_DIR)


if __name__ == "__main__":
    main()
