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
  read-aloud:
    fontFamily: "Libron"
    fontSize: "16pt"
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
  place-given-name:
    fontFamily: "Libron"
    fontSize: "24pt"
    fontWeight: 700
    lineHeight: 1.25
  place-surname:
    fontFamily: "Libron"
    fontSize: "29pt"
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
  discovery-inset: "16pt"
  speech-inset: "24pt"
components:
  discovery-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "528pt"
    height: "302pt"
    padding: "16pt"
  speech-box:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    width: "528pt"
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

**Creative North Star: "Readable museum working documents"**

The Meridian Museum gala uses white stock, scholarly book typography, restrained blue institutional identity and thin rules. These are working objects for reading aloud, handwriting, room finding and cutting. The theatrical character comes from museum records, art-world identities and recognizable portraits rather than decorative clutter. This document records `scripts/build.py` and `scripts/evidence_design.py`; the independent homepage authority remains `docs/DESIGN.md`.

The Living Collection gives thirty fictional identities three distinct artworks each: Van Gogh inspired public portraits, Picasso inspired private portraits and transparent chibi place-card avatars. Matching facial features, costume colors and signature accessories support recognition. The event belongs to 2026 and costume inspiration is optional. All thirty roles are eligible for the memorized animal selection.

**Key Characteristics:**
- Fourteen-point narrative floor and larger public introductions.
- Twelve-page self-contained packets with named questions, answers, records, ballot and Coming Clean.
- Branch labels outside speech boxes and explicit stop instructions.
- Realistic records and photographic evidence.
- Transparent chibi cards with names on two lines.
- Flat white paper, generous margins and restrained museum color.

## Colors

Meridian Blue is the primary institutional accent: museum headers, public names, section titles, speech-box outlines and sign frames. Private Warning is secondary, applied to explicit privacy and stop text, discovery annotations and stamps. Words carry these instructions as well as color.

Museum Ink carries narrative, ordinary headers and writing rules. White Stock is the page ground. Table Separator is the pale facilitator table rule. Ivory Portrait Matte sits behind public, private and invitation paintings. Character painting palettes remain specific to the artwork rather than replacing this shared palette.

## Typography

Libron Regular, Bold, Italic and BoldItalic are embedded as `Book`, `BookBold`, `BookItalic` and `BookBoldItalic`. Canvas paragraphs use 1.25 leading. Manuals use 14/18 pt body and 20/24 pt headings. The font cache in `build/fonts` is checked against `scripts/font.sha256` when downloaded; standalone font binaries are excluded from the source ZIP.

Public introductions measure their text and select the largest fitting size from 18, 17 and 16 pt; names are 34 pt, roles and section labels 16 pt, metadata 12 pt. Packet names and ballot/Coming Clean titles are 30 pt; Questions to ask and Your answer headings are 27 pt; action headings are 18 pt. Named ASK rows use bold 14 pt and questions use 16 pt. Motive and Opportunity speech use 16 pt; Method speech, its integrated records and Coming Clean use 14 pt. Branch labels use bold 16 pt.

Place cards set first and middle names together at 24 pt and surnames on the second line at 29 pt; roles use 14 pt. Discovery titles use 22 pt, narrative and record rows 14 pt, departments/stamps/discovery numbers 12 pt. Reports use 30 pt titles, 18 pt Certified findings headings and 14 pt findings; supporting report summaries use 16 pt, with the F3 timeline labels at 18 pt. Room signs use 48 pt names, 24 pt museum identity and 23 pt descriptions. Awards use 34 pt titles. Auxiliary footers, roster names and ticks' labels, and assembly directories use 12 pt.

**The Narrative Floor Rule.** Preserve 14 pt narrative text; introductory prose measures between 16 and 18 pt. Twelve-point type serves auxiliary labels rather than shrinking narrative to fit.

## Layout

US Letter stock is 612 × 792 pt; room signs use landscape 792 × 612 pt. Coordinates in this document run down from the top. General content begins at x=42 and spans 528 pt. Canvas museum metadata begins at y=28, document labels at y=55, the rule at y=82 and footers at y=760. Manuals use 42 pt side margins, 90 pt top and 48 pt bottom margins.

