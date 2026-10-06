---
name: The Last Acquisition — Museum Gala Print
description: Light-paper museum stationery, readable player books and separately scoped dark phone images.
colors:
  ink: "#191b1c"
  burgundy: "#720f29"
  gold: "#866632"
  paper: "#ffffff"
  relationship-highlight: "#fff099"
  pale: "#faf4f1"
  table-rule: "#b9aca3"
typography:
  body: {fontFamily: "Libron", fontSize: "14pt", fontWeight: 400, lineHeight: 1.25}
  read-aloud: {fontFamily: "Libron", fontSize: "16pt", fontWeight: 400, lineHeight: 1.25}
  hearing-speech: {fontFamily: "Libron", fontSize: "measured 16 or 15pt", fontWeight: 400, lineHeight: 1.25}
  coming-clean: {fontFamily: "Libron", fontSize: "15pt", fontWeight: 400, lineHeight: 1.25}
  poster-body: {fontFamily: "Libron", fontSize: "measured 17, 16.5 or 16pt", fontWeight: 400, lineHeight: 1.2}
  poster-name: {fontFamily: "Libron", fontSize: "largest fitting integer 28–43pt", fontWeight: 700, lineHeight: 1.2}
  cover-event: {fontFamily: "Libron", fontSize: "34pt", fontWeight: 700, lineHeight: 1.2}
  cover-subtitle: {fontFamily: "Libron", fontSize: "23pt", fontWeight: 400, lineHeight: 1.2}
  cover-name: {fontFamily: "Libron", fontSize: "36pt", fontWeight: 700, lineHeight: 1.2}
  place-given-name: {fontFamily: "Libron", fontSize: "fit to one line, maximum 64pt", fontWeight: 700, lineHeight: 1.25}
  place-surname: {fontFamily: "Libron", fontSize: "fit to one line, maximum 76pt", fontWeight: 700, lineHeight: 1.25}
  round-marker: {fontFamily: "Libron", fontSize: "16pt", fontWeight: 700, lineHeight: 1.25}
  footer: {fontFamily: "Libron", fontSize: "12pt", fontWeight: 400, lineHeight: 1.25}
spacing:
  page-margin: "42pt"
  cover-margin: "48pt"
  speech-inset: "18pt"
components:
  speech-box: {backgroundColor: "{colors.pale}", textColor: "{colors.ink}", width: "528pt"}
  discovery-exhibit: {backgroundColor: "{colors.paper}", textColor: "{colors.ink}", width: "528pt"}
  stop-panel: {backgroundColor: "{colors.pale}", textColor: "{colors.burgundy}", width: "528pt", height: "61pt"}
  tent-face: {backgroundColor: "{colors.paper}", textColor: "{colors.ink}", width: "612pt", height: "288pt"}
---

# Design System: The Last Acquisition — Print

## Overview

**Creative North Star: “Museum Patron Folio”**

The user chose an ornate professional museum gala and then requested the black/red After Hours accents across every printable asset, with light paper for comfortable reading. White stock, near-black reading text, burgundy headings and restrained gilt detail now unite invitations, character sheets, player packets, manuals, records, cut cards, room signs and certificates. Libron, the approved identity and existing artwork remain. The current extension updates evidence flow and player/host instructions without changing that identity.

This document extracts `scripts/print_identity.py`, `scripts/build.py`, `scripts/printable_v2.py`, `scripts/after_hours_print.py` and `scripts/evidence_design.py`. It governs printable PDFs. The approved dark phone invitation and thirty character JPEGs remain separately scoped in the sidecar's `afterHoursPublic` extension; their temporary build PDFs are image-export intermediates. The independent homepage remains governed by `docs/DESIGN.md`, with no webpage changes authorized by this print refinement.

The concept seed `ad4b8f59`, assigned index 5, records the earlier Museum Patron Folio direction. Reconstructed possibilities were gala invitation, exhibition catalog, conservation dossier, artist salon, museum patron folio, accession ledger and exhibition wall label, not presented user choices. The October 5 light-paper direction supersedes the former teal print palette while retaining the folio geometry, Libron and ornate frames.

**Key Characteristics:**

