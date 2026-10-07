"""Prepare phase-ordered, player-visible fixtures from the rendered private kit.
No organizer ledger or ending is released to blind participants before voting.
"""
import argparse,json,random,re
from pathlib import Path
import fitz,yaml
from build import ROOT,KIT,GAME
from character_copy import load_characters

def pdf_text(path):
    with fitz.open(path) as d:return '\n\n'.join(p.get_text(sort=True) for p in d)

def prepare(output,seed,count=16):
    all_chars=load_characters();active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    rng=random.Random(seed);chars=sorted(rng.sample([c for c in all_chars if c['id'] in active],count),key=lambda c:c['id'])
    animals=rng.sample(GAME['animals'],count);culprit=rng.randrange(count)
    rounds=json.loads((ROOT/'source/question_rounds.json').read_text(encoding='utf-8'))
    personas=json.loads((ROOT/'source/playtest_personas.json').read_text(encoding='utf-8'))
    attendance='\n'.join(c['name']+' / '+c['role'] for c in chars)
    shared_hunt=pdf_text(KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf')
    output.mkdir(parents=True,exist_ok=True);orders=[]
    for rd in rounds:
        order=list(range(count));rng.shuffle(order);orders.append(order)
    for i,c in enumerate(chars):
        dest=output/f'player-{i+1:02d}';dest.mkdir(exist_ok=True)
        (dest/'identity.txt').write_text(f'{c["name"]}\nPERSONALITY: {personas[i % len(personas)]}\nMemorized animal: {animals[i]}. Slip returned; no retained token.\nATTENDING:\n{attendance}',encoding='utf-8')
        d=fitz.open(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf')
        if {x['id'] for x in chars}==active:
            roster=json.loads((ROOT/'build/event-roster.json').read_text(encoding='utf-8'))
            with fitz.open(KIT/roster['packet_file']) as event:
                offset=roster['characters'].index(c['name'])*12
                d.close();d=fitz.open();d.insert_pdf(event,from_page=offset,to_page=offset+11)
        with d:
            (dest/'01-arrival.txt').write_text(d[1].get_text(sort=True)+'\n'+d[2].get_text(sort=True)+'\n'+d[3].get_text(sort=True)+'\nSHARED FINDS\n'+shared_hunt,encoding='utf-8')
            for ri,rd in enumerate(rounds):
                ids={'motive':['F1','F2'],'opportunity':['F3'],'method':['F4','F5']}[rd['key']]
                text=(f'HOST announces twice: selected animal {animals[culprit]}.\n' if ri==0 else '')
                text+='PUBLIC REPORTS\n'+'\n\n'.join(pdf_text(KIT/'PRINT_WITHOUT_READING/Reports'/(x+'.pdf')) for x in ids)
                pages=GAME['packet_pages'][rd['key']+'_questions']+[GAME['packet_pages'][rd['key']+'_answer']]
                text+='\nYOUR CURRENT PAGES\n'+'\n\n'.join(d[p-1].get_text(sort=True) for p in pages)
                text+='\nPUBLIC ROUND: scripted table read, not live improvisation\n'
                for pos,j in enumerate(orders[ri]):
                    guest=chars[j];asker=chars[orders[ri][pos-1]];g=next(g for g in rd['groups'] if guest['name'] in g['targets'])
                    base={'motive':'motive','opportunity':'where','method':'evidence'}[rd['key']]
                    speech=guest['hearing'][base+'_'+('murderer' if j==culprit else 'innocent')]
                    with fitz.open(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{guest["slug"]}_SECRET.pdf') as gd:
                        printed=gd[GAME['packet_pages'][rd['key']+'_answer']-1].get_text(sort=True)
                        assert re.sub(r'\s+','',speech) in re.sub(r'\s+','',printed),('Fixture speech does not match rendered packet',guest['name'])
                    text+=f'\n{asker["name"]} asks {guest["name"]}: {g["question"]}\n{guest["name"]}: {speech}\n'
                (dest/f'{ri+2:02d}-{rd["key"]}.txt').write_text(text,encoding='utf-8')
                for pn in pages:d[pn-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(dest/f'packet-page-{pn:02d}.png')
            (dest/'05-ballot.txt').write_text(d[10].get_text(sort=True),encoding='utf-8')
            # Endings remain organizer-only. Participants must lock their vote first.
        if i==0:(dest/'host-guide.txt').write_text(pdf_text(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf'),encoding='utf-8')
    organizer={'seed':seed,'culprit':chars[culprit]['name'],'selected_animal':animals[culprit],'attending':[c['name'] for c in chars],'orders':orders,'fixture_type':'Phase-ordered scripted transcript from rendered kit','human_playtest':False,'ending_withheld':True}
    (output/'ORGANIZER_ONLY_DO_NOT_SHARE.json').write_text(json.dumps(organizer,indent=2)+'\n',encoding='utf-8')
    print(f'Prepared {count} isolated rendered-kit fixtures; all report pages included; endings withheld.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'build/playtest-restructure');p.add_argument('--seed',type=int,default=60626);p.add_argument('--count',type=int,default=16);a=p.parse_args();prepare(a.output,a.seed,a.count)
