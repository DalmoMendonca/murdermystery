# The Last Acquisition

Museum gala murder mystery, October 30, 2026, Tulsa. 30 eligible roles; 22 currently confirmed.

## Downloads and spoilers

[Live homepage](https://murder.dalmo.ai) has complete-kit and editable-source ZIPs. The repository and source ZIP contain the full solution. Send each guest only their own pre-party introduction and invitation.

Start with `00_READ_ME_FIRST.pdf`. Each guest receives one complete twelve-page private packet: safe ornate cover, highlighted introduction, private briefing, hunt hints, all Motive/Opportunity/Method questions with named targets, prepared speeches, ballot and Coming Clean. No separate player catalog, letter cards or finale envelopes. Print actual size, single-sided. `OPEN_FREELY` is host-safe; handle private files face down. `SPOILERS_DO_NOT_OPEN` contains the solution bible.

Every character has a Van Gogh portrait on the public introduction, a Picasso portrait on the private cover, and a transparent chibi on the place card. Place cards put first and middle names on one line and surname on the next; one US Letter sheet per guest, with two faces, fold lines and tape-together base flaps. All thirty roles can be selected through the same memorized animal draw. Casting tiers indicate story prominence, not murderer eligibility.

Printable PDFs use white/light reading areas, black text and burgundy/gold museum accents. The invitation retains its photographic upper section. Phone JPEGs keep the approved dark After Hours design; use those images for texting rather than rendering the print PDFs.

## Editable sources

- `source/character_copy.yaml`: the already-sent public copy, now frozen by `source/public_assets_lock.json`.
- `source/investigation_copy.yaml`: canonical private briefings, six hearing speeches, two endings and exclusion arguments for all thirty roles.
- `source/case_design.yaml`: the crime, evidence dependencies, release order and limits of the inference.
- `source/evidence_design.yaml`: five official reports and sixteen short discoveries.
- `source/characters.json`, `investigation.json`, `discoveries.json` and `case.json`: generated compatibility output; edit the YAML sources.
- `source/game.json`: address, packet page map and one familiar animal pool.
- `source/question_rounds.json`: generated shared questions, with two to four named targets per question; the confirmed edition filters absent names.
- `source/discoveries.json`: sixteen actual museum document payloads.
- `source/evidence_art.json`: photographic exhibit prompts and hashes.
- `source/investigation.json`: current staged forensic reports and physical evidence and competing accounts.
- `source/art_direction.json`: 30 distinct fictional identities, palettes, signature accessories, exact generation prompts and asset hashes.
- `assets/portraits/`: all original portraits and transparent cutout derivatives, used by the PDF pipeline. No image-generation API call is required to build.
- `source/name_map.json`: simultaneous aliases applied to archived source text.
- `source/facilitator.json`: intentionally paginated host-safe guide with tables and checklists.
- `source/v1/`: preserved original precursors; supplies remapped scavenger discoveries, exhibit descriptions and invitation text. Current structured JSON and GAME_FLOW supersede historical mechanics and names.
- `scripts/build.py`: measured ReportLab layouts, embedded Libron, high-quality JPEG poster exports and ZIP packaging.
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

## Agent table read

Read the spoiler-safe `docs/PLAYTEST_SUMMARY.md`. The previous 15/15 solve result was an ease warning, not a difficulty success. Current staged assessments and their limitations are recorded under `docs/playtest/2026-10-06-RESTRUCTURE-SPOILERS`; older results remain historical. AI transcript accuracy is not a human party difficulty measurement. Historical editions are preserved under source/history and docs/history, not used by the build.

## Editing private testimony

`source/investigation_copy.yaml` is organizer-only source containing all thirty characters, their six hearing speeches, two Coming Clean endings, suspicious disclosure and linked clearance. The already-sent public descriptions, relationships and costumes are frozen in `source/character_copy.yaml`; the build rejects changes to them. Do not send either private source or full ZIPs to players. Rebuild after an edit, run `scripts/check_content.py` (which includes packet checks), then render with `scripts/verify.py` and inspect the affected pages before publishing. Spoken hearing and Coming Clean text uses at least 15pt.

See `docs/RESTRUCTURE_2026_10_06.md` for the current revision audit and `docs/THREE_ROUND_REVIEW.md` for the preceding rewrite audit and its difficulty limitations. Historical playtest results refer to earlier editions, not these rewritten speeches.

## Editing hunt hints

Edit `source/hunt_copy.yaml`. Each numbered envelope has its real hiding place and the character names and hints that point there. Change the `hint` text directly; keep each character assigned to three different locations. The build validates all ninety hints and regenerates the packet pages, host placement table and compatibility snapshot `source/hunt.json`. Do not edit that generated JSON. Rebuild with `python scripts/build.py`, then check content and inspect rendered pages before publishing.

The sixteen discovery exhibits contain only their own short evidence. Five official reports release the shared case facts in stages. No discovery contains appended alibi summaries or a recovery section.

## October 6 restructure

Use `03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf` for the current party. The 30-role masters remain available for roster changes. The public invitation and every already-sent character image/PDF are hash-locked and skipped by the build. See `docs/RESTRUCTURE_2026_10_06.md` for the architecture, independent reviews, trial results and limitations.


## Rebuilding the source archive

The source ZIP excludes generated downloads. On its first build, missing frozen public exports are restored from the pinned baseline complete kit and checked against the public lock. Existing files are never replaced. For an offline rebuild, put the complete-kit ZIP and `All_30_Characters_and_Invite.zip` beside the extracted source and call `restore_missing_public` in `scripts/public_lock.py` with their paths before building. Editing private testimony does not regenerate the already-sent invitation or character sheets.

The organizer book contains the case, discovery resolutions and one resolution page per character. Full speeches are in the player packets and `source/investigation_copy.yaml`.
