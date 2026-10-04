---
name: The Last Acquisition — Museum Gala Print
description: Ornate invitations and readable, self-contained museum gala player books.
colors:
  ink: "#132e38"
  teal: "#057294"
  gold: "#9b783b"
  private-warning: "#8b2636"
  paper: "#ffffff"
  relationship-highlight: "#fff099"
  stop-ground: "#fff4f1"
  table-rule: "#a8c4cd"
  portrait-matte: "#f6f1e7"
typography:
  body: {fontFamily: "Libron", fontSize: "14pt", fontWeight: 400, lineHeight: 1.25}
  read-aloud: {fontFamily: "Libron", fontSize: "16pt", fontWeight: 400, lineHeight: 1.25}
  poster-body: {fontFamily: "Libron", fontSize: "16–17pt", fontWeight: 400, lineHeight: 1.25}
  poster-name: {fontFamily: "Libron", fontSize: "34pt", fontWeight: 700, lineHeight: 1.25}
  cover-name: {fontFamily: "Libron", fontSize: "36pt", fontWeight: 700, lineHeight: 1.25}
  place-given-name: {fontFamily: "Libron", fontSize: "31pt", fontWeight: 700, lineHeight: 1.25}
  place-surname: {fontFamily: "Libron", fontSize: "38pt", fontWeight: 700, lineHeight: 1.25}
  round-marker: {fontFamily: "Libron", fontSize: "16pt", fontWeight: 700, lineHeight: 1.25}
  footer: {fontFamily: "Libron", fontSize: "12pt", fontWeight: 400, lineHeight: 1.25}
spacing:
  page-margin: "42pt"
  poster-margin: "48pt"
  speech-inset: "18pt"
  discovery-inset: "16pt"
components:
  speech-box: {backgroundColor: "{colors.paper}", textColor: "{colors.ink}", width: "528pt"}
  discovery-card: {backgroundColor: "{colors.paper}", textColor: "{colors.ink}", width: "528pt", height: "302pt", padding: "16pt"}
  stop-panel: {backgroundColor: "{colors.stop-ground}", textColor: "{colors.private-warning}", width: "528pt", height: "61pt"}
  tent-face: {backgroundColor: "{colors.paper}", textColor: "{colors.ink}", width: "540pt", height: "288pt"}
---

# Design System: The Last Acquisition — Print

## Overview

**Creative North Star: “Museum Patron Folio”**

The user explicitly chose an ornate, professional museum gala and retained the improved teal color and readable book font. Gilded portrait frames and fine ornamental borders establish the occasion; the inside pages make the evening easy to follow. This specification extracts `scripts/build.py`, `scripts/printable_v2.py` and `scripts/evidence_design.py`. The independent homepage remains governed by `docs/DESIGN.md`.

The concept seed `ad4b8f59`, assigned index 5, is process provenance. Seven grounded possibilities reconstructed within the pinned museum world are gala invitation, exhibition catalogue, conservation dossier, artist salon, museum patron folio, accession ledger and exhibition wall label. These were not presented as user choices. The implemented patron folio translates the assignment within the user's fixed gala, teal, Libron and ornate-frame direction. No new approval ceremony is implied.

**Key Characteristics:**

- Safe face-up framed Picasso covers and twelve-page self-contained books.
- Single-page Van Gogh posters with full-width Acting Tips.
- Bold yellow relationship names and strong round boundaries.
- Ninety distinct hunt hints, photographic evidence and freeform accusations.
- Thirty large, two-sided tent cards with transparent avatars.

## Colors

Meridian Blue carries names, headings, round markers and speech outlines. Gold belongs to page ornament, framing and fold guides. Museum Ink supports reading on white stock. Yellow is restricted to relationship names on the day-of introduction page. Private Warning and the pale stop ground announce boundaries in words as well as color. Portraits retain their individual palettes.

## Typography

Libron Regular, Bold, Italic and BoldItalic are embedded as `Book`, `BookBold`, `BookItalic` and `BookBoldItalic`. The build pins v0.25 and verifies its archive against `scripts/font.sha256`. Standalone font binaries remain in the ignored build cache and are excluded from downloads.

