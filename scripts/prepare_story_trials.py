"""Freeze a story candidate and make distinct, stratified blind transcript trials."""
from pathlib import Path
import json,yaml,random,hashlib,shutil,argparse
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/story-pass-12-SPOILERS'
OUT=ROOT/'build/story-pass12'

def make(version=12, selection_from=None):
    global SOURCE, OUT
    SOURCE=ROOT/f'docs/story-pass-{version}-SPOILERS'
    OUT=ROOT/f'build/story-pass{version}'
    if (OUT/'private-manifest.json').exists():
        raise SystemExit('Trial already frozen. Use a new version/directory; never replace tested inputs or selections.')
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    story=yaml.safe_load((SOURCE/'investigation_copy.yaml').read_text(encoding='utf-8'))
    rows=story['characters']
    by={r['id']:r for r in rows}
    evidence=yaml.safe_load((SOURCE/'evidence_design.yaml').read_text(encoding='utf-8'))
    active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    sets=[('A',set(by),['02','06','11','12','20','23']),
          ('B',active,['09','18','19','25','28','29']),
          ('C',active,['01','05','08','10','13','14'])]
    if version>=13:
        sets=[('A',set(by),sorted(by)),('B',active,sorted(active)),('C',active,sorted(active))]
    frozen=OUT/'tested-source';frozen.mkdir(parents=True,exist_ok=True)
    for p in SOURCE.glob('*.yaml'):shutil.copy2(p,frozen/p.name)
    prior=None
    if selection_from is not None:
        prior=json.loads((ROOT/f'build/story-pass{selection_from}/private-manifest.json').read_text(encoding='utf-8'))
    manifest={'selection':(f'Same originally random draws as pass{selection_from} for comparison; all trials retained.' if prior else ('Random within declared strata' if version==12 else 'Uniform random from attending cast per trial')+', without replacement across trials; all trials retained.'),
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen.glob('*.yaml')},'trials':[]}
    if version >= 19:
        manifest['presentation'] = 'Shared evidence text equivalents; renderer-only layout/photo identifiers omitted. No actual images supplied to transcript readers.'
    rng=random.SystemRandom();used=set()
    for label,present,pool in sets:
        path=OUT/label;path.mkdir(parents=True,exist_ok=True)
        cast=[c for c in chars if c['id'] in present]
        if prior:
            previous=next(t for t in prior['trials'] if t['trial']==label)
            assert previous['cast_ids']==[c['id'] for c in cast], 'Controlled comparison must preserve attending cast'
            killer=previous['killer_id'];assert killer in pool and killer not in used
        else:
            killer=rng.choice([ident for ident in pool if ident not in used])
        if 'prototype_guilty_ids' in story:
            assert killer in story['prototype_guilty_ids'], 'Untested prototype role cannot be selected'
            manifest['scope'] = 'Three designated culprit worlds only; remaining guilty branches are not validated.'
        used.add(killer)
        private={'trial':label,'killer_id':killer,'cast_ids':[c['id'] for c in cast]}
        (path/'private-selection.json').write_text(json.dumps(private,indent=2)+'\n',encoding='utf-8')
        manifest['trials'].append(private)
        lines=['Introductions / '+str(len(cast))+' attending characters','']
        for c in cast:lines += [c['name']+' / '+c['role'],c['introduction'],'']
        if version >= 17:
            lines += ['Game premise: Exactly one of the listed playing characters is the murderer. There are no accomplices or offstage killers. Nonplaying staff are not accusation choices. Guest statements may be evasive or false.']
        (path/'checkpoint_01.txt').write_text('\n'.join(lines),encoding='utf-8')
        for n,items in [(2,evidence['discoveries']),(3,[r for r in evidence['reports'] if r['id'] in ['F1','F2']]),(5,[r for r in evidence['reports'] if r['id']=='F3']),(7,[r for r in evidence['reports'] if r['id'] in ['F4','F5']])]:
            if version >= 19:
                # Internal asset names are not player evidence. Text must carry
                # every observation needed for a fair transcript evaluation.
                items=[{k:v for k,v in item.items() if k not in ('layout','photo','photos','service_photo','document_label')} for item in items]
            (path/f'checkpoint_{n:02}.txt').write_text(json.dumps(items,indent=2,ensure_ascii=False),encoding='utf-8')
        for n,key in [(4,'motive'),(6,'where'),(8,'evidence')]:
            lines=[]
            for c in cast:lines += [c['name'],by[c['id']]['hearings'][key+('_murderer' if c['id']==killer else '_innocent')],'']
            (path/f'checkpoint_{n:02}.txt').write_text('\n'.join(lines),encoding='utf-8')
    (OUT/'private-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Frozen 3 distinct selections; A=30, B/C=confirmed22. No selected identities printed.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',type=int,default=12)
    p.add_argument('--selection-from',type=int)
    args=p.parse_args();make(args.version,args.selection_from)
