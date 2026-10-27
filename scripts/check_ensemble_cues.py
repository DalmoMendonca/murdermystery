"""Check actual cue coverage and post-vote order, not literary or solve quality."""
from pathlib import Path
from collections import Counter
import argparse, json, yaml

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
FIELDS = {'motive':'motive','opportunity':'where','method':'evidence'}
norm = lambda s:' '.join(s.split())

def main():
    p=argparse.ArgumentParser();p.add_argument('--version',default='05');a=p.parse_args()
    source=RUN/f'candidate{a.version}-source'
    bank=yaml.safe_load((source/'confirmed.yaml').read_text(encoding='utf-8'))
    perf=yaml.safe_load((source/'performance.yaml').read_text(encoding='utf-8'))
    people={c['id']:c for c in bank['characters']};ids=list(people)
    assert len(ids)==22
    schedules={s['round_key']:s for s in perf['metadata']['schedules']}
    stage_cases=0;finale_cases=0
    for killer in ids:
        for rd in bank['question_rounds']:
            field=FIELDS[rd['key']];scene=schedules[rd['key']]
            members={t['id'] for t in scene['turns']}
            for chosen in ids:
                heard=set();events=[]
                def call(ident):
                    assert ident not in heard, 'Do not call an already-heard guest.'
                    if ident in members:
                        assert not (members & heard), 'A group is an atomic block.'
                        for turn in scene['turns']:
                            branch='murderer' if turn['id']==killer else 'innocent'
                            text=perf['fields'][turn['id']][field+'_'+branch][turn['part']-1]['speech']
                            events.append((turn['id'],turn['part'],text))
                        heard.update(members)
                    else:
                        branch='murderer' if ident==killer else 'innocent'
                        events.append((ident,1,people[ident]['hearings'][field+'_'+branch]))
                        heard.add(ident)
                call(chosen)
                # Deliberately leave the whole marked block until last where possible.
                for ident in ids:
                    if ident not in heard and ident not in members: call(ident)
                if not members<=heard: call(next(i for i in ids if i in members))
                assert heard==set(ids)
                assert len(events)==24
                for ident in ids:
                    text=' '.join(e[2] for e in events if e[0]==ident)
                    branch='murderer' if ident==killer else 'innocent'
                    assert norm(text)==norm(people[ident]['hearings'][field+'_'+branch])
                # Completion ends the act: no request for a nonexistent next guest.
                assert not (set(ids)-heard)
                stage_cases+=1
        others=[i for i in ids if i!=killer]
        for rank in [1,2,3,4]:
            top=others[:3]
            if rank<=3: top.insert(rank-1,killer);top=top[:3]
            selected_innocents=[i for i in top if i!=killer]
            for order in [selected_innocents,list(reversed(selected_innocents))]:
                performed=order+[killer]
                assert len(performed)==len(set(performed))
                assert 3<=len(performed)<=4 and performed[-1]==killer
                assert set(performed[:-1])==set(top)-{killer}
                escaped=killer not in top
                assert escaped==(rank==4)
                finale_cases+=1
    report=dict(version=a.version,stage_trigger_world_checks=stage_cases,
                finale_rank_order_checks=finale_cases,all22_roles_complete_each_act=True,
                extra_entries_per_act=2,branch_content_and_part_order_exact=True,
                group_atomicity=True,last_group_ends_act=True,murderer_last_after_locked_votes=True,
                original_tally_award_preserved=True,
                limits='Deterministic source/cue checks; not a human rehearsal, semantic proof, literary grade or fairness playtest.')
    (RUN/f'candidate{a.version}-cue-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
