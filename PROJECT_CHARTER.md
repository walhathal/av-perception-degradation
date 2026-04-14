# Project Charter
## Infrastructure-Conditioned Perception Degradation in Autonomous Monocular Vision
### A San Diego Coastal Environment Study

---

## 1. Project Overview

**Project Title:** Infrastructure-Conditioned Perception Degradation in Autonomous Monocular Vision: A San Diego Coastal Environment Study

**Researcher:** Wael  
**Program:** Master's in Applied AI  
**Start Date:** April 2026  
**Target Completion:** December 2026  
**Status:** Active — Phase 1

**One-sentence pitch:**
> I'm a civil engineer and AI researcher quantifying how road infrastructure degradation compounds with San Diego's coastal weather to create measurable perception failures in monocular autonomous vision systems — benchmarked against the Waymo Open Dataset.

---

## 2. The Problem

Autonomous vehicle perception research almost universally assumes the road surface is a clean, known quantity. It isn't.

In real-world deployments — especially in coastal urban environments like San Diego — two compounding variables are routinely ignored:

1. **Infrastructure degradation:** Faded lane markings, cracked pavement, poor road geometry, worn surface texture
2. **Coastal environmental conditions:** Marine layer/fog, direct sun glare, wet pavement after coastal drizzle

No published research treats these two variables as a *compound* failure system. This project fills that gap, using a civil engineer's domain expertise to score infrastructure conditions with credibility that a pure ML researcher cannot replicate.

---

## 3. Research Question

> *How does road infrastructure condition — pavement degradation, faded lane markings, and poorly designed geometry — compound with San Diego's coastal environmental variables (marine layer, sun glare, wet pavement) to create measurable perception failure modes in monocular autonomous vision systems?*

### Hypotheses
- H1: Perception accuracy degrades significantly faster when infrastructure degradation and adverse weather co-occur than when either variable appears alone
- H2: Faded lane markings under marine layer/fog conditions represent the highest-risk compound failure mode in the San Diego coastal corridor
- H3: The Waymo Open Dataset underrepresents the specific infra+weather failure combinations most common in San Diego's coastal environment

---

## 4. Researcher Background & Unique Advantage

**Civil Engineering background** — enables domain-credible infrastructure scoring. Unlike pure ML researchers, the investigator can define *why* a road surface is degraded, not just that a model failed to detect it. This is the core research differentiator.

**Applied AI Master's program** — active coursework in ML interpretability, smart cities, autonomous systems ethics, and urban technology governance directly informs the research framing.

**Local knowledge** — San Diego resident with direct access to the coastal corridors where marine layer, glare, and pavement degradation intersect most frequently.

---

## 5. Sensor Setup

| Component | Spec | Notes |
|-----------|------|-------|
| Camera | VIOFO A329S (2 or 3-channel) | Sony STARVIS 2 sensor, 4K front + 2K rear |
| GPS | Built-in quad-system (GPS/BeiDou/Galileo/GLONASS) | Precise location + speed logging |
| Storage | 2× 512GB high-endurance microSD (rotated per session) | SanDisk Max Endurance or Samsung Pro Endurance |
| Archive | 2TB external desktop drive | Session offload after every drive |
| Modality | Monocular vision (camera only) | LiDAR upgrade planned post-December 2026 |

**Monocular framing note:** This project is explicitly scoped as monocular perception research. This is a legitimate and active research subfield. LiDAR, when added, will serve as a Phase 2 upgrade that benchmarks monocular findings — not a replacement.

---

## 6. Study Area

**Primary:** San Diego, California — all routes  
- Coastal corridors: La Jolla, Pacific Beach, Mission Bay (marine layer, glare priority)  
- Urban grid: Downtown San Diego  
- Freeways: I-5, I-8, I-15  
- Suburban: Miramar, Kearny Mesa, Chula Vista  

**Extended:** Road trips as needed for comparative/out-of-region data  

**Target conditions per session:**
| Condition Tag | Description | Best capture time |
|--------------|-------------|-------------------|
| `clear` | Dry, sunny, good visibility | Midday |
| `marine_layer` | Coastal fog, reduced contrast | Early morning (6–9am) |
| `glare` | Direct sun on wet/dry road | Late afternoon (4–6pm) |
| `wet_pavement` | Post-rain surface, no active rain | After coastal drizzle |

---

## 7. Research Stack — Three Layers

