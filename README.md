# The Last Acquisition

Working repository for the 2026 murder mystery party: **The Last Acquisition**, set at Tulsa's fictional Meridian Museum of Art & World Cultures during the opening of *Treasures of the World*.

## Important: spoilers

This repository contains full solution material, murderer branches, evidence logic, and confessions. The repository is currently **public on GitHub**. If guests might discover the repo, make it private until after the party. Netlify can deploy from a private GitHub repository.

## What is in the repo

- `source/v1/characters/` — editable source for all 30 spoiler-safe character sheets **and** all 30 private party-night packets.
- `source/v1/*.md` plus `source/v1/evidence_cards/` and `source/v1/spoiler_bible/` — editable precursors for facilitator materials, scavenger clues, forensic evidence, A/B character evidence, invitation, decor, scoring, and the full continuity bible.
- `source/v1/cast.csv` — quick cast/tier index.
- `docs/GAME_DESIGN_BRIEF.md` — the canonical constraints agreed with Dalmo.
- `docs/QA.md` — release-blocker checks for fairness, continuity, attendance resilience, host blindness, and print quality.
- `docs/ASSET_MANIFEST.md` — all 73 generated kit files.
- `scripts/build.py` — reproducible generator for individual PDFs, combined PDFs, the complete game ZIP, and an editable-source ZIP.
- `site/` — spoiler-safe project homepage; Netlify publishes this directory.
- `netlify.toml` — installs dependencies, runs the generator, and publishes `site/`.

Generated binary PDFs/ZIPs are **build outputs rather than hand-edited source files**. This keeps iteration sane: edit the text/data source once, rebuild, and every affected downloadable updates automatically. The deployed site receives:

- `site/downloads/The_Last_Acquisition_Complete_Kit.zip`
- `site/downloads/The_Last_Acquisition_Source.zip`
- `site/downloads/current/The_Last_Acquisition_Complete_Kit/...` with all 73 individual/composite game assets.

## Local build

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build.py
```

The current build has been smoke-tested locally and produces the complete 73-file kit.

## Netlify

Connect this repository to a Netlify project. `netlify.toml` already defines the build command and `site/` publish directory, so no manual build settings are required.

## Iteration rule

Treat `source/v1/` as the canonical editable content. Future changes should happen there first, followed by a rebuild. When the game reaches a new stable milestone, preserve it as a new version instead of destructively overwriting the previous one.