Canvas paragraphs use 1.25 leading; manuals use 14/18 pt narrative and 20/24 pt headings. Posters measure content and choose 17 or 16 pt narrative, with 34 pt names and 16 pt roles/section labels. Acting Tips have the same wide measure and narrative size as the relationships below the portrait.

Packets use 16 pt round markers, 14 pt running names, 27 pt section titles and 36 pt cover names. Introductions, histories and Motive/Method speaking boxes use 16 pt. Opportunity boxes use 16 pt, or 15 pt when measured content requires it. Coming Clean uses 14 pt. All ten questions and named targets fit on one page at 14 pt. Hunt hints use 19 pt italic. Auxiliary metadata uses 12 pt.

Tent cards use 31 pt first/middle names, 38 pt surnames and 16 pt roles. Discovery narratives and fields use 14 pt, titles 22 pt and stamps 12 pt. Room signs retain 48 pt names.

**The Reading Floor Rule.** Preserve at least 14 pt narrative. Reflow or edit content before reducing type. Twelve-point metadata is not a substitute for readable narrative.

## Layout

US Letter is 612 × 792 pt. Coordinates run down from the top. Ordinary content starts at x=42 and spans 528 pt; posters use x=48 and 516 pt. Room signs use landscape Letter.

Posters have gold rectangles at (28,28,556,736) and (33,33,546,726), with corner rosettes. Names start at (48,49), roles at y=98 and the divider at y=142. The Van Gogh frame occupies (41,150,196,234); description starts at (246,157), width 318 pt. Relationships, Acting Tips and Costume Suggestions flow beneath both columns across 516 pt. Footer y=740. Each poster is one unnumbered PDF and a 1224 × 1584 pixel JPEG at 144 dpi, quality 90, subsampling 0.

The authoritative twelve-page map is `source/game.json`:

| Page | Content |
| --- | --- |
| 1 | Safe ornate Picasso cover |
| 2 | INTRODUCTIONS: identity, highlighted relationships, acting tips, spoken introduction |
| 3 | INTRODUCTIONS: private background and conversations |
| 4 | HUNT FOR CLUES: three cryptic hints |
| 5–6 | ACT I: MOTIVE: one question page, common answer |
| 7–8 | ACT II: OPPORTUNITY: one question page, role answers |
| 9–10 | ACT III: METHOD: one question page, common answer and discovery index |
| 11 | ACCUSATIONS: loose ballot |
| 12 | COMING CLEAN: retained role statements |

Cover portrait frame: (149,169,314,458). Event title: (62,62); name: (62,636); safe numbering y=716; date/museum y=737. No branch, animal, grievance or secret appears on the cover. Page 2 has no costume suggestions or second portrait.

Round markers start at (42,30), running names y=62 and divider y=89. Questions occupy two 252 pt columns at x=42/318, five groups each starting y=226. Each group has three named targets. Directions point to answer pages 6,8,10. Speech boxes span 528 pt, text starts at x=60 across 492 pt, and box height is measured text plus 22 pt.

Stop panels occupy (42,686,528,61). A red octagon centered at (66,716), radius 20 pt, reinforces the 14 pt message at (96,700): **“STOP! Do not turn the page yet. Wait for the host to announce the next round.”** Bottom footers number packet pages. Within-round transitions instead give explicit continuation instructions.

Discoveries are two 528 × 302 pt records at (42,104)/(42,422), with 496 × 116 pt photo slots. F1/F5 report photos use 528 × 225 pt, F4 uses 528 × 180 pt, and F3 includes a 528 × 135 pt floor diagram.

Each tent uses one Letter sheet: cut rectangle (36,36,540,720), two 540 × 288 pt faces and two 72 pt base flaps. Fold guides y=108/396/684. Rotate the upper face 180 degrees so both faces read upright when assembled. Names start x=64, avatars occupy a 132 × 230 pt slot at x=410. Overlap and tape the base flaps. Print single-sided at 100%.

Leave ballot page 11 loose inside and staple the other pages in order. Guests retain Coming Clean. Do not use booklet or two-pages-per-sheet printing.

## Elevation & Depth

