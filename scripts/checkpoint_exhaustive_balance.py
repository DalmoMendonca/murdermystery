"""Save an honest continuation checkpoint from audited results, without rescoring."""
import json
from datetime import datetime, timezone
from report_exhaustive_balance import collect, render
from exhaustive_balance import RUN
data = collect()
render(data)
done = [t for t in data['trials'] if t['status'] == 'complete']
clean = [t for t in done if not t['audit_flags']]
flagged = [t for t in done if t['audit_flags']]
remaining = [t['trial'] for t in data['trials'] if t['status'] != 'complete']
running = [t['trial'] for t in data['trials'] if t['status'] == 'running']
state_path = RUN / 'resume-state.json'
state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
state.update(completed=len(done), remaining=110-len(done), next_trial=remaining[0] if remaining else None,
             unfinished_active_trials=running, updated_utc=datetime.now(timezone.utc).isoformat(),
             reason='Audit in progress; preserve interrupted readers and immutable scores.' if remaining else 'All 110 trials audited complete.')
state_path.write_text(json.dumps(state, indent=2)+'\n', encoding='utf-8')

def count(key, rows=done):
    return sum(t['metrics'][key] for t in rows)

title = 'Final findings' if len(done) == 110 else 'Interim findings'
lines = [f'# {title} — {len(done)} of 110 tests / SPOILERS', '',
         f"This audit is {'complete' if len(done)==110 else 'incomplete'}. Each of 22 RSVP characters has five predetermined trials. Completed per-character counts are in the dashboard and case-summary.csv. No cases were rerolled and no game copy was changed.", '',
         f"Frozen published revision: `{data['revision']}`. Verified deploy: `{data['deploy']}`.", '',
         '## Results', '',
         f"- Correct locked accusations: {count('correct')}/{len(done)}. Earned finale reviews: {count('earned')}/{len(done)}. Reviews reporting decisive new finale facts: {sum(t['metrics']['new_facts']>0 for t in done)}.",
         f"- Explicit clear-culprit declarations before Act III: {count('early_clear')}/{len(done)}. This declaration measure does not rule out earlier numeric leads.",
         f"- Score/conclusion conflicts: {len(flagged)} ({', '.join(t['trial'] for t in flagged) or 'none'}). Raw numbers, reasoning, and accusations remain unchanged. Do not repair them by inference.",
         f"- Sensitivity subset excluding entire flagged trials: {len(clean)} readers. E3 murderer score 5–7: {count('e3_ready',clean)}/{len(clean)}; final murderer at least 9: {count('final_strong',clean)}/{len(clean)}; uniquely highest: {count('unique_top',clean)}/{len(clean)}.",
         f"- In that subset, at least eight suspects strictly above 5 after Act II: {sum(t['metrics']['act2_suspects']>=8 for t in clean)}/{len(clean)}. At least three innocent alternatives at 5–7 after Act III: {sum(t['metrics']['final_alternatives']>=3 for t in clean)}/{len(clean)}.", '',
         '## Reader feedback', '']
for key in ['fair_play','clarity','voice_distinction','arc_variety','naturalness','drama']:
    value = sum(t['accusation']['ratings'][key] for t in done)/len(done) if done else 0
    lines.append(f"- {key.replace('_',' ').capitalize()}: {value:.1f}/10.")
lines.append('')
for group in sorted(data['issue_summary'], key=lambda g: -len(g['trials'])):
    lines.append(f"- {group['category'].capitalize()}: explicitly raised in {len(group['trials'])}/{len(done)} reviews; {len(group['major'])} marked major. Full examples and trial references are in the dashboard.")
lines += ['', '## Priorities for a later rewrite', '',
          '1. Preserve the existing culprit contradiction and release order where they produce correct accusations and earned confessions. Do not rebuild successful logic merely to change scores.',
          '2. Broaden Act II suspicion through existing personal conflicts and suspicious actions. Do not add more incidental trips to the historical bottle.',
          '3. Identify innocent Act III replies that interpret exhibits or settle scandals. Preserve deduction facts, but move optional explanation and tidy resolution to Coming Clean.',
          '4. Reduce repeated technical descriptions, dossier recaps, and identical emotional rhythms. Let characters react as distinct people under pressure.',
          '5. Treat dense access to the historical loan and convenient paperwork resolutions as story problems; extra explanatory instructions will not solve them.',
          '6. Rank character-specific rewrites only after all five readers per culprit finish. Use the score ranges and flagged-trial sensitivity data rather than a single mean.', '',
          '## Limits and continuation', '',
          'These are attentive fresh-context AI text readers, not human solve-rate estimates. Every reader receives all 16 hunt exhibits. Physical discovery, party interruptions, visual interpretation, and imperfect human recall are not simulated. Identical instructions are used; personalities are not assigned.', '',
          'Inputs, sequential score locks, accusation locks, and completion hashes are audited by the report script. Interrupted original readers resume without replacing earlier scores. Pending trials are not successes. Technical deviations and score/conclusion conflicts remain visible.', '',
          f"Remaining: {110-len(done)}. Saved running trials: {', '.join(running) or 'none'}. The user-authorized continuation is `{state.get('automation_id','not recorded')}`; scheduled: {state.get('background_continuation_scheduled',False)}. No reset credit or purchase has been used by this audit.", '',
          'Resume original interrupted readers, then fresh fork-none agents for unstarted trials through t110, one agent per trial, using READER_INSTRUCTIONS.md. Never freeze again or expose other trials to a reader. Rebuild with checkpoint_exhaustive_balance.py and chart_exhaustive_balance.py. Disable the continuation after all 110 tests are verified complete.', '']
(RUN/'FINDINGS.md').write_text('\n'.join(lines), encoding='utf-8')
