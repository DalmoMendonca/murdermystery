"""Desk rehearsal of the printed named-question chain, draw and Coming Clean."""
import json,random
from build import ROOT,GAME

def finalists(votes):
    return sorted(votes,key=lambda n:(-votes[n],n))[:3]

def rehearse():
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    rounds=json.loads((ROOT/'source/question_rounds.json').read_text(encoding='utf-8'))
    by_name={c['name']:c for c in chars};all_names=list(by_name)
    rng=random.Random(20261030);runs=0;confessions=0;outside=0
    for trial in range(50):
        for attending in [all_names,all_names[:15],rng.sample(all_names[:15],10)+rng.sample(all_names[15:],7)]:
            bowl_a=list(GAME['animals']);rng.shuffle(bowl_a)
            memory={n:bowl_a.pop() for n in attending};closed_return=list(memory.values())
            bowl_b=[a for a in GAME['animals'] if a not in bowl_a]
            assert len(set(memory.values()))==len(attending)==len(closed_return)
            assert set(bowl_b)==set(memory.values())
            selected=rng.choice(bowl_b);killer=next(n for n,a in memory.items() if a==selected)
            assert sum(a==selected for a in memory.values())==1
            for rd in rounds:
                pending=set(attending);asker=rng.choice(attending);heard=[]
                while pending:
                    choices=list(pending-{asker})
                    if not choices:choices=list(pending)
                    respondent=rng.choice(sorted(choices))
                    group=next(g for g in rd['groups'] if respondent in g['targets'])
                    assert group['question'] and respondent in by_name
                    branch='murderer' if respondent==killer else 'innocent'
                    key={'motive':'motive','opportunity':'where_'+branch,'method':'evidence_'+branch}[rd['key']]
                    assert by_name[respondent]['hearing'][key]
                    heard.append(respondent);pending.remove(respondent);asker=respondent
                assert set(heard)==set(attending) and len(heard)==len(set(heard))
            facts={n:by_name[n]['case_facts']['murderer' if n==killer else 'innocent'] for n in attending}
            assert [n for n,f in facts.items() if all(f[k] for k in ['salon','key','linen'])]==[killer]
            for votes in [{n:rng.randrange(5) for n in attending},{n:1 for n in attending},{n:0 for n in attending}]:
                top=finalists(votes);readers=list(top)
                assert len(top)==min(3,len(attending)) and set(top)<=set(attending)
                if killer not in readers:readers.append(killer);outside+=1
                assert sum(n==killer for n in readers)==1
                for n in readers:assert by_name[n]['private']['final_'+('murderer' if n==killer else 'innocent')]
                confessions+=1
            if bowl_a:assert bowl_a[-1]!=selected
            runs+=1
    assert finalists({'Zoe':2,'Anne':2,'Mona':2,'Reed':2,'Zero':0})==['Anne','Mona','Reed']
    assert finalists({'Zoe':16,'Anne':0,'Mona':0,'Reed':0})==['Zoe','Anne','Mona']
    assert finalists({'Zoe':0,'Anne':0,'Mona':0,'Reed':0})==['Anne','Mona','Reed']
    report={'draw_and_turn_rehearsals':runs,'coming_clean_rehearsals':confessions,'outside_top_three_reveals':outside,'passed':True,'human_playtest':False,
            'coverage':['all thirty roles eligible','unique memorized animals returned to closed box','unused animals excluded from B','one attending murderer','named questions inside each packet','every present guest answers once per round','absences and late arrivals','combined evidence uniquely identifies culprit','top-three and alphabetical tie handling','murderer outside top three always confesses']}
    (ROOT/'build/rehearsal-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':rehearse()
