"""Report all three fixed diagnostics without modifying the original audit."""
import json
from statistics import mean
from pathlib import Path
import report_exhaustive_balance as report
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

report.RUN = Path(__file__).resolve().parents[1] / 'docs/playtest/2026-10-11-BOUNDED-STORY-SPOILERS'
data = report.collect()
data['total'] = 3
report.write(report.RUN / 'aggregate.json', data)
done = [t for t in data['trials'] if t['status'] == 'complete']
baseline = report.read(report.RUN.parent / '2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/aggregate.json')
lines = [f'# Bounded story pass: {len(done)}/3 complete / SPOILERS', '',
         'Six innocent Method replies were rewritten; Elle’s two Opportunity replies gained existing financial pressure. All exhibit text, final murderer claims, introductions, and confessions are unchanged. Fixed scenarios are Elle, Chip, and Barb, one fresh reader each. These are exploratory comparisons against five prior readers per case, not paired controlled measurements.', '',
         'The frozen diagnostic retains the longer Elle Opportunity copy. The separate candidate-confirmed.yaml shortens those two replies for layout, preserving the stated actions and pressure. That wording is not scored. No published game source or sent asset has changed.', '',
         '| Scenario | E3 baseline mean (range) → new | Final culprit | Innocent alternatives 5–7: baseline mean → new | Naturalness: baseline mean → new | Correct |',
         '| --- | --- | ---: | --- | --- | --- |']
for t in done:
    b = next(c for c in baseline['cases'] if c['name'] == t['murderer'])
    m = t['metrics']
    lines.append(f"| {t['murderer']} | {b['e3_score']['mean']} ({b['e3_score']['min']}–{b['e3_score']['max']}) → {m['e3_score']} | {m['final_score']} | {b['final_alternatives']['mean']} → {m['final_alternatives']} | {b['ratings']['naturalness']} → {t['accusation']['ratings']['naturalness']} | {m['correct']} |")
lines += ['', '## Original feedback', '']
for t in done:
    lines += [f"### {t['murderer']} ({t['trial']})", '', t['accusation']['feedback'], '',
              'Finale: ' + t['finale']['feedback'], '']
    for issue in t['accusation']['issues']:
        lines += [f"- {issue['severity']} / {issue['category']}: {issue['detail']} Suggested direction: {issue['suggested_fix']}"]
    lines.append('')
lines += ['## Decision', '',
          'Do not promote this diagnostic directly. It covers three selected worlds, not all thirty branches, and the final layout-shortened Elle wording has not been scored. Retain the published baseline until a coherent bounded successor improves the flagged weaknesses and passes artifact checks.', '',
          'Technical history: the gate initially had a roster encoding mismatch. All three readers were blocked at their first validation; only canonical-name keys were repaired. Later quota interruptions resumed the original readers with earlier scores locked. No trials or results were replaced.', '',
          'Individual scores and all reasoning are preserved in aggregate.json and blind/. Scores are not probabilities or human solve-rate estimates.', '']
(report.RUN / 'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
if len(done) == 3:
    cmap = LinearSegmentedColormap.from_list('museum', ['#e0eee7', '#9ac8ae', '#f0dd75', '#efaa5e', '#af3439', '#71293e'])
    fig, axes = plt.subplots(1, 3, figsize=(22, 12), gridspec_kw={'wspace': .12})
    fig.patch.set_facecolor('#faf7ef')
    names = [p['name'] for p in data['roster']]
    for index, (ax, trial) in enumerate(zip(axes, done)):
        grid = [[s['scores'][name] for s in trial['stages']] for name in names]
        ax.imshow(grid, vmin=0, vmax=10, cmap=cmap, aspect='auto')
        ax.set_xticks(range(8), ['Intro','Hunt','E1','Act I','E2','Act II','E3','Act III'], rotation=45, ha='right')
        ax.set_yticks(range(22), names if index == 0 else [''] * 22)
        ax.set_title('Reader ' + chr(65 + index) + '\n' + trial['murderer'], fontsize=15)
        for y, row in enumerate(grid):
            for x, value in enumerate(row): ax.text(x, y, str(value), ha='center', va='center', fontsize=9, color='white' if value>=8 else '#252521')
        ax.set_xticks([x-.5 for x in range(9)], minor=True)
        ax.set_yticks([y-.5 for y in range(23)], minor=True)
        ax.grid(which='minor', color='#faf7ef', linewidth=2)
        ax.tick_params(which='minor', bottom=False, left=False)
    fig.suptitle('Bounded story diagnostic · three fixed RSVP22 scenarios · SPOILERS', fontsize=20)
    fig.subplots_adjust(left=.13, right=.98, top=.90, bottom=.10)
    fig.savefig(report.RUN/'heatmaps.png', dpi=150, facecolor=fig.get_facecolor())
    fig.savefig(report.RUN/'heatmaps.pdf', facecolor=fig.get_facecolor())
    plt.close(fig)
print(json.dumps({'complete':len(done),'invalid':data['invalid'],'correct':sum(t['metrics']['correct'] for t in done)}))
