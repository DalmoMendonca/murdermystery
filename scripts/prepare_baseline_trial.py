"""Freeze a bounded edit to the published story and one blind all-thirty trial."""
from pathlib import Path
import copy, hashlib, json, random, yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'docs/baseline-improvement-01-SPOILERS'
OUT = ROOT / 'build/baseline-improvement-01'
if (OUT / 'private-selection.json').exists():
    raise SystemExit('Already frozen; do not replace a draw or tested inputs.')

story = yaml.safe_load((ROOT / 'source/investigation_copy.yaml').read_text(encoding='utf-8'))
original = copy.deepcopy(story)
rows = {r['id']: r for r in story['characters']}
patch = yaml.safe_load((CANDIDATE / 'opportunity-edits.yaml').read_text(encoding='utf-8'))
assert len(patch['edits']) == len({e['id'] for e in patch['edits']}) == 10
for edit in patch['edits']:
    row = rows[edit['id']]
    text = edit['opportunity'].strip()
    assert 55 <= len(text.split()) <= 110
    row['hearings']['where_innocent'] = text
    row['hearings']['where_murderer'] = text
    proof = row['exclusion']
    if 'activity_premise' in proof:
        proof['activity_premise'] = text
    for fragment in proof.get('claim_fragments', []):
        if fragment['round'] == 'where':
            fragment['text'] = text
for before, after in zip(original['characters'], story['characters']):
    for key in ('motive_innocent', 'motive_murderer', 'evidence_innocent', 'evidence_murderer'):
        assert before['hearings'][key] == after['hearings'][key]
    assert before['coming_clean'] == after['coming_clean']

CANDIDATE.mkdir(exist_ok=True)
(CANDIDATE / 'investigation_copy.yaml').write_text(yaml.safe_dump(story,sort_keys=False,allow_unicode=True,width=105),encoding='utf-8')
evidence = yaml.safe_load((ROOT / 'source/evidence_design.yaml').read_text(encoding='utf-8'))
(CANDIDATE / 'evidence_design.yaml').write_bytes((ROOT / 'source/evidence_design.yaml').read_bytes())
characters = json.loads((ROOT / 'source/characters.json').read_text(encoding='utf-8'))
assert len(characters) == len(rows) == 30
killer = random.SystemRandom().choice(characters)['id']
OUT.mkdir(parents=True,exist_ok=True)
def write(n, text):
    (OUT / f'checkpoint_{n:02}.txt').write_text(text,encoding='utf-8')
lines = ['Exactly one of these thirty guests committed the murder alone. Nonplaying staff are not suspects.','']
for c in characters:
    lines.extend([c['name']+' / '+c['role'],c['introduction'],''])
write(1,'\n'.join(lines))
for n,items in ((2,evidence['discoveries']),(3,[r for r in evidence['reports'] if r['id'] in ('F1','F2')]),(5,[r for r in evidence['reports'] if r['id']=='F3']),(7,[r for r in evidence['reports'] if r['id'] in ('F4','F5')])):
    stripped = [{k:v for k,v in item.items() if k not in ('layout','photo','photos','service_photo','document_label')} for item in items]
    write(n,json.dumps(stripped,indent=2,ensure_ascii=False))
for n,key in ((4,'motive'),(6,'where'),(8,'evidence')):
    lines = []
    for c in characters:
        branch = 'murderer' if c['id']==killer else 'innocent'
        lines.extend([c['name'],rows[c['id']]['hearings'][key+'_'+branch],''])
    write(n,'\n'.join(lines))
manifest = {'killer_id':killer,'cast_ids':[c['id'] for c in characters],
            'selection':'One uniform random draw; no reselection; all outcomes retained.',
            'presentation':'Text equivalents, not actual clue photographs. No branch labels or endings released.',
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('checkpoint_*.txt')}}
(OUT / 'private-selection.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Frozen one all-thirty trial: ten shared Opportunity edits, unchanged Motive/Method/endings/evidence. No selected identity printed.')
