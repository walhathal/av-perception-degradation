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
**GPS extraction:** EasyOCR pipeline — 96% timestamp, 90% latitude, 44% longitude, 100% speed
**Coordinates:** 32.72–32.75 N, -117.17 to -117.19 W
**Completed:** GPS extraction pipeline built and tested, batch run complete
**Next session:** Marine layer coastal drive — 6-8 AM target
**Blockers:** Longitude OCR at 44% — fix before next batch run
**Time spent:** 4 hours

---

### Session 2 — [DATE]
**Worked on:**
**Completed:**
**Next session:**
**Blockers:**
**Time spent:**

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
