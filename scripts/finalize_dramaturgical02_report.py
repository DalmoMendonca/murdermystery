"""Package the complete rejected experiment without promoting it."""
from pathlib import Path
import json, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(r'C:/Users/dalmo/Documents/Codex/2026-10-24/what/outputs')
RUN = ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-02-BLIND-SPOILERS'
AUTHOR = ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-02-SPOILERS'
REPORT = OUT/'dramaturgical02-test-report'
CAND = OUT/'dramaturgical-candidate02'
d = json.loads((RUN/'results.json').read_text(encoding='utf-8'))
assert d['stats']['completed'] == 22 and d['stats']['score_values'] == 3872
assert d['stats']['all_journals_and_locks_verified']
assert not json.loads((RUN/'acceptance-review.json').read_text())['fairness_headline_gates_pass']

review = '''# Second dramaturgical candidate rejected — October 26, 2026

The complete second fresh 22-reader cohort returned 20 correct accusations, 20 earned endings, zero early clear culprits, and 20 unique final culprit leaders. Mean naturalness is 6.14/10 (range 6–7); arc variety is 6.95 (range 6–8). Neither the fairness acceptance gates nor the naturalness aspiration above eight passed. This candidate must not replace the verified print edition.

| Version | Correct | Earned | Early clear | Naturalness | Arc variety |
|---|---:|---:|---:|---:|---:|
| Protected print edition | 22/22 | 22/22 | 0 | 6.41 | 7.18 |
| Rejected candidate 01 | 17/22 | 19/22 | 0 | 6.05 | 6.95 |
| Rejected candidate 02 | 20/22 | 20/22 | 0 | 6.14 | 6.95 |

The protected edition has exact-input versioned coverage; each candidate has its own complete fresh cohort. These independent readings are descriptive comparisons, not a matched causal experiment or human solve rates. The higher correct count in candidate 02 does not establish that any one edit caused the change. No favorable individual scores were carried between versions.

## The two failed cases

- **Paige Turner:** the reader accused Elle (confidence 6/10). Elle scored 8 and Paige 6 at the final checkpoint. The reader found the recording contradiction but considered Paige's solitary return and acquisition of poison missing links supplied by the confession. The ending was judged unearned.
- **Elon Mosaic:** the reader accused Elle (confidence 4/10). Elon's impossible camera claim could, for that reader, protect a failed sales demonstration; Elle’s cloth route and financial lie remained the stronger alternative. The confession confirmed an available mechanism but did not resolve the reader's concern about identifying the hand responsible. The ending was judged unearned.

These judgments are preserved as failures. They do not authorize adding a witness, transfer trace, access restriction or new forensic fact. The nonunique paper scrap must remain nonunique.

## What the full cohort still found artificial

The most consistent criticism is the repeated dramatic procedure: grouped question, individual account of access, documentary correction, renewed denial. More individual phrasing and sustained practical concerns did not sufficiently change that experience. Readers repeatedly praised Monet's payroll urgency, Al's need to call home, Reed's insistence on credit, and Brie's concern for staff. Those concerns gave characters lives beyond the puzzle, but did not conceal the common disclosure structure.

The dense mixed-source administrative pages still resemble a compiled case digest. Readers found the photographs legible and useful, especially the seal, wooden model and frame comparison. The criticism concerns the uniform compilation and the concentration of unrelated financial corrections, not unreadable photos. All nine evidence pages remained byte-identical throughout this experiment.

Several readers distinguished a plausible comparative accusation from exclusive physical proof. That limitation also appears in successful cases; a correct vote alone does not erase it. The innocent financial lies and broad access intentionally keep alternatives alive, and weakening them to make a candidate pass would violate priority one.

One concrete finale collision also remains: in Chip's culprit scenario, Elle immediately accepting his help packing after his murder admission feels like an independent ending pasted into the scene. It has been recorded, not silently repaired after the frozen trial.

## Scope and integrity

Candidate 01 revised all 176 passages. Candidate 02 changed 40 hearing fields, developed six sustained actions, removed the unintended exclusive-roll request without altering Elle's route or lie, and restored five guilty Method replies exactly to the protected baseline. Pre-vote text is 7,833 words against 8,040 baseline. Endings remain as tested in candidate 01.

All 22 readers had fresh, isolated contexts and only sequential player-facing releases. Interrupted readers t007–t009 resumed with their same identities and immutable scores. Each accusation preceded the finale. All 3,872 scores, 176 stage locks, frozen source hashes, accusation locks and completion hashes passed verification. No reader received a selected culprit, target rating, prior feedback or author draft.

The 264-page candidate packet book has 416 verified branches across both editions; the 22 pages changed from candidate 01 were rendered and reviewed. Final checks confirm canonical source still matches 2cb64b9, and protected host, hunt, evidence, tents and draw-card PDFs match the candidate's unchanged copies. The six Act III pages and three approved pages are preserved. No promotion, publication or deployment occurred.

## Recommended next decision

Keep the protected print edition available. Further sentence polishing alone has not delivered the requested improvement in these two complete experiments. The repeated structure is the next credible thing to test, not another promise of better wording.

The approved plan locks turn allocation/order and all evidence pages. Expanding to actual short printed exchanges therefore needs the user's approval. A concrete, unimplemented Artie/Monet/Sue example and limits are in `OPTIONAL_SCENE_STRUCTURE_PROTOTYPE.md` alongside this report. It proposes a small pilot before any full-cast work: split selected speeches into cued responses within their existing act, preserve every assertion/lie/certainty and branch, and audit that no one acquires new knowledge. No improvised factual replies, new witnesses or forensic clues. If separately approved, distinguish existing source extracts on only the three replacement artifact pages; keep six Act III pages and the three approved sheets exact. A new frozen full cohort and user approval would still be required before promotion.

This report delivers the completed candidate experiment, not a successful naturalness rewrite. Both rejected versions and all adverse results remain available. The aspiration above eight has not been met.
'''
(REPORT/'revision-review.md').write_text(review, encoding='utf-8')
(REPORT/'READ_RESULTS.md').write_text(review, encoding='utf-8')
(RUN/'RESULTS.md').write_text(review, encoding='utf-8')
shutil.copy2(RUN/'acceptance-review.json', REPORT/'acceptance-review.json')
shutil.copy2(CAND/'ACT_III_Evidence.pdf', REPORT/'tested-ACT_III_Evidence.pdf')
shutil.copy2(AUTHOR/'final-protection-check.json', REPORT/'final-protection-check.json')
shutil.copy2(OUT/'dramaturgical-revision-plan/OPTIONAL_SCENE_STRUCTURE_PROTOTYPE.md', REPORT/'OPTIONAL_SCENE_STRUCTURE_PROTOTYPE.md')
(CAND/'CANDIDATE_STATUS.txt').write_text('REJECTED — DO NOT PRINT OR REPLACE THE VERIFIED EDITION.\nFresh 22-reader cohort: 20 correct, 20 earned, naturalness 6.14/10.\nFailed fairness acceptance gates; no promotion or deployment.\nThe protected final-party-print-kit remains the printing release.\nFull results: ../dramaturgical02-test-report/results.html\n', encoding='utf-8')
html = (REPORT/'results.html').read_text(encoding='utf-8')
html = html.replace('Dramaturgical revision: 22 blind scenarios', 'Rejected candidate 02: full blind results')
html = html.replace('<div id="cards"', '<p><strong>REJECTED — do not print this candidate. Fairness gates failed; naturalness aspiration not met. The verified print edition remains unchanged.</strong></p><div id="cards"', 1)
(REPORT/'results.html').write_text(html, encoding='utf-8')
with (AUTHOR/'CURRENT_STATE.md').open('a', encoding='utf-8') as f:
    f.write('\nFINAL: all 22 complete, all 3,872 scores and locks verified. REJECTED: 20 correct/earned/unique, zero early clear, naturalness 6.14, arc variety 6.95. Paige and Elon readers accused Elle and judged their endings unearned. Full report exported; canonical source and protected PDFs unchanged. No more frozen-input edits or rerolls. Further turn/evidence presentation changes require expanded user approval; concrete prototype exported.\n')
with (ROOT/'PLAN.md').open('a', encoding='utf-8') as f:
    f.write('\n## Dramaturgical experiment complete — approval boundary\n\nBoth full fresh cohorts retained. Candidate 01 rejected (17 correct, 19 earned, naturalness 6.05). Candidate 02 rejected (20 correct, 20 earned, zero early clear, naturalness 6.14, arc variety 6.95). All 3,872 candidate02 scores verified and exported. The 2cb64b9 print edition remains canonical; no promotion. Deliver report and unimplemented scene-structure proposal for user decision before expanding fixed turn/evidence scope.\n')
print(json.dumps({'report': str(REPORT), 'candidate_status': 'rejected', 'protected_print_edition_unchanged': True}))
