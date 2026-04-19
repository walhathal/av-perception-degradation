# AV Capstone — Claude Code Context
*Read this file at the start of every session. This is the permanent project briefing.*

---

## Who I am
Wael — civil engineer pivoting into AI/ML, pursuing a Master's in Applied AI.
My CE background is the research differentiator for this project. I can score infrastructure
degradation with domain authority that a pure ML researcher cannot replicate.

---

## Research question
How does road infrastructure condition (pavement degradation, faded lane markings, poor geometry)
compound with San Diego's coastal environmental variables (marine layer, sun glare, wet pavement)
to create measurable perception failure modes in monocular autonomous vision systems?

---

## Project context
- This is an independent research project AND potential Master's capstone (TBD in ~6 months)
- Target audience: AV company recruiters (Waymo, Zoox) + academic reviewers
- Public outputs: LinkedIn, YouTube, GitHub, arXiv preprint
- Timeline: April – December 2026
- Current phase: CHECK phase_log.md for current status

---

## Sensor setup
- Camera: VIOFO A329S (2 or 3-channel), Sony STARVIS 2, 4K front + 2K rear
- GPS: Built-in quad-system (precise lat/lon/speed/timestamp per frame)
- Storage: Rotating 512GB high-endurance microSD cards
- Modality: MONOCULAR VISION ONLY — do not suggest LiDAR solutions yet

---

## Study area
- Primary: All San Diego routes — coastal (La Jolla, PB, Mission Bay), downtown, freeways (I-5/I-8/I-15), suburban
- Extended: Road trips as needed
- 5 weather condition tags: `clear`, `overcast`, `marine_layer`, `glare`, `wet_pavement`

---

## Three-layer research stack
1. Infrastructure condition layer — YOLOv8 fine-tuned on CE-scored footage
2. Environmental condition layer — Open-Meteo API weather tagging by GPS + timestamp
3. Perception performance layer — UFLD lane detection confidence vs infra score × weather tag
Benchmark: Waymo Open Dataset (Phase 4)

---

## Folder structure
```
av-capstone/
├── data/
│   ├── raw_footage/        ← VIOFO MP4 files (never modify originals)
│   ├── gps_logs/           ← extracted GPS CSVs
│   ├── weather_tags/       ← weather-tagged drive session logs
│   └── labeled_frames/     ← Roboflow export for YOLO training
├── models/
│   ├── yolo_infra/         ← YOLOv8 checkpoints
│   └── lane_detection/     ← UFLD / LaneATT checkpoints
├── notebooks/              ← Jupyter EDA only — not production code
├── scripts/                ← production Python scripts
├── results/
│   ├── maps/               ← Folium/Plotly HTML outputs
│   ├── charts/             ← PNG + HTML visualizations
│   └── logs/               ← per-session result CSVs
├── docs/
│   ├── rubric.md           ← CE degradation rubric (source of truth)
│   └── literature/         ← paper summaries
├── social/                 ← LinkedIn + YouTube script drafts
├── CLAUDE.md               ← this file
└── SKILL.md                ← Claude Cowork context
```

---

## Tech stack
- Python 3.11
- PyTorch (model training + inference)
- Ultralytics YOLOv8 (infrastructure defect detection)
- OpenCV (video processing, frame extraction)
- Pandas (data manipulation, results logging)
- Folium + Plotly (interactive maps, visualizations)
- Roboflow (frame annotation for YOLO training)
- Open-Meteo API (free, no key required for historical data)
- Git / GitHub (version control — commit every working session)

---

## My coding style preferences
- I am a beginner-intermediate Python coder — I rely on vibe coding with Claude
- ALWAYS add type hints to function signatures
- ALWAYS add a docstring to every function (one-liner is fine for simple functions)
- NEVER just print() results — always log to CSV in results/logs/
- Save ALL plots to results/charts/ as both PNG and interactive HTML
- Use tqdm for any loop over files or frames (I need to see progress)
- Handle errors gracefully — never let a bad file crash the whole pipeline
- When I say "write a script", put it in /scripts/ not a notebook
- When I say "explore" or "check", use a notebook in /notebooks/

---

## Important constraints
- Raw footage in data/raw_footage/ is NEVER modified or deleted — always read-only
- Do not suggest paid APIs — use free alternatives (Open-Meteo not OpenWeatherMap paid tier)
- Do not suggest cloud training — everything runs locally for now
- Always check that a library is pip-installable before recommending it
- If a task will take >10 minutes to run, add a progress bar and estimated time

---

## How to start each session
1. Read this file
2. Read phase_log.md to know current status and next task
3. Confirm with me what we're working on before writing any code
4. Use /plan for any task touching more than 2 files

---

## GitHub conventions
- Branch: work on `main` for now (solo project)
- Commit message format: `[phase-N] short description of what was done`
- Example: `[phase-1] add weather tagging pipeline with Open-Meteo API`
- Never commit raw MP4 files — add data/raw_footage/ to .gitignore

---

## Terminology (use these exact terms consistently)
- "Degradation score" not "quality score"
- "Infrastructure condition" not "road quality"  
- "Weather condition tag" not "weather label"
- "Compound failure" not "combined failure"
- "Monocular perception" not just "camera-based"
- "Coastal environment" to describe San Diego context

---

*Version 1.0 — April 2026*
