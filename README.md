# The Last Acquisition

Museum gala murder mystery, October 30, 2026, Tulsa. 15 core roles and up to 15 optional guests.

## Downloads and spoilers

[Live homepage](https://murder.dalmo.ai) has complete-kit and editable-source ZIPs. The repository and source ZIP contain the full solution. Send each guest only their own pre-party introduction and invitation.

The kit contains 80 PDFs (294 pages including combined copies), 30 single-page character PNGs and a read-me. Start with `00_READ_ME_FIRST.pdf`. Print actual size, single-sided. `OPEN_FREELY` is host-safe; handle `PRINT_WITHOUT_READING` face down using the separate blind assembly guide. `SPOILERS_DO_NOT_OPEN` contains the solution bible.

## Editable sources

- `source/characters.json`: canonical structured introductions, private routes, final statements and A/B evidence.
- `source/facilitator.json`: intentionally paginated host-safe guide with tables and checklists.
- `source/v1/`: preserved original precursors; still supplies clues, animal assignment text, exhibit descriptions, invitation and canonical murder facts. Structured character/facilitator JSON supersedes their flattened counterparts.
- `scripts/build.py`: measured ReportLab layouts, embedded Libron, PNG exports and ZIP packaging.
- `scripts/verify.py`: renders every PDF page, checks bounds/type/glyphs and maps exact visual duplicates.
- `scripts/check_content.py`: branch/evidence preservation checks against generated PDFs.
- `scripts/migrate_v1_characters.py`: one-time migration of flattened v1 character columns. Do not rerun after editing canonical JSON.
- `scripts/archive/build_v1.py`: historical generator, not used for builds.
- `docs/`: game brief, design, reference study, manifest and release QA evidence.
- `site/downloads/`: committed generated release.

## Build and review

```sh
python -m venv .venv
pip install -r requirements.txt
python scripts/build.py
python scripts/check_content.py
python scripts/verify.py
```

Libron v0.25 downloads to ignored `build/fonts/`, checked against a pinned archive SHA-256. Font files are embedded in PDFs and excluded from both ZIPs and the repository. Guests install nothing. The source ZIP includes the license notice.

Review every contact sheet in `build/review/` and questionable full-size pages before releasing. Structural checks alone cannot certify layout. Duplicate raster hashes identify identical combined-file pages.

## Deployment

`netlify.toml` installs pinned dependencies, generates the kit and publishes `site/`. Production: https://murder.dalmo.ai. Complete content checks and visual review before deploying; compare deployed ZIP SHA-256 values with the reviewed local ZIPs.
