# Phase Log — AV Capstone
## Infrastructure-Conditioned Perception Degradation in Autonomous Monocular Vision

---

## Current Phase: 1 — Data Pipeline & CE Rubric
## Current Status: STARTING — April 2026

---

## Phase 1 Checklist (Apr – May 2026)

### Setup
- [ ] Folder structure created on local machine
- [ ] GitHub repo initialized and made public
- [ ] CLAUDE.md placed in repo root
- [ ] SKILL.md placed in repo root
- [ ] .gitignore configured (raw footage, model weights excluded)
- [ ] README.md published (placeholder is fine)
- [ ] Claude Project created on claude.ai
- [ ] PROJECT_CHARTER.md, CLAUDE.md, SKILL.md uploaded to Claude Project

### Data engineering
- [ ] Claude Code installed in VS Code
- [ ] GPS extraction script written (VIOFO MP4 → CSV)
- [ ] GPS extraction tested on at least 1 real drive file
- [ ] Open-Meteo weather tagging function written
- [ ] Weather tagging tested and producing correct tags
- [ ] Full pipeline: drive → GPS CSV → weather-tagged CSV working end to end

### Field work
- [ ] Drive session 1 completed (coastal route — marine layer target)
- [ ] Drive session 2 completed (urban grid + freeways)
- [ ] Drive session 3 completed (afternoon — glare target)
- [ ] At least one example of each weather condition captured

### CE Rubric
- [ ] Draft of rubric written (4 categories, 0-10 scale)
- [ ] Rubric saved as docs/rubric.md
- [ ] Rubric reviewed and finalized
- [ ] Rubric published as PDF for LinkedIn

### Public presence
- [ ] GitHub repo public with placeholder README
- [ ] LinkedIn post 1 drafted
- [ ] LinkedIn post 1 published

---

## Phase 1 Definition of Done
GPS CSV + weather tag pipeline running on real footage AND CE rubric document published.

---

## Session Log

### Session 1 — 2026-04-17
**Route:** Coastal — Mission Beach, Pacific Beach and La Jolla
**Condition tag:** clear
**Time:** 11:41 AM – 12:47 PM
**Duration:** 66 minutes
**Clips collected:** 21 front camera (F) MP4s
**GPS extraction:** EasyOCR pipeline — 96% timestamp, 90% latitude, 95% longitude, 100% speed (re-run 2026-04-19 after `\b` regex fix; original was 44%; re-run 2026-05-07 after `W[:\s]*` fix)
**Coordinates:** 32.72–32.75 N, -117.17 to -117.19 W
**Completed:** GPS extraction pipeline built and tested, batch run complete
**Next session:** Marine layer coastal drive — 6-8 AM target
**Blockers:** Longitude still at 49% after regex fix — remaining misses are OCR detection failures on low-contrast frames, not regex. CLAHE preprocessing flagged as pre-Phase 2 task to push toward 85%+
**Time spent:** 4 hours

---

### Session 2 — 2026-04-18
**Route:** Coastal / Urban mix
**Condition tag:** glare (12:40–12:58 PM), clear (1:00–2:27 PM)
**Time:** 12:40 PM – 2:27 PM
**Duration:** ~107 minutes
**Clips collected:** 36 front camera (F) MP4s
**GPS extraction:** Raw RGB pipeline — 80% timestamp, 89% latitude, 71% longitude, 100% speed (re-run 2026-04-19 after `\b` regex fix; re-run 2026-05-07 after `W[:\s]*` fix)
**Completed:** Weather tagging pipeline tested, camera settings optimized for all future drives
**Next session:** Marine layer coastal drive — 6-8 AM target
**Blockers:** 12-hour timestamp bug in April 18 data — fixed in camera for future sessions. Longitude at 62% due to midday glare washing out cyan overlay; CLAHE preprocessing required to improve
**Time spent:** ~3 hours

---

### Session 3 — 2026-04-19
**Route:** Urban (Downtown → Bankers Hills area)
**Condition tag:** overcast (visual review — partial-to-heavy cloud cover, flat diffuse light, reduced road contrast; Open-Meteo returned `clear` for this hour, which reflects an API limitation: the hourly aggregate masked partial overcast conditions that were visually present)
**Time:** 9:08 AM – 9:44 AM
**Duration:** ~36 minutes
**Clips collected:** 13 front camera (F) MP4s
**GPS extraction:** Raw RGB pipeline — 98% timestamp, 98% latitude, 74% longitude, 100% speed (re-run 2026-05-07 after `W[:\s]*` fix)
**Completed:** GPS CSV + weather-tagged CSV pipeline complete end-to-end with real timestamps
**Bug fixed:** Camera timestamp format changed to ISO (YYYY-MM-DD HH:MM:SS) after April 18 camera fix — `_RE_TS_ISO` regex added to `extract_gps_ocr.py`; `tag_weather.py` now has filename-date fallback for future zero-timestamp edge cases
**Time spent:** ~2 hours

