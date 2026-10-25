"""Prepare only the real party's print jobs, preserving their reviewed PDFs."""
from pathlib import Path
import sys,json,zipfile,hashlib,shutil,fitz
from pypdf import PdfReader,PdfWriter
import yaml
from character_copy import load_characters

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-24-SHARED-PREVIEW-PRINT-SPOILERS')
KIT=Path((RUN/'candidate-kit-path.txt').read_text().strip())
OUT=KIT.parent/'Print_Today_Current_22';OUT.mkdir(exist_ok=True)
copy={
'01_Host_Guide.pdf':'OPEN_FREELY/01_Facilitator_Run_of_Show.pdf',
'02_Hunt_Clues.pdf':'OPEN_FREELY/04_Scavenger_Discoveries.pdf',
'03_Staged_Evidence.pdf':'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf',
'04_Guest_Packets_PRINT_WITHOUT_READING.pdf':'PRINT_WITHOUT_READING/03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf',
'06_Animal_Draw_Cards.pdf':'OPEN_FREELY/Animal_Draw_Cards.pdf',
}
for target,source in copy.items():shutil.copy2(KIT/source,OUT/target)
bank=yaml.safe_load((RUN/'candidate-source/confirmed.yaml').read_text(encoding='utf-8'))
active={c['id'] for c in bank['characters']};chars=load_characters()
source=PdfReader(KIT/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf');assert len(source.pages)==len(chars)==30
writer=PdfWriter()
for index,c in enumerate(chars):
    if c['id'] in active:writer.add_page(source.pages[index])
assert len(writer.pages)==22
with (OUT/'05_Name_Tents_Current_22.pdf').open('wb') as f:writer.write(f)
counts={p.name:len(fitz.open(p)) for p in OUT.glob('*.pdf')}
assert counts['04_Guest_Packets_PRINT_WITHOUT_READING.pdf']==264
evidence_sets=3
with fitz.open(OUT/'03_Staged_Evidence.pdf') as evidence_pdf:
    act_pages={act:[n+1 for n,p in enumerate(evidence_pdf) if p.get_text().startswith('ACT '+roman+': '+act)] for act,roman in [('MOTIVE','I'),('OPPORTUNITY','II'),('METHOD','III')]}
def span(numbers):
    assert numbers and numbers==list(range(numbers[0],numbers[-1]+1))
    return str(numbers[0]) if len(numbers)==1 else f'{numbers[0]}-{numbers[-1]}'
total=sum(counts.values())+(evidence_sets-1)*counts['03_Staged_Evidence.pdf']
canonical=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
same_source=all(hashlib.sha256((RUN/'candidate-source'/name).read_bytes()).hexdigest()==value for name,value in canonical['sha256'].items())
edition=canonical['revision'] if same_source else RUN.name
text=f'''THE LAST ACQUISITION / CURRENT22 PRINT JOBS

Edition: {edition}
Presentation: Five-sheet Act III / October 25, 2026
This bundle has only the real party's 22 adult suspects. Hugh, Tess and the
nonplaying child are excluded. Cary and Robin attend. Sent invitations and
character sheets have not changed. Do not mix packets or evidence from
another edition. Read RELEASE_NOTES.txt before printing.

PRINT SINGLE-SIDED, LETTER, ACTUAL SIZE / 100%.
Print 03_Staged_Evidence.pdf THREE TIMES, all other PDFs ONCE.
The six jobs total {total} sheets with three identical evidence sets.
The evidence is staged: cover later releases until the host calls for them.

01: Host guide. Read freely; follow its sequence and hiding-place list.
02: Hunt discoveries. One numbered discovery per corresponding envelope.
03: Matching 22-person evidence. Print THREE identical sets for three tables.
    In EACH set: PDF page {span(act_pages['MOTIVE'])} goes in ACT I: MOTIVE;
    pages {span(act_pages['OPPORTUNITY'])} in ACT II: OPPORTUNITY; pages {span(act_pages['METHOD'])} in ACT III: METHOD. Each sheet has its
    act at the top. You will have NINE folders: three per act, one per table.
    Keep folders locked/covered until that act. These are NOT hidden clues.
    Only job 02 goes into the sixteen hidden envelopes.
    At the host's interview-reading step, read Paige Interview followed by
    Robin Interview on the Record Comparisons sheet.
04: 264 private packet pages. DO NOT READ while printing. Keep the printed
    stack in order and divide it every 12 pages. Each packet begins with its
    character's framed portrait. Put the cover face-up at the assigned seat.
    Every packet already includes the ballot and Coming Clean page.
05: 22 foldable name tents, one whole sheet each. Fold, overlap, tape; no cut.
06: Animal draw cards. Each guest draws a different animal and memorizes it.
    Collect all DRAWN cards, mix those cards only, and select the murderer's
    animal. Unused cards must not enter that second draw. Do not match the
    cards to names. Never let guests keep a card after memorizing it.

Do not print the all-30 packet book or the separate duplicate ballots.
Use the current 22 edition even if an absent person's old invitation exists.

SHEETS BY JOB
'''+''.join(f'{name}: {count}\n' for name,count in sorted(counts.items()))+'\nPrint the staged evidence job 3 times; its count above is per set.\n'
(OUT/'PRINT_FIRST.txt').write_text(text,encoding='utf-8')
(OUT/'RELEASE_NOTES.txt').write_text('Reviewed playable current22 print release. One independent blind AI text reader per selected culprit:22/22 correct and earned, with no premature clear identification. Strict targets are still unmet:2/22 scenarios retain eight suspects above5 after ActII;13/22 retain three innocent alternatives at5-7 at the end. Scores are not human solve rates. No human rehearsal is claimed. Sent public assets are unchanged. Use one edition throughout.\n',encoding='utf-8')
receipt={'revision':edition,'adult_count':22,'single_sided_sheets':total,'evidence_copies':evidence_sets,'act_pdf_pages':act_pages,'pdf_pages':counts,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.pdf')},'source_status':canonical.get('release_decision','Candidate; see release notes.') if same_source else 'Unpromoted candidate'}
(OUT/'print-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
z=KIT.parent/'Print_Today_Current_22.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for p in sorted(OUT.iterdir()):archive.write(p,OUT.name+'/'+p.name)
receipt['zip_sha256']=hashlib.sha256(z.read_bytes()).hexdigest();receipt['zip_bytes']=z.stat().st_size
(RUN/'print-pack-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'path':str(z),'sheets':total,'zip_bytes':z.stat().st_size}))
