"""Match published print downloads against the reviewed local receipt."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,sys,urllib.request

root=Path(__file__).resolve().parents[1]
run=root/'docs/playtest'/sys.argv[1]
deploy=json.loads((run/'deploy-output.json').read_text(encoding='utf-8-sig'))
base=deploy['deploy_url'].rstrip('/')
expected=json.loads((run/'predeploy-receipt.json').read_text())['downloads']
names=['01_Host_Guide.pdf','02_Hunt_Clues.pdf','03_Staged_Evidence.pdf',
       '04_Guest_Packets_PRINT_WITHOUT_READING.pdf','05_Name_Tents_Current_22.pdf',
       '06_Animal_Draw_Cards.pdf','Print_Today_Current_22.zip',
       'The_Last_Acquisition_Complete_Kit.zip','The_Last_Acquisition_Source.zip']
def verify(name):
    url=base+'/downloads/'+name
    sha=hashlib.sha256();size=0
    request=urllib.request.Request(url,headers={'Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=120) as response:
        assert response.status==200
        for chunk in iter(lambda:response.read(1024*1024),b''):
            size+=len(chunk);sha.update(chunk)
    digest=sha.hexdigest()
    assert size==expected[name]['bytes'] and digest==expected[name]['sha256'],name
    return {'name':name,'url':url,'bytes':size,'sha256':digest,'matches_reviewed_file':True}
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(verify,names))
(run/'live-receipt.json').write_text(json.dumps({'deploy':deploy,'verified_downloads':rows},indent=2)+'\n')
print(json.dumps({'url':base,'verified_downloads':len(rows),'all_hashes_match':True}))
