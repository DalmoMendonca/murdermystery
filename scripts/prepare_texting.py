"""Pair public invitation/character JPEGs using a private, local guest roster."""
import argparse,hashlib,io,json,re,shutil,zipfile
from pathlib import Path
import fitz,yaml
from PIL import Image
from character_copy import load_characters,ROOT

def prepare(guests_path,output):
    guests=json.loads(guests_path.read_text(encoding='utf-8'))
    chars={c['name']:c for c in load_characters()}
    active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    assert len({g['character'] for g in guests})==len(guests), 'Duplicate character assignment'
    assert {chars[g['character']]['id'] for g in guests}==active, 'Guest assignments must match the active cast'
    kit=ROOT/'site/downloads/current/The_Last_Acquisition_Complete_Kit/OPEN_FREELY'
    with fitz.open(kit/'06_Invitation_and_Arrival_Guide.pdf') as doc:
        pix=doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
        image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        data=io.BytesIO();image.save(data,'JPEG',quality=94,optimize=True);invite=data.getvalue()
    output.mkdir(parents=True,exist_ok=True)
    manifest=[];messages=[];folders=set()
    for g in sorted(guests,key=lambda g:(g['first'],g['last'])):
        c=chars[g['character']]
        name=f"{g['first']} {g['last']} - {c['name']}"
        folder=re.sub(r'[<>:"/\\|?*]','',name).strip().rstrip('.')
        assert folder and folder not in folders;folders.add(folder)
        target=output/folder;target.mkdir(exist_ok=True)
        (target/'01_Invite.jpg').write_bytes(invite)
        poster=kit/'PreParty_Individual'/f'{c["slug"]}.jpg'
        with fitz.open(poster.with_suffix('.pdf')) as doc:
            assert len(doc)==1 and c['name'] in doc[0].get_text()
        shutil.copy2(poster,target/'02_Character.jpg')
        files=[]
        for filename in ['01_Invite.jpg','02_Character.jpg']:
            path=target/filename
            with Image.open(path) as image:assert image.size==(1224,1584)
            files.append({'file':filename,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        manifest.append({'guest':f"{g['first']} {g['last']}",'character':c['name'],'folder':folder,'files':files})
        messages.append(f"{name}\nHi {g['first']}! You're playing {c['name']} at our murder mystery dinner on Friday, October 30 at 6 PM. Here are your invitation and character sheet. Have fun with the costume!\n")
    (output/'Messages.txt').write_text('\n'.join(messages),encoding='utf-8')
    (output/'Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'READ_ME.txt').write_text('Open the folder named for your guest. Attach 01_Invite.jpg and 02_Character.jpg together in their text conversation. Optional copy-and-paste messages are in Messages.txt. These are public pre-party materials.\n',encoding='utf-8')
    archive=output.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(output.rglob('*')):
            if p.is_file():z.write(p,Path(output.name)/p.relative_to(output))
    with zipfile.ZipFile(archive) as z:assert len([n for n in z.namelist() if n.endswith('.jpg')])==len(guests)*2
    print(f'{len(guests)} guest folders / {len(guests)*2} images: {archive}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--guests',type=Path,required=True,help='Private JSON list: character, first, last')
    parser.add_argument('--out',type=Path,required=True,help='Local output folder outside the public site/repository')
    args=parser.parse_args()
    destination=args.out.resolve()
    assert not destination.is_relative_to(ROOT), 'Keep guest-named folders outside the public repository'
    prepare(args.guests,destination)
