"""Compile the causal draft separately from production and frozen prior trials."""
from pathlib import Path
import json, yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/baseline-improvement-02-SPOILERS'
patch = yaml.safe_load((OUT/'shared-scene-edits.yaml').read_text(encoding='utf-8'))
story = yaml.safe_load((ROOT/'docs/baseline-improvement-01-SPOILERS/investigation_copy.yaml').read_text(encoding='utf-8'))
chip = next(r for r in story['characters'] if r['id']=='05')
for branch in ('innocent','murderer'):
    old=chip['hearings']['where_'+branch]
    new=old.replace("During the walkthrough I replaced the bottle's museum custody band", "Before the walkthrough I replaced the bottle's museum custody band")
    assert new != old
    chip['hearings']['where_'+branch]=new
    proof=chip['exclusion']
    if proof.get('activity_premise')==old:proof['activity_premise']=new
    for fragment in proof.get('claim_fragments',[]):
        if fragment['round']=='where' and fragment['text']==old:fragment['text']=new
repairs=yaml.safe_load((OUT/'method-repairs.yaml').read_text(encoding='utf-8'))
by_id={r['id']:r for r in story['characters']}
assert len(repairs['guilty_edits'])==30 and len({r['id'] for r in repairs['guilty_edits']})==30
for edit in repairs['innocent_edits']:
    row=by_id[edit['id']];old=row['hearings']['evidence_innocent'];new=edit['text'].strip()
    row['hearings']['evidence_innocent']=new
    proof=row['exclusion']
    proof['anchors']=[new if t==old else t for t in proof.get('anchors',[])]
    for fragment in proof.get('claim_fragments',[]):
        if fragment['round']=='evidence' and fragment['text']==old:fragment['text']=new
for edit in repairs['guilty_edits']:
    row=by_id[edit['id']];text=edit['text'].strip()
    row['hearings']['evidence_murderer']=text
    row['positive_trace']['anchor']=text
    row['positive_trace']['meaning']='Unexplained red foil-backed material in this guest\'s retained belongings is consistent with the glass scrap. Shared source/glass access comes from common evidence, not a guilty-only verbal itinerary. Material similarity is circumstantial and does not identify a unique source or prove handling. Independent inference remains unvalidated.'
for edit in repairs.get('ending_corrections', []):
    row = by_id[edit['id']]
    old = row['coming_clean']['murderer']
    assert old.count(edit['old']) == 1, edit['id']
    row['coming_clean']['murderer'] = old.replace(edit['old'], edit['new'])

evidence = yaml.safe_load((ROOT/'source/evidence_design.yaml').read_text(encoding='utf-8'))
for edit in patch['reports']:
    target=next(r for r in evidence['reports'] if r['id']==edit['id'])
    for key in ('text','rows','timeline'):
        if key in edit:target[key]=edit[key]
    if edit['id']=='F2':target['photo']='bottle_closed_incoming_replacement_required'
    if edit['id']=='F3':
        target['photo']='ordinary_gala_contact_sheet_replacement_required'
        target['photography_note']=edit['photography_note']
        target['photo_contract']=edit['photo_contract']
    if edit['id']=='F4':target['photo']='incoming_condition_document_replacement_required'
    if edit['id']=='F5':
        for row in target['rows']:
            if row[0]=='Acquired poison bottle':row[1]=edit['residue_table_wording']
        target['photo']='ordinary_gala_contact_sheet_replacement_required'
        target['trace_exhibit']['photo']='material_comparison_replacement_required'
for edit in patch['discoveries']:
    target=next(r for r in evidence['discoveries'] if r['number']==edit['number'])
    for key in ('department','title','stamp','rows','paragraphs','annotation'):
        if key in edit:target[key]=edit[key]
    if 'remove_photo' in edit:target.pop('photo',None)
    if 'remove_paragraph' in edit:
        assert edit['remove_paragraph'] in target['paragraphs']
        target['paragraphs'].remove(edit['remove_paragraph'])
for row in evidence.get('discovery_resolutions',[]):
    if row['number']==14:
        row['resolution']='Grant supplied an inert-liquid declaration contradicted by his original-contents purchase condition. Source-access timing is provided by Evidence 4, not this incoming record.'
        row['essential']=False
case=yaml.safe_load((ROOT/'source/case_design.yaml').read_text(encoding='utf-8'))
case['revision']='Shared-scene repair of published baseline; bounded editorial acceptance only'
case['status']='Causal and question-alignment review accepted; four retrospective corrections applied; no fresh score trial or final artwork'
case['crime']['necessary_actions'][0]['explanation']=patch['custody_scene']['staff_action']+' '+patch['custody_scene']['later_finding']
case['crime']['necessary_actions'][1]['explanation']='The manager set the glass at 6:32, returned to the kitchen, collected it at 6:44, poured at 6:46 and served the toast at 6:49. Photographs show isolated observations; they are not continuous surveillance.'
case['poison_backstory']['conflict']='Grant declared the contents inert to incoming-loan staff while privately requiring the seller to retain the original poison. Public display approval was withheld. No claim of potency rests on the antique label.'
case['custody_scene']=patch['custody_scene']
for name,data in (('investigation_copy.yaml',story),('evidence_design.yaml',evidence),('case_design.yaml',case)):
    (OUT/name).write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=105),encoding='utf-8')
assert (OUT/'question_rounds.json').exists(), 'Run align_packet_questions.py before compiling; retain candidate prompts separately.'
print('Compiled separate causal candidate; source and glass windows unchanged; no production PDF/art replacement.')