Generated gilt framing supplies carved museum depth, with a native transparent center. Interior pages stay flat, using spacing, outlines and hierarchy. There are no PDF drop shadows, motion or responsive breakpoints.

## Shapes

Double gold borders and circular corner ornaments establish the folio. Records and speech boxes stay square. Ordinary outlines are 0.7 pt and rules 0.6 pt. Cut lines use 3/3 pt dashes; gold tent folds use 5/3 pt. The red octagon reinforces the written stop.

## Components

**Framed portrait.** `framed()` intentionally crops the print composition into the gilt aperture with aspect-preserving scaling and clipping. Aperture fractions are x=0.18, y=0.14, width=0.64, height=0.72 of the 2:3 frame. This replaces the old “never crop” rule for poster and cover placements. Full-resolution, full-composition masters remain in the source archive. Other `Sheet.image()` placements retain centered aspect-fit.

**Image encoding.** Opaque print images fit within 900 × 900 and use quality-88 JPEG, subsampling 1. Ornament color uses that encoding with a lossless native-alpha soft mask. Other alpha artwork uses PNG within 480 × 480 and an automatic mask. The thirty native chibi WebP masters preserve full-resolution alpha. Public Portraits contain sixty JPEGs and thirty lossless alpha WebPs within 900 × 900. Organizer source retains exact prompts and hashes; public exports carry harmless provenance.

**Introduction.** Relationship names are bold/yellow, including unambiguous first-name aliases where used. Description, relationships and wide Acting Tips orient the guest. Only the bordered introduction is spoken. Private briefing follows separately.

**Hearing.** Guests choose unanswered present characters by name; the host tracks turns. Role headings stay outside spoken boxes. Motive and Method have common boxes; Opportunity and Coming Clean have IF INNOCENT/IF MURDERER boxes. There is no investigation grid, separate catalog or selected-clue checklist.

**Hunt.** Thirty pages each have three distinct cryptic hints from `source/hunt.json`, totaling ninety distinct texts across sixteen house locations. Findings go to the shared Evidence Table. Guests may request physical help; the host retrieves missing envelopes before hearings.

**Museum evidence.** Sixteen original records and five staged reports mix agreements, notes, work orders, diagrams and photographs. Clock-comparison, actual-installation and obsolete-display images join the earlier evidence art; gilt framing is generated too. The old proposal and actual installation photograph carry distinct documentary contexts. These are evidence objects, not descriptions of imagined images.

**Hosting.** Fifteen planned guide pages organize preparation, directories, memorized-animal selection, assembly, sixteen placements, agenda, announcements and finale. A separate three-page roster/tally tracks turns. Player books do not reduce the mystery to a three-column deduction grid.

**The Locked Ballot Rule.** Collect ballots and match attendance before Coming Clean. Rank attending names by votes, including zero; break ties alphabetically by full name. Exactly three suspects read their appropriate statements, all three even after an early confession. If none confesses, call the selected animal to read IF MURDERER.

## Do's and Don'ts

- Do preserve the safe cover, twelve-page order, loose ballot and retained finale.
- Do keep relationship names bold/yellow and Acting Tips full width.
- Do preserve readable narrative, distinct art identities and native avatar alpha.
- Do print one tent sheet per guest at 100%, with taped base flaps.
- Do preserve the three spoiler-handling directories and immediately returned memorized-animal slips.
- Don't reintroduce notes grids, A/B cards, external catalogs or separate finale files.
- Don't put private information on a face-up cover or shrink prose to hide overflow.
- Don't distribute font binaries or organizer prompts to guests.
- Don't replace the separate homepage identity with ornate print styling.

Build assertions check measured bounds and glyph support. `scripts/verify.py` renders PDFs and maps repeated visuals by raster hash. Actual review coverage, corrections and confirmation belong in `docs/GALA_FINISH_REVIEW.md` and the current review report. This specification carries no frozen review counts, release hashes or “ship” claim. Playtest scope belongs in `docs/PLAYTEST_SUMMARY.md`; earlier all-correct/2-of-5 ratings describe the rejected edition. Digital review and model table reads do not establish physical printer quality or live-human difficulty.
