---
name: The Last Acquisition — printable museum system
description: Readable, cuttable documents for the Meridian Museum gala in 2026.
colors:
  ink: "#132e38"
  teal: "#057294"
  private-warning: "#8b2636"
  paper: "#ffffff"
  table-rule: "#a8c4cd"
  portrait-matte: "#f6f1e7"
typography:
  body:
    fontFamily: "Libron"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.25
  introduction:
    fontFamily: "Libron"
    fontSize: "16–18pt"
    fontWeight: 400
    lineHeight: 1.25
  character-name:
    fontFamily: "Libron"
    fontSize: "34pt"
    fontWeight: 700
    lineHeight: 1.25
  manual-heading:
    fontFamily: "Libron"
    fontSize: "20pt"
    fontWeight: 700
    lineHeight: 1.2
  room-sign:
    fontFamily: "Libron"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 1.25
  footer:
    fontFamily: "Libron"
    fontSize: "12pt"
    fontWeight: 400
    lineHeight: 1.25
spacing:
  page-margin: "42pt"
  evidence-inset: "16pt"
  card-inset: "18pt"
components:
  evidence-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "528pt"
    height: "293pt"
    padding: "16pt"
  discovery-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "528pt"
    height: "303pt"
  introduction-portrait:
    backgroundColor: "{colors.portrait-matte}"
    width: "180pt"
    height: "230pt"
  private-portrait:
    backgroundColor: "{colors.portrait-matte}"
    width: "144pt"
    height: "216pt"
  place-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "252pt"
    height: "302pt"
---

# Design System: The Last Acquisition — Print

## Overview

This document records the PDF implementation in `scripts/build.py`, guided by `PRODUCT.md`. Its scope is the printable kit and pre-party character images. The homepage retains the independent system in `docs/DESIGN.md`.

The museum's objects are readable working documents: book typography, plain white stock, blue institutional fields, and enough space to read, annotate, cut, and seal. The setting is the Meridian Museum's October 30, 2026 gala, not a period costume requirement. Costume suggestions are optional inspiration.

The Living Collection extends that system with 90 separately generated artworks for 30 fictional identities: a Van Gogh inspired portrait for each public introduction, a Picasso inspired portrait for the first private packet page, and a chibi manga avatar for each museum-label place card. Facial features, hair, costume colors and signature accessories carry across each trio; the artwork adds character recognition without changing the investigation or the homepage design authority.

## Colors

Ink carries reading text and fine rules. Teal marks the museum identity, section titles, sign borders, and introduction/invitation names and frames. Introductions and invitations retain white-stock reading areas rather than solid teal headers. The private-warning color marks private document headers; privacy instructions also appear in words, so color does not carry the distinction alone. Table-rule is the facilitator table separator.

Portrait-matte is the warm ivory field behind introduction, private-page and invitation artwork. The varied painting palettes belong to the fictional identities recorded in `source/art_direction.json`; they do not replace the museum palette.

## Typography

All printable roles use Libron Regular, Bold, Italic, or BoldItalic, registered as `Book`, `BookBold`, `BookItalic`, and `BookBoldItalic`. Narrative body is at least 14 pt. Footer and short evidence handling instructions are 12 pt; these are supporting labels, not the body-text target. General canvas paragraphs use 1.25 leading; manuals use 14/18 pt and 20/24 pt headings.

Introductions measure their actual text and choose the largest fitting size from 18, 17, and 16 pt. They have 34 pt names, 16 pt roles and section headings, and 12 pt collection/date labels. Playable packets use 30 pt names, 26 pt hearing titles, 18 pt action headings, 16 pt speech boxes, and 14 pt private background and instructions. Place cards use 26 pt names, 14 pt roles and 12 pt collection/ID labels. Discovery/exhibit cards use 22 pt titles and 16 pt bodies. Signs use 48 pt names, 24 pt museum identity, and 23 pt descriptions. Awards use 34 pt titles.

Build fonts are cached under `build/fonts`; the Libron v0.25 archive is checked against `scripts/font.sha256` when downloaded. PDFs embed their fonts and need no guest font installation. The source ZIP excludes `.ttf`, `.woff`, `.woff2`, and `.pyc`; font binaries are not distributed as standalone assets.

## Layout

Default stock is US Letter, 612 × 792 pt. General content spans x=42 to x=570, a 528 pt width. The museum header begins at y=28, the document label at y=55, and the rule at y=82; canvas coordinates are measured down from the top. Footers begin 32 pt above the bottom. Manuals have 42 pt side margins, 90 pt top margins, and 48 pt bottom margins.

