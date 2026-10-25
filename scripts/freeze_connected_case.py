"""Freeze an immutable eight-stage current case; never overwrite a selected trial."""
from pathlib import Path
import argparse
import hashlib
import json
import random
import yaml
from compile_connected_story import ROOT, LAB, compile_bank
from validate_playable_evidence import validate


def export(active, killer, out):
    bank=compile_bank(active)
    evidence=validate()
    public=yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))
    all_people={str(p['id']).zfill(2):p for p in public['characters']}
    rows={str(p['id']).zfill(2):p for p in bank['characters']}
    people={i:all_people[i] for i in rows}
    killer=str(killer).zfill(2)
    if killer not in rows:
        raise ValueError('Selected culprit must be in the compiled cast.')
    visible={'number','title','department','stamp','paragraphs','rows','images'}
    def shown(exhibit):
        item={k:v for k,v in exhibit.items() if k in visible}
        if exhibit.get('id')=='original_interview':
            if not bank['pre_method_press_interview_opening']:
                return None
            item['paragraphs']=bank['pre_method_press_interview_opening']
        return json.dumps(item,ensure_ascii=False,indent=2)
    def release(key):
        exhibits=next(r for r in evidence['releases'] if r['key']==key)['exhibits']
        return '\n\n'.join(x for e in exhibits if (x:=shown(e)) is not None)
    def speeches(key):
        blocks=[]
        for group in next(r for r in bank['question_rounds'] if r['key']==key)['groups']:
            blocks.append('Question for '+', '.join(group['targets'])+': '+group['question'])
            for name in group['targets']:
                ident=next(i for i,p in people.items() if p['name']==name)
                phase={'motive':'motive','opportunity':'where','method':'evidence'}[key]
                branch='murderer' if ident==killer else 'innocent'
                blocks.append(name+'\n'+rows[ident]['hearings'][phase+'_'+branch])
        return '\n\n'.join(blocks)
    stages={
        1:f'Exactly one of these {len(rows)} characters committed the murder alone. Other mentioned staff are not selectable suspects.\n\n'+'\n\n'.join(p['name']+' / '+p['role']+'\n'+p['introduction'] for p in people.values()),
        2:'\n\n'.join(shown(e) for e in evidence['hunt']),
        3:release('before_motive'),4:speeches('motive'),
        5:release('before_opportunity'),6:speeches('opportunity'),
        7:release('before_method'),8:speeches('method'),
    }
    # Validate the full export before creating its immutable trial directory.
    out=out.resolve()
    if not out.is_relative_to(LAB) and not out.is_relative_to(ROOT/'build'):
        raise ValueError('Trial output must remain in lab or build.')
    out.mkdir(parents=True,exist_ok=False)
    frozen=out/'frozen-source'; frozen.mkdir()
    for name in ('five-role-bank.yaml','production-family-scenes.yaml','collection-scenes.yaml',
                 'market-scenes.yaml','remaining-scenes.yaml','motive-dialogue.yaml','stage-dialogue.yaml',
                 'dramatic-dialogue-01.yaml','dramatic-dialogue-02.yaml','dramatic-dialogue-03.yaml',
                 'voice-story-bible.yaml',
                 'attendance-edits.yaml','question-rounds.yaml','evidence-contracts.yaml','playable-evidence.yaml'):
        (frozen/name).write_bytes((LAB/name).read_bytes())
    (frozen/'character_copy.yaml').write_bytes((ROOT/'source/character_copy.yaml').read_bytes())
    (frozen/'compiled-bank.yaml').write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
    for n,text in stages.items():
        (out/f'checkpoint_{n:02}.txt').write_text(text+'\n',encoding='utf-8')
    manifest={'killer_id':killer,'cast':[{'id':i,'name':p['name']} for i,p in people.items()],
              'scope':'Eight stages including all16 hunt exhibits and named questions. Intended image observations; no rendered artwork or Coming Clean. Attendance compiled before export.',
              'sha256':{str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in out.rglob('*') if f.is_file()}}
    (out/'private-selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return stages


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--active',default='all')
    parser.add_argument('--killer',help='Reuse a prior hidden selection; omit for one uniform random draw.')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    ids=[str(r['id']).zfill(2) for r in compile_bank(args.active)['characters']]
    selected=args.killer or random.SystemRandom().choice(ids)
    export(args.active,selected,args.output)
    print('Frozen eight sequential checkpoints. Hidden culprit not printed; no score claim.')