### Layer 1: Infrastructure Condition (CE expertise)
Fine-tune YOLOv8 to classify road surface and marking quality from dashcam footage. Assign a degradation score (0–10) per GPS road segment using a formal rubric developed from civil engineering domain knowledge.

**CE Degradation Rubric categories:**
- Pavement condition (cracking, rutting, surface wear)
- Lane marking clarity (fading, missing, incorrect)
- Road geometry (sight distance, cross-slope, transitions)
- Surface grip indicators (texture loss, standing water zones)

### Layer 2: Environmental Condition (San Diego-specific)
Tag all footage by one of four dominant coastal conditions using Open-Meteo historical weather API cross-referenced with GPS timestamp. Manual review for ambiguous clips.

### Layer 3: Perception Performance (ML core)
Run lane detection (UFLD or LaneATT) + object detection pipeline across all footage. Measure confidence score drop-off as a joint function of Layer 1 (infra score) and Layer 2 (weather tag). Cross-validate against comparable scenes in the Waymo Open Dataset.

**Primary output:** A compound failure risk matrix showing which infra+weather combinations cause steepest perception degradation, mapped to GPS coordinates across San Diego.

---

## 8. Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Primary language |
| PyTorch | Model training and inference |
| Ultralytics YOLOv8 | Infrastructure defect detection |
| OpenCV | Video processing, frame extraction |
| Pandas | Data manipulation, results logging |
| Folium / Plotly | Interactive GPS maps, visualizations |
| Roboflow | Dataset annotation for YOLO training |
| Open-Meteo API | Historical weather data by GPS + timestamp |
| Waymo Open Dataset | Benchmark cross-validation |
| Git / GitHub | Version control, public portfolio |
| VS Code + Claude Code | Development environment |
| Claude Cowork | Research operations, writing, organization |

---

## 9. Phased Roadmap (Mar – Dec 2026)

### Phase 1: Data Pipeline & CE Rubric (Mar – Apr 2026)
**Goal:** Working data infrastructure and formal rubric document

- [ ] Set up folder structure and GitHub repo
- [ ] Write GPS extraction script (VIOFO MP4 → structured CSV)
- [ ] Build weather tagging pipeline (Open-Meteo API by timestamp + GPS)
- [ ] Write and publish CE Infrastructure Degradation Scoring Rubric (PDF)
- [ ] Conduct first 3 research drives covering coastal + urban routes
- [ ] LinkedIn post: "I'm a civil engineer building an AV perception dataset"

**Phase 1 done when:** GPS CSV + weather tag pipeline running on real footage, rubric document published

---

### Phase 2: Infrastructure Detection Model (May – Jun 2026)
**Goal:** Fine-tuned YOLO model that scores road conditions per segment

- [ ] Label 500–1000 frames using CE rubric (Roboflow)
- [ ] Fine-tune YOLOv8 on pavement/marking degradation categories
- [ ] Score all collected footage, map degradation scores to GPS with Folium
- [ ] Validate model outputs against own CE judgment (qualitative review)
- [ ] YouTube video: "I trained an AI to see roads the way a civil engineer does"

**Phase 2 done when:** Per-segment infra scores exported to CSV and mapped on interactive Folium map

---

### Phase 3: Perception Pipeline & Failure Logging (Jul – Aug 2026)
**Goal:** End-to-end pipeline correlating detection performance with infra + weather

- [ ] Run UFLD lane detection across all footage, log per-frame confidence
- [ ] Join results with weather_tag + infra_score by filename/timestamp
- [ ] Compute mean confidence grouped by weather_tag × infra_score bucket
- [ ] Build working failure logger with video clip tagging
- [ ] **Demo-ready prototype by Aug 2026** — screencastable for outreach
- [ ] LinkedIn post: first quantitative results with data visualization

**Phase 3 done when:** Compound failure patterns are measurable and visualizable

---

### Phase 4: Waymo Benchmark & Compound Matrix (Sep – Oct 2026)
**Goal:** External validation and signature research output

- [ ] Access Waymo Open Dataset, pull comparable urban scenes
- [ ] Run same pipeline on Waymo scenes, compare to San Diego results
- [ ] Build 4×3 compound failure risk matrix (weather × infra score bucket)
- [ ] Map highest-risk corridors to San Diego GPS locations (Plotly interactive)
- [ ] LinkedIn post tagging Waymo Research: "Here's what your dataset underrepresents"
- [ ] YouTube: "Comparing my footage to what Waymo publishes"

**Phase 4 done when:** Compound matrix complete, Waymo comparison quantified

---