Introductions use a 552 × 732 pt frame at (30,30), a name at (42,44), a role at y=93 and a rule at y=141. The ivory portrait frame is 180 × 230 pt at (42,158), with a 178 × 228 pt image slot inset by 1 pt. Biography and immediate relationships occupy the 324 pt right column at x=246; acting tips sit below the portrait in a 180 pt left column at y=414. The full-width 528 pt costume section starts below the taller column. Every introduction remains exactly one PDF page, without page numbers or numerical ages, exported to a 2× PNG for sending and zooming on phones. This is a fixed page image, not a responsive web layout.

Playable packets are four pages per guest: private background and three tasks, Round 1 / Motive, Round 2 / Opportunity, and Round 3 / Method. On the first page only, a 144 × 216 pt ivory portrait frame at x=42 starts below the name; its image slot is 142 × 214 pt with a 1 pt inset. Private background occupies a 360 pt column at x=210, and the task section starts 19 pt below the taller of the background and portrait. Later pages retain the full-width speech boxes with 528 pt frames and 480 pt text at x=66. Selection labels sit outside their boxes at x=55, with a 502 pt measure. Only the boxed words are spoken; labels remain private. There is no confession in these four pages. Each guest has a separate, single-page FINALE document sealed in its own named envelope. The host holds all FINALE envelopes on a tray and distributes them only after all ballots are collected.

Evidence uses 30 sheets: one guest per sheet, with their A/B cards stacked vertically. Rectangles are 528 × 293 pt at y=106 and y=425, with 496 pt text measures and 16 pt side insets. Discovery and exhibit cards are two per sheet, 528 × 303 pt, with 492 pt text measures. Animal slips are a three-column, five-row grid of 166 × 106 pt rectangles. Name/place cards are two columns by two rows, 252 × 302 pt, four per Letter page and eight pages for 30 cards. Card origins are x=42/318 and y=104/422. The chibi slot is 110 × 169 pt at (x+10,y+97); the 106 pt role column starts at (x+133,y+105). Names have a 226 pt measure, followed by a rule at y+277 and the collection/ID label at y+282. Ballots are two 528 × 305 pt forms per sheet. Landscape room signs use 792 × 612 pt stock and a 720 × 540 pt frame at (36,36).

The invitation's first page retains the 552 × 732 pt frame and uses three Van Gogh artworks: Artie Ficial, Dada DiCapo and Vincent Van Faux. Their ivory frames are 164 × 212 pt at x=48/224/400, y=200, with 162 × 210 pt image slots. The event details begin below the gallery at y=431; the second page remains the arrival guide.

Print single-sided at Actual size / 100%. The layout and assembly instructions assume this scale and explicitly exclude booklet and two-pages-per-sheet modes.

## Elevation & Depth

The print system is flat. Solid fields, whitespace, typography, and rules establish hierarchy. There are no shadows or gradients.

## Shapes

Frames and cuttable cards have square corners. Rectangle outlines are 0.7 pt; rules are 0.6 pt. Cuttable pieces use a 3 pt on / 3 pt off dash. Sign, invitation, and introduction frames are solid. Dashed borders indicate physical cutting, not an interactive state.

## Components

**Introduction:** identity field, prose description, relationship bullets, acting tips, and optional costume inspiration on one page. Do not add game branches or secret mechanics to this pre-party document.

**Character artwork:** `Sheet.image` converts to RGB, thumbnails within 900 × 900 pixels and embeds a quality-92 JPEG with subsampling disabled. Each slot uses the smaller width/height scale and centers the full composition, without stretching or cropping. Ivory matte remains visible around unequal aspect ratios in the introduction, private and invitation frames. Place-card avatars fit their white-stock slot. Artwork is identical for both guilt branches and never appears in later hearing pages. Exact prompts, identity specifications and hashes remain in organizer-only `source/art_direction.json` and full-resolution JPEG metadata in the source ZIP. The complete kit's 90 `OPEN_FREELY/Portraits` JPEG derivatives and 30 introduction PNGs carry harmless origin metadata; native generated PNGs remain at the image tool's original local locations. Builds consume committed assets without regenerating them.

**Museum-label place card:** a chibi avatar beside the 14 pt role, with a large name above and collection/ID label below. Display flat or attach to a place-card stand; the dashed border is a cutting boundary, not a fold instruction.

