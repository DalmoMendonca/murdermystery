---
name: The Last Acquisition — After Hours Public Print
description: Nocturnal museum gala invitation and companion character posters on US Letter.
colors:
  night: "#061415"
  cream: "#fff1d5"
  gold: "#edc189"
  wine: "#620e21"
typography:
  invitation-display: {fontFamily: "Libron", fontSize: "51pt", fontWeight: 700, lineHeight: 0.98}
  invitation-subtitle: {fontFamily: "Libron", fontSize: "23pt", fontWeight: 400, lineHeight: 1.2}
  invitation-tagline: {fontFamily: "Libron", fontSize: "25pt", fontWeight: 400, lineHeight: 1.2}
  invitation-date: {fontFamily: "Libron", fontSize: "27pt", fontWeight: 700, lineHeight: 1.2}
  invitation-time: {fontFamily: "Libron", fontSize: "21pt", fontWeight: 400, lineHeight: 1.2}
  invitation-address: {fontFamily: "Libron", fontSize: "19pt", fontWeight: 700, lineHeight: 1.2}
  invitation-body: {fontFamily: "Libron", fontSize: "16pt", fontWeight: 400, lineHeight: 1.2}
  museum-label: {fontFamily: "Libron", fontSize: "18pt", fontWeight: 400, lineHeight: 1.2}
  poster-name: {fontFamily: "Libron", fontSize: "28–43pt, largest fitting 528pt", fontWeight: 700, lineHeight: 1.2}
  poster-role: {fontFamily: "Libron", fontSize: "17pt", fontWeight: 400, lineHeight: 1.2}
  poster-body: {fontFamily: "Libron", fontSize: "17pt, 16.5pt or 16pt, measured", fontWeight: 400, lineHeight: 1.2}
  poster-label: {fontFamily: "Libron", fontSize: "15pt", fontWeight: 700, lineHeight: 1.2}
  poster-footer: {fontFamily: "Libron", fontSize: "12pt", fontWeight: 400, lineHeight: 1.2}
spacing:
  page-margin: "42pt"
  text-measure: "528pt"
  portrait-description-gap: "24pt"
  relationship-gap: "5pt"
  acting-top-gap: "16pt"
  costume-top-gap: "19pt"
components:
  public-page: {backgroundColor: "{colors.night}", textColor: "{colors.cream}", width: "612pt", height: "792pt"}
  invitation-date-band: {backgroundColor: "{colors.wine}", textColor: "{colors.cream}", width: "612pt", height: "102pt"}
  poster-costume-panel: {backgroundColor: "{colors.wine}", textColor: "{colors.cream}", width: "556pt"}
  portrait-frame: {width: "aspect 2:3, fit within measured portrait slot"}
---

# Design System: The Last Acquisition — After Hours Public Print

## Overview

**Creative North Star: "After Hours"**

The user approved the live After Hours world and requested its extension to the public Letter invitation and character posters. Near-black green, warm cream, antique gold, velvet burgundy and embedded Libron make the printed invitation feel like commissioned gala artwork. The invitation reuses the landing page's commissioned museum lion scene; each character keeps the existing Van Gogh portrait and edited public copy.

This document extracts `scripts/after_hours_print.py` and its `scripts/build.py` integration. Its scope is the invitation front and thirty unnumbered character poster fronts. The invitation's second-page arrival guide retains its light operational layout. Private player packets, packet covers, host materials, evidence and tent cards retain the separate light print system documented in `PRINT_DESIGN.md`; the public dark world does not replace those tokens. The live site remains the visual authority identified in `AFTER_HOURS_PUBLIC_BRIEF.md`.

**Key Characteristics:**

- Full-page night ground with cream reading text and gold hierarchy.
- Commissioned lion scene, large left-hand invitation title and burgundy date band.
- Van Gogh character paintings in ornate gilded art frames, restored at the user's request.
- Measured description columns, full-width relationships and Acting Tips.
- Burgundy Costume Suggestions panel and a quiet gold footer.

## Colors

Night is a deep green-black ground; Cream keeps dense character copy readable against it. Antique Gold connects the museum, section labels, fine rules and portrait mounts. Velvet Wine gives the invitation date and costume advice a distinct visual place.

Gold labels carry words as well as color. Portrait colors remain those of the supplied paintings. The public palette is local to this scope; light private paper, teal headings, yellow relationship highlights and red stop panels keep their existing meanings.

## Typography

Libron is embedded through the existing `Book`, `BookBold` and `BookItalic` PDF font registrations. Public text uses 1.2 leading except the invitation display title, which uses 0.98. The title's deliberate two lines read “The Last / Acquisition” at 51 pt bold. The subtitle is 23 pt italic; the museum is 18 pt regular; the tagline is 25 pt italic. Date, time and address are 27 pt bold, 21 pt regular and 19 pt bold. Invitation narrative is 16 pt; the preparation reminder is gold italic at the same size.

Poster names choose the largest integer size from 43 down to 28 pt that fits 528 pt. Roles are 17 pt gold italic and may wrap. Narrative chooses 17, 16.5 or 16 pt after measuring the entire page. Description, relationships, Acting Tips and costume text share that selected size. Section labels are 15 pt bold gold, uppercase. Footer metadata is 12 pt gold italic.