---
### Session 4 — 2026-04-22
**Route:** I-94, I-5, I-8, El Cajon Blvd, Main St (San Diego → El Cajon)
**Condition tag:** glare
**Time:** 6:20 PM – 7:10 PM
**Duration:** ~50 minutes
**Clips collected:** 14 front camera (F) MP4s
**GPS extraction:** OCR pipeline — 96% timestamp, 98% latitude, 42% longitude, 98% speed
**Completed:** GPS extraction and weather tagging complete. First freeway session (I-8 corridor). Longitude at 42% on three clips (321, 323, 325) — root cause is sunset glare washing out W: field on overlay. Known limitation, flagged for CLAHE preprocessing pre-Phase 2. Open-Meteo returned clear — overridden to glare based on visual conditions (direct sun, eastbound I-8, 6:20–7:10 PM).
**Next session:** Marine layer coastal drive — 6–8 AM target (La Jolla/PB corridor)
**Blockers:** Longitude OCR degraded under direct glare — confirms sunset glare as primary driver of W: field detection failures
**Time spent:** ~1 hour
---
### Session 5 — 2026-04-24
**Route:** Mission Bay, Sunset Cliffs, Harbor Dr, Downtown San Diego
**Condition tag:** overcast
**Time:** 5:30 PM – 7:26 PM
**Duration:** ~116 minutes
**Clips collected:** 33 front camera (F) MP4s
**GPS extraction:** OCR pipeline — 96% timestamp, 99% latitude, 73% longitude, 100% speed (re-run 2026-05-07 after `W[:\s]*` fix)
**Completed:** GPS extraction and weather tagging complete. Longest session to date (33 clips, 1,068 rows). Open-Meteo returned mixed tags (glare/clear/marine_layer) — all overridden to overcast based on visual conditions (partial to full cloud cover throughout). Hour 19 marine_layer tag confirmed as sunset physics not coastal fog.
**Next session:** Marine layer coastal drive — 6–8 AM target (La Jolla/PB corridor)
**Blockers:** Longitude at 72% — consistent with prior sessions, no action needed pre-Phase 2
**Time spent:** ~2 hours
---

### Session 6 — 2026-04-25
**Route:** Fiesta Island, Mission Valley, Hillcrest, Downtown San Diego
**Condition tag:** wet_pavement
**Time:** 3:49 PM – 4:52 PM
**Duration:** ~63 minutes
**Clips collected:** 17 front camera (F) MP4s
**GPS extraction:** OCR pipeline — 98% timestamp, 100% latitude, 61% longitude, 100% speed
**Completed:** GPS extraction and weather tagging complete. First `wet_pavement` session in dataset. Open-Meteo confirmed measurable precipitation for April 25 — no override needed; API tag accepted as-is. 600 total rows, all 17 clips tagged `wet_pavement`.
**Next session:** Marine layer coastal drive — 6–8 AM target (La Jolla/PB corridor)
**Blockers:** Longitude at 61% — consistent with wet/overcast conditions reducing overlay contrast. Known limitation, flagged for CLAHE preprocessing pre-Phase 2.
**Time spent:** ~1 hour
---
### Session 7 — 2026-05-02
**Route:** I-5 North, San Diego (Miramar) → Long Beach (405/I-22 interchange)
**Condition tag:** marine_layer
**Time:** 10:43 AM – 11:57 AM
**Duration:** ~74 minutes
**Clips collected:** 25 front camera (F) MP4s
**GPS extraction:** OCR pipeline — 94% timestamp, 99% latitude, 100% longitude, 100% speed (regex fix `W[:\s]*` applied same session)
**Completed:** GPS extraction and weather tagging complete. First session leaving San Diego County — route extended to LA County (Torrance/Long Beach). Open-Meteo returned clear (falls through all thresholds) — overridden to marine_layer based on visual conditions (coastal fog, flat diffuse light, suppressed direct radiation at 25% of shortwave at hour 10) and entirely coastal I-5 corridor route. First confirmed marine_layer session — all 5 condition tags now captured.
**Next session:** CE rubric scoring + Phase 2 planning
**Blockers:** None — longitude resolved to 100% after `W[:\s]*` regex fix applied same session
**Time spent:** ~1 hour


## Pipeline Debug Log

### Longitude OCR — 2026-04-19
**Issue:** Longitude parse rates below target across all three sessions (44–73%)
**Root cause investigation:**
- `\b` word boundary in `_RE_LON` caused silent misses when decimal had 5+ OCR digits or when the next field started with a letter (no space between fields)
- Fix: removed `\b` from regex — `(\d{4})` stops naturally at the first non-digit
- Result: Session 1 recovered +5pp (44% → 49%); Sessions 2 and 3 unchanged
**True root cause for remaining misses:** OCR detection failure — EasyOCR does not emit a `W:` token for frames where the cyan overlay has insufficient contrast (glare, flat light). No regex change can recover these.
**Next step:** Implement CLAHE (Contrast Limited Adaptive Histogram Equalization) preprocessing on the overlay crop before passing to EasyOCR. Target: 85%+ longitude across all sessions. Flag as **pre-Phase 2 task** before labeling begins.

---

## Phase 2 Preview (May – Jun 2026)
- Label 500–1000 frames using CE rubric (Roboflow)
- Fine-tune YOLOv8 on infrastructure degradation categories
- Map per-segment degradation scores to GPS (Folium)
- YouTube video 1

## Phase 3 Preview (Jul – Aug 2026)
- UFLD lane detection pipeline across all footage
- Failure logging: confidence vs infra_score × weather_tag
- Demo-ready prototype

## Phase 4 Preview (Sep – Oct 2026)
- Waymo Open Dataset access and benchmark
- Compound failure risk matrix
- Waymo-tagging LinkedIn post

## Phase 5 Preview (Nov – Dec 2026)
- arXiv preprint / ITSC workshop paper
- Full interactive San Diego risk map
- Clean public GitHub repo

---

*Update this file at the end of every working session. Re-upload to Claude Project after each update.*
