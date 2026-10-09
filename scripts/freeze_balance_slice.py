"""Freeze a matched 15-role, no-hunt diagnostic. Never changes production."""
from pathlib import Path
import hashlib
import json
import random
import sys
import yaml
from compile_connected_story import compile_bank

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'docs/connected-story-01-SPOILERS'
OLD = ROOT / 'docs/baseline-improvement-02-SPOILERS'
OUT = LAB / 'balance-slice-01'
if OUT.exists():
    raise SystemExit('Refusing to overwrite a selected or tested trial.')
available = compile_bank('all')['characters']
ids = [str(r['id']).zfill(2) for r in available]
current = compile_bank(','.join(ids))
public = yaml.safe_load((ROOT / 'source/character_copy.yaml').read_text(encoding='utf-8'))
people = {str(r['id']).zfill(2): r for r in public['characters']}
old_bank = yaml.safe_load((OLD / 'investigation_copy.yaml').read_text(encoding='utf-8'))
old_rows = {str(r['id']).zfill(2): r for r in old_bank['characters']}
new_rows = {str(r['id']).zfill(2): r for r in current['characters']}
old_evidence = yaml.safe_load((OLD / 'evidence_design.yaml').read_text(encoding='utf-8'))
old_questions = json.loads((OLD / 'question_rounds.json').read_text(encoding='utf-8'))
contracts = yaml.safe_load((LAB / 'evidence-contracts.yaml').read_text(encoding='utf-8'))
groups = [yaml.safe_load((LAB / f).read_text(encoding='utf-8')) for f in
          ('three-role-scenes.yaml', 'replacement-primary-scenes.yaml',
           'production-family-scenes.yaml', 'collection-scenes.yaml')]
killer = random.SystemRandom().choice(ids)
OUT.mkdir()
(OUT / 'frozen-source').mkdir()
sources = [LAB / f for f in ('five-role-bank.yaml','production-family-scenes.yaml','collection-scenes.yaml',
    'attendance-edits.yaml','evidence-contracts.yaml','evidence-stage-map.yaml','story-ledger.yaml')]
sources += [OLD / f for f in ('investigation_copy.yaml','evidence_design.yaml','question_rounds.json')]
sources += [ROOT / 'source/character_copy.yaml']
for i, path in enumerate(sources):
    (OUT / 'frozen-source' / f'{i:02}_{path.name}').write_bytes(path.read_bytes())

visible = {'department','title','text','rows','paragraphs','annotation','timeline',
           'photography_note','photo_contract','document_label'}
def shown(report):
    data = {k:v for k,v in report.items() if k in visible}
    if report.get('trace_exhibit'):
        data['trace_exhibit'] = {k:v for k,v in report['trace_exhibit'].items() if k in ('title','text')}
    return json.dumps(data,ensure_ascii=False,indent=2)

initial = '\n\n'.join(shown(r) for r in old_evidence['reports'] if r['id'] in ('F1','F2'))
new_ii = '\n\n'.join([
    'SERVICE MANAGER\n'+contracts['ordinary_manager_record'],
    'GALA COORDINATOR\n'+contracts['coordinator_note'],
    'LABORATORY: Cyanide was found in Grant\'s individual glass. None was detected in the shared punch or food.',
    'CATERING ORDER: Private toast booked separately. Additional cheese course ordered but payment not approved. The accounts invoice puts that added charge on hold.',
    'RUNNING ORDER: Public acceptance announcement withheld. Private hospitality remains booked. Grant\'s family requested a quiet private place.',
    'PRODUCTION DRAFT: Donor Collapse cue alongside the toast. Artist credit removed; performance rejected.',
    'SECURITY: Donor asked for no live monitor of the private room. Gala log lists a camera fault. The technician disconnected the camera.',
    'COLLECTION PAPERS: Bowl ownership disputed; old and corrected label wording retained. Earlier press copies held. Bottle press entry repeats inert display liquid. Founding policy memo removed from display papers.',
])
new_iii = '\n\n'.join([
    'ORIGINAL INTAKE SHEET: Contents described as inert display liquid, supplied by Grant. Public exhibition approval withheld; closed preview may proceed. No opening or handling.',
    'PREVIEW PHOTOGRAPH: The recognizable Velvet Widow bottle is physically present on its support during the closed preview. This is one ordinary wide image.',
    'CONSERVATION SHEET: New closure band applied and checked before preview. Material: red foil-backed paper. Retained unused stock shows its red face and silver backing. Separate rear close-up shows a hidden split. A scrap from Grant\'s glass is similar shared stock; no unique torn-edge match is established.',
    'PURCHASE FILE: Executed condition requires original contents to remain in the Velvet Widow bottle. '+contracts['seller_statement'],
    'LABORATORY COMPARISON\n'+json.dumps(contracts['ingredient_results'],ensure_ascii=False),
    'DIRECTOR NOTE AND BOARD COPY: No accepted gift or public announcement without board approval. We will forgo the gift if these terms are not approved.',
    'LEGAL MARKUP: Do not publicly celebrate this unsigned agreement as an accepted gift. This objection does not cancel ordinary private hospitality.',
    'PROPOSED SUCCESSION CLAUSE: Upon the donor\'s death, the donor appointment shall pass to Tess Tament. This clause becomes effective only upon acceptance by the museum board. Family note asks counsel whether that can be a family appointment while Grant is alive.',
    'PERFORMANCE DELIVERY: The prerecorded studio film shows an empty jacket falling out of a gilded chair. Production booking lists screen/playback only. Grant\'s reply: No live stunt involving me or any guest. I am not falling at dinner. Submit the screen version; that is the only version under discussion. The film itself was subsequently rejected too.',
    'CAMERA WORK ORDER: Remove power adapter for donor privacy; restore after private meeting. Approved: Barb Dwyer. Technician: I removed power, not the network cable. Without power the camera cannot save recordings. Labeled photograph shows unplugged power adapter and still-attached network lead.',
    'EXHIBITION CATALOG PROOF, DATED BEFORE GALA: Bottle working entry quotes Original contents to remain in the bottle. Art\'s query quotes that condition and asks how it fits the inert loan description. Reed\'s marked press proof strikes that sentence; the short handout retains only the inert description. Full working copy and purchase attachment remain. Separate bowl correction withdraws settled ownership and keeps the missing-document warning.',
    'POLICY FILE: Original founding shortcut accepts lender descriptions before complete papers. Later policy withdraws that shortcut. Both are retained. Staff tested Anya\'s retained old spare: it opens the present preparation cupboard. Other staff keys also permit access; locked storage does not prove uninterrupted inaccessibility.',
    'PETITION AND BOWL CARD: Robin\'s retained rectangular card is the disputed bowl ownership label. Petition demands an intact return through claimants\' representatives and a hearing.',
    'ORIGINAL PRESS RECORDING OPENING\n'+'\n'.join(current['pre_method_press_interview_opening']),
])

