from pathlib import Path
import json,yaml,fitz
import build as b
from public_lock import verify_public_lock
run=b.ROOT/'docs/playtest/2026-10-25-SURGICAL-RECOVERY-SPOILERS';source=run/'candidate-source'
out=Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\surgical-recovery')
b.WORK=b.ROOT/'build/2026-10-25-surgical-recovery';b.KIT=Path((run/'candidate-kit-path.txt').read_text().strip())
bank=yaml.safe_load((source/'confirmed.yaml').read_text(encoding='utf-8'))
from american_copy import american
norm=lambda s:''.join(c.lower() for c in american(s) if c.isalnum())
checked=0
for edition,label in [('all','03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf'),('confirmed','03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf')]:
 expected=yaml.safe_load((source/(edition+'.yaml')).read_text(encoding='utf-8'))
 with fitz.open(b.KIT/'PRINT_WITHOUT_READING'/label) as doc:
  assert len(doc)==12*len(expected['characters'])
  for n,c in enumerate(expected['characters']):
   for field,page in [('motive',5),('where',7),('evidence',9)]:
    text=norm(doc[n*12+page].get_text())
    for branch in ['innocent','murderer']:assert norm(c['hearings'][field+'_'+branch]) in text,(c['name'],field,branch);checked+=1
   for branch in ['innocent','murderer']:assert norm(c['coming_clean'][branch]) in norm(doc[n*12+11].get_text());checked+=1
assert checked==416
review=run/'renders';review.mkdir(exist_ok=True)
with fitz.open(out/'04_Guest_Packets_PRINT_WITHOUT_READING.pdf') as doc:
 for ident,page in [('02',9),('06',7),('11',9),('12',7),('27',7)]:
  n=next(i for i,c in enumerate(bank['characters']) if c['id']==ident);doc[n*12+page].get_pixmap(matrix=fitz.Matrix(1.1,1.1)).save(review/f'packet-{ident}-{page+1}.png')
oldbank=yaml.safe_load((b.ROOT/'docs/playtest/2026-10-25-FINAL-ARTIFACT-BLIND22-SPOILERS/frozen-source/confirmed.yaml').read_text(encoding='utf-8'));old={c['id']:c for c in oldbank['characters']}
before=sum(len(c['hearings'][f'evidence_{x}'].split()) for c in oldbank['characters'] for x in ['innocent','murderer']);after=sum(len(c['hearings'][f'evidence_{x}'].split()) for c in bank['characters'] for x in ['innocent','murderer'])
for c in bank['characters']:
 assert c['coming_clean']==old[c['id']]['coming_clean']
 for key in ['motive_innocent','motive_murderer','where_innocent']:assert c['hearings'][key]==old[c['id']]['hearings'][key]
verify_public_lock(b.ROOT)
report={'verified_spoken_branches':checked,'packets':52,'current_guest_packet_pages':264,'act_iii_pages':6,'motive_and_innocent_opportunity_accounts_unchanged':True,'all_confessions_unchanged':True,'method_words_before':before,'method_words_after':after,'method_words_reduction_percent':round(100*(before-after)/before,1),'root_release_and_public_assets_unchanged':True,'fresh_blind_retest':'pending; no improved score claimed'}
(run/'packet-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
