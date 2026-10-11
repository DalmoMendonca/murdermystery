"""Produce case-specific next-pass priorities after all original readers finish."""
import json
from statistics import mean
from exhaustive_balance import RUN

data = json.loads((RUN / 'aggregate.json').read_text(encoding='utf-8'))
assert data['completed'] == 110 and data['invalid'] == 0
assert len(data['cases']) == 22 and all(c['n'] == 5 for c in data['cases'])
trials = {t['trial']: t for t in data['trials']}
clean = [t for t in trials.values() if not t['audit_flags']]
flagged = [t for t in trials.values() if t['audit_flags']]
lines = ['# Final rewrite priorities / SPOILERS', '',
         'The audit is complete: five original readers for each of 22 murderers. These are recommendations, not changes to the published game. Preserve the baseline and already-sent invitations.', '',
         '## What the tests establish', '',
         f"All {sum(t['metrics']['correct'] for t in trials.values())}/110 locked accusations identify the selected murderer. That supports solvability for attentive AI readers; it does not estimate the success rate of distracted human guests.", '',
         f"{len(flagged)} original score/conclusion conflicts remain visible. The raw heatmap retains them. The sensitivity heatmap excludes whole flagged trials and uses {len(clean)} numeric samples. Al and Claire must not be judged from their distorted raw final means.", '',
         '## Case-by-case timing review', '',
         'The E3 column measures suspicion after the final evidence but before Act III speeches. These are whole-trial sensitivity values, not repaired scores. Counts below 5 reflect flagged originals, not missing tests. A low score suggests late recognition; an 8 suggests premature concentration. Neither alone proves a story defect.', '',
         '| Murderer scenario | Usable / completed | E3 mean (range) | E3 5–7 | Final mean | Suggested scope |',
         '| --- | ---: | ---: | ---: | ---: | --- |']
for case in data['cases']:
    rows = [trials[t] for t in case['trials'] if not trials[t]['audit_flags']]
    scores = [t['metrics']['e3_score'] for t in rows]
    low = sum(s < 5 for s in scores)
    high = sum(s >= 8 for s in scores)
    action = ('Earlier existing pressure/access needs attention' if low >= 2 else
              'Check that E3 does not concentrate suspicion too soon' if high >= 2 else
              'Keep culprit timing; focus on innocent alternatives and voice')
    lines.append(f"| {case['name']} | {len(rows)}/5 | {mean(scores):.1f} ({min(scores)}–{max(scores)}) | {sum(5 <= s <= 7 for s in scores)}/{len(rows)} | {mean(t['metrics']['final_score'] for t in rows):.1f} | {action} |")
