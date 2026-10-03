---
name: The Last Acquisition — printable museum system
description: Readable, cuttable documents for the Meridian Museum gala in 2026.
colors:
  ink: "#132e38"
  teal: "#057294"
  private-warning: "#8b2636"
  paper: "#ffffff"
  table-rule: "#a8c4cd"
typography:
  body:
    fontFamily: "Libron"
    fontSize: "14pt"
    fontWeight: 400
    lineHeight: 1.25
  introduction:
    fontFamily: "Libron"
    fontSize: "16–20pt"
    fontWeight: 400
    lineHeight: 1.25
  character-name:
    fontFamily: "Libron"
    fontSize: "36pt"
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
---

# Design System: The Last Acquisition — Print

## Overview

This document records the PDF implementation in `scripts/build.py`, guided by `PRODUCT.md`. Its scope is the printable kit and pre-party character images. The homepage retains the independent system in `docs/DESIGN.md`.

The museum's objects are readable working documents: book typography, plain white stock, blue institutional fields, and enough space to read, annotate, cut, and seal. The setting is the Meridian Museum's October 30, 2026 gala, not a period costume requirement. Costume suggestions are optional inspiration.

## Colors

Ink carries reading text and fine rules. Teal marks the museum identity, section titles, sign borders, and introduction/invitation fields. White text appears on those solid teal fields. The private-warning color marks private document headers; privacy instructions also appear in words, so color does not carry the distinction alone. Table-rule is the facilitator table separator.

## Typography

All printable roles use Libron Regular, Bold, Italic, or BoldItalic, registered as `Book`, `BookBold`, `BookItalic`, and `BookBoldItalic`. Narrative body is at least 14 pt. Footer and short evidence handling instructions are 12 pt; these are supporting labels, not the body-text target. General canvas paragraphs use 1.25 leading; manuals use 14/18 pt and 20/24 pt headings.

Introductions measure their actual text and choose the largest fitting size from 20, 19, 18, 17, and 16 pt. They have 36 pt names, 16 pt roles and section headings, and a 12 pt date line. Playable packets use 30 pt names, 26 pt hearing titles, 18 pt action headings, 16 pt speech boxes, and 14 pt private background and instructions. Discovery/exhibit cards use 22 pt titles and 16 pt bodies. Signs use 48 pt names, 24 pt museum identity, and 23 pt descriptions. Awards use 34 pt titles.

Build fonts are cached under `build/fonts`; the Libron v0.25 archive is checked against `scripts/font.sha256` when downloaded. PDFs embed their fonts and need no guest font installation. The source ZIP excludes `.ttf`, `.woff`, `.woff2`, and `.pyc`; font binaries are not distributed as standalone assets.

## Layout

Default stock is US Letter, 612 × 792 pt. General content spans x=42 to x=570, a 528 pt width. The museum header begins at y=28, the document label at y=55, and the rule at y=82; canvas coordinates are measured down from the top. Footers begin 32 pt above the bottom. Manuals have 42 pt side margins, 90 pt top margins, and 48 pt bottom margins.

Introductions use a 552 × 732 pt frame at (30,30), a 151 pt tall teal header, and a 516 pt text measure at x=48. Every character introduction is exactly one PDF page, exported to a 2× PNG for sending and zooming on phones. This is a fixed page image, not a responsive web layout. Playable packets are four pages per guest: private background and three tasks, Hearing 1 / Motive, Hearing 2 / Whereabouts, and Hearing 3 / Evidence. The full-width speech boxes have 528 pt frames and 480 pt text at x=66. Selection labels sit outside their boxes at x=55, with a 502 pt measure. Only the boxed words are spoken; labels remain private. There is no confession in these four pages. Each guest has a separate, single-page FINALE document sealed in its own named envelope until all ballots are collected.

Evidence uses 30 sheets: one guest per sheet, with their A/B cards stacked vertically. Rectangles are 528 × 293 pt at y=106 and y=425, with 496 pt text measures and 16 pt side insets. Discovery and exhibit cards are two per sheet, 528 × 303 pt, with 492 pt text measures. Animal slips are a three-column, five-row grid of 166 × 106 pt rectangles. Name cards are two columns by three rows, 252 × 196 pt. Ballots are two 528 × 305 pt forms per sheet. Landscape room signs use 792 × 612 pt stock and a 720 × 540 pt frame at (36,36).

