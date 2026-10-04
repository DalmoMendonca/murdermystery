"""Printed book consistency; these checks do not measure human difficulty."""
import json,re,hashlib,zipfile
from collections import Counter
from PIL import Image
import fitz
from build import ROOT,KIT,SITE,GAME
norm=lambda t:re.sub(r'\s+','',t)
def printed(p):
    with fitz.open(p) as d:return '\n'.join(x.get_text() for x in d)
def load(name):return json.loads((ROOT/'source'/name).read_text(encoding='utf-8'))
def check():
    chars=load('characters.json');rounds=load('question_rounds.json');profiles=load('art_direction.json');hunt=load('hunt.json');case=load('case.json')
    assert len(chars)==30 and len({c['name'] for c in chars})==30
    names={c['name'] for c in chars};pixels=[]
    expected={'cover':1,'introduction':2,'background':3,'hunt':4,'motive_questions':[5],'motive_answer':6,'opportunity_questions':[7],'opportunity_answer':8,'method_questions':[9],'method_answer':10,'ballot':11,'coming_clean':12}
    assert GAME['packet_pages']==expected
    assert len(GAME['animals'])==len(set(GAME['animals']))==30
    assert {'ELEPHANT','LION','IGUANA'}<=set(GAME['animals'])
    assert {h['envelope'] for h in hunt['locations']}==set(range(1,17)) and len({h['location'] for h in hunt['locations']})==16
    assert set(hunt['characters'])=={c['slug'] for c in chars}
    hints=[h for hs in hunt['characters'].values() for h in hs]
    assert len(hints)==len({h['text'] for h in hints})==90
    coverage=Counter(h['envelope'] for h in hints)
    assert set(coverage)==set(range(1,17)) and set(coverage.values())<={5,6}
    assert {h['envelope'] for c in chars[:15] for h in hunt['characters'][c['slug']]}==set(range(1,17))
    for rd in rounds:
        assert len(rd['groups'])==10 and all(len(g['targets'])==3 for g in rd['groups'])
        targets=[n for g in rd['groups'] for n in g['targets']]
        assert len(targets)==len(set(targets))==30 and set(targets)==names
        for group in rd['groups']:
            key={'motive':'motive','opportunity':'where_innocent','method':'evidence_innocent'}[rd['key']]
            assert len({c['hearing'][key] for c in chars if c['name'] in group['targets']})==3
    phases={2:'INTRODUCTIONS',3:'INTRODUCTIONS',4:'HUNT FOR CLUES',5:'ACT I: MOTIVE',6:'ACT I: MOTIVE',7:'ACT II: OPPORTUNITY',8:'ACT II: OPPORTUNITY',9:'ACT III: METHOD',10:'ACT III: METHOD',11:'ACCUSATIONS',12:'COMING CLEAN'}
    for c,profile in zip(chars,profiles):
        assert c['name']==profile['name'] and 'age' not in c
        assert len(hunt['characters'][c['slug']])==len({h['envelope'] for h in hunt['characters'][c['slug']]})==3
        for style,a in profile['assets'].items():
            p=ROOT/a['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']
            with Image.open(p) as im:
                assert min(im.size)>=1024;pixels.append(hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest())
                if style=='chibi':
                    assert im.mode=='RGBA';alpha=im.getchannel('A');assert alpha.getextrema()[0]==0
                    assert sum(alpha.histogram()[:10])>im.width*im.height*.2
            ext='.webp' if style=='chibi' else '.jpg'
            with Image.open(KIT/'OPEN_FREELY/Portraits'/c['slug']/(style+ext)) as im:
                origin=str(im.getexif().get(270,'')) if style=='chibi' else im.info.get('comment',b'').decode()
                assert 'Origin:' in origin and not any(x in origin.lower() for x in ['poison','cabinet','linen','murderer'])
        with fitz.open(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf') as d:
            assert len(d)==12 and len(d[0].get_images())>=2
            assert not any(p.get_images() for p in list(d)[1:])
            texts=[p.get_text() for p in d];alltext='\n'.join(texts)
            assert norm('Murder Mystery Dinner Party 2026') in norm(texts[0]) and norm(c['name']) in norm(texts[0])
            assert not any(norm(c['private'][k]) in norm(texts[0]) for k in ['history','secret','final_murderer'])
            intro=texts[1]
            assert 'COSTUME' not in intro and 'YOUR INTRODUCTION' in intro and norm(c['introduction']) in norm(intro)
            for val in [c['preparty']['description'],c['preparty']['acting'],*c['preparty']['relationships']]:assert norm(val) in norm(intro),(c['name'],val)
            assert any(v.get('fill') and all(abs(v['fill'][i]-[1,240/255,153/255][i])<.01 for i in range(3)) for v in d[1].get_drawings()),c['name']
            spans=[s for b in d[1].get_text('dict')['blocks'] if 'lines' in b for line in b['lines'] for s in line['spans']]
            assert any('Bold' in s['font'] for s in spans)
            for page,phase in phases.items():assert phase in texts[page-1] and f'{page} of 12' in texts[page-1],(c['name'],page)
            for page in [3,4,6,8,10,11]:assert norm('STOP! Do not turn the page yet. Wait for the host to announce the next round.') in norm(texts[page-1])
            for h in hunt['characters'][c['slug']]:assert norm(h['text']) in norm(texts[3])
            for rd in rounds:
                qt=norm(texts[expected[rd['key']+'_questions'][0]-1])
                for g in rd['groups']:assert norm(g['question']) in qt and all(norm(n) in qt for n in g['targets'])
            for val in [c['private']['history'],c['private']['secret'],*c['hearing'].values()]:assert norm(val) in norm(alltext),(c['name'],val)
            assert c['hearing']['evidence_innocent']==c['hearing']['evidence_murderer']
            for branch in ['innocent','murderer']:assert norm(c['private']['final_'+branch]) in norm(texts[11])
            assert 'Your ballot' in texts[10] and 'COMING CLEAN' in texts[11] and 'give only the ballot' in texts[10]
            assert 'IF INNOCENT' in texts[7] and 'IF MURDERER' in texts[7]
            before='\n'.join(texts[:11]).lower()
            assert not any(x in before for x in ['i poisoned','i stole the toxin','you poisoned','you dampened','i dampened','i decided he would not'])
            assert norm(c['private']['final_murderer']) not in norm(before)
            assert 'investigation notes' not in before and 'preparation-record' not in before
        public=printed(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf')
        assert 'ACTING TIPS' in public and 'COSTUME SUGGESTIONS' in public and not re.search(r'Age\s+\d',public)
        assert 'WHAT YOU ALREADY KNOW' not in public and 'OPTIONAL QUIPS' not in public
        with Image.open(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.jpg') as im:assert im.size==(1224,1584)
    assert len(set(pixels))==90
    assert {c['name'] for c in chars if c['case_facts']['innocent']['false_alibi']}==set(case['innocent_false_alibis'])
    assert {c['name'] for c in chars if c['case_facts']['innocent']['fabricated_installation']}==set(case['innocent_fabricated_early_errands'])
    cases=0
    for killer in range(30):
        for present in [list(range(30)),sorted(set(range(15))|{killer}),[i for i in range(30) if i==killer or i%3!=killer%3],[i for i in range(30) if i==killer or i%2!=killer%2]]:
            rows={i:chars[i]['case_facts']['murderer' if i==killer else 'innocent'] for i in present}
            assert [i for i,f in rows.items() if f['false_alibi'] and f['fabricated_installation']]==[killer]
            assert all(f['access_to_setup_supplies'] for f in rows.values())
            if len(present)==30:
                assert sum(f['false_alibi'] for i,f in rows.items() if i!=killer)>=7
                assert sum(f['fabricated_installation'] for i,f in rows.items() if i!=killer)>=7
            assert chars[killer]['case_facts']['murderer']['actual_poisoning_interval']==case['poisoning_interval']
            cases+=1
    with fitz.open(KIT/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf') as d:
        assert len(d)==30
        for c,p in zip(chars,d):
            t=p.get_text();assert len(p.get_images())>=1 and 'Living Collection' not in t
            assert norm(t).count(norm(c['card_name']['first_middle']+' '+c['card_name']['last']))==2
            assert 'BASE / fold inward' in t and 'BASE / overlap and tape' in t
            assert p.rect.width==612 and p.rect.height==792
    guidepath=KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf'
    with fitz.open(guidepath) as d:assert len(d)==15
    guide=printed(guidepath)
    assert 'closed return box' in guide and 'top three' in guide and 'alphabetically' in guide
    for x in hunt['locations']:assert norm(x['location']) in norm(guide)
    obsolete=['kept animal slip','ANIMAL NOT CALLED','ANIMAL CALLED','continuous alibi','seating pair','seat-order','next seated','question catalog','Card A','Card B','FINALE envelope','selected receipt','optional bowl']
    allowed={'01_Facilitator_Guide_SPOILER_SAFE.pdf','10_Blind_Printing_and_Assembly.pdf','99_SPOILER_BIBLE_DO_NOT_OPEN.pdf'}
    for p in KIT.rglob('*.pdf'):
        t=printed(p)
        if p.name not in allowed:assert not any(re.search(r'\b'+re.escape(x)+r'\b',t,re.I) for x in obsolete),(p.name,'obsolete instruction')
        assert not any(x in t for x in ['Sterling Voss','Pryce','VOSS COLLECTION','â€'])
    for rel in ['PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','PRINT_WITHOUT_READING/03B_Sealed_Finales_PRINT_DO_NOT_READ.pdf','OPEN_FREELY/11_Questions_and_Notes.pdf','PRINT_WITHOUT_READING/Finale_Individual']:assert not (KIT/rel).exists(),rel
    for report in load('investigation.json'):assert norm(report['text']) in norm(printed(KIT/'PRINT_WITHOUT_READING/Reports'/(report['id']+'.pdf')))
    with fitz.open(KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf') as d:assert len(d)==8
    assert norm(GAME['address']) in norm(printed(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf'))
    for name in ['The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']:
        with zipfile.ZipFile(SITE/'downloads'/name) as z:assert not z.testzip() and not any(n.lower().endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
    (ROOT/'build/mechanics-check.json').write_text(json.dumps({'cases':cases,'shared_question_groups':30,'working_murderer_branches':30,'packet_pages':12,'unique_hunt_hints':90,'tent_sheets':30,'passed':True,'human_difficulty_test':False},indent=2),encoding='utf-8')
    print('Passed 30 twelve-page packets, 30 question groups, 90 unique hunt hints, 120 culprit/attendance cases, 30 two-sided tents and all report facts.')
