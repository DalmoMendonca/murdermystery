# The Last Acquisition

Working repository for the 2026 murder mystery party: **The Last Acquisition**, set at Tulsa's fictional Meridian Museum of Art & World Cultures during the opening of *Treasures of the World*.

## Important: spoilers

This repository contains full solution material, murderer branches, evidence logic, and confessions. The repository is currently **public on GitHub**. If guests might discover the repo, make it private until after the party. Netlify can deploy from a private GitHub repository.

## Structure

- `site/` - spoiler-safe project homepage and downloadable v1 release assets; Netlify publishes this folder.
- `source/v1/characters.json` - consolidated editable source for all 30 character packets.
- `source/v1/*.md` - editable text precursors for facilitator, clues, evidence, decor, awards, invitation, and spoiler bible.
- `docs/GAME_DESIGN_BRIEF.md` - design constraints agreed in conversation.
- `docs/QA.md` - release-blocker checks for continuity/fairness.
- `scripts/build.py` - simple Python/WeasyPrint iteration pipeline for future versions.
- `site/downloads/The_Last_Acquisition_Complete_Kit_v1.zip` - canonical complete v1 kit.

## Local build

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build.py
```

The current PDFs are retained as canonical v1 artifacts even if the editable-source renderer evolves. Future changes should happen in `source/` first, then produce a new release rather than destructively overwriting v1.

## Netlify

`netlify.toml` publishes the `site/` directory. Connect this repo to a Netlify project and deploy with no build command required.
