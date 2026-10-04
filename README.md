# The Last Acquisition

Museum gala murder mystery, October 30, 2026, Tulsa. 15 core roles and up to 15 optional guests.

## Downloads and spoilers

[Live homepage](https://murder.dalmo.ai) has complete-kit and editable-source ZIPs. The repository and source ZIP contain the full solution. Send each guest only their own pre-party introduction and invitation.

Start with `00_READ_ME_FIRST.pdf`. Each guest receives one complete twelve-page private packet: background, all Motive/Opportunity/Method question pages with named targets, their prepared answers and records, ballot and Coming Clean. No separate player catalog, letter cards or finale envelopes. Print actual size, single-sided. `OPEN_FREELY` is host-safe; handle private files face down. `SPOILERS_DO_NOT_OPEN` contains the solution bible.

Every character has a Van Gogh portrait on the public introduction, a Picasso portrait on the private cover, and a transparent chibi on the place card. Place cards put first and middle names on one line and surname on the next; four per US Letter page. All thirty roles can be selected through the same memorized animal draw. Casting tiers indicate story prominence, not murderer eligibility.

## Editable sources

- `source/characters.json`: canonical introductions, prepared answers, private canon, preparation records and both Coming Clean statements.
- `source/game.json`: address, packet page map and one familiar animal pool.
- `source/question_rounds.json`: ten shared questions per round, each with three named targets.
- `source/discoveries.json`: sixteen actual museum document payloads.
- `source/evidence_art.json`: photographic exhibit prompts and hashes.
- `source/investigation.json`: current staged forensic reports and closed physical evidence chain.
- `source/art_direction.json`: 30 distinct fictional identities, palettes, signature accessories, exact generation prompts and asset hashes.
- `assets/portraits/`: all original portraits and transparent cutout derivatives, used by the PDF pipeline. No image-generation API call is required to build.
- `source/name_map.json`: simultaneous aliases applied to archived source text.
- `source/facilitator.json`: intentionally paginated host-safe guide with tables and checklists.
- `source/v1/`: preserved original precursors; supplies remapped scavenger discoveries, exhibit descriptions and invitation text. Current structured JSON and GAME_FLOW supersede historical mechanics and names.
- `scripts/build.py`: measured ReportLab layouts, embedded Libron, PNG exports and ZIP packaging.
- `scripts/verify.py`: renders every PDF page, checks bounds/type/glyphs and maps exact visual duplicates.
- `scripts/check_content.py`: hearing/branch/evidence preservation checks against generated PDFs.
- `scripts/rehearse.py`: animal-draw and question-handoff desk rehearsals including absences.
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
python scripts/rehearse.py
python scripts/verify.py
```

Libron v0.25 downloads to ignored `build/fonts/`, checked against a pinned archive SHA-256. Font files are embedded in PDFs and excluded from both ZIPs and the repository. Guests install nothing. The source ZIP includes the license notice.

Review every contact sheet in `build/review/` and questionable full-size pages before releasing. Structural checks alone cannot certify layout. Duplicate raster hashes identify identical combined-file pages.

Archives use fixed entry timestamps, stable ordering and normalized text line endings so rebuilding an unchanged release preserves ZIP hashes. PDF illustrations use print derivatives; the organizer source retains larger portrait files. Public portrait metadata gives its origin without exposing plot-related prompt constraints.

## Deployment

`netlify.toml` installs pinned dependencies, generates the kit and publishes `site/`. Production: https://murder.dalmo.ai. Complete content checks and visual review before deploying; compare deployed ZIP SHA-256 values with the reviewed local ZIPs.