Introductions have a 552 × 732 pt frame at (30,30), a name at (42,44), role at y=93 and rule at y=141. The ivory portrait frame at (42,158) is 180 × 230 pt; its one-point-inset slot is 178 × 228 pt. Biography and relationships use a 324 pt column at x=246. Acting tips start at (42,414) in a 180 pt column; the 528 pt costume section follows the taller column. Each introduction is one PDF page and a 2× PNG (144 dpi metadata) for sending to phones; this is a fixed page image.

Each named packet has twelve pages in this exact sequence:

| Pages | Content |
| --- | --- |
| 1 | Private background, Picasso portrait and three social tasks |
| 2–3 | Motive questions |
| 4 | Common Motive answer |
| 5–6 | Opportunity questions |
| 7 | IF INNOCENT / IF MURDERER Opportunity answers |
| 8–9 | Method questions |
| 10 | Branch Method answers with preparation records inside each box |
| 11 | Ballot |
| 12 | Coming Clean, both branches |

The first private page has a 144 × 216 pt portrait frame at x=42 below the name and a 142 × 214 pt inset image slot; its background column starts at x=210 with a 360 pt measure. Tasks start 19 pt below the taller column. Question pages begin their five groups at y=218. Each group lists three full names; the ten shared groups per round cover all thirty roles. There is no fixed-seat question order.

Ordinary speech boxes span 528 pt at x=42, with a 480 pt text measure at x=66. Their height is measured text height plus 30 pt; private labels are drawn separately at x=55 across 502 pt. Coming Clean uses a 500 pt measure at x=56 and boxes of measured height plus 24 pt. Ballot fields use generous ruled writing space. Notes appear after round answers only where measured space remains.

Discovery cards are two per sheet: 528 × 302 pt at (42,104) and (42,422), with 496 pt text measure and 16 pt side insets. Photo slots measure 496 × 116 pt. Reports are five separate one-page sheets; F1 and F5 use 528 × 225 pt photographic slots. Place cards are 252 × 302 pt, four per Letter sheet over eight sheets, at x=42/318 and y=104/422. Names start at x+13; the transparent avatar slot is (x+10,y+97), 110 × 189 pt. The role column is at (x+133,y+105), 106 pt wide. These cards have no seat number or collection footer.

The invitation retains the 552 × 732 pt frame and three Van Gogh frames at x=48/224/400, y=200, each 164 × 212 pt with 162 × 210 pt image slots. Event details begin at y=431; page two is the arrival guide. Animal slips are 166 × 106 pt, three columns and five rows per sheet; four sheets supply matching thirty-animal A and B sets. Extra standalone ballots are two 528 × 305 pt forms per sheet. Signs have a 720 × 540 pt frame at (36,36).

Print single-sided at Actual size / 100%. Do not use booklet or two-pages-per-sheet modes. Staple the twelve-page packet in order along the left edge and give it with a pencil at arrival.

## Elevation & Depth

The system is flat. Whitespace, thin rules, typography and occasional ivory portrait grounds establish hierarchy. There are no shadows, gradients, motion or responsive breakpoints in the PDF system.

## Shapes

Frames and cuttable cards have square corners. Canvas rectangle outlines are 0.7 pt and rules 0.6 pt; facilitator table separators are 0.4 pt. Cut boundaries use a 3 pt on / 3 pt off dash. Introduction, invitation, speech and sign frames are solid. Place cards display flat or in stands; their cut border is not a folding instruction.

## Components

**Public introduction:** one-page identity, biography, relationships, acting tips and optional costume guidance. Send this document before the party; the private packet stays at the venue.

**Character artwork:** `Sheet.image` centers the full composition with aspect-fit scaling. RGB paintings are thumbnailed within 900 × 900 pixels and embedded as quality-92 JPEGs with subsampling disabled. Alpha artwork becomes RGBA, thumbnailed within 480 × 480 and embedded as PNG with an automatic transparency mask. The committed thirty `chibi.webp` assets preserve native full-resolution RGBA transparency; original chibi JPEG precursors remain in assets. Public Portraits contain sixty painting JPEGs and thirty lossless chibi WebPs, thumbnailed within 900 × 900, with harmless provenance. Organizer source retains full-resolution assets and exact generation metadata. Builds consume committed artwork without regenerating it.

