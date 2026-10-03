from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
src=root/'source/v1'
flat=lambda s:' '.join(s.split())
chars=sum([json.loads(p.read_text(encoding='utf-8')) for p in sorted((src/'characters').glob('*.json'))],[])
bible='\n'.join(p.read_text(encoding='utf-8') for p in sorted((src/'spoiler_bible').glob('*.md')))
def between(t,a,b): return t.split(a,1)[1].split(b,1)[0].strip()
def columns(t,left_tail=False):
    a=[];b=[]
    for line in t.splitlines():
        if not line.strip() or 'IF INNOCENT' in line or line.strip()=='IF MURDERER':continue
        halves=re.split(r' {3,}',line.strip(),maxsplit=1)
        if len(halves)==2:a.append(halves[0]);b.append(halves[1])
        elif line.strip():(a if left_tail else b).append(line.strip())
    return flat(' '.join(a)),flat(' '.join(b))
out=[]
for c in chars:
    pre=c['preparty_markdown'];s=c['secret_markdown'];id=int(c['id'])
    entry=bible.split(f'{id}. {c["name"]} - ',1)[1]
    if id<30: entry=entry.split(f'{id+1}. ',1)[0]
    else:entry=entry.split('Difficulty tuning rationale',1)[0]
    innocent_e=flat(between(entry,'Innocent evidence:','Murderer evidence:'))
    murderer_e=flat(entry.split('Murderer evidence:',1)[1])
    instructions=flat(between(s,'ACT III EVIDENCE CARD','FINAL STATEMENT'))
    letters=re.findall(r'secretly submit Card ([AB])',instructions)
    assert len(letters)==2 and set(letters)=={'A','B'},c['name']
    final=columns(s.split('IF INNOCENT',2)[2].split('IF MURDERER',1)[1], id in [12,16,28,29])
    route_text=between(s,'ACT II - AFTER STERLING DIES','ACT III EVIDENCE CARD').split('IF INNOCENT',1)[1]
    routes=columns(route_text,False)
    # All singleton route lines are resolved against the canonical branch matrix.
    canonical_routes=(flat(between(entry,'Innocent route:','Murderer route:')),flat(between(entry,'Murderer route:','Innocent evidence:')))
    if id<=15:
        routes=canonical_routes
    relationships=[flat(x) for x in between(pre,'WHAT YOU ALREADY KNOW','COSTUME').split('•') if x.strip()]
    item={k:c[k] for k in ['id','slug','name','role','age','tier']}
    costume=flat(between(pre,'COSTUME','OPTIONAL QUIPS'))
    costume=re.sub(r'\bCarry\b','You might carry',costume)
    costume=re.sub(r'\bBring\b','You might bring',costume)
    costume=costume.replace('Do not dress as a cop; think senior museum security professional.','A senior museum security look could work well.')
    costume=costume.replace('Add glasses, notebook, museum catalogue full of tabs.','Optional extras: glasses, a notebook or a museum catalogue full of tabs.')
    costume=costume.replace('Aim for','For inspiration, think of')
    costume=costume.replace('Think luxury event professional, not waiter costume.','A luxury event professional could be your inspiration.')
    costume=costume.replace('Avoid costume-protester clichés.','A bold accessory may be all you need.')
    item['preparty']={'description':flat(pre.split('HOW TO PLAY THEM')[0]),'relationships':relationships,'acting':flat(between(pre,'HOW TO PLAY THEM','WHAT YOU ALREADY KNOW')),'costume':'Optional inspiration: '+costume}
    item['private']={'history':flat(between(s,'Your private history with Sterling Voss','What you are hiding')),'secret':flat(between(s,'What you are hiding','Your objectives')),'objectives':[flat(x) for x in between(s,'Your objectives','What you know about other guests').split('•') if x.strip()],'knowledge':[flat(x) for x in between(s,'What you know about other guests','ACT II - AFTER STERLING DIES').split('•') if x.strip()],'innocent':routes[0],'murderer':routes[1],'evidence_instruction':instructions,'innocent_card':letters[0],'murderer_card':letters[1],'final_innocent':final[0],'final_murderer':final[1]}
    item['evidence']={letters[0]:innocent_e,letters[1]:murderer_e}
    out.append(item)
(root/'source/characters.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Structured',len(out),'characters, 60 evidence cards, 60 final statements')
