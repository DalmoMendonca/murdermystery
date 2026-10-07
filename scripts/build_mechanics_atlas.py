"""Organizer-only evidence flow and complete thirty-role branch atlas."""
from pathlib import Path
from xml.sax.saxutils import escape
import yaml,json,sys
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.colors import HexColor
import fitz
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import build
from character_copy import load_characters
build.fonts()
OUT=ROOT/'build/organizer';OUT.mkdir(parents=True,exist_ok=True)
PDF=OUT/'Game_Mechanics_2026_ORGANIZER_ONLY.pdf'
W,H=1224,792;INK='#242424';RED='#740c28';GOLD='#a78049';PALE='#faf7ef'
c=canvas.Canvas(str(PDF),pagesize=(W,H),invariant=1)
data=yaml.safe_load((ROOT/'source/investigation_copy.yaml').read_text(encoding='utf-8'))['characters']
evidence=yaml.safe_load((ROOT/'source/evidence_design.yaml').read_text(encoding='utf-8'))
case=yaml.safe_load((ROOT/'source/case_design.yaml').read_text(encoding='utf-8'))
names={x['id']:x['name'] for x in load_characters()}
active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
def text(t,x,y,w,size=16,font='Book',color=INK,draw=True):
 p=Paragraph(escape(t).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.22,textColor=HexColor(color)))
 _,h=p.wrap(w,2000)
 assert y+h<748,(t[:70],y,h)
 if draw:p.drawOn(c,x,H-y-h)
 return y+h

def rule(y):
 c.setStrokeColor(HexColor(GOLD));c.setLineWidth(.6);c.line(42,H-y,W-42,H-y)

def box(x,y,w,h):
 c.setFillColor(HexColor(PALE));c.setStrokeColor(HexColor(GOLD));c.rect(x,H-y-h,w,h,fill=1,stroke=1)

def head(title,sub,n):
 text('THE LAST ACQUISITION / ORGANIZER ONLY / SPOILERS',42,24,1100,14,'BookBold',RED)
 text(title,42,58,1140,30,'BookBold',RED);text(sub,42,103,1140,16)
 rule(136);rule(752)
 c.setFont('Book',12);c.drawString(42,27,'ORGANIZER ONLY / October 6, 2026');c.drawRightString(W-42,27,str(n)+' / 32')

head('The evening: what arrives, and when','Discoveries add context and suspicion. Official exhibits establish the crime facts before voting.',1)
stages=[('ARRIVAL','Introduce yourselves. Memorize and return your animal slip.','A separate matching bowl selects only an attending guest. The branch stays fixed all evening.'),('HUNT FOR CLUES','Find, read and display all sixteen envelopes. The host supplies missed finds.','13: acquisition receipt. 14: conservator objection. 16: private toast schedule. Other finds expose scandals.'),('ACT I: MOTIVE','Release Evidence 1 (gift terms) and 2 (empty acquired bottle). Everyone answers.','The takeover gives many guests motives. The bottle has been opened; this does not identify who opened it.'),('ACT II: OPPORTUNITY','Release Evidence 3: the caterer’s photos and signed handling record.','The glass is wrapped until 6:40, unattended until 6:44, then sealed and watched. Earlier visits do not prove poisoning.'),('ACT III: METHOD','Release Evidence 4 (bottle access and room plan) and 5 (lab and material records).','Bottle accessible 6:20–6:28. West return slot does not reach it. Received embossing begins 6:45. Punch and food are clear.'),('ACCUSATIONS','Discuss, submit ballots, tally and lock votes.','All necessary facts are available now. Nobody needs a confession to solve the case.'),('COMING CLEAN','Hear the top three suspects. If none confesses, call the selected animal.','Endings connect existing facts and resolve other scandals; they introduce no essential new evidence.')]
y=151
for title,action,meaning in stages:
 text(title,42,y,185,15,'BookBold',RED)
 a=text(action,242,y,410,16);z=text(meaning,680,y,500,16)
 y=max(a,z)+15;rule(y-7)