- Safe face-up Picasso covers composed on a centered exhibition-poster axis, and twelve-page self-contained books.
- Light single-page Van Gogh character PDFs with full-width Acting Tips; separate approved dark phone JPEGs.
- Bold yellow relationship names and strong round boundaries.
- Ninety distinct hunt hints, photographic evidence and freeform accusations.
- Thirty full-sheet, two-sided tent cards with transparent avatars, black given names and burgundy surnames.

## Colors

Museum Ink (#191b1c) carries reading text on White Stock (#ffffff). Burgundy (#720f29) carries headings, labels, phase gates and warnings. Gilt Ornament (#866632) is limited to fine rules, portrait borders and fold guides. Pale Blush (#faf4f1) gives speech boxes, stop panels, instruction bands and the evidence diagram a light ground; Table Separator (#b9aca3) keeps manual tables quiet. Relationship Yellow (#fff099) remains restricted to bold names on day-of introductions. Portraits and evidence photographs retain their palettes.

`build.TEAL` and `build.RED` are compatibility aliases of the shared burgundy token, not additional colors. `print_identity.py` owns the shared print values. Do not reuse the dark phone palette for printable reading areas. The invitation's photographic top 383 pt retains the approved scene, night overlay and cream/gold display lettering; its lower reading area is white with burgundy accents and a pale date band.

## Typography

Libron Regular, Bold, Italic and BoldItalic are embedded as `Book`, `BookBold`, `BookItalic` and `BookBoldItalic`. The build pins v0.25 and verifies its archive against `scripts/font.sha256`. Standalone font binaries remain in the ignored build cache and are excluded from downloads.

Canvas paragraphs use 1.25 leading; manuals use 14/18 pt narrative and 20/24 pt headings. Character sheets measure content and choose 17, 16.5 or 16 pt narrative with 1.2 leading, names at the largest fitting integer from 28–43 pt, 17 pt italic roles and 15 pt section labels. Acting Tips have the same wide measure and narrative size as the relationships below the portrait.

Packets use 16 pt round markers, 14 pt running names and 27 pt section titles. Covers use a 34 pt bold event title, 23 pt italic subtitle and 36 pt bold character name, each with 1.2 leading and centered alignment. Introductions and histories use 16 pt. Each hearing page uses the same measured size for both speaking branches: 16 pt, or 15 pt when the paired content requires it. Coming Clean uses 15 pt for both statements. All ten questions and named targets fit on one page at 14 pt. Hunt hints use 19 pt italic. Auxiliary narrative stays at least 14 pt; auxiliary spoken instructions use 15–16 pt. Footer metadata uses 12 pt.

Tent cards fit given-name lines up to 64 pt and surnames up to 76 pt in a 365 pt measure; italic roles choose quarter-point sizes from 16–52 pt to fit at most two lines and 65 pt height. Full-page discoveries use 16 pt departments, 32 pt titles, 18 pt body, 17 pt fields and italic annotations, and 14 pt stamps. Discovery 3 uses 24 pt italic body. Room signs retain 48 pt names.

**The Reading Floor Rule.** Preserve at least 14 pt narrative. Reflow or edit content before reducing type. Twelve-point metadata is not a substitute for readable narrative.

**The Spoken Floor Rule.** Hearing speeches and Coming Clean stay at least 15 pt. On each hearing page, both branches receive the same type size, measure, inset and border treatment; their heights follow their measured text.

## Layout

US Letter is 612 × 792 pt. Coordinates run down from the top. Ordinary content and character sheets start at x=42 and span 528 pt; covers use x=48 and 516 pt. Room signs use landscape Letter.

Character sheets use the shared After Hours composition with light print colors: name at (42,36), role at (42,94), and hero top max(141, role_end+18). Portraits start at x=42 and use a measured 196 pt width, expanded to 250 or 230 pt when content fits. Descriptions start at x=portrait_width+66 in a 528−portrait_width−24 pt measure. Relationships and Acting Tips span 528 pt below the portrait. A pale costume band starts x=28 with width 556 pt, and its body spans 500 pt. The gold footer rule is y=747 and footer text y=756. Light character PDFs are in `OPEN_FREELY/PreParty_Individual` and the merged `02_PreParty_Character_Sheets_ALL.pdf`.

The invitation retains its (0,0,612,383) photographic hero and 62% night overlay on the left (0,0,306,383). The title begins (38,72), subtitle (42,238) and museum label (42,321). The light reading area begins below the hero, with gold divider y=388, burgundy tagline y=407, pale full-width date band (0,453,612,102), date y=469, time y=505, address y=576, collection y=619, attire y=678 and preparation reminder y=723. The printable `06_Invitation_and_Arrival_Guide.pdf` includes the light arrival guide as page 2.

Dark phone images come from separate `build/phone-posters/<slug>.pdf`, `build/phone-posters.pdf` and `build/phone-invite.pdf` intermediates, not the light printable PDFs. Character JPEGs are 1224 × 1584 pixels at 144 dpi, quality 90, subsampling 0, with provenance comments. The invitation JPEG uses the same 2× raster dimensions and quality 94. The phone ZIP contains exactly thirty character JPEGs plus `00_Invite.jpg`; `/iphone/Invite.jpg` uses the dark invitation. JPEGs and printable character PDFs deliberately differ in background treatment.

The authoritative twelve-page map is `source/game.json`:

| Page | Content |
| --- | --- |
| 1 | Safe ornate Picasso cover |
| 2 | INTRODUCTIONS: identity, highlighted relationships, acting tips, spoken introduction |
| 3 | INTRODUCTIONS: private background and conversations |
| 4 | HUNT FOR CLUES: three cryptic hints |
| 5–6 | ACT I: MOTIVE: one question page, IF INNOCENT / IF MURDERER answers |
| 7–8 | ACT II: OPPORTUNITY: one question page, IF INNOCENT / IF MURDERER answers |
| 9–10 | ACT III: METHOD: one question page, IF INNOCENT / IF MURDERER answers; no discovery index |
| 11 | ACCUSATIONS: loose ballot |
| 12 | COMING CLEAN: retained role statements |

Covers use one vertical axis at x=306. All cover text sits in a 516 pt measure starting x=48 and is centered. “Murder Mystery” starts y=54 at 34 pt bold; “Dinner Party 2026” starts y=99 at 23 pt italic. A 160 pt gold rule sits y=141. The Picasso frame occupies (144,156,324,462). The character name starts y=636 at 36 pt bold, followed by a second 160 pt gold rule y=695, “The Meridian Museum” y=711 at 14 pt italic, and date/private-packet/page metadata y=735 at 12 pt. Quiet double borders retain rectangles (28,28,556,736) and (33,33,546,726); the cover omits the corner crosshair ornaments. No branch, animal, grievance or secret appears on the cover. Page 2 has no costume suggestions or second portrait.

The user rejected the earlier cover screenshot because its left-aligned title did not share the portrait’s axis and the composition looked uncentered. This correction aligns event, portrait, sitter and museum metadata as one exhibition poster. The ornate frame supplies the depth, while restrained outer borders and short rules give the text a deliberate hierarchy. The centered cover composition remains in the current light-paper refinement; its subtitle and museum label now use burgundy while the event title and sitter name use black.

Round markers start at (42,30), running names y=62 and black divider y=89, with an additional 0.4 pt gold rule y=92. A 22 pt burgundy museum mark sits at (542,28). Questions occupy two 252 pt columns at x=42/318, five groups each starting y=226. Each group has three named targets. Directions point to answer pages 6,8,10. Speech boxes span 528 pt, text starts at x=60 across 492 pt, and box height is measured text plus 22 pt.

Stop panels occupy (42,686,528,61). A burgundy octagon centered at (66,716), radius 20 pt, reinforces the 14 pt message at (96,700): **“STOP! Do not turn the page yet. Wait for the host to announce the next round.”** Bottom footers number packet pages. Within-round transitions give explicit continuation instructions. Ballot page 11 has no stop panel: guests tear off and turn in that page, then keep the packet for Coming Clean.

The current discovery set has sixteen short, stand-alone original records, each on a full Letter page in its numbered envelope, with no cutting or dashed cut border. The active `build_evidence()` renderer starts each department at (42,110) in the 528 pt measure, then flows a 32 pt title, an optional 528 × 245 pt photo, rows, body and annotation. Department advance is measured text plus 12 pt; title advance adds 24 pt. Photos advance 265 pt. Row labels span 170 pt at x=42; values span 344 pt at x=226; rows add 10 pt after the taller cell. Body paragraphs add 14 pt. Annotations begin 12 pt after body and add 14 pt; stamps begin 16 pt after content and end by y=730. The footer identifies the museum and discovery number. There are no attached recovery, authentication or alibi sections. The obsolete half-sheet `draw_discovery()` helper is not invoked.

F4 occupies two pages: installation inspection, followed by a technical AV archive. Its archive groups the current thirty generic sources under telephone circuits, access-control logs, and audio/video records; identities and private conversation contents are redacted. It reports technical observations rather than solving advice. F5 gives raw clock synchronization and textile/toxin comparison findings. F1/F5 photos retain 528 × 225 pt, F4 retains 528 × 180 pt, and F3 retains a 528 × 135 pt floor diagram. These are current source-derived configurations, not frozen release counts.

Each tent uses the entire Letter sheet, with no cutting or outer border: two 612 × 288 pt faces and two 108 pt base flaps. Dotted fold guides sit at y=108/396/684. Rotate the upper face 180 degrees so both faces read upright when assembled. Names start x=42 in a 365 pt column, fitting each name line at the largest size allowed by its width and height. Titles fit in at most two lines within a 65 pt height; short titles can use larger type. Transparent avatars occupy a 145 × 249 pt slot at x=425. Overlap and tape the base flaps. Print single-sided at 100%.

Leave ballot page 11 loose inside and staple the other pages in order. Guests retain Coming Clean. Do not use booklet or two-pages-per-sheet printing.

## Elevation & Depth

Generated gilt framing supplies carved museum depth, with a native transparent center. Interior pages stay flat, using spacing, outlines and hierarchy. There are no PDF drop shadows, motion or responsive breakpoints.

## Shapes

Safe packet covers retain double gold borders and omit corner ornaments, keeping a quiet outer mat around the ornate portrait. Character sheets use the framed portrait and horizontal rules from the After Hours composition rather than the obsolete double-border poster renderer. Records and speech boxes stay square. Ordinary outlines are 0.7 pt and rules 0.6 pt. Tent cards have no borders; gold fold guides are 0.8 pt with a [1,3] pt dash. The burgundy octagon reinforces the written stop.

## Components

**Framed portrait.** `framed()` intentionally crops the print composition into the gilt aperture with aspect-preserving scaling and clipping. Aperture fractions are x=0.18, y=0.14, width=0.64, height=0.72 of the 2:3 frame. This replaces the old “never crop” rule for poster and cover placements. Full-resolution, full-composition masters remain in the source archive. Other `Sheet.image()` placements retain centered aspect-fit.

**Image encoding.** Opaque print images fit within 900 × 900 and use quality-88 JPEG, subsampling 1. Ornament color uses that encoding with a lossless native-alpha soft mask. Other alpha artwork uses PNG within 480 × 480 and an automatic mask. The thirty native chibi WebP masters preserve full-resolution alpha. Public Portraits contain sixty JPEGs and thirty lossless alpha WebPs within 900 × 900. Organizer source retains exact prompts and hashes; public exports carry harmless provenance.

**Museum stationery header.** The architectural museum mark is burgundy geometry with a 0.85 pt stroke. Generic headers use 24 pt marks at (42,26); manual headers use 18 pt marks there; packet headers use 22 pt marks at (542,28). Generic/manual headers pair a 0.9 pt burgundy rule at y=82 with a 0.4 pt gold rule at y=86, spanning x=42 to page_width−42. Manual label and brand positions preserve the existing reading space. Footer rules are 0.4 pt gold. Signs keep the larger 40 pt museum mark within their existing landscape composition.

**Introduction.** Relationship names are bold/yellow, including unambiguous first-name aliases where used. Description, relationships and wide Acting Tips orient the guest. Only the bordered introduction is spoken. Private briefing follows separately. If a measured spoken introduction ends with a single word, the renderer joins only its final two words with a nonbreaking space and remeasures the box. Source words and punctuation stay unchanged; other speech content and body sizes are preserved.

**Hearing.** Guests choose unanswered present characters by name and pass the question to the next guest. All three hearing pages (6, 8 and 10) contain independently authored IF INNOCENT and IF MURDERER speeches. Role headings stay outside pale, burgundy-bordered spoken boxes. Both branches share identical styling and the same measured 16 or 15 pt size. Coming Clean uses the same paired-box pattern at 15 pt. Select and announce the eligible animal before Motive; retain that branch through all hearings and Coming Clean. There is no investigation grid, separate catalog, Method discovery index or selected-clue checklist.

**Hunt.** The private page is titled “The game is afoot”. Its introduction asks guests to bring found envelopes to their seat at the table; the guest with the most envelopes wins a special prize. It has three hints and no closing paragraph. `source/hunt_copy.yaml` is the editable, location-first source; `scripts/hunt_copy.py` validates the current ninety unique hints, three distinct locations per role, and numbered-envelope coverage. `source/hunt.json` is a generated compatibility snapshot, not the editing source.

**Museum evidence.** Sixteen original records and five staged reports mix agreements, notes, work orders, diagrams and photographs. Clock-comparison, actual-installation and obsolete-display images join the earlier evidence art; gilt framing is generated too. The old proposal and actual installation photograph carry distinct documentary contexts. These are evidence objects, not descriptions of imagined images.

Each discovery is the original evidence object alone. Generic technical recordings belong on F4's AV inspection page, without assigning a fixed personal alibi. Selected testimony provides each role's personal account. Coming Clean resolves testimony after voting and supplies no essential new proof.

**Hosting.** The guide organizes preparation, directories, memorized-animal selection, assembly, placements, agenda, announcements and finale. Host instructions omit turn tracking, repeated-answer and discussion directions. Attendance and ballot tallying support the finale. The player Coming Clean introduction says to read only when called and use the role's own box; the animal fallback remains in the host's finale instructions.

**American copy.** Current editable copy uses American spelling. `scripts/american_copy.py` normalizes current output, including exported historical material; original historical precursor files remain preserved.

**The Locked Ballot Rule.** Collect ballots and match attendance before Coming Clean. Rank attending names by votes, including zero; break ties alphabetically by full name. Exactly three suspects read their appropriate statements, all three even after an early confession. If none confesses, call the selected animal to read IF MURDERER.

## Do's and Don'ts

- Do preserve the centered cover axis at x=306, safe cover, twelve-page order, loose ballot and retained finale.
- Do give all three hearings equally styled branch boxes at 15 pt or larger, and Coming Clean statements at 15 pt.
- Do select the animal before Motive and preserve the same branch through the finale.
- Do keep each short original discovery on its own full Letter page in one numbered envelope.
- Do keep light printable PDFs and approved dark phone JPEGs separate.
- Do preserve source words, all game mechanics, fonts and geometry during visual refinements.
- Do keep relationship names bold/yellow and Acting Tips full width.
- Do preserve readable narrative, distinct art identities and native avatar alpha.
- Do print one tent sheet per guest at 100%, with taped base flaps.
- Do preserve the three spoiler-handling directories and immediately returned memorized-animal slips.
- Don't reintroduce notes grids, A/B cards, external catalogs or separate finale files.
- Don't restore common Motive/Method answers, the Method discovery index or half-sheet discovery cutting.
- Don't attach recovery or authenticated alibi extracts to discoveries, or add solving advice to raw technical findings.
- Don't put private information on a face-up cover or shrink prose to hide overflow.
- Don't distribute font binaries or organizer prompts to guests.
- Don't apply dark phone backgrounds to printable reading areas.
- Don't replace the separate homepage identity with ornate print styling.

Build assertions check measured bounds and glyph support. `scripts/verify.py` renders PDFs and maps repeated visuals by raster hash. Actual review coverage, corrections and confirmation belong in `docs/GALA_FINISH_REVIEW.md` and the current review report. This specification carries no frozen review counts, release hashes or “ship” claim. Playtest scope belongs in `docs/PLAYTEST_SUMMARY.md`; earlier all-correct/2-of-5 ratings describe the rejected edition. Digital review and model table reads do not establish physical printer quality or live-human difficulty.
