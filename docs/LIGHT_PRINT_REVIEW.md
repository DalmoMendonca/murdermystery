# Light print release review — 2026-10-05

## Scope and result

All 87 printable PDFs were regenerated. Every one of the 961 page instances was rasterized; exact raster duplicates map to 529 distinct pages across 133 contact sheets. Structural preflight reported no issues. That preflight was followed by human-like independent visual review, rather than being treated as visual approval itself.

Three fresh Impeccable reviewers inspected complementary, complete partitions:

| Reviewer | Contact sheets | Distinct pages | Disposition |
| --- | --- | --- | --- |
| print_finish_a | 00–44 | 180 | SHIP |
| print_finish_b | 45–88 | 176 | SHIP |
| print_finish_c | 89–132 | 173 | SHIP |

Their five-section returns covered capture validity, direction fidelity, strengths, severity-ranked findings and disposition. There were no material findings. Minor refinements were a lone final word in two introductions and cramped guide emblem spacing; the renderer now keeps the final word pair together whenever an introduction would end with one word, and reduces only the guide emblem. The invitation artwork also has a continuous dark upper mat rather than gray letterbox edges. Final recaptures covered all 74 changed distinct pages, using updated contact sheets and full-resolution details. Reviewers scored every refinement resolved and found no new material issue; SHIP was retained.

## Preserved behavior

The complete PDF text and page-count comparison against the preceding committed kit covers all 961 pages. Whitespace-normalized words are identical. Editable source files, animal selection, branches, round sequence, questions, clues, ballots, Coming Clean and host-blind architecture are unchanged. Minimum checked text remains 12 pt; reading copy remains at its existing larger sizes. All 31 approved dark phone JPEGs are byte-identical to the preceding release.

Letter PDFs are light print variants. Dark phone images stay dark; the print invitation retains a dark photographic upper section. Portrait ink coverage remains substantial on art covers and posters, while reading surfaces use paper white, black, burgundy and small gold details.

## Evidence and limits

Reproducible checks: `python scripts/build.py`, `python scripts/verify.py`, `python scripts/check_content.py`. Render manifest: `build/review/report.json`. Release comparison: `build/print-content-preservation.json`.

These reviews establish screen-rendered layout quality. No physical printer, folded paper or party pacing was tested in this visual pass. No new blind playtest was run; the previously documented difficulty concern remains separate from this release.