lines += ['', '## A bounded next pass', '',
          '1. **Lock the proof before changing prose.** For each of the 22 branches, record the exact claim, the earlier exhibit that contradicts it, how the character could know that fact, and the source-to-drink opportunity chain. Preserve those facts and their reveal order. A lie about an exhibit is evidence of concealment; it should connect to the murder through access and motive rather than function as an automatic guilty label.', '',
          '2. **Work first on the late-recognition cases in the table.** Strengthen pressure already in their story or make existing access legible before Act III. Do not add a new bottle errand, matching cloth contact, synchronized alibi, or late physical clue. For Artie, examine whether refusing the donation has prematurely neutralized the threat to his job. For Elle, clarify when the pattern-rights amendment became effective and when she knew it. An unresolved grievance is more natural than an invented second encounter.', '',
          '3. **Keep several innocent conflicts alive.** Identify the Act III innocent answers that explain exhibits or completely settle personal scandals. Preserve the factual distinction needed to eliminate their murder branch, but move optional settlement and interpretation into Coming Clean. Leave a few credible disputes, losses, or resentments unresolved. These should sustain human uncertainty without making innocent facts false or the selected murderer arbitrary.', '',
          '4. **Reduce E3 density without deleting essential proof.** Its production, press, board, and job-account bundle contains many branch-specific refutations. Map dependencies first; then remove repeated explanatory gloss and peripheral settlements. Make references to off-roster workers intelligible. A corrected account should not double as a neatly resolved life story.', '',
          '5. **Rewrite delivery, not the deduction.** Keep the indispensable action/detail while varying length, rhythm, defensiveness, grief, interruption, and whom the speaker addresses. Avoid everyone delivering a polished admission followed by an emotionally tidy explanation. Al’s exact material wording is a particular candidate for a more natural spoken claim while preserving the material contradiction.', '',
          '6. **Repair knowledge and access gaps where readers named them.** Check Frank’s receipt of the omitted-glass-front revision; Monet’s exposure to the purchase warning; Barb’s connection between camera concealment and access. Use an existing record or relationship instead of another elaborate clue. These are reader concerns to verify against the source, not established new facts.', '',
          '7. **Test the bounded change, then publish only if it improves.** Repeat the affected culprit cases and a small fixed regression set against this frozen baseline. Compare E3 readiness, final culprit recognition, Act II breadth, final innocent alternatives, and naturalness. Do not launch another 110-test cycle merely to chase a color distribution. A small human rehearsal is needed for hunt discovery, pacing, and distracted recall.', '',
          '## Traceable reader observations', '',
          'Representative original observations below retain their trial IDs. The dashboard contains every review and the complete scores. Reader proposals are hypotheses; verify that each preserves the proof dependencies before implementing it.', '']
for category in ['motive', 'fairness', 'evidence', 'naturalness', 'pacing', 'voice', 'clarity']:
    group = next((g for g in data['issue_summary'] if g['category'] == category), None)
    if not group:
        continue
    lines += [f"### {category.capitalize()} — {len(group['trials'])}/110 readers explicitly raised it", '']
    for ex in group['examples'][:3]:
        lines += [f"- **{ex['trial']} ({ex['murderer']}; {ex['severity']}):** {ex['detail']} Suggested direction: {ex['suggested_fix']}"]
    lines.append('')
lines += ['## Evidence and limits', '',
          '110 accusation locks and 110 post-finale reviews are retained. There are 880 sequential score releases and 19,360 individual suspicion values. No rerolls, game edits, reset credits, or purchased credits were used. The score/conclusion conflicts are measurement failures and remain in the raw record.', '',
          'The readers saw all sixteen hunt exhibits as text. They did not simulate envelope discovery, conversational interruptions, physical prop interpretation, printing, or human memory. All had the same instructions; they were not assigned different personalities. Agreement among these readers is not independent evidence that a real dinner party will be too easy or guaranteed to work.', '']
(RUN / 'REWRITE_PRIORITIES.md').write_text('\n'.join(lines), encoding='utf-8')
conflicts = ['## Original score/conclusion conflicts', '',
             '| Trial | Accused and declared culprit | That character’s final score | Highest numeric score |',
             '| --- | --- | ---: | --- |']
for trial in flagged:
    scores = trial['stages'][-1]['scores']
    top = max(scores.values())
    leaders = ', '.join(f'{name}: {score}' for name, score in scores.items() if score == top)
    conflicts.append(f"| {trial['trial']} | {trial['accusation']['accused']} | {scores[trial['accusation']['accused']]} | {leaders} |")
conflicts += ['', 'All three accusations remain counted as correct. Their numerical scores are retained in the raw chart but excluded wholesale from the sensitivity chart. This leaves Al with 3 usable numeric trials, Claire with 4, and every other character with 5.', '']
text = (RUN / 'REWRITE_PRIORITIES.md').read_text(encoding='utf-8')
text = text.replace('## Case-by-case timing review', '\n'.join(conflicts) + '\n## Case-by-case timing review')
(RUN / 'REWRITE_PRIORITIES.md').write_text(text, encoding='utf-8')
print('Wrote final case-specific priorities.')
