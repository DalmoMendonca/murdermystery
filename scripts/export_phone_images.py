"""One flat ZIP containing all thirty public character images and one invite."""
from pathlib import Path
import io,zipfile,json
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def export():
    public=ROOT/'site/downloads/current/The_Last_Acquisition_Complete_Kit/OPEN_FREELY'
    characters=sorted((public/'PreParty_Individual').glob('*.jpg'))
    assert len(characters)==30
    invite=ROOT/'build/phone-invite.pdf'
    with fitz.open(invite if invite.exists() else public/'06_Invitation_and_Arrival_Guide.pdf') as doc:
        pix=doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
        image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        buffer=io.BytesIO();image.save(buffer,'JPEG',quality=94,optimize=True)
    target=ROOT/'site/downloads/All_30_Characters_and_Invite.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('00_Invite.jpg',buffer.getvalue())
        for path in characters:
            with Image.open(path) as image:assert image.size==(1224,1584)
            archive.write(path,path.name)
    with zipfile.ZipFile(target) as archive:
        assert len(archive.namelist())==31 and archive.testzip() is None
        assert all('/' not in name and name.endswith('.jpg') for name in archive.namelist())
    phone=ROOT/'site/iphone';phone.mkdir(exist_ok=True)
    (phone/'Invite.jpg').write_bytes(buffer.getvalue())
    from character_copy import load_characters
    names={c['slug']:c['name'] for c in load_characters()}
    entries=[{'label':'Invitation','name':'Invite.jpg','url':'/iphone/Invite.jpg'}]
    for path in characters:
        entries.append({'label':names[path.stem],'name':path.name,'url':'/downloads/current/The_Last_Acquisition_Complete_Kit/OPEN_FREELY/PreParty_Individual/'+path.name})
    (phone/'images.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'31 images, no folders or extra files: {target}')
    return target
if __name__=='__main__':export()
