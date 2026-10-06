"""Create isolated current-kit handouts for a future sixteen-agent blind table read.

This creates fixtures, not agents, human playtest results, or live conversations.
The organizer must release phases sequentially and lock ballots before endings.
"""
import argparse,json,random
from pathlib import Path
import fitz
from build import ROOT,KIT,GAME

def prepare(output,seed):
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))[:16]
    reports=json.loads((ROOT/'source/investigation.json').read_text(encoding='utf-8'))
    rounds=json.loads((ROOT/'source/question_rounds.json').read_text(encoding='utf-8'))
    personalities=json.loads((ROOT/'source/playtest_personas.json').read_text(encoding='utf-8'))
    rng=random.Random(seed);animals=rng.sample(GAME['animals'],16);culprit=rng.randrange(16)
    orders=[]
    for _ in rounds:
        order=list(range(16));rng.shuffle(order);orders.append(order)
    attendance='\n'.join(c['name']+' / '+c['role'] for c in chars)
    output.mkdir(parents=True,exist_ok=True)
    for i,c in enumerate(chars):
        dest=output/f'player-{i+1:02d}';dest.mkdir(exist_ok=True)
        with fitz.open(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf') as d:
            (dest/'identity.txt').write_text(f'{c["name"]}\n{personalities[i]}\nSimulated memorized animal: {animals[i]}. Returned immediately to CLOSED box; no kept slip.\nATTENDING:\n{attendance}\n',encoding='utf-8')
            with fitz.open(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf') as pre:
                arrival=pre[0].get_text()+'\nPRIVATE BRIEFING\n'+d[2].get_text()
            (dest/'01-arrival.txt').write_text(arrival,encoding='utf-8')
            discoveries=json.loads((ROOT/'source/discoveries.json').read_text(encoding='utf-8'))
            (dest/'hunt.txt').write_text(d[3].get_text()+'\nSHARED FINDS\n'+json.dumps(discoveries,ensure_ascii=False,indent=2),encoding='utf-8')
            for ri,rd in enumerate(rounds):
                text=''
                if ri==0:text=f'HOST: Selected animal {animals[culprit]}. Selected animal {animals[culprit]}. Keep the comparison private.\n'
                ids={'motive':['F1','F2'],'opportunity':['F3'],'method':['F4','F5']}[rd['key']]
                text+='\nPUBLIC REPORTS\n'+'\n\n'.join(x['id']+' '+x['text'] for x in reports if x['id'] in ids)
                pages=GAME['packet_pages'][rd['key']+'_questions']+[GAME['packet_pages'][rd['key']+'_answer']]
                text+='\nYOUR PAGES\n'+'\n'.join(d[p-1].get_text() for p in pages)
                text+='\nCANONICAL PUBLIC TABLE READ (not live dialogue)\n'
                for pos,j in enumerate(orders[ri]):
                    guest=chars[j];asker=chars[orders[ri][pos-1]]
                    group=next(g for g in rd['groups'] if guest['name'] in g['targets'])
                    branch='murderer' if j==culprit else 'innocent'
                    key={'motive':'motive_'+branch,'opportunity':'where_'+branch,'method':'evidence_'+branch}[rd['key']]
                    speech=guest['hearing'][key]
                    text+=f'\n{asker["name"]} asks {guest["name"]}: {group["question"]}\n{guest["name"]}: {speech}\n'
                (dest/f'{ri+2:02d}-{rd["key"]}.txt').write_text(text,encoding='utf-8')
            (dest/'05-ballot.txt').write_text(d[GAME['packet_pages']['ballot']-1].get_text(),encoding='utf-8')
            for pn in [1,GAME['packet_pages']['opportunity_answer'],GAME['packet_pages']['method_answer'],GAME['packet_pages']['ballot']]:
                d[pn-1].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(dest/f'packet-page-{pn:02d}.png')
        if i==0:
            for name in ['01_Facilitator_Guide_SPOILER_SAFE.pdf','12_Attendance_and_Hearing_Roster.pdf']:
                with fitz.open(KIT/'OPEN_FREELY'/name) as host:
                    (dest/(Path(name).stem+'.txt')).write_text('\n'.join(p.get_text() for p in host),encoding='utf-8')
    data={'TEST_DATA_ONLY':True,'seed':seed,'attending':[c['name'] for c in chars],'culprit':chars[culprit]['name'],'synthetic_animal_assignments':dict(zip((c['name'] for c in chars),animals)),'selected_animal':animals[culprit],'orders':orders,'ending_withheld':True,'human_playtest':False}
    (output/'ORGANIZER_ONLY_DO_NOT_SHARE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Created sixteen isolated current-kit fixtures. No agents were run. Keep organizer file private.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'build/playtest');parser.add_argument('--seed',type=int,default=163071)
    args=parser.parse_args();prepare(args.output,args.seed)
