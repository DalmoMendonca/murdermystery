"""Check every canonical private fact/branch and neutral evidence placement."""
import json,re,zipfile
import fitz
from build import ROOT,KIT,SITE
norm=lambda s: re.sub(r'\s+','',s)
def text(path):
    with fitz.open(path) as d:return '\n'.join(p.get_text() for p in d)
def check():
    chars=json.loads((ROOT/'source/characters.json').read_text(encoding='utf-8'))
    assert len(chars)==30 and len({c['name'] for c in chars})==30
    evidence=KIT/'PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf'
    with fitz.open(evidence) as doc:
        assert len(doc)==15
        for i,c in enumerate(chars):
            private=norm(text(KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf'))
            for key,value in c['private'].items():
                if key.endswith('_card'):continue
                for v in value if isinstance(value,list) else [value]:assert norm(v) in private,(c['name'],key)
            top=129+(i%2)*323
            for letter,x in [('A',42),('B',318)]:
                card=norm(doc[i//2].get_text(clip=fitz.Rect(x,top,x+252,top+272)))
                assert norm(c['evidence'][letter]) in card,(c['name'],letter)
                assert norm(c['name']) in card and norm('Card '+letter) in card
            public=text(KIT/'OPEN_FREELY/PreParty_Individual'/f'{c["slug"]}.pdf')
            assert all(norm(v) in norm(public) for v in [c['preparty']['description'],c['preparty']['acting'],c['preparty']['costume']]+c['preparty']['relationships'])
            assert 'ACTING TIPS' in public and 'COSTUME SUGGESTIONS' in public
    for name in ['The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']:
        with zipfile.ZipFile(SITE/'downloads'/name) as z:
            assert not z.testzip()
            assert not any(n.lower().endswith(('.ttf','.otf','.woff','.woff2')) for n in z.namelist())
    print('Content verified: 30 introductions, 60 private routes/final statements, 60 correctly placed A/B cards; ZIPs valid and no font files.')
if __name__=='__main__':check()