intro = 'Exactly one of these fifteen guests committed the murder alone. Other mentioned people are business contacts or nonplaying staff, not additional suspects.\n\n'
intro += '\n\n'.join(people[i]['name']+' / '+people[i]['role']+'\n'+people[i]['introduction'] for i in ids)

def question_for(group, phase, ident):
    q = group['questions'][phase]
    if isinstance(q,str): return q
    if phase=='opportunity' and ident=='05': return group['questions']['opportunity_chip']['text']
    return q['text']

def speeches(which,phase,key):
    lines=[]
    if which=='old':
        round_ = next(r for r in old_questions if r['key']==phase)
        for g in round_['groups']:
            names=[name for name in g['targets'] if name in {people[i]['name'] for i in ids}]
            if not names:continue
            lines += ['Question for '+', '.join(names)+': '+g['question']]
            for name in names:
                ident=next(i for i in ids if people[i]['name']==name)
                branch='murderer' if ident==killer else 'innocent'
                lines += [name+'\n'+old_rows[ident]['hearings'][key+'_'+branch]]
    else:
        for group in groups:
            assignments={}
            for row in group['characters']:
                ident=str(row['id']).zfill(2)
                if ident in ids:assignments.setdefault(question_for(group,phase,ident),[]).append(ident)
            for question, targets in assignments.items():
                lines += ['Question for '+', '.join(people[i]['name'] for i in targets)+': '+question]
                for ident in targets:
                    branch='murderer' if ident==killer else 'innocent'
                    lines += [people[ident]['name']+'\n'+new_rows[ident]['hearings'][key+'_'+branch]]
    return '\n\n'.join(lines)

for which in ('old','new'):
    folder=OUT/which
    folder.mkdir()
    stages={1:intro,2:initial,3:speeches(which,'motive','motive'),
            4:'\n\n'.join(shown(r) for r in old_evidence['reports'] if r['id']=='F3') if which=='old' else new_ii,
            5:speeches(which,'opportunity','where'),
            6:'\n\n'.join(shown(r) for r in old_evidence['reports'] if r['id'] in ('F4','F5')) if which=='old' else new_iii,
            7:speeches(which,'method','evidence')}
    for n,content in stages.items():
        (folder/f'checkpoint_{n:02}.txt').write_text(content+'\n',encoding='utf-8')

manifest={'killer_id':killer,'cast':[{'id':i,'name':people[i]['name']} for i in ids],
    'selection':'Single uniform random draw from the fifteen complete routes, shared between versions; no reselection.',
    'scope':'Matched fifteen-role, seven-stage diagnostic; hunt omitted in both; text/intended image observations, not rendered kit.',
    'comparison_limits':'One independent reader per version; cast is not all thirty or confirmed twenty-two. Initial exhibits identical. Later authored evidence/prompt sets differ as part of revision. Offcast old references remain business/background contacts. Not a controlled population estimate or full-game validation.',
    'sha256':{str(f.relative_to(OUT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in OUT.rglob('*') if f.is_file()}}
(OUT/'private-selection.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Frozen two seven-stage inputs with the same fifteen roles and one hidden uniform selection. Identity not printed.')
