# Interim findings — 37 of 110 tests / SPOILERS

This is an incomplete audit, not a completed 110-reader result. Every one of the 22 RSVP murderers has one completed reader; 15 have a second. The other 73 predetermined trials have not run. No cases were rerolled, and no game copy was changed.

The published complete-kit ZIP was hash-verified before freezing the inputs. The tested adult revision is `act3-five-speech-refinement-2026-10-10`, deployed as `6acaae2d208c9cee1b30f908`.

## Findings so far

- All 37 locked accusations identify the selected murderer. All 37 finale reviews find the confession earned; none reports a decisive new fact that was required to solve it.
- No reader explicitly declares a clear culprit before Act III. This is a declaration measure, not proof that no earlier numeric lead exists.
- Three records have conflicting final numbers and conclusions: t001 and t030 (Al Baster), and t018 (Claire O’Scuro). Their reasoning, clear-culprit declaration, and accusation name the actual murderer, while their highest numeric score belongs to someone else. Original records are preserved, not corrected by inference.
- In a sensitivity analysis excluding those three conflicting numeric records, 30/34 put the murderer at 5–7 at E3; all 34 score the murderer at least 9 and uniquely highest at the end.
- Only 3/34 have at least eight suspects strictly above 5 after Act II. Only 1/34 retains at least three innocents at 5–7 after Act III. The suspect-field targets are therefore not being replicated reliably.
- Average review ratings: fair play 8.1, clarity 7.8, voice distinction 7.9, arc variety 7.2, naturalness 6.8, drama 7.9 (all out of 10).
- 35/37 readers flag naturalness issues, 23/37 pacing, and 9/37 evidence issues. These are explicit review categories, not an automated guess about sentiment. No reviewer marks an issue major.

## Priorities for a later rewrite

1. Preserve the existing culprit contradiction and evidence release order. Correct accusations and earned confessions are the strongest results here; a wholesale new architecture is not justified by this sample.
2. Broaden credible Act II suspicion through existing personal conflicts and suspicious actions. Do not add more incidental trips to the historical bottle to achieve a score target.
3. Audit which innocent Act III replies fully interpret the exhibits or settle their scandal. Move optional explanation and tidy resolution into Coming Clean, while preserving the factual clues that let attentive players make their own deductions.
4. Reduce repeated technical material descriptions and dossier recaps in dialogue. Keep the facts visible in the evidence; let characters respond as people under pressure.
5. Treat dense access to the historical loan and repeated paperwork explanations as story problems, not reasons to add more explanatory instructions.
6. Diagnose remaining low-E3 or early-high branches only after their five independent readers finish. One or two readings per culprit cannot establish a reliable character-specific weakness.

## Limits and continuation

These are fresh-context AI text readers, not human solve-rate estimates. All 16 hunt exhibits are supplied to every reader; physical discovery, live pacing, visual interpretation, and social interruptions are not simulated. The readers use identical instructions; no different human personalities are assigned.

An earlier usage cutoff interrupted t010–t012; the same agents resumed with prior scores locked. At this checkpoint the live account usage tool reports 95% of the five-hour allowance and 86% of the weekly allowance used. Further new reader launches are held to preserve a usable handoff rather than exhausting the account. The current five-hour window resets at 12:31 AM Central on October 11. Completing the remaining 73 requires additional available quota; no account reset or purchase was performed, and no background continuation is scheduled.

Resume with fresh fork-none agents for t038 through t110, one trial per agent, using READER_INSTRUCTIONS.md. Do not run the freeze command again. Run `scripts/report_exhaustive_balance.py` to audit hashes and rebuild the dashboard, then `scripts/chart_exhaustive_balance.py` for the overview image. Preserve all original results and any failed attempts. Score/conclusion conflicts must remain visible.