**The Full Composition Rule.** Center artwork using the smaller slot-to-image scale; never stretch or crop the composition.

**Place card:** two name lines above a transparent chibi and adjacent role. No matte rectangle, numbered seat identifier or Living Collection footer appears. Four cards per sheet preserve cutting clearance.

**Complete packet:** a private background followed by the three hearings, internal ballot and final Coming Clean page. Common grouped questions live in `source/question_rounds.json`, character answers and records in `source/characters.json`, and page mapping in `source/game.json`. Each question chain chooses an unanswered present guest by name; the host checklist confirms everyone answers once. Guests read only their appropriate box and keep its label private. Method records are embedded in the spoken answer, with no A/B card selection or evidence envelopes.

**The Locked Ballot Rule.** Coming Clean stays unread until every ballot is collected and locked. The top three suspects read their appropriate statements; if none confesses, the announced animal stands and reads IF MURDERER.

**Discovery and forensic report:** sixteen actual fictional museum records and photographs occupy eight two-up sheets. Five one-page mandatory reports release F1–F2 before Motive, F3 before Opportunity and F4–F5 before Method. Six photographic assets cover the warning note, condition photo, crate seal, performance sketch, silver coupe and fiber comparison. Typed text supports the handwritten warning scan. Department lines, record fields, annotations and stamps create the artifact rather than prose describing an imagined prop.

**Host-safe guides:** fifteen planned facilitator pages provide preparation, copy counts, directory, animal draw, assembly, clue placement, agenda, welcome, hearing scripts, voting and troubleshooting. A page-count assertion checks that each source section remains one page. The attendance checklist has thirty named rows spaced 18 pt apart and four 11 pt ticks at x=365/425/485/545 for Here, Motive, Opportunity and Method. Assembly lists names and twelve-page blocks without branch content. `OPEN_FREELY`, `PRINT_WITHOUT_READING` and `SPOILERS_DO_NOT_OPEN` remain packaging boundaries.

**Physical props:** two matching animal sets serve all thirty roles. Guests memorize and immediately return folded A slips to a closed return box; remove unused A animals from B before selection. Ballots and awards provide handwriting space, museum signs support room finding and exhibition labels use the same institutional vocabulary.

## Do's and Don'ts

- Do preserve the twelve-page sequence, including preparation records, ballot and both Coming Clean statements.
- Do keep explicit stop warnings and branch labels outside spoken boxes.
- Do use named question groups and tick each attending respondent once per round.
- Do memorize animals and immediately return folded slips to a closed box.
- Do print single-sided at 100% and cut dashed borders.
- Do embed PDF fonts without shipping standalone font binaries.
- Do preserve character identity across all three artwork styles and transparent avatar edges.
- Do inspect new rendered evidence whenever source or rendering changes.
- Don't replace the independent homepage system.
- Don't send private packets as pre-party introductions.
- Don't reintroduce separate finales, A/B evidence cards, question catalogs or seat-order mechanics.
- Don't shrink narrative text to conceal overflow.
- Don't expose exact prompts in public derivatives.
- Don't add branch-dependent portraits or illustrations to later private rounds.
- Don't stretch or crop character artwork.

Build assertions reject unsupported glyphs and overflow beyond measured text limits. `scripts/verify.py` renders all PDF pages, maps visual duplicates by raster hash and checks text bounds, type below 11.9 pt, replacement glyphs and blank pages. The current `build/review/report.json` records 87 PDFs, 930 rendered pages, 498 unique visuals, 125 contact sheets and zero structural issues. The independent finish review in `.impeccable/review/complete-packet-finish-review.md` records inspection of all 125 contact sheets and eight full-page zooms, with disposition **ship** and no material fixes. This is digital visual evidence, not a physical printer proof or an independent gameplay simulation. No HTML detector ran for the PDF canvas system. Documentation synchronization does not change the reviewed PDF source or generated PDFs.