**Playable packet:** four consecutive pages with private background and tasks, Motive, Opportunity, and Method. Every guest has tailored questions stored in `source/characters.json` under `questions`. The motive answer is the same for both branches; Opportunity and Method have private IF INNOCENT / IF MURDERER labels outside their safe speech boxes. Guests memorize animals and immediately return folded slips to a closed box; nobody keeps a slip. The announced memorized animal selects the murderer branch. Every boxed response is safe to read at its round. Lines below the motive answer support notes. No improvisation is required; acting remains optional.

**Sealed finale:** one separate named page held by the host in the FINALE tray until ballots are locked; only the announced murderer then opens and reads its confession. Optional roles have no selectable confession. The combined finale file is for blind printing, never guest sharing.

**Evidence pair:** both branches carry neutral MERIDIAN / SETUP RECEIPT text, guest identification, salon door entry, cabinet-key loan, linen inventory, and an ordinary setup purpose. No unique guilty title or confession distinguishes the selected receipt. Both A/B cards travel together in a labeled EVIDENCE envelope; the Method page tells the player which to submit privately. The facilitator counts one selected receipt per attending ID, returns it, and the guest reads their Method answer followed by that receipt. Salon entry after 6:40, cabinet-key access during setup, and matching linen intersect to identify the murderer; each criterion alone can implicate innocent guests. A and B do not consistently identify innocence or guilt.

**Discovery/report card:** textual act labels separate Act I finds from F1–F5 reports released in stages: F1–F2 before Motive, F3 before Opportunity, and F4–F5 before Method. Two note cards use Italic, while records use Regular.

**Host-safe assembly guide:** names and sheet numbers only; no evidence or branch assignments. `OPEN_FREELY`, `PRINT_WITHOUT_READING`, and `SPOILERS_DO_NOT_OPEN` remain functional packaging boundaries.

**Questions & Notes:** one complete nine-page copy per seating pair combines a deduction-notes cover and an ID-ordered catalog of every guest's tailored Motive, Opportunity, and Method questions. The cover has ruled spaces for motive, salon entry after 6:40, cabinet-key access, and matching linen. Guests ask the next occupied seat's named question for the current round; the last asks the first and absent IDs are skipped. Cover instructions and note labels are 16 pt, catalog guest headings 18 pt, and catalog question text 14 pt. Catalog entries are measured and moved together to the next page when necessary.

**Attendance and Hearing Roster:** the facilitator tracks all 30 characters by ID and name. Rows are 18 pt apart, with 11 pt square ticks labeled Here / R1 / R2 / R3. Roster labels are supporting 12 pt text. Absent IDs are skipped; ticks confirm every attending guest has participated in all three rounds.

**Facilitator guide:** fifteen planned pages contain a contents page, preparation and copy-count checklists, the 30-character ID directory over two pages, memorized animal assignment, blind assembly, numbered clue placement, a timed agenda, welcome and three round scripts, vote/finale/awards instructions, and quick cues/troubleshooting. Each planned section starts on its own page. The guide remains spoiler-safe; it does not expose branch assignments or confessions.

**Props:** signs support room finding; blanks on ballots and certificates support handwriting. Core player and murderer bowls contain matching 15-animal sets; optional animals stay out of the murderer bowl.

## Do's and Don'ts

- Do preserve the canonical murder facts, branch assignments, evidence contents, and host-blind selection logic when changing layout.
- Do keep introductions single-page and phone-readable, playable packets four-page with separately sealed single-page finales, and evidence pairs cuttable without revealing guilt through their labels.
- Do preserve optional costume language and physical play without QR codes or phone mechanics.
- Do measure text before drawing, preserve the 14 pt narrative floor, and use explicit overflow limits rather than truncating content.
- Do preserve all three distinct artworks per fictional identity, the full aspect-fit composition, and harmless public provenance metadata.
- Do review both the 90 source artworks and rendered placements when artwork or geometry changes.
- Don't distribute the font cache or send private packets with pre-party introductions.
- Don't expose exact generation prompts in public derivatives; their negative constraints refer to plot objects.
- Don't add branch-dependent portraits, later-round illustrations or visual evidence to character artwork.
- Don't infer that a rendered PDF proves the murder logic correct or every page visually approved.

Build assertions reject unsupported glyphs and canvas text exceeding each block's bottom limit. The build asserts single-page introductions and exports all 30 character PNGs. `scripts/verify.py` renders every PDF page, maps exact visual duplicates to shared review images, checks safe bounds, text below 11.9 pt, replacement glyphs, blank pages, single-page introduction, four-page playable packet, and single-page finale counts, A/B presence, distinct branch cards, and nonempty branch/final statements. Its contact sheets support human visual review. These are implemented checks, not a substitute for inspecting the renders or a claim about the latest run's outcome.
