# Claude Project Setup Guide
## AV Capstone — Infrastructure-Conditioned Perception Degradation

---

## What is a Claude Project?

A Claude Project gives you a persistent workspace on claude.ai where Claude remembers
context across every conversation. Instead of re-explaining your project every time,
you upload documents once and Claude reads them automatically in every chat.

Think of it as giving Claude a permanent briefing room for your research.

---

## Step 1: Create the Project

1. Go to claude.ai
2. Click "Projects" in the left sidebar
3. Click "New Project"
4. Name it: **AV Perception Research — San Diego**
5. Add a description: "Monocular AV perception degradation research using VIOFO A329S dashcam data across San Diego routes. Civil engineering + ML hybrid approach."

---

## Step 2: Upload These Files to the Project

Upload ALL of the following files to your Claude Project's knowledge base.
These are the files that Claude will read automatically in every conversation.

### REQUIRED — Upload immediately:

| File | Why it matters |
|------|---------------|
| `PROJECT_CHARTER.md` | Full research scope, hypotheses, timeline, deliverables |
| `CLAUDE.md` | Coding preferences, folder structure, terminology |
| `SKILL.md` | Writing style, task templates, Cowork preferences |

### ADD as you create them (Phase 1):

| File | When to add |
|------|-------------|
| `docs/rubric.md` | When CE degradation rubric is written (Apr 2026) |
| `phase_log.md` | Create this now — update it every session |
| `docs/literature/` summary files | As you complete each paper review |

### DO NOT upload:
- Raw MP4 footage files (too large, not needed)
- CSV data files (Claude can't process large datasets this way — use Claude Code instead)
- Model checkpoint files (.pt, .pth)
- Any file containing personal information or passwords

---

## Step 3: Create phase_log.md Right Now

Create this file and upload it to your Project. Update it after every working session.

```markdown
# Phase Log — AV Capstone

## Current Phase: 1 — Data Pipeline & CE Rubric
## Current Status: STARTING

---

## Phase 1 Tasks (Mar – Apr 2026)

- [ ] Folder structure created on local machine
- [ ] GitHub repo initialized (public)
- [ ] CLAUDE.md added to repo root
- [ ] SKILL.md added to repo root
- [ ] GPS extraction script written and tested
- [ ] Weather tagging pipeline written and tested
- [ ] First 3 research drives completed
- [ ] CE Infrastructure Degradation Rubric written
- [ ] LinkedIn post 1 published

## Session Log

### Session 1 — [DATE]
- What I worked on:
- What got done:
- What's next:
- Blockers:
```

---

## Step 4: Write a Project System Prompt

In your Claude Project settings, there is a field called "Project instructions" or
"Custom instructions." Paste this in:

```
You are my research co-pilot for an independent AV perception study. I am a civil engineer
and Applied AI Master's student in San Diego, CA.

Always read PROJECT_CHARTER.md, CLAUDE.md, SKILL.md, and phase_log.md before responding.

Key rules:
- Frame my work as independent research, not a student project
- Use my exact terminology: "degradation score", "compound failure", "infrastructure condition"
- My Python level is beginner-intermediate — explain code clearly, never assume ML knowledge
- Never suggest LiDAR solutions — I am monocular-only through December 2026
- When I ask for writing, match my style: direct, no em dashes, technical but accessible
- When I ask for code help, suggest I use Claude Code in my terminal for actual execution
- Always check phase_log.md to understand where I am before giving advice

My primary audiences are: AV company recruiters (Waymo, Zoox) and academic reviewers.
```

---

## Step 5: How to Use the Claude Project Day-to-Day

### For research questions and planning:
Use claude.ai with the Project open. Claude already knows your full context.

Example prompts that work well in the Project:
- "What should I prioritize this week given where I am in Phase 1?"
- "I'm about to write my CE rubric — what sections should it include?"
- "Review this LinkedIn draft and make it sound less like a student project"
- "I'm stuck on [X] — what's the simplest approach for my skill level?"
- "Help me write the abstract for my Phase 4 Waymo comparison findings"

### For writing tasks (rubric, LinkedIn, paper sections):
Use the Project in claude.ai for drafts. Claude Cowork for file management.

### For all Python code:
Switch to Claude Code in your terminal — don't try to run code in the Project chat.
Come back to the Project when you need to think through approach or debug logic.

### For file organization:
Use Claude Cowork (desktop app) — point it at your av-capstone folder.

---

## Step 6: Suggested Weekly Workflow

| When | Tool | What to do |
|------|------|-----------|
| Start of session | Claude Project | Check phase_log, ask "what should I work on?" |
| During coding | Claude Code (VS Code) | Build scripts, run pipelines, commit to GitHub |
| During writing | Claude Project or Cowork | Drafts, literature review, LinkedIn content |
| End of session | Claude Project | Update phase_log.md, re-upload to Project |
| Friday | Claude Cowork | Scheduled weekly digest from results/logs/ |

---

## Folder Structure to Create on Your Machine Right Now

Open your terminal and run:

```bash
mkdir -p av-capstone/{data/{raw_footage,gps_logs,weather_tags,labeled_frames},models/{yolo_infra,lane_detection},notebooks,scripts,results/{maps,charts,logs},docs/literature,social}

cd av-capstone
git init
echo "data/raw_footage/" >> .gitignore
echo "models/" >> .gitignore
echo "*.mp4" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".DS_Store" >> .gitignore

# Copy your CLAUDE.md and SKILL.md into the root folder
# Then:
git add .
git commit -m "[setup] initialize av-capstone project structure"
```

---

## What Your GitHub README Should Say Right Now

Even on Day 1 with no results, publish this:

```markdown
# Infrastructure-Conditioned Perception Degradation in Autonomous Monocular Vision
### A San Diego Coastal Environment Study

**Status:** Active Research — Phase 1 (Data Pipeline)  
**Researcher:** [Your Name] — Civil Engineer + Applied AI  
**Timeline:** April – December 2026

## Research Question
How does road infrastructure condition compound with San Diego's coastal environmental
variables to create measurable perception failures in monocular autonomous vision systems?

## Why This Matters
AV perception research assumes roads are clean and known. They aren't. This study
quantifies the compound effect of infrastructure degradation + coastal weather on
monocular vision performance — benchmarked against the Waymo Open Dataset.

## Sensor Setup
- VIOFO A329S dashcam (4K front + 2K rear, built-in GPS)
- Study area: San Diego, CA — all routes
- Modality: Monocular vision (camera-only)

## Tech Stack
Python · PyTorch · YOLOv8 · OpenCV · Pandas · Folium · Plotly

## Progress
- [x] Project initialized
- [ ] Phase 1: Data pipeline + CE rubric (Apr 2026)
- [ ] Phase 2: Infrastructure detection model (Jun 2026)
- [ ] Phase 3: Perception failure pipeline (Aug 2026)
- [ ] Phase 4: Waymo benchmark + compound matrix (Oct 2026)
- [ ] Phase 5: Capstone + publication (Dec 2026)

## Follow the Research
LinkedIn: [your profile]  
YouTube: [your channel]
```

---

*Setup guide version 1.0 — April 2026*
