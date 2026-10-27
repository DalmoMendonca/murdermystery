"""Export the protected whole-cast text for isolated editorial readers."""
from pathlib import Path
import json, yaml, hashlib

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
RUN.mkdir(exist_ok=True)
source = ROOT/'source/connected_release/confirmed.yaml'
b = yaml.safe_load(source.read_text(encoding='utf-8'))
parts = ['# Complete ensemble manuscript for editorial reading\n',
         'All 22 active roles; innocent and murderer alternatives. In a played world, exactly one role uses its murderer alternatives and the others use innocent alternatives. These are private alternatives, not conversations every character knows. Read the complete text, including all endings.\n',
         '## Group questions and order\n', yaml.safe_dump(b['question_rounds'], sort_keys=False, allow_unicode=True)]
for c in b['characters']:
    parts.append(f"\n## {c['id']}: {c['name']}\n")
    for stage, key in [('Act I', 'motive'), ('Act II', 'where'), ('Act III', 'evidence')]:
        for branch in ['innocent', 'murderer']:
            parts.append(f"### {stage}, {branch}\n\n{c['hearings'][key+'_'+branch]}\n")
    for branch in ['innocent', 'murderer']:
        parts.append(f"### Finale, {branch}\n\n{c['coming_clean'][branch]}\n")
(RUN/'ensemble-manuscript.md').write_text('\n'.join(parts), encoding='utf-8')
(RUN/'baseline-provenance.json').write_text(json.dumps({'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'roles': 22, 'passages': 176, 'protected_commit': '2cb64b9'}, indent=2)+'\n')
(RUN/'CURRENT_STATE.md').write_text('User delegated whole-cast editorial judgment to independent subagents. Start from protected 2cb64b9, not rejected revisions. Full 22-role/176-passage audit before drafting. Two fresh editorial readers assess ensemble patterns independently; separate semantic steward records protected claims. No external publishing, source promotion or blind playtest started. Current printing release and evidence remain protected.\n', encoding='utf-8')
print(str(RUN))
