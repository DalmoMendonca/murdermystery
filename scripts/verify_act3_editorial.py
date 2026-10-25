"""Audit edited evidence against source facts, printed copy and the prior kit."""
from pathlib import Path
import hashlib,json,sys
import fitz,yaml
from public_lock import verify_public_lock

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/sys.argv[1]
OLD=ROOT/'docs/playtest/2026-10-24-RECOVERED-PRINT-REFRESH-SPOILERS'
KIT=Path((RUN/'candidate-kit-path.txt').read_text().strip())
BASE=Path((OLD/'candidate-kit-path.txt').read_text().strip())
copy=json.loads((ROOT/'source/act3_editorial.json').read_text(encoding='utf-8'))
source=yaml.safe_load((ROOT/'source/connected_release/playable-evidence.yaml').read_text(encoding='utf-8'))
norm=lambda s:''.join(c.lower() for c in s if c.isalnum())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
atoms={}
for item in source['releases'][-1]['exhibits']:
    ident=item['id']
    for i,row in enumerate(item.get('rows',[])):atoms[f'{ident}/r{i}']=': '.join(row)
    for i,text in enumerate(item.get('paragraphs',[])):atoms[f'{ident}/p{i}']=text
    for image in item.get('images',[]):atoms[f'{ident}/i:{image["id"]}']=image['observation']
atoms['original_interview/dialogue']='Attendance-specific opening, checked against both frozen banks.'
mapped={key:[] for key in atoms}
for index,page in enumerate(copy['pages']):
    for block in page['blocks']+page.get('results',[]):
        for ref in block['refs']:
            assert ref in atoms,('Unknown source fact',ref)
            mapped[ref].append({'sheet':index+1,'block':block.get('id',block.get('sample')),'text':block.get('text',json.dumps(block,ensure_ascii=False))})
assert all(mapped.values()),('Unmapped source facts',[k for k,v in mapped.items() if not v])

new_pages=[];issues=[];word_counts={};rendered=0
for label in ['CONFIRMED_22','ALL_30']:
    relative=Path(f'OPEN_FREELY/05_Staged_Evidence_{label}.pdf')
    with fitz.open(KIT/relative) as doc,fitz.open(BASE/relative) as old:
        assert len(doc)==10
        for i in range(3):
            assert doc[i].get_pixmap().samples==old[i].get_pixmap().samples,('Early act changed',label,i)
        word_counts[label]={'before':sum(len(p.get_text().split()) for p in list(old)[3:]),'after':sum(len(p.get_text().split()) for p in list(doc)[3:])}
        for i,page in enumerate(doc):
            rendered+=1;text=page.get_text()
            assert text.strip() and '\ufffd' not in text,(label,i,'broken text')
            pix=page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False)
            out=RUN/'full-kit-review'/f'{label}-{i+1:02}.png';out.parent.mkdir(exist_ok=True);pix.save(str(out))
            if i>=3:
                item=copy['pages'][i-3]
                assert text.startswith('ACT III: METHOD') and norm(item['title']) in norm(text)
                for block in item['blocks']:
                    assert norm(block['text']) in norm(text),(label,block['id'],'missing edited copy')
                    assert '/' not in block['text'],('Slash shorthand',block['id'])
                spans=[s for block in page.get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for s in line['spans']]
                body=[s for s in spans if s['bbox'][1]>155 and 'Bold' not in s['font']]
                assert body and min(s['size'] for s in body)>=16,('Small body type',label,i)
                assert all(0<=s['bbox'][0]<s['bbox'][2]<=612 and 0<=s['bbox'][1]<s['bbox'][3]<=755 for s in spans),(label,i,'text outside page')
                if i==6:
                    rect=page.search_for('Purchase condition requires original contents to remain.')[0]
                    assert any(d['rect'].width>300 and d['rect'].height<2 and rect.y0<d['rect'].y0<rect.y1 for d in page.get_drawings()),'Press edit must remain visibly deleted'
                    assert all(date in text for date in ['October 30, 2026','October 29, 2026'])
            new_pages.append({'file':str(relative),'page':i+1,'image':str(out),'sha256':hashlib.sha256(pix.samples).hexdigest()})
        assert word_counts[label]['after']<word_counts[label]['before']

changed={Path(f'OPEN_FREELY/05_Staged_Evidence_{label}.pdf') for label in ['CONFIRMED_22','ALL_30']}
before={p.relative_to(BASE) for p in BASE.rglob('*.pdf')};after={p.relative_to(KIT) for p in KIT.rglob('*.pdf')}
assert before==after,('Unexpected PDF added/removed',before^after)
for relative in after-changed:assert sha(KIT/relative)==sha(BASE/relative),('Unrelated PDF changed',relative)
manifest=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
for name,expected in manifest['sha256'].items():assert sha(ROOT/'source/connected_release'/name)==expected
verify_public_lock(ROOT)
facts={'source_fact_groups':len(atoms),'frozen_fact_checks':len(atoms)*2,'act_sheet_counts':[1,2,7],
       'word_counts':word_counts,'unchanged_other_pdfs':len(after-changed),
       'early_act_pixels_identical':True,'source_and_public_lock_pass':True,
       'mapping_review':'Each source fact mapped to its edited wording. Semantic equivalence reviewed alongside the source; this coverage test is not a blind playtest.'}
(RUN/'fact-verification.json').write_text(json.dumps(facts,indent=2)+'\n')
(RUN/'semantic-audit.json').write_text(json.dumps({k:{'source':atoms[k],'rendered_in':mapped[k]} for k in atoms},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
report={'rendered_pages':rendered,'pdf_count':2,'scope':'Every page of the two edited evidence PDFs; all other PDFs byte-identical to reviewed baseline.',
        'issues':issues,'pages':new_pages,'visual_review_complete':False,'candidate':str(KIT)}
(RUN/'full-kit-review/report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(facts))
