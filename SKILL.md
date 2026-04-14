# AV Capstone — Claude Cowork Context
*This file gives Claude Cowork permanent project context for all non-coding tasks.*

---

## Who I am
Wael — civil engineer + Applied AI Master's student, San Diego, CA.
I am building an independent AV perception research project as both a public portfolio
and potential academic capstone. My CE background is my research differentiator.

---

## The project in one sentence
I'm quantifying how road infrastructure degradation compounds with San Diego's coastal
weather to create measurable perception failures in monocular autonomous vision systems —
benchmarked against the Waymo Open Dataset.

---

## My writing style preferences
- Direct and confident — no filler phrases like "it's worth noting that" or "it's important to"
- No em dashes (—) in casual writing — use commas or periods instead
- No excessive bullet points in prose — write in sentences when possible
- Sound like a researcher, not a student — frame work as independent research
- Technical but accessible — AV engineers should understand it, not just academics
- Short paragraphs — maximum 3–4 sentences each
- For LinkedIn: conversational, lead with a question or bold claim, under 300 words
- For academic writing: precise, cite-ready, IEEE formatting preferred

---

## Terminology (always use these exact terms)
- "Degradation score" not "quality score"
- "Infrastructure condition" not "road quality"
- "Weather condition tag" not "weather label"
- "Compound failure" not "combined failure"
- "Monocular perception" not "camera-based perception"
- "Coastal environment" when describing San Diego context
- "CE rubric" when referring to the infrastructure scoring methodology

---

## My folder structure (what you have access to)
```
av-capstone/
├── data/                   ← raw footage and processed logs
├── results/                ← CSVs, maps, charts
├── docs/
│   ├── rubric.md           ← CE degradation rubric — source of truth
│   └── literature/         ← paper summaries
├── social/                 ← LinkedIn and YouTube drafts go here
├── CLAUDE.md               ← Claude Code context
└── SKILL.md                ← this file
```

---

## Common tasks I'll ask you to do

### Literature review
When asked to research papers: output to docs/literature/ as individual .md files.
Format each as: Title, Authors, Year, Key method, Key finding, Relevance to my project (2 sentences).
Focus on: monocular lane detection, domain adaptation, adverse weather perception, infrastructure + AV.

### LinkedIn drafts
Save to social/linkedin_YYYY-MM-DD.md
Always: lead with a research question or surprising finding, include 1-2 data points,
end with "open to connecting with AV engineers and researchers."
Never: start with "Excited to share...", use jargon without explanation, exceed 300 words.

### YouTube scripts
Save to social/youtube_script_phaseN.md
Structure: hook (30 sec) → problem setup (1 min) → what I did (3 min) → findings (2 min) → what's next (30 sec)
Tone: technical presenter, not vlogger. Think "researcher explaining to engineers."

### Weekly digest
Every Friday: scan results/logs/ for new CSVs, summarize changes in detection accuracy,
save to docs/weekly_digest_YYYY-MM-DD.md. Keep it under 200 words.

### Document drafting
When drafting formal documents (rubric, paper sections): use IEEE formatting conventions.
When drafting informal documents (README, project notes): use clear markdown with headers.

---

## Research phases (current status — check phase_log.md)
- Phase 1 (Mar-Apr 2026): Data pipeline + CE rubric
- Phase 2 (May-Jun 2026): YOLO infrastructure detection model
- Phase 3 (Jul-Aug 2026): Perception pipeline + failure logging
- Phase 4 (Sep-Oct 2026): Waymo benchmark + compound failure matrix
- Phase 5 (Nov-Dec 2026): Capstone polish + publication

---

## Target audiences
- Primary: AV company recruiters and engineers (Waymo, Zoox, Aurora)
- Secondary: Applied AI academic reviewers / capstone committee
- Public: LinkedIn followers interested in AV + smart cities + CE

---

## Important rules for Cowork tasks
- NEVER modify anything in data/raw_footage/ — read only
- Always show me a plan before reorganizing files or folders
- Save drafts before final versions — use _draft suffix
- When creating reports, always include the date in the filename
- If asked to schedule a recurring task, confirm the cadence before setting it

---

*Version 1.0 — April 2026*
