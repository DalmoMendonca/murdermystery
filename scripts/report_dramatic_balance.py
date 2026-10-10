"""Validate and plot one three-reader frozen case without altering input or ratings."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--case', required=True, type=Path)
parser.add_argument('--readers', default='abc', help='Three distinct saved reader letters, in panel order')
args = parser.parse_args()
assert len(args.readers) == 3 and len(set(args.readers)) == 3 and args.readers.isalpha()
out = args.case.resolve()
assert out.is_relative_to(ROOT/'docs/connected-story-01-SPOILERS')
assert not ((out/'reader_a_audit.md').exists() and 'a' in args.readers.lower()), \
    'Reader A has an unreconstructable mapping error; use --readers bcd for this case.'
manifest = json.loads((out/'private-selection.json').read_text(encoding='utf-8'))
for relative, expected in manifest['sha256'].items():
    assert hashlib.sha256((out/relative).read_bytes()).hexdigest() == expected, relative
post_vote = json.loads((out/'post-vote-hash.json').read_text(encoding='utf-8'))
assert hashlib.sha256((out/post_vote['file']).read_bytes()).hexdigest() == post_vote['sha256']
names = [r['name'] for r in manifest['cast']]
killer = next(r['name'] for r in manifest['cast'] if r['id'] == manifest['killer_id'])
labels = ['Intro', 'Hunt', 'E1', 'Act I', 'E2', 'Act II', 'E3', 'Act III']
count = len(names)
readers, metrics, arrays = {}, {}, {}
for letter in args.readers:
    key = 'Reader ' + letter.upper()
    result = json.loads((out/f'reader_{letter}.json').read_text(encoding='utf-8-sig'))
    assert len(result['checkpoints']) == 8, key
    assert result.get('final_feedback') and result.get('post_vote_feedback'), key
    assert result.get('narrative_ratings'), key
    stages = []
    for number, checkpoint in enumerate(result['checkpoints'], 1):
        assert checkpoint['stage'] == number, (key, number)
        scores = checkpoint['scores']
        assert len(scores) == count and set(scores) == set(names), (key, number)
        assert all(isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 10
                   for v in scores.values()), (key, number)
        leaders = [n for n in names if scores[n] == max(scores.values())]
        margin = scores[killer] - max(scores[n] for n in names if n != killer)
        stages.append(dict(stage=number, above_five=sum(v > 5 for v in scores.values()),
                           culprit_score=scores[killer], leaders=leaders,
                           correct_sole_leader=leaders == [killer], culprit_margin=margin,
                           alternatives_five_six=sum(5 <= scores[n] <= 6 for n in names if n != killer),
                           alternatives_six_seven=sum(6 <= scores[n] <= 7 for n in names if n != killer),
                           obvious_culprit=checkpoint.get('obvious_culprit')))
    early = any(s['obvious_culprit'] == killer for s in stages[:6])
    metric = dict(stages=stages, act_ii_above_five=stages[5]['above_five'],
                  correct_final_leader=stages[-1]['correct_sole_leader'],
                  final_culprit_score=stages[-1]['culprit_score'],
                  final_culprit_margin=stages[-1]['culprit_margin'],
                  final_alternatives_five_six=stages[-1]['alternatives_five_six'],
                  final_alternatives_six_seven=stages[-1]['alternatives_six_seven'],
                  early_obvious_culprit=early,
                  early_large_lead=any(s['correct_sole_leader'] and s['culprit_score'] >= 8
                                       and s['culprit_margin'] >= 2 for s in stages[:6]),
                  protocol_deviation=result.get('protocol_deviation', ''),
                  first_reported_correct_obvious_stage=next((s['stage'] for s in stages
                                              if s['obvious_culprit'] == killer), None),
                  narrative_ratings=result.get('narrative_ratings', {}))
    metric['numerical_targets_met'] = (metric['act_ii_above_five'] >= math.ceil(count/3)
           and metric['correct_final_leader'] and not metric['early_obvious_culprit']
           and not metric['early_large_lead'] and 3 <= metric['final_alternatives_five_six'] <= 4)
    metrics[key] = metric
    readers[key] = result
    arrays[key] = np.array([[s['scores'][n] for s in result['checkpoints']] for n in names])
(out/'metrics.json').write_text(json.dumps(metrics, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
with (out/'scores.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['Character'] + [f'{reader}: {stage}' for reader in readers for stage in labels])
    for name in names:
        writer.writerow([name]+[s['scores'][name] for r in readers.values() for s in r['checkpoints']])

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
def draw(ax, values, title, show_names):
    im = ax.imshow(values, cmap='RdYlGn_r', vmin=0, vmax=10, aspect='auto', interpolation='nearest')
    ax.set_title(title, fontsize=14, pad=15, fontweight='bold')
    ax.set_xticks(range(8), labels, rotation=35, ha='right')
    ax.set_yticks(range(count), names if show_names else ['']*count)
    ax.tick_params(axis='both', length=0)
    for row in range(count):
        for col in range(8):
            val = values[row, col]
            ax.text(col, row, f'{val:g}', ha='center', va='center', fontsize=9,
                    color='white' if val >= 8 or val <= 1 else '#17231c')
    ax.add_patch(Rectangle((-.5, names.index(killer)-.5), 8, 1, fill=False,
                          edgecolor='#171717', linewidth=1.7))
    for spine in ax.spines.values():
        spine.set_visible(False)
    return im

height = 14 if count == 30 else 11
fig, axes = plt.subplots(1, 3, figsize=(19, height))
fig.patch.set_facecolor('#faf8f2')
for ax, (key, values) in zip(axes, arrays.items()):
    im = draw(ax, values, key, ax is axes[0])
fig.subplots_adjust(left=.14, right=.96, bottom=.14, top=.87, wspace=.10)
fig.suptitle(f'{count} characters: three independent blind balance checks',
             fontsize=23, fontweight='bold', y=.965)
fig.text(.14, .914, f'Same random case per group · spoilers · outlined row: {killer}', fontsize=12)
fig.text(.14, .041, 'E1: first evidence   E2: before Act II   E3: before Act III   |   Scores 0–10; higher means more suspicion.', fontsize=11)
footnote = 'Text case, not a live party. Scores locked before Coming Clean; no forced distribution.'
if args.readers == 'bcd':
    footnote += ' Reader A excluded: unreconstructable name mapping; see audit.'
fig.text(.14, .019, footnote, fontsize=10)
cax = fig.add_axes([.14, .087, .38, .014])
fig.colorbar(im, cax=cax, orientation='horizontal', ticks=[0,2,4,6,8,10])
fig.savefig(out/'three_reader_heatmap.png', dpi=170, facecolor=fig.get_facecolor())
fig.savefig(out/'three_reader_heatmap.pdf', facecolor=fig.get_facecolor())
plt.close(fig)
for key, values in arrays.items():
    fig, ax = plt.subplots(figsize=(9, height))
    draw(ax, values, key, True)
    fig.subplots_adjust(left=.29, right=.95, bottom=.12, top=.93)
    fig.text(.29, .025, f'{count} characters · spoilers · outlined row: {killer}', fontsize=10)
    fig.savefig(out/(key.lower().replace(' ', '_')+'_heatmap.png'), dpi=160)
    plt.close(fig)

lines = [f'# Dramatic revision: {count}-character three-reader results', '',
         f'**Spoilers. Selected culprit: {killer}.** Three fresh readers received the same eight frozen stages. All sixteen hunt envelopes were shown. Accusations were locked before post-vote narrative review. No prior results, target ratings, branch labels, private routes or voice bible were shown.', '',
         '| Metric | ' + ' | '.join(args.readers.upper()) + ' |', '|---|---:|---:|---:|']
if args.readers == 'bcd':
    lines[3:3] = ['Reader A is excluded from numeric comparison because its positional score construction misassigned names. The original JSON is preserved. [The audit](reader_a_audit.md) can independently recover only one intended score, not the whole table. Reader D is a fresh replacement using the same frozen inputs. Reader B\'s wrong accusation is retained as a valid outcome.', '']
for title, field in [('Above 5 after Act II', 'act_ii_above_five'),
                     ('Correct sole final leader', 'correct_final_leader'),
                     ('Culprit final score', 'final_culprit_score'),
                     ('Final leader margin', 'final_culprit_margin'),
                     ('Other final suspects 5–6', 'final_alternatives_five_six'),
                     ('Other final suspects 6–7', 'final_alternatives_six_seven'),
                     ('Early obvious culprit', 'early_obvious_culprit'),
                     ('First reported correct obvious stage', 'first_reported_correct_obvious_stage')]:
    lines.append('| '+title+' | '+' | '.join(str(m[field]) for m in metrics.values())+' |')
lines += ['', f'At-least-one-third midpoint target is {math.ceil(count/3)}/{count} strictly above 5. Final alternatives at 5–6 target remains 3–4; 6–7 counts are separately reported because the user also wants stronger lingering suspicion. No averaging away disagreements. These are model judgments of one selected case, not human accusation rates or validation of every eligible murderer.', '',
          f'Validated {count*8*3} scores and every frozen input hash. Intended image observations remain text; actual artwork, print ergonomics and party pacing are outside this test.', '',
          '## Reader feedback', '']
for key, result in readers.items():
    lines += ['### '+key, '', result.get('final_feedback', ''), '',
              'Narrative ratings: '+json.dumps(result.get('narrative_ratings', {}), ensure_ascii=False), '',
              'Act II observation: '+result['checkpoints'][5].get('naturalness',''), '',
              'Act III observation: '+result['checkpoints'][7].get('naturalness',''), '',
              'Additional observations: '+json.dumps(result.get('narrative_observations', []), ensure_ascii=False), '',
              'Post-vote review: '+result.get('post_vote_feedback', ''), '',
              'Protocol deviation: '+(result.get('protocol_deviation') or 'None reported.'), '']
lines += ['## Artifacts', '', '[Combined heatmap](three_reader_heatmap.png) · [CSV](scores.csv) · [Metrics](metrics.json)', '']
(out/'RESULTS.md').write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({key:{k:v for k,v in metric.items() if k not in ('stages','narrative_ratings')}
                  for key,metric in metrics.items()}, indent=2))
