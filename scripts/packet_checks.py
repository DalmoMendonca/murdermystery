"""Actual packet content, grouped questions, branch consistency and reveal safety."""
import json,re,hashlib,zipfile
from PIL import Image
import fitz
from build import ROOT,KIT,SITE,GAME
norm=lambda t:re.sub(r'\s+','',t)
def printed(p):
    with fitz.open(p) as d:return '\n'.join(x.get_text() for x in d)
def facts(record):return ('no later entry' not in record,'no key loan' not in record,'white linen cloth, gold seam' in record)
def check():
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'));rounds=json.loads((ROOT/'source/question_rounds.json').read_text(encoding='utf-8'));profiles=json.loads((ROOT/'source/art_direction.json').read_text(encoding='utf-8'))
    assert len(chars)==30 and len({x['name'] for x in chars})==30
    names={x['name'] for x in chars};pixels=[]
    assert len(GAME['animals'])==len(set(GAME['animals']))==30
    assert {'ELEPHANT','LION','IGUANA'}<=set(GAME['animals'])
    for rd in rounds:
        assert len(rd['groups'])==10 and all(len(g['targets'])==3 for g in rd['groups'])
        targets=[n for g in rd['groups'] for n in g['targets']]
        assert len(targets)==len(set(targets))==30 and set(targets)==names
        for group in rd['groups']:
            key={'motive':'motive','opportunity':'where_innocent','method':'evidence_innocent'}[rd['key']]
            assert len({c['hearing'][key] for c in chars if c['name'] in group['targets']})==3
    for c,profile in zip(chars,profiles):
        assert c['name']==profile['name'] and 'age' not in c
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
            assert len(d)==14 and len(d[0].get_images())==1 and not any(p.get_images() for p in list(d)[1:])
            texts=[p.get_text() for p in d];alltext='\n'.join(texts)
            for rd in rounds:
                indices=[p-1 for p in GAME['packet_pages'][rd['key']+'_questions']]
                qt=norm('\n'.join(texts[i] for i in indices))
                for g in rd['groups']:assert norm(g['question']) in qt and all(norm(n) in qt for n in g['targets'])
            for val in [c['private']['history'],c['private']['secret'],*c['hearing'].values()]:assert norm(val) in norm(alltext),(c['name'],val)
            for branch in ['innocent','murderer']:
                rec=c['preparation_record'][branch];f=facts(rec)
                assert f==tuple(c['case_facts'][branch][k] for k in ['salon','key','linen']),(c['name'],branch,rec)
                assert norm('\n'.join(rec.splitlines()[1:4])) in norm(texts[GAME['packet_pages']['method_answer']-1])
                assert norm(c['private']['final_'+branch]) in norm(texts[GAME['packet_pages']['coming_clean']-1])
                where=c['hearing']['where_'+branch];method=c['hearing']['evidence_'+branch]
                assert ('did not go back' not in where)==f[0]
                assert ('did not borrow' not in where)==f[1]
                assert ('white linen cloth with a gold seam' in method)==f[2]
            assert not all(facts(c['preparation_record']['innocent'])) and all(facts(c['preparation_record']['murderer']))
            assert 'Your ballot' in texts[12] and 'Coming Clean' in texts[13]
            grid='\n'.join(texts[1:3]);assert all(norm(n) in norm(grid) for n in names)
            assert 'including the three preparation-record lines' in texts[11]
            assert 'give only the ballot' in texts[12]
            before='\n'.join(texts[:13]).lower()
            assert not any(x in before for x in ['i poisoned','i stole the toxin','you poisoned','you dampened','i dampened','i decided he would not'])
            assert norm(c['private']['final_murderer']) not in norm(before)
        public=printed(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf')
        assert 'ACTING TIPS' in public and 'COSTUME SUGGESTIONS' in public and not re.search(r'Age\s+\d',public)
    assert len(set(pixels))==90
    cases=0
    for killer in range(30):
        for present in [list(range(30)),sorted(set(range(15))|{killer}),[i for i in range(30) if i==killer or i%3!=killer%3],[i for i in range(30) if i==killer or i%2!=killer%2]]:
            rows={i:facts(chars[i]['preparation_record']['murderer' if i==killer else 'innocent']) for i in present}
            assert [i for i,f in rows.items() if all(f)]==[killer]
            if len(present)==30:
                assert all(sum(f[j] for f in rows.values())>=10 for j in range(3))
                assert all(sum(f[a] and f[b] for f in rows.values())>=5 for a,b in [(0,1),(0,2),(1,2)])
            cases+=1
    with fitz.open(KIT/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf') as d:
        assert len(d)==8 and sum(len(p.get_images()) for p in d)==30
        t='\n'.join(p.get_text() for p in d);assert 'Living Collection' not in t
        for c in chars:assert norm(c['card_name']['first_middle']+'\n'+c['card_name']['last']) in norm(t)
    guide=printed(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf')
    assert len(fitz.open(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf'))==15
    assert 'closed return box' in guide and 'top three' in guide and 'alphabetically' in guide
    obsolete=['kept animal slip','ANIMAL NOT CALLED','ANIMAL CALLED','continuous alibi','seating pair','seat-order','next seated','question catalog','Card A','Card B','FINALE envelope','selected receipt','optional bowl']
    allowed={'01_Facilitator_Guide_SPOILER_SAFE.pdf','10_Blind_Printing_and_Assembly.pdf','99_SPOILER_BIBLE_DO_NOT_OPEN.pdf'}
    for p in KIT.rglob('*.pdf'):
        t=printed(p)
        if p.name not in allowed:assert not any(x.lower() in t.lower() for x in obsolete),(p.name,'obsolete instruction')
        assert not any(x in t for x in ['Sterling Voss','Pryce','VOSS COLLECTION','â€'])
    for rel in ['PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','PRINT_WITHOUT_READING/03B_Sealed_Finales_PRINT_DO_NOT_READ.pdf','OPEN_FREELY/11_Questions_and_Notes.pdf','PRINT_WITHOUT_READING/Finale_Individual']:assert not (KIT/rel).exists(),rel
    for report in json.loads((ROOT/'source/investigation.json').read_text(encoding='utf-8')):assert norm(report['text']) in norm(printed(KIT/'PRINT_WITHOUT_READING/Reports'/(report['id']+'.pdf')))
    assert len(fitz.open(KIT/'PRINT_WITHOUT_READING/Discovery_Props.pdf'))==8
    assert norm(GAME['address']) in norm(printed(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf'))
    for name in ['The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']:
        with zipfile.ZipFile(SITE/'downloads'/name) as z:assert not z.testzip() and not any(n.lower().endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
    (ROOT/'build/mechanics-check.json').write_text(json.dumps({'cases':cases,'shared_question_groups':30,'working_murderer_branches':30,'packet_pages':14,'passed':True},indent=2),encoding='utf-8')
    print('Passed 30 complete packets, 30 shared question groups, 30 Coming Clean branches, 120 culprit/attendance cases, 30 transparent avatars and all report facts.')
