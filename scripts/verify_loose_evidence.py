"""Check every frozen fact survives layout consolidation in the proper act."""
from pathlib import Path
import sys,json,re,hashlib,yaml,fitz
from public_lock import verify_public_lock

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/sys.argv[1]
KIT=Path((RUN/'candidate-kit-path.txt').read_text().strip())
with fitz.open(KIT/'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf') as probe:
    editorial=len(probe)>3 and 'The Poison Bottle' in probe[3].get_text()
if editorial:
    import runpy
    runpy.run_path(str(ROOT/'scripts/verify_act3_editorial.py'),run_name='__main__')
    raise SystemExit(0)
load=lambda p:yaml.safe_load(p.read_text(encoding='utf-8'))
e=load(ROOT/'source/connected_release/playable-evidence.yaml')
def norm(s):return ''.join(c.lower() for c in str(s) if c.isalnum())
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
        assert len(d)==9
        texts={act:[] for act in ACTS.values()}
        for n,page in enumerate(d):
            text=page.get_text();act=next((a for a in texts if text.startswith(a)),None)
            assert act,(edition,n)
            assert 'The Last Acquisition /' not in text and label not in text
            texts[act].append(text)
        assert [len(x) for x in texts.values()]==[1,2,6]
        for release in e['releases']:
            text='\n'.join(texts[ACTS[release['key']]])
            for item in exhibits(e,release,edition=='confirmed'):
                if item['id']=='original_interview':item['paragraphs']=bank['pre_method_press_interview_opening']
                if item['id']=='gift_status':
                    # Repair source's accidental paragraph splits without changing its meaning.
                    item['paragraphs']=['Grant Larceny has died at the gala after his private toast.',
                        'The proposed gift remains unsigned and unaccepted.',
                        "The naming terms, donor control and director's resignation are proposals, not completed decisions."]
                if item['id']=='collection_working_proof':
                    # Four summary rows and a prose description are replaced by
                    # the actual proof, once. Check every equivalent fact on it.
                    clauses=['October 29, 2026 / Dr. Art E. Fact',
                        'Seller requires original contents. Lender calls contents inert.',
                        'Please clarify before opening.', 'INTAKE REPLY: Unresolved. Keep closed.',
                        'Reed DeLabel / PRESS MARKUP',
                        'Purchase condition requires original contents to remain.',
                        'STAFF COPY: full query and seller attachment retained',
                        'PRESS COPY: shortened inert caption']
                    for n,clause in enumerate(clauses):includes(text,clause,f'{edition}/proof/fact{n}')
                    proofpage=next(p for p in d if 'CATALOG / WORKING PROOF' in p.get_text())
                    deleted=proofpage.search_for('Purchase condition requires original contents to remain.')
                    assert len(deleted)==1
                    line=deleted[0]
                    assert any(x['rect'].width>300 and x['rect'].height<2 and line.y0<x['rect'].y0<line.y1 for x in proofpage.get_drawings()),'Deletion must be visibly crossed out'
                    top=proofpage.search_for('CATALOG / WORKING PROOF')[0].y0-1
                    bottom=proofpage.search_for('PRESS COPY: shortened inert caption')[0].y1+1
                    proof_spans=[s for block in proofpage.get_text('dict')['blocks'] if 'lines' in block for ln in block['lines'] for s in ln['spans'] if top<=s['bbox'][1] and s['bbox'][3]<=bottom]
                    assert proof_spans and min(s['size'] for s in proof_spans)>=14,'Proof text must remain at least 14pt'
                    item['rows']=item['rows'][4:];item['images']=[]
                for key,value in fields(item):includes(text,value,f'{edition}/{item["id"]}/{key}')
        assert 'SAINT FRANCIS HOSPITAL' in d[2].get_text() and 'Tulsa, Oklahoma' in d[2].get_text()

manifest=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
for name,sha in manifest['sha256'].items():assert hashlib.sha256((ROOT/'source/connected_release'/name).read_bytes()).hexdigest()==sha
verify_public_lock(ROOT)
report={'frozen_fact_checks':len(checks),'hunt_images':16,'staged_sheets':9,'act_sheet_counts':[1,2,6],'generic_loose_footers_removed':True,'frozen_source_and_public_lock_pass':True,'proof_description_replaced_by_actual_marked_proof':True,'checks':checks}
(RUN/'fact-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
