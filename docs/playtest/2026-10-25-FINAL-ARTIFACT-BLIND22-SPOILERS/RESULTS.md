# Final blind playtest: six-page Act III candidate

Completed **22/22** scenarios: one fresh blind AI player-reader for each RSVPd role as the selected murderer. **17/22 correct accusations; 17/22 endings judged earned.** Five incorrect accusations are listed below. No reader declared a clear culprit before the final testimony.

Mean ratings (0-10): clarity **7.36**, voice distinction **7.86**, drama **7.86**, fair play **6.23**, naturalness **6.18**. Confidence ranged from 5 to 9. This is not a clean pass and not a human solve-rate estimate.

## Open first

- **results.html**: interactive report. Choose the assigned murderer to see all 22 guests at all eight checkpoints, the locked accusation, each checkpoint's reasoning, original qualitative feedback and bounded suggestions.
- **all-suspicion-scores.csv**: all **3,872 suspicion values** (22 scenarios x 22 guests x 8 checkpoints), suitable for Excel filtering.
- **scenario-summary.csv**: one row per scenario, including the selected murderer's trajectory, accusation, confidence, ratings and ambiguity measures.
- **surgical-recommendations.md**: author triage of the reader feedback, with small edits separated from structural changes.
- **all-player-feedback.md**: all 22 full reviews and post-finale assessments.
- **tested-ACT_III_Evidence.pdf**: exact six-page evidence snapshot used by the readers.

## Incorrect accusations

| Assigned murderer | Reader accused | Confidence |
|---|---|---|
| Claire O’Scuro | Chip Patina | 5/10 |
| Dada DiCapo | Elle Loominate | 5/10 |
| Barb Dwyer | Elle Loominate | 5/10 |
| Paige Turner | Chip Patina | 6/10 |
| Robin Banks | Elle Loominate | 6/10 |

All five missed cases concentrated on two innocent alternatives: Elle or Chip. Readers generally understood the bottle-to-glass route, but several found that access plus a contradicted account selected a preferred suspect without uniquely identifying the actor. This was a concern even in some correct cases. The false claims and physical access should not be confused with a new independent forensic match.

## Scores of the assigned murderer in every scenario

These rows track only the assigned murderer in each separate scenario. The interactive report and full CSV contain EVERY guest's scores in EVERY scenario.

| Assigned murderer | Intro | Hunt | E1 | Act I | E2 | Act II | E3 | Act III | Accused |
|---|---|---|---|---|---|---|---|---|---|
| Artie Ficial | 1 | 4 | 5 | 5 | 5 | 5 | 4 | 8 | Artie Ficial |
| Claire O’Scuro | 1 | 2 | 2 | 4 | 4 | 6 | 6 | 7 | Chip Patina |
| Monet Bags | 1 | 2 | 2 | 5 | 5 | 6 | 7 | 9 | Monet Bags |
| Chip Patina | 1 | 3 | 3 | 5 | 6 | 7 | 7 | 8 | Chip Patina |
| Dada DiCapo | 1 | 3 | 3 | 4 | 3 | 5 | 4 | 6 | Elle Loominate |
| Vincent Van Faux | 1 | 3 | 3 | 4 | 4 | 5 | 5 | 8 | Vincent Van Faux |
| Sue Venir | 1 | 2 | 2 | 4 | 4 | 6 | 5 | 8 | Sue Venir |
| Dr. Art E. Fact | 1 | 2 | 2 | 4 | 4 | 5 | 4 | 8 | Dr. Art E. Fact |
| Barb Dwyer | 1 | 4 | 4 | 5 | 5 | 6 | 6 | 7 | Elle Loominate |
| Paige Turner | 1 | 1 | 1 | 3 | 3 | 5 | 4 | 7 | Chip Patina |
| Frank Lloyd Wrong | 1 | 3 | 2 | 4 | 4 | 5 | 5 | 9 | Frank Lloyd Wrong |
| Mona Lott | 0 | 2 | 2 | 3 | 3 | 5 | 4 | 8 | Mona Lott |
| Elon Mosaic | 1 | 2 | 2 | 4 | 4 | 6 | 7 | 8 | Elon Mosaic |
| Elle Loominate | 1 | 2 | 2 | 4 | 4 | 6 | 6 | 9 | Elle Loominate |
| Reed DeLabel | 1 | 1 | 1 | 4 | 4 | 5 | 6 | 8 | Reed DeLabel |
| Al Baster | 1 | 1 | 1 | 4 | 4 | 6 | 5 | 8 | Al Baster |
| Brie DeVivre | 1 | 3 | 4 | 4 | 5 | 6 | 5 | 8 | Brie DeVivre |
| Cary Crates | 1 | 4 | 4 | 5 | 6 | 6 | 4 | 8 | Cary Crates |
| Anne E. Dote | 1 | 3 | 3 | 4 | 3 | 6 | 6 | 9 | Anne E. Dote |
| Robin Banks | 1 | 2 | 2 | 3 | 2 | 5 | 5 | 7 | Elle Loominate |
| Penny Pincher | 1 | 1 | 1 | 4 | 4 | 6 | 6 | 8 | Penny Pincher |
| Justin Tyme | 2 | 2 | 2 | 4 | 3 | 5 | 5 | 8 | Justin Tyme |

E1/E2/E3 are the staged documentary releases; Act I/II/III are the subsequent spoken testimony. Scores are integers from 0 (no current suspicion) to 10 (overwhelming suspicion). They are not probabilities.

## What the feedback supports

The image comparisons and service chronology were useful. The weaker presentation elements were the executor recording's neatly comprehensive exposition, file tables that collect unrelated secrets, and the repeated rhythm of documentary denial followed by an emotional aside. A style edit can address those concerns, but cannot be claimed to repair all five missed accusations.

The lowest-risk options are a narrower, routine purpose for Grant's recording; source-specific labels for physical findings; reading that short recording aloud once; and keeping the service chronology available at voting. Preserve the innocent cover lies and all murder-relevant assertions. Adding a unique custody witness or a new timing event would need another route-by-route test.

## Integrity and limits

All 176 checkpoint score files, all 22 accusations and post-finale records were checked against their locks. Eight releases were sequentially gated. All scenarios used the same frozen shared evidence and exactly one selected murderer branch, with the other 21 innocent branches. All six Act III page images were required viewing. The unchanged RSVP roster and source hashes passed mechanical checks.

Three partial readers hit the usage limit. The SAME readers resumed at their saved checkpoints after capacity became available; saved judgments remained byte-identical. No rerolls or replacement trials were used.

Each scenario has one AI reader in a fresh context, from the same model family. They observed all public introductions, all 16 hunt clues, shared evidence and scripted testimony, rather than playing an assigned private role in an interacting group. All 16 hunt clues were supplied; search/discovery failures were not modeled. Human improvisation, missed discoveries, acting, fatigue and group voting are not simulated. There is no matched control trial of the previous edition, so these results do not establish that the editorial redesign caused a change from earlier test results.

No game content changed during testing. No proposed surgical revision has been applied or tested. The production site, existing preview and sent assets were not changed by this suite.
