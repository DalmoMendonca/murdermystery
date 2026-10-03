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
    cases=0
    for killer in range(15):
        for present in [list(range(30)),list(range(15)),[i for i in range(30) if i==killer or i%3!=killer%3]]:
            submitted=[chars[i]['evidence'][chars[i]['private']['murderer_card' if i==killer else 'innocent_card']] for i in present]
            contradictions=[v for v in submitted if 'SALON INCIDENT RECORD' in v]
            assert len(contradictions)==1 and chars[killer]['name'] in contradictions[0]
            assert all('6:40' in v and '6:49' in v for v in submitted if 'SALON INCIDENT RECORD' not in v)
            cases+=1
    invitation=text(KIT/'OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf');assert norm(GAME['address']) in norm(invitation)
    for pdf in KIT.rglob('*.pdf'):
        printed=text(pdf)
        assert not any(a in printed for a in oldnames),(pdf.name,'old full name')
        assert 'Pryce' not in printed,(pdf.name,'old partial name')
    for name in ['The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']:
        with zipfile.ZipFile(SITE/'downloads'/name) as z:
            assert not z.testzip()
            assert not any(n.lower().endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
    print(f'Passed 30 safe play packets, 60 card placements, isolated finales, names/address/animals, and {cases} branch/attendance simulations.')
if __name__=='__main__':check()
