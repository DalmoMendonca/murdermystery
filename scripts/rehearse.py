"""Deterministic desk rehearsal of animal draws, absences and question handoffs.

This validates the printed procedure's model; it is not a human playtest.
"""
import json, random
from build import ROOT, GAME

def rehearse():
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    rng=random.Random(20261030)
    runs=0
    for trial in range(50):
        for attending in [list(range(30)),list(range(15)),sorted(rng.sample(range(15),10)+rng.sample(range(15,30),7))]:
            core=[i for i in attending if chars[i]['tier']=='CORE']
            optional=[i for i in attending if chars[i]['tier']!='CORE']
            bowl_a=list(GAME['core_animals']);rng.shuffle(bowl_a)
            optional_bowl=list(GAME['optional_animals']);rng.shuffle(optional_bowl)
            memory={};closed_return=[]
            for i in core:
                memory[i]=bowl_a.pop();closed_return.append(memory[i])
            for i in optional:
                memory[i]=optional_bowl.pop();closed_return.append(memory[i])
            # Remove unused A animals from B; return box is never the draw bowl.
            bowl_b=[a for a in GAME['core_animals'] if a not in bowl_a]
            assert len(set(memory.values()))==len(attending)==len(closed_return)
            assert set(bowl_b)=={memory[i] for i in core}
            selected=rng.choice(bowl_b)
            killers=[i for i in attending if memory[i]==selected]
            assert len(killers)==1 and killers[0] in core
            killer=killers[0]
            for round_name in ['motive','opportunity','method']:
                heard=[]
                for n,respondent in enumerate(attending):
                    asker=attending[n-1]
                    assert asker!=respondent
                    assert chars[respondent]['questions'][round_name]
                    branch='murderer' if respondent==killer else 'innocent'
                    speech_key={'motive':'motive','opportunity':'where_'+branch,'method':'evidence_'+branch}[round_name]
                    assert chars[respondent]['hearing'][speech_key]
                    heard.append(respondent)
                assert heard==attending and len(set(heard))==len(attending)
            receipts={i:chars[i]['case_facts']['murderer' if i==killer else 'innocent'] for i in attending}
            assert [i for i,facts in receipts.items() if all(facts[k] for k in ['salon','key','linen'])]==[killer]
            # A late core guest draws unused A: that animal was excluded from B.
            if bowl_a:assert bowl_a[-1]!=selected
            runs+=1
    report={'draw_and_turn_rehearsals':runs,'passed':True,'human_playtest':False,
            'coverage':['unique memorized animals','unused A removed from B','optional animals excluded',
                        'one eligible murderer','every present guest asks and answers every round',
                        'absent IDs skipped','combined evidence unique','late core arrival cannot be killer']}
    (ROOT/'build/rehearsal-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':rehearse()