c.showPage()
head('How evidence turns an account into a deduction','Both actions are necessary. An innocent account rules out at least one; a murderer account leaves both possible.',2)
box(42,155,538,85);box(644,155,538,85)
text('TAKE THE POISON',60,167,500,20,'BookBold',RED);text('Preparation shelf / 6:20–6:28 / Evidence 2 + 4',60,203,500,17)
text('REACH INSIDE THE GLASS',662,167,500,20,'BookBold',RED);text('Donor Salon / 6:40–6:44 / Evidence 3 + 5',662,203,500,17)
text('AND',589,183,50,16,'BookBold',RED)
families=[('Continuous activity','A live, fixed or hands-occupied task covers an entire necessary window.','The murderer’s task finishes before, or begins after, that window.'),('First admission','The first entrance is after 6:28, when the bottle is already locked away.','The murderer enters earlier and can reach the shelf during the tour.'),('Physical route','A west-side paperwork exchange cannot reach the bottle through the wall.','The murderer enters the east visitor room, where the shelf is accessible.'),('Guarded glass','The only visit to the table ends while the blue plastic wrapping is intact.','The murderer sees an uncovered glass on a blue cloth placemat.'),('Document sequence','An original bears the raised RECEIVED mark first used at 6:45; the sole delivery is later.','The murderer delivers a red-pencil working copy before the cover is sealed.')]
y=263
text('ACCOUNT TYPE',42,y,195,14,'BookBold',RED);text('IF INNOCENT + EVIDENCE',260,y,440,14,'BookBold',RED);text('IF MURDERER + EVIDENCE',735,y,445,14,'BookBold',RED);y+=31
for title,i,g in families:
 text(title,42,y,195,17,'BookBold');a=text(i,260,y,440,17);z=text(g,735,y,445,17);y=max(a,z)+19;rule(y-9)
text('Reading rule: printed innocent facts are true. Lack of an exclusion alone is not proof of guilt in real life; this fictional case specifies one killer, no accomplice and no second poison source. Motives and unrelated wrongdoing create suspicion, not a murder verdict.',42,y+7,1140,16)
c.showPage()
maprows=[]
for index,ch in enumerate(data):
 title=names[ch['id']];p=ch['exclusion'];blocked='taking the poison' if p['action']=='acquire_sample' else 'reaching the inside of the glass'
 head(title+' / branch comparison',('CONFIRMED GUEST' if ch['id'] in active else 'RESERVE CHARACTER')+' / Read the three accounts together; do not judge a single answer in isolation.',index+3)
 y=151;text('IF INNOCENT',177,y,478,16,'BookBold',RED);text('IF MURDERER',705,y,477,16,'BookBold',RED);y+=29
 for key,label in [('motive','MOTIVE'),('where','OPPORTUNITY'),('evidence','METHOD')]:
  text(label,42,y,125,13,'BookBold',RED)
  a=text(ch['hearings'][key+'_innocent'],177,y,478,15)
  z=text(ch['hearings'][key+'_murderer'],705,y,477,15)
  y=max(a,z)+15;rule(y-7)
 refs='Evidence 2 + 4' if p['action']=='acquire_sample' else 'Evidence 3 + 5'
 y=text('WHY THE INNOCENT ACCOUNT EXCLUDES '+blocked.upper(),42,y+2,1140,16,'BookBold',RED)+9
 y=text(p['explanation']+' Apply '+refs+'.',42,y,1140,16)+10
 text('Suspicious admission in both branches: '+ch['suspicion']+'. The murderer account contains no complete exclusion of either required action.',42,y,1140,15)
 maprows.append({'id':ch['id'],'name':title,'confirmed':ch['id'] in active,'suspicion':ch['suspicion'],'excluded_action':p['action'],'evidence':refs,'reason':p['explanation'],'hearings':ch['hearings']})
 c.showPage()
c.save()
(OUT/'branch_map.json').write_text(json.dumps(maprows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with fitz.open(PDF) as d:
 for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1,1)).save(str(OUT/f'page-{i+1:02}.png'))
print('Built 32-page organizer flow and complete branch atlas:',PDF)
