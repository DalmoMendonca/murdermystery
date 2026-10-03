"""Content and branch simulations for every eligible murderer and attendance pattern."""
import json,re,zipfile
import fitz
from build import ROOT,KIT,SITE,GAME
norm=lambda s: re.sub(r'\s+','',s)
def text(path):
    with fitz.open(path) as d:return '\n'.join(p.get_text() for p in d)
def check():
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    assert len(chars)==30 and len({c['name'] for c in chars})==30
    assert len(GAME['core_animals'])==len(GAME['optional_animals'])==15
    assert len(set(GAME['core_animals']+GAME['optional_animals']))==30
    assert {'ELEPHANT','LION','IGUANA'}<=set(GAME['core_animals'])
    oldnames=[a for a,b in json.loads((ROOT/'source/name_map.json').read_text(encoding='utf-8')) if ' ' in a]
    evidence=KIT/'PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf'
    with fitz.open(evidence) as doc:
        assert len(doc)==30
        for i,c in enumerate(chars):
            assert 'age' not in c
            private=text(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf')
            for value in list(c['hearing'].values())+[c['private']['history'],c['private']['secret']]:assert norm(value) in norm(private),(c['name'],value)
            if c['tier']=='CORE':assert norm(c['private']['murderer']) not in norm(private)
            for banned in ['I poisoned','you poisoned','you tipped','you killed']:assert banned.lower() not in private.lower(),(c['name'],banned)
            for row,letter in enumerate(['A','B']):
                card=norm(doc[i].get_text(clip=fitz.Rect(42,106+row*319,570,399+row*319)))
                assert norm(c['evidence'][letter]) in card,(c['name'],letter)
                assert norm(c['name']) in card and norm('Card '+letter) in card
            public=text(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf')
            assert not re.search(r'Age\s+\d',public) and 'ACTING TIPS' in public and 'COSTUME SUGGESTIONS' in public
            assert not any(a in private+public for a in oldnames)
            if c['tier']=='CORE':
                finale=text(KIT/'PRINT_WITHOUT_READING/Finale_Individual'/f'{c["slug"]}_FINALE.pdf')
                assert norm(c['private']['final_murderer']) in norm(finale)
    # Decode actual printed receipts, rather than merely trusting source flags.
    def receipt_facts(c,branch):
        value=c['evidence'][c['private'][branch+'_card']]
        assert value.startswith('MERIDIAN / SETUP RECEIPT')
        return ('no later entry' not in value,'no key loan' not in value,'white linen cloth, gold seam' in value)
    for c in chars:
        for branch in ['innocent','murderer']:
            facts=receipt_facts(c,branch)
            assert facts==tuple(c['case_facts'][branch][k] for k in ['salon','key','linen'])
            where=c['hearing']['where_'+branch];method=c['hearing']['evidence_'+branch]
            assert ('did not go back' not in where)==facts[0]
            assert ('did not borrow' not in where)==facts[1]
            assert ('white linen cloth with a gold seam' in method)==facts[2]
        assert sum(receipt_facts(c,'innocent'))<=2
    cases=0
    elimination=[]
    for killer in range(15):
        for present in [list(range(30)),list(range(15)),[i for i in range(30) if i==killer or i%3!=killer%3]]:
            rows={i:receipt_facts(chars[i],'murderer' if i==killer else 'innocent') for i in present}
            assert [i for i,f in rows.items() if all(f)]==[killer]
            if present==list(range(15)):
                counts=[sum(f[k] for f in rows.values()) for k in range(3)]
                pairs=[sum(f[a] and f[b] for f in rows.values()) for a,b in [(0,1),(0,2),(1,2)]]
                assert all(10<=n<=11 for n in counts),(killer,counts)
                assert all(5<=n<=6 for n in pairs),(killer,pairs)
                elimination.append({'killer':chars[killer]['name'],'single_clue_suspects':counts,'two_clue_suspects':pairs,'combined_suspects':1})
            cases+=1
    catalog=text(KIT/'OPEN_FREELY/11_Questions_and_Notes.pdf')
    for c in chars:
        for q in c['questions'].values():assert norm(q) in norm(catalog)
    guide=text(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf')
    assert 'memorize' in guide.lower() and 'closed return box' in guide
    assert len(fitz.open(KIT/'OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf'))==15
    forbidden=['kept animal slip','Check your kept','ANIMAL NOT CALLED','ANIMAL CALLED','continuous alibi','SALON INCIDENT RECORD','I dispute the service','Listen for the fictional','guests during the party are not evidence','â€']
    invitation=text(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf');assert norm(GAME['address']) in norm(invitation)
    for pdf in KIT.rglob('*.pdf'):
        printed=text(pdf)
        assert not any(a in printed for a in oldnames),(pdf.name,'old full name')
        assert 'Pryce' not in printed and 'VOSS' not in printed,(pdf.name,'old partial name')
        assert not any(x.lower() in printed.lower() for x in forbidden),(pdf.name,'obsolete mechanic or encoding')
    for name in ['The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']:
        with zipfile.ZipFile(SITE/'downloads'/name) as z:
            assert not z.testzip()
            assert not any(n.lower().endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
    (ROOT/'build/mechanics-check.json').write_text(json.dumps({'cases':cases,'elimination':elimination},indent=2),encoding='utf-8')
    print(f'Passed 30 safe packets, 60 neutral receipt cards, memorized animals, 15-page host guide, tailored questions, and {cases} three-strand simulations.')
if __name__=='__main__':check()
