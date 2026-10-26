"""Build the isolated surgical candidate without promoting frozen release sources."""
from pathlib import Path
import copy,shutil,json,yaml,hashlib,re
import fitz
import build as b
from character_copy import load_characters
from printable_v2 import packets
from public_lock import verify_public_lock

run=b.ROOT/'docs/playtest/2026-10-25-SURGICAL-RECOVERY-03-SPOILERS';source=run/'candidate-source'
out=Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\surgical-recovery-03')
base=Path((b.ROOT/'docs/playtest/2026-10-25-ACT3-TWO-RECORD-SHEETS-SPOILERS/candidate-kit-path.txt').read_text().strip())
b.fonts();b.WORK=b.ROOT/'build/2026-10-25-surgical-recovery-03';b.KIT=b.WORK/'connected-release-kit'/base.name;b.CONNECTED_RELEASE=True
assert not b.KIT.exists(),'Candidate kit already exists; do not silently overwrite.'
shutil.copytree(base,b.KIT);(run/'candidate-kit-path.txt').write_text(str(b.KIT)+'\n')
chars={c['id']:c for c in load_characters()}
voices={r['id']:r for r in yaml.safe_load((source/'voice-story-bible.yaml').read_text(encoding='utf-8'))['characters']}
public={r['id']:r for r in yaml.safe_load((b.ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['characters']}
def cast(bank):
 result=[];attending={c['id'] for c in bank['characters']}
 for row in bank['characters']:
  c=copy.deepcopy(chars[row['id']]);v=voices[row['id']]
  for field in ['relationships','packet_relationships']:c['preparty'][field]=[r['text'] for r in public[c['id']].get(field,[]) if set(r['with'])<=attending]
  c['hearing']=row['hearings'];c['private'].update(history=v['private_stake'],secret=bank['player_briefing'],objectives=['Mingle using the relationships on your introduction page.','Keep your private branch readings for their announced rounds.'],final_innocent=row['coming_clean']['innocent'],final_murderer=row['coming_clean']['murderer']);result.append(c)
 return result
allbank=yaml.safe_load((source/'all.yaml').read_text(encoding='utf-8'));bank=yaml.safe_load((source/'confirmed.yaml').read_text(encoding='utf-8'))
packets(cast(allbank),b,allbank['question_rounds']);allpdf=b.KIT/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf';backup=b.WORK/'all-packets.pdf';shutil.copy2(allpdf,backup)
packets(cast(bank),b,bank['question_rounds']);allpdf.replace(b.KIT/'PRINT_WITHOUT_READING/03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf');shutil.copy2(backup,allpdf)
for label in ['ALL_30','CONFIRMED_22']:shutil.copy2(out/'03_Staged_Evidence.pdf',b.KIT/f'OPEN_FREELY/05_Staged_Evidence_{label}.pdf')
shutil.copy2(b.KIT/'PRINT_WITHOUT_READING/03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf',out/'04_Guest_Packets_PRINT_WITHOUT_READING.pdf')
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
oldbank=yaml.safe_load((b.ROOT/'source/connected_release/confirmed.yaml').read_text(encoding='utf-8'));old={c['id']:c for c in oldbank['characters']}
before=sum(len(c['hearings'][f'evidence_{x}'].split()) for c in oldbank['characters'] for x in ['innocent','murderer']);after=sum(len(c['hearings'][f'evidence_{x}'].split()) for c in bank['characters'] for x in ['innocent','murderer'])
for c in bank['characters']:
 assert c['coming_clean']==old[c['id']]['coming_clean']
 for key in ['motive_innocent','motive_murderer','where_innocent']:assert c['hearings'][key]==old[c['id']]['hearings'][key]
verify_public_lock(b.ROOT)
report={'verified_spoken_branches':checked,'packets':52,'current_guest_packet_pages':264,'act_iii_pages':6,'motive_and_innocent_opportunity_accounts_unchanged':True,'all_confessions_unchanged':True,'method_words_before':before,'method_words_after':after,'method_words_reduction_percent':round(100*(before-after)/before,1),'root_release_and_public_assets_unchanged':True,'fresh_blind_retest':'pending; no improved score claimed'}
(run/'packet-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
