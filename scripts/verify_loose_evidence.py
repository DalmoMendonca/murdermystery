"""Check every frozen fact survives layout consolidation in the proper act."""
from pathlib import Path
import sys,json,re,hashlib,yaml,fitz
from public_lock import verify_public_lock

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/sys.argv[1]
KIT=Path((RUN/'candidate-kit-path.txt').read_text().strip())
load=lambda p:yaml.safe_load(p.read_text(encoding='utf-8'))
e=load(ROOT/'source/connected_release/playable-evidence.yaml')
def norm(s):return re.sub(r'\s+','',s).replace('’',"'").replace('–','-').replace('—','-')
checks=[]
def includes(text,value,label):
    assert norm(str(value)) in norm(text),f'Missing printed fact: {label}: {value}'
    checks.append(label)
def fields(item):
    for key in ['title','department','stamp']:
        if item.get(key):yield key,item[key]
    for n,t in enumerate(item.get('paragraphs',[])):yield f'paragraph{n}',t
    for n,row in enumerate(item.get('rows',[])):
        for k,t in enumerate(row):yield f'row{n}/{k}',t
    for im in item.get('images',[]):yield im['id'],im['observation']

with fitz.open(KIT/'OPEN_FREELY/04_Scavenger_Discoveries.pdf') as d:
    assert len(d)==16
    for n,item in enumerate(e['hunt']):
        text=d[n].get_text();assert text.startswith(f'DISCOVERY {n+1:02}')
        assert d[n].get_images(),f'Discovery {n+1} missing artwork'
        assert 'The Last Acquisition /' not in text
        for key,value in fields(item):includes(text,value,f'hunt{n+1}/{key}')

from visible_evidence import exhibits
from loose_evidence import ACTS
for edition,label in [('confirmed','CONFIRMED_22'),('all','ALL_30')]:
    bank=load(ROOT/f'source/connected_release/{edition}.yaml')
    with fitz.open(KIT/f'OPEN_FREELY/05_Staged_Evidence_{label}.pdf') as d:
        assert len(d)==12
        texts={act:[] for act in ACTS.values()}
        for n,page in enumerate(d):
            text=page.get_text();act=next((a for a in texts if text.startswith(a)),None)
            assert act,(edition,n)
            assert 'The Last Acquisition /' not in text and label not in text
            texts[act].append(text)
        assert [len(x) for x in texts.values()]==[1,1,10]
        for release in e['releases']:
            text='\n'.join(texts[ACTS[release['key']]])
            for item in exhibits(e,release,edition=='confirmed'):
                if item['id']=='original_interview':item['paragraphs']=bank['pre_method_press_interview_opening']
                for key,value in fields(item):includes(text,value,f'{edition}/{item["id"]}/{key}')

manifest=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
for name,sha in manifest['sha256'].items():assert hashlib.sha256((ROOT/'source/connected_release'/name).read_bytes()).hexdigest()==sha
verify_public_lock(ROOT)
report={'frozen_fact_checks':len(checks),'hunt_images':16,'staged_sheets':12,'act_sheet_counts':[1,1,10],'generic_loose_footers_removed':True,'frozen_source_and_public_lock_pass':True,'checks':checks}
(RUN/'fact-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
