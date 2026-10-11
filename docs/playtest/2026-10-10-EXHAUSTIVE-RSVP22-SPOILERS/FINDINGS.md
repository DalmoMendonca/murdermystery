# Interim findings — 88 of 110 tests / SPOILERS

This audit is incomplete. Each of 22 RSVP characters has five predetermined trials. Completed per-character counts are in the dashboard and case-summary.csv. No cases were rerolled and no game copy was changed.

Frozen published revision: `act3-five-speech-refinement-2026-10-10`. Verified deploy: `6acaae2d208c9cee1b30f908`.

## Results

- Correct locked accusations: 88/88. Earned finale reviews: 88/88. Reviews reporting decisive new finale facts: 0.
- Explicit clear-culprit declarations before Act III: 0/88. This declaration measure does not rule out earlier numeric leads.
- Score/conclusion conflicts: 3 (t001, t018, t030). Raw numbers, reasoning, and accusations remain unchanged. Do not repair them by inference.
- Sensitivity subset excluding entire flagged trials: 85 readers. E3 murderer score 5–7: 73/85; final murderer at least 9: 85/85; uniquely highest: 85/85.
- In that subset, at least eight suspects strictly above 5 after Act II: 7/85. At least three innocent alternatives at 5–7 after Act III: 1/85.

## Reader feedback

- Fair play: 8.1/10.
- Clarity: 7.9/10.
- Voice distinction: 7.9/10.
- Arc variety: 7.2/10.
- Naturalness: 6.8/10.
- Drama: 8.0/10.

- Naturalness: explicitly raised in 78/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Pacing: explicitly raised in 60/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Evidence: explicitly raised in 21/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Voice: explicitly raised in 6/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Clarity: explicitly raised in 4/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Motive: explicitly raised in 2/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.
- Fairness: explicitly raised in 1/88 reviews; 0 marked major. Full examples and trial references are in the dashboard.

## Priorities for a later rewrite

1. Preserve the existing culprit contradiction and release order where they produce correct accusations and earned confessions. Do not rebuild successful logic merely to change scores.
2. Broaden Act II suspicion through existing personal conflicts and suspicious actions. Do not add more incidental trips to the historical bottle.
3. Identify innocent Act III replies that interpret exhibits or settle scandals. Preserve deduction facts, but move optional explanation and tidy resolution to Coming Clean.
4. Reduce repeated technical descriptions, dossier recaps, and identical emotional rhythms. Let characters react as distinct people under pressure.
5. Treat dense access to the historical loan and convenient paperwork resolutions as story problems; extra explanatory instructions will not solve them.
6. Rank character-specific rewrites only after all five readers per culprit finish. Use the score ranges and flagged-trial sensitivity data rather than a single mean.

## Limits and continuation

These are attentive fresh-context AI text readers, not human solve-rate estimates. Every reader receives all 16 hunt exhibits. Physical discovery, party interruptions, visual interpretation, and imperfect human recall are not simulated. Identical instructions are used; personalities are not assigned.

Inputs, sequential score locks, accusation locks, and completion hashes are audited by the report script. Interrupted original readers resume without replacing earlier scores. Pending trials are not successes. Technical deviations and score/conclusion conflicts remain visible.

Remaining: 22. Saved running trials: t088, t090. The user-authorized continuation is `complete-the-110-reader-murder-mystery-audit`; scheduled: True. No reset credit or purchase has been used by this audit.

Resume original interrupted readers, then fresh fork-none agents for unstarted trials through t110, one agent per trial, using READER_INSTRUCTIONS.md. Never freeze again or expose other trials to a reader. Rebuild with checkpoint_exhaustive_balance.py and chart_exhaustive_balance.py. Disable the continuation after all 110 tests are verified complete.
