"""One flat ZIP containing all thirty public character images and one invite."""
from pathlib import Path
import io,zipfile,shutil
import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def export():
    public=ROOT/'site/downloads/current/The_Last_Acquisition_Complete_Kit/OPEN_FREELY'
    characters=sorted((public/'PreParty_Individual').glob('*.jpg'))
    assert len(characters)==30
    with fitz.open(public/'06_Invitation_and_Arrival_Guide.pdf') as doc:
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
    print(f'31 images, no folders or extra files: {target}')
    return target
if __name__=='__main__':export()