### Phase 5: Capstone Polish & Publication (Nov – Dec 2026)
**Goal:** Defensible research output ready for academic and professional audiences

- [ ] Failure mode taxonomy ranked by severity and geographic frequency
- [ ] Full interactive San Diego risk map (Plotly/Folium)
- [ ] Clean GitHub repo with detailed README (portfolio piece)
- [ ] Paper formatted for arXiv preprint or ITSC workshop submission
- [ ] Final YouTube: "What I found about AV perception in San Diego"
- [ ] LinkedIn full findings post (tag Waymo, Zoox, Aurora)

**Phase 5 done when:** Paper submitted, repo public, findings posted

---

## 10. Deliverables Summary

| Deliverable | Format | Audience | Target date |
|------------|--------|----------|-------------|
| CE Infrastructure Rubric | PDF document | Academic + recruiters | Apr 2026 |
| GPS + weather pipeline | GitHub (Python) | Technical | Apr 2026 |
| YOLO infra detection model | GitHub (PyTorch) | Technical | Jun 2026 |
| San Diego infra degradation map | Interactive Folium HTML | Public | Jun 2026 |
| Perception failure logger | GitHub (Python) | Technical | Aug 2026 |
| Demo prototype | Screen recording | Recruiters | Aug 2026 |
| Compound failure risk matrix | Plotly heatmap | Public + academic | Oct 2026 |
| Waymo benchmark comparison | GitHub notebook | Technical | Oct 2026 |
| arXiv preprint / workshop paper | PDF | Academic | Dec 2026 |
| Public GitHub portfolio repo | GitHub | Recruiters + academic | Dec 2026 |

---

## 11. Public Presence Strategy

### LinkedIn
- Post frequency: 1× per phase milestone (every 4–6 weeks minimum)
- Always lead with the *problem*, never the process
- Frame as independent research, not a student project
- Tag AV company research accounts at Phase 4+
- Hook formula: "Why do self-driving cars [specific failure]?" → your data → call to connect

### YouTube
- 1 video per phase (5 total)
- Technical but accessible — not vlog style
- Titles focused on the research question, not the tools
- Use screen recordings of actual model outputs

### GitHub
- Repo public from Day 1 (with a placeholder README)
- Commit every working session — frequency signals active development
- README is the portfolio piece — treat it like a research abstract
- Tag: `autonomous-vehicles`, `computer-vision`, `monocular-perception`, `san-diego`, `civil-engineering`

---

## 12. Target Companies

**Primary:** Waymo, Zoox  
**Secondary:** Aurora, Mobileye, Motional, Torc Robotics, Kodiak Robotics  
**Strategy:** Begin networking at Phase 3 (Aug 2026) when prototype exists. Apply post-graduation with full portfolio.

---

## 13. Success Metrics

| Metric | Target |
|--------|--------|
| Research drives completed | 20+ sessions by Dec 2026 |
| Footage collected | 50+ hours across all conditions |
| Frames labeled for YOLO | 500 minimum, 1000 target |
| Infra score × weather conditions covered | All 4 weather tags × all route types |
| LinkedIn followers gained | 500+ from project content |
| GitHub repo stars | 50+ |
| Paper submission | 1 arXiv preprint or workshop paper |
| Recruiter conversations initiated | 5+ at target companies |

---

## 14. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Footage quality issues (glare on lens, camera angle) | Medium | CPL filter included with A329S; test sessions before full collection |
| Waymo Open Dataset access complexity | Low | Free academic access available; start registration in Phase 3 |
| Python skill gaps slow pipeline development | Medium | Vibe coding with Claude Code bridges gaps; plan for 2× time estimates |
| Time commitment drops during busy periods | High | Phases designed to be paused/resumed; microSD rotation keeps data safe |
| Capstone requirements conflict with project scope | Medium | Revisit in 6 months; project is designed to be academically defensible |
| Weather condition capture gaps | Low | San Diego's seasonal marine layer is reliable; schedule early AM drives |

---

## 15. Constraints & Assumptions

- **Budget:** Low — open-source tools only, free dataset access, existing hardware
- **Sensor:** Monocular camera only through December 2026
- **Time:** 6–10 hours/week average, with significant seasonal variation
- **Coding:** Vibe coding with Claude Code as primary development method — acceptable
- **Capstone:** Requirements TBD in ~6 months; project scope flexible enough to adapt
- **Advisor:** Not yet assigned — project proceeds independently until assigned

---

*Last updated: April 2026 | Version 1.0*
