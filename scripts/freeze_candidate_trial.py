"""Freeze one candidate's actual questions and sequential public disclosures."""
from pathlib import Path
import argparse, hashlib, json, random, sys, yaml
from character_copy import load_characters

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('candidate', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
candidate, output = args.candidate.resolve(), args.output.resolve()
if output.exists():
    raise SystemExit('Refusing to overwrite a trial, selection or previously tested inputs.')
characters = load_characters(ROOT)
story = yaml.safe_load((candidate/'investigation_copy.yaml').read_text(encoding='utf-8'))
evidence = yaml.safe_load((candidate/'evidence_design.yaml').read_text(encoding='utf-8'))
questions = json.loads((candidate/'question_rounds.json').read_text(encoding='utf-8'))
rows = {r['id']: r for r in story['characters']}
by_name = {c['name']: c for c in characters}
assert len(characters) == len(rows) == 30
for round_ in questions:
    targets = [name for group in round_['groups'] for name in group['targets']]
    assert len(targets) == len(set(targets)) == 30 and set(targets) == set(by_name)
killer = random.SystemRandom().choice(characters)['id']
output.mkdir(parents=True)
snapshot = output/'frozen-source'
snapshot.mkdir()
for name in ['investigation_copy.yaml','evidence_design.yaml','case_design.yaml','question_rounds.json']:
    (snapshot/name).write_bytes((candidate/name).read_bytes())
for name in ['characters.json','character_copy.yaml','public_assets_lock.json']:
    (snapshot/name).write_bytes((ROOT/'source'/name).read_bytes())

def write(n, text):
    (output/f'checkpoint_{n:02}.txt').write_text(text, encoding='utf-8')

intro = ['Exactly one of these thirty guests committed the murder alone. Nonplaying staff are not suspects.', '']
for c in characters:
    intro.extend([c['name']+' / '+c['role'], c['introduction'], ''])
write(1, '\n'.join(intro))
# Strict allowlist: no authored resolution, trace anchor, role branch or art filename.
visible = {'number','department','title','stamp','text','rows','paragraphs','annotation',
           'timeline','photography_note','photo_contract','trace_exhibit','document_label'}
def artifact(item):
    result = {k:v for k,v in item.items() if k in visible}
    if 'trace_exhibit' in result:
        result['trace_exhibit'] = {k:v for k,v in result['trace_exhibit'].items() if k in ('title','text')}
    return result
for n, items in [(2,evidence['discoveries']),
                 (3,[r for r in evidence['reports'] if r['id'] in ('F1','F2')]),
                 (5,[r for r in evidence['reports'] if r['id']=='F3']),
                 (7,[r for r in evidence['reports'] if r['id'] in ('F4','F5')])]:
    write(n, 'Transcribed exhibit text and intended visible observations; actual artwork is not shown.\n'+
          json.dumps([artifact(r) for r in items], ensure_ascii=False, indent=2))
for n, phase, hearing in [(4,'motive','motive'),(6,'opportunity','where'),(8,'method','evidence')]:
    round_ = next(r for r in questions if r['key']==phase)
    lines = [round_['title'], '']
    for group in round_['groups']:
        lines.extend(['Question for '+', '.join(group['targets'])+': '+group['question'], ''])
        for name in group['targets']:
            c = by_name[name]
            branch = 'murderer' if c['id']==killer else 'innocent'
            lines.extend([name, rows[c['id']]['hearings'][hearing+'_'+branch], ''])
    write(n, '\n'.join(lines))
manifest = {'killer_id':killer, 'cast':[{'id':c['id'],'name':c['name']} for c in characters],
            'selection':'One uniform random draw from all thirty; no reselection.',
            'fidelity':'Actual named questions included. Text and intended image observations only; no final artwork or live-party performance.',
            'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.glob('checkpoint_*.txt'))},
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(snapshot.iterdir())}}
(output/'private-selection.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Frozen one all-thirty sequential trial with questions. Selected identity not printed.')
