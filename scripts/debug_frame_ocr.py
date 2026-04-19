"""
Debug OCR on a single frame — shows raw crop, cyan mask, and EasyOCR text.

Usage:
  python scripts/debug_frame_ocr.py <video_path> [frame_sec]

Saves to results/charts/:
  debug_raw_crop.png      — bottom 10% of the frame as-is
  debug_cyan_mask.png     — HSV cyan mask after dilation
  debug_mask_on_crop.png  — cyan pixels highlighted on the raw crop

Prints the raw EasyOCR detections (text + confidence) before any regex.
"""

import sys
from pathlib import Path

import cv2
import numpy as np

try:
    import easyocr
except ImportError:
    sys.exit("easyocr not installed. Run: pip install easyocr")

ROOT     = Path(__file__).resolve().parents[1]
OUT_DIR  = ROOT / "results" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── load args ─────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    sys.exit("Usage: python debug_frame_ocr.py <video_path> [frame_sec]")

video_path = Path(sys.argv[1])
frame_sec  = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

# ── grab frame ────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    sys.exit(f"Cannot open {video_path}")

fps        = cap.get(cv2.CAP_PROP_FPS) or 30.0
frame_idx  = int(frame_sec * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
ok, frame  = cap.read()
cap.release()

if not ok:
    sys.exit(f"Could not read frame at {frame_sec}s (idx {frame_idx})")

print(f"Frame: {frame_idx}  ({frame.shape[1]}×{frame.shape[0]})  @{frame_sec}s")

# ── crop bottom 10% ───────────────────────────────────────────────────────────
h    = frame.shape[0]
crop = frame[int(h * 0.90):, :]
print(f"Crop size: {crop.shape[1]}×{crop.shape[0]} px")

# ── cyan mask ─────────────────────────────────────────────────────────────────
hsv        = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
lower_cyan = np.array([80, 80, 80],   dtype=np.uint8)
upper_cyan = np.array([105, 255, 255], dtype=np.uint8)
mask       = cv2.inRange(hsv, lower_cyan, upper_cyan)
kernel     = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
mask_dil   = cv2.dilate(mask, kernel, iterations=1)

# Overlay mask pixels as bright green on a copy of the raw crop
overlay = crop.copy()
overlay[mask_dil > 0] = (0, 255, 0)

# ── save images ───────────────────────────────────────────────────────────────
raw_path     = OUT_DIR / "debug_raw_crop.png"
mask_path    = OUT_DIR / "debug_cyan_mask.png"
overlay_path = OUT_DIR / "debug_mask_on_crop.png"

cv2.imwrite(str(raw_path),     crop)
cv2.imwrite(str(mask_path),    mask_dil)
cv2.imwrite(str(overlay_path), overlay)

print(f"\nSaved:\n  {raw_path}\n  {mask_path}\n  {overlay_path}")

# ── EasyOCR on raw RGB crop ───────────────────────────────────────────────────
print("\nLoading EasyOCR…")
reader = easyocr.Reader(["en"], gpu=False, verbose=False)

print("\n─── RAW RGB crop — EasyOCR detections (text, confidence) ───")
rgb_results = reader.readtext(
    cv2.cvtColor(crop, cv2.COLOR_BGR2RGB),
    detail=1,
    allowlist="0123456789NWnw:./-MPHmph ",
    paragraph=False,
)
if not rgb_results:
    print("  (no detections)")
for bbox, text, conf in rgb_results:
    print(f"  {conf:.2f}  '{text}'")

print("\n─── CYAN MASK — EasyOCR detections (text, confidence) ───")
mask_results = reader.readtext(
    mask_dil,
    detail=1,
    allowlist="0123456789NWnw:./-MPHmph ",
    paragraph=False,
)
if not mask_results:
    print("  (no detections)")
for bbox, text, conf in mask_results:
    print(f"  {conf:.2f}  '{text}'")

print("\n─── Full joined strings ───")
raw_joined  = " ".join(t for _, t, _ in rgb_results)
mask_joined = " ".join(t for _, t, _ in mask_results)
print(f"  RGB  : '{raw_joined}'")
print(f"  MASK : '{mask_joined}'")
