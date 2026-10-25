"""Verify user-requested layout edits without changing any mystery branch."""
from pathlib import Path
import sys,json,re,yaml,fitz
from printable_v2 import BEST_PRACTICES
from american_copy import american
from public_lock import verify_public_lock
ROOT=Path(__file__).resolve().parents[1];RUN=ROOT/'docs/playtest'/sys.argv[1]
KIT=Path((RUN/'candidate-kit-path.txt').read_text().strip())
norm=lambda s:re.sub(r'\s+','',american(s)).replace('’',"'")
branches=0;packets=0
voices={r['id']:r for r in yaml.safe_load((ROOT/'source/connected_release/voice-story-bible.yaml').read_text(encoding='utf-8'))['characters']}
for edition,file in [('all','03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf'),('confirmed','03A_Confirmed_22_Guest_Packets_PRINT_DO_NOT_READ.pdf')]:
    bank=yaml.safe_load((ROOT/f'source/connected_release/{edition}.yaml').read_text(encoding='utf-8'))
    with fitz.open(KIT/'PRINT_WITHOUT_READING'/file) as doc:
        assert len(doc)==len(bank['characters'])*12
        for index,c in enumerate(bank['characters']):
            pages=list(doc)[index*12:index*12+12];text=[p.get_text() for p in pages];packets+=1
            for key,page in [('motive',5),('where',7),('evidence',9)]:
                for branch in ['innocent','murderer']:
                    assert norm(c['hearings'][key+'_'+branch]) in norm(text[page]),(c['name'],key,branch);branches+=1
            for branch in ['innocent','murderer']:
                assert norm(c['coming_clean'][branch]) in norm(text[11]);branches+=1
            assert 'Tips for a Successful Dinner' in text[2] and "What's at Stake" in text[2] and 'Best Practices' in text[2]
            assert norm(voices[c['id']]['private_stake']) in norm(text[2])
            assert all(norm(tip) in norm(text[2]) for tip in BEST_PRACTICES)
            assert 'Behind the portrait' not in text[2] and 'Conversations to start' not in text[2]
            assert 'The Game is Afoot' in text[3]
            for page in [4,6,8]:assert 'Questions for the Room' in text[page]
            for page in [5,7,9]:assert 'Your Answer' in text[page]
            ballot=text[10];assert ballot.startswith('BALLOT') and ballot.count(c['name'])==1
            assert all(label in ballot for label in ['I accuse...','Because...','Best Actor','Best Costume'])
            assert not any(old in ballot for old in ['Your ballot','Your character name','ACCUSATIONS','STOP!'])
            boxes=[d for d in pages[10].get_drawings() if d['rect'].width>200 and d['rect'].y0>=200 and d['rect'].y1<=630]
            assert len(boxes)==4,(c['name'],'ballot box count',len(boxes))
verify_public_lock(ROOT)
report={'packets_checked':packets,'unchanged_spoken_branches':branches,'ballot_boxes':4,'required_tips':6,'public_asset_lock':True}
(RUN/'packet-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