**The Public Reading Floor Rule.** Keep poster narrative at least 16 pt. Resolve measured space through the implemented layout choices; do not replace body copy with footer-sized text.

## Layout

US Letter is 612 × 792 pt. Coordinates below run down from the top. The normal reading column begins at x=42 and spans 528 pt. These are fixed print compositions with no responsive breakpoints. PDFs are printed single-sided at 100%.

The invitation's artwork slot is (0,0,612,383), using the exact `site/art/museum-after-hours.webp` scene. A night rectangle covers the left 306 × 383 pt at 0.62 alpha. The title begins at (38,72), width 375 pt. Subtitle begins at (42,238), width 320 pt; museum label at (42,321), width 400 pt. A gold rule sits at y=388. The tagline starts at y=407. The full-width wine date band occupies (0,453,612,102); date and time begin at y=469 and 505. Address begins y=576, collection narrative y=619, attire y=678 and preparation reminder y=723.

Poster names start at (42,36), roles at (42,94). The portrait/description region begins at `max(141, role_end + 18)`, keeping wrapped roles clear of the artwork. Initial portrait width is 196 pt; region height is the larger of width × 1.16 and the measured description height. After choosing body size, the layout attempts widths 250 then 230 pt, taking the first whose full composition fits at or before y=736. Otherwise it retains 196 pt. The description begins x=portrait_width + 66, y=hero_y + 3, and uses width 528 − portrait_width − 24.

Relationships follow beneath the taller portrait/description region across all 528 pt. Their starting gap is 18 pt plus up to 24 pt of extra air derived from the available space. Each bullet has 5 pt after its text. A gold divider follows at relationship_end + 7; Acting Tips begins at relationship_end + 16, with 5 pt between its label and body.

The costume panel begins 19 pt after Acting Tips at x=28, width 556 pt. Its height is 18 + 5 + measured costume height at a 500 pt text measure + 22 pt. The label begins 9 pt inside the panel, at x=42; costume body uses x=42 and 500 pt. Footer rule is fixed at y=747, with metadata at (42,756), width 528 pt. Text drawing asserts its bottom is at or before y=774.

Each character poster is a single-page PDF in `OPEN_FREELY/PreParty_Individual`; the build merges those pages into `OPEN_FREELY/02_PreParty_Character_Sheets_ALL.pdf`. Individual poster JPEGs are 1224 × 1584 pixels at 144 dpi, quality 90, subsampling 0, with build provenance in their comments. The invitation front is page one of `OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf`.

## Elevation & Depth

The commissioned scene and paintings provide visual depth. Print layout uses flat color bands, fine gilt rules and a translucent night overlay to protect title legibility. It has no drop shadows or motion. The public portraits reuse the same native-alpha ornate frame and aperture composition as the private packet covers.

## Shapes

Page bands and costume panels are square rectangles. Public rules are 0.55 pt. Portrait frames retain their organic gilded ornament and native transparency; their outer proportions remain 2:3. No rounded corners are introduced.

## Components

**Invitation front.** The scene sets the occasion; the left overlay supports title and subtitle, followed by museum, tagline, date/time, address, collection introduction, attire and preparation. Date content is an explicit text band rather than image lettering.

**Ornate portrait frame.** Reuse `printable_v2.framed()` with `assets/ornaments/gilt_frame.png`. The frame is centered within the measured slot at width min(slot_width, slot_height × 2/3), height frame_width × 1.5. The aperture begins at 18% of frame width and 14% of frame height, spans 64% width and 72% height, and clips the centered portrait beneath the native-alpha ornament. Keep the original portrait masters intact.

**Character story.** Name and role lead the page. Description sits beside the painting; relationships and Acting Tips use the full reading measure beneath both columns. Existing active relationships and public character copy remain authoritative. Each poster is unnumbered and carries no private background, guilt branch or game secret.

**Costume panel.** The wine rectangle contains a gold uppercase label and cream narrative at the selected body size. Its height is measured from the actual copy, keeping costume guidance readable instead of forcing a uniform empty box.

**Public export.** Opaque artwork embedded through `Sheet.image()` is reduced within 900 × 900 pixels and encoded as quality-88 JPEG with subsampling 1; full-resolution source artwork remains separate. Poster JPEGs are rasterizations of the final PDFs, not separately typeset versions.

## Do's and Don'ts

- Do carry the approved After Hours palette through public invitation and poster fronts.
- Do reuse the exact commissioned lion scene and existing character paintings.
- Do retain full painting compositions, full-width relationships and Acting Tips.
- Do measure every poster and preserve the 16 pt narrative floor.
- Do keep the dark public scope distinct from light private and operational materials.
- Don't replace the ornate art frames with thin gold borders; the user explicitly requested their restoration.
- Don't expose private game information on public character posters.
- Don't overwrite the older print document or private sidecar tokens when extending this scope.
- Don't claim that digital review proves physical printer output.

Review verdicts and artifact coverage belong in the current finish-review records. This document records implementation facts; it does not freeze release hashes or independently certify a shipping build.