Print single-sided at Actual size / 100%. The layout and assembly instructions assume this scale and explicitly exclude booklet and two-pages-per-sheet modes.

## Elevation & Depth

The print system is flat. Solid fields, whitespace, typography, and rules establish hierarchy. There are no shadows or gradients.

## Shapes

Frames and cuttable cards have square corners. Rectangle outlines are 0.7 pt; rules are 0.6 pt. Cuttable pieces use a 3 pt on / 3 pt off dash. Sign, invitation, and introduction frames are solid. Dashed borders indicate physical cutting, not an interactive state.

## Components

**Introduction:** identity field, prose description, relationship bullets, acting tips, and optional costume inspiration on one page. Do not add game branches or secret mechanics to this pre-party document.

**Playable packet:** four consecutive pages with private background, shared motive answer, privately selected whereabouts answer, and privately selected evidence reply. Innocent and murderer selection depends on whether the kept animal was called; selection instructions sit outside speech boxes. Every boxed response is safe to read at its hearing. Lines below the motive answer support notes. No improvisation is required; acting remains optional.

**Sealed finale:** one separate named page; only the announced murderer opens and reads its confession after ballots are locked. Optional roles have no selectable confession. The combined finale file is for blind printing, never guest sharing.

**Evidence pair:** the guest name and neutral A/B labels support assembly without exposing branch assignment. Both cards travel together in a labeled envelope; the Hearing 3 page tells the player which to submit privately, and the facilitator counts every guest's card before that hearing. A and B do not consistently identify innocence or guilt.

**Discovery/report card:** textual act labels separate Act I finds from F1–F5 reports released in stages: F1–F2 at death, F3–F4 before Hearing 2, and F5 before Hearing 3. Two note cards use Italic, while records use Regular.

**Host-safe assembly guide:** names and sheet numbers only; no evidence or branch assignments. `OPEN_FREELY`, `PRINT_WITHOUT_READING`, and `SPOILERS_DO_NOT_OPEN` remain functional packaging boundaries.

**Questions & Notes:** one shared sheet per guest contains the same three hearing questions, turn instructions, and ruled spaces for motive, fictional 6:40–6:49 whereabouts, and confirming or contradicting evidence. Questions use 16 pt, headings 20 pt, and instructions 14 pt.

**Attendance and Hearing Roster:** the facilitator tracks all 30 characters by ID and name. Rows are 18 pt apart, with 11 pt square ticks for attendance, motive, whereabouts, and card. Roster labels are supporting 12 pt text. Absent IDs are skipped; fictional printed witness facts carry evidence, not real guest movements.

**Props:** signs support room finding; blanks on ballots and certificates support handwriting. Core player and murderer bowls contain matching 15-animal sets; optional animals stay out of the murderer bowl.

## Do's and Don'ts

- Do preserve the canonical murder facts, branch assignments, evidence contents, and host-blind selection logic when changing layout.
- Do keep introductions single-page and phone-readable, playable packets four-page with separately sealed single-page finales, and evidence pairs cuttable without revealing guilt through their labels.
- Do preserve optional costume language and physical play without QR codes or phone mechanics.
- Do measure text before drawing, preserve the 14 pt narrative floor, and use explicit overflow limits rather than truncating content.
- Don't distribute the font cache or send private packets with pre-party introductions.
- Don't infer that a rendered PDF proves the murder logic correct or every page visually approved.

Build assertions reject unsupported glyphs and canvas text exceeding each block's bottom limit. The build asserts single-page introductions and exports all 30 character PNGs. `scripts/verify.py` renders every PDF page, maps exact visual duplicates to shared review images, checks safe bounds, text below 11.9 pt, replacement glyphs, blank pages, single-page introduction, four-page playable packet, and single-page finale counts, A/B presence, distinct branch cards, and nonempty branch/final statements. Its contact sheets support human visual review. These are implemented checks, not a substitute for inspecting the renders or a claim about the latest run's outcome.
