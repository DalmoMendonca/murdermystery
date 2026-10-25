from pathlib import Path
import sys,json,hashlib,html,re
import fitz,yaml
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from PIL import Image
import io

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'docs/playtest/2026-10-25-ACT3-ARTIFACTS-DRAFT-SPOILERS'
OUT=Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\act3-artifact-redesign')
OUT.mkdir(parents=True,exist_ok=True);RUN.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'scripts'));import build as b
b.fonts()
prior=json.loads((ROOT/'source/act3_editorial.json').read_text(encoding='utf-8'))
oldblocks={i['id']:i for p in prior['pages'] for i in p['blocks']}
bank=yaml.safe_load((ROOT/'source/connected_release/confirmed.yaml').read_text(encoding='utf-8'))
refs=lambda *ids:sorted({r for ident in ids for r in oldblocks[ident]['refs']})
data={
 'status':'Local editorial candidate; not promoted or blind-playtested.',
 'pages':[
  {'title':"Grant's Estate File",'groups':[
   {'id':'estate-video','kind':'video','source':'PRIVATE VIDEO / TRANSCRIPT EXCERPT','title':'For my executors',
    'paragraphs':[
     "If I die before this gift is settled, read the unsigned papers. Artie will lose my donation rather than accept it without a board vote.",
     "The family gets a board seat only if the gift is accepted. They already want the appointment while I am alive.",
     "Sue has stopped my public announcement. My private toast can go ahead.",
     "The bowl is off the market. The historic bottle stays on loan. Vincent will not let me print his painting. I can withhold his last payment.",
     "Dada, I rejected your live stunt. I asked for a film. I have rejected that too."
    ],'refs':refs('gift-record','family-and-claim','sales-records')+['production_originals/r1','production_originals/r2']},
   {'id':'announcement-slip','kind':'slip','source':'ANNOUNCEMENT DESK / RETAINED ORIGINAL','title':'Unsigned announcement withdrawn',
    'text':"Master: UNSIGNED / WITHDRAWN. Public copy held by coordinator. Separate private copy held by Grant.",'refs':['governing_papers/p0']},
   {'id':'accounts','kind':'ledger','source':'ACCOUNTS / RETURNED ITEMS','title':'Gala settlement attachments',
    'rows':[
     ['Elon: camera connection','Invoice REJECTED: connection not installed.'],
     ['Staff wages','Paid from restricted funds without approval.'],
     ['Gala fabric','Paid from another client\u2019s commission advance.'],
     ['Sculpture','Resin + metal powder. Label corrected; final payment reduced.'],
     ['Sculpture sample','Materials: bronze powder + gold leaf. Sealing paper: NONE.'],
     ['Family appraisal','Condition: INTACT. Comparison used: DAMAGED object.'],
     ['Sale endorsement','Withdrawal received BEFORE public announcement.'],
     ['School places','Workshop funds used. Paid weekend session CANCELED.']
    ],'refs':refs('materials-and-value','account-entries')+['collector_working_folder/r3']}
  ]},
  {'title':"The Registrar's Working File",'groups':[
   {'id':'purchase','kind':'receipt','source':'BOTTLE / RECEIVING COPY','title':'Purchase condition and loan caption',
    'text':"The purchase requires original contents, not an empty bottle or replica. Seller confirms contents retained; no cancellation or substitution received. Received before gala: closed bottle, dealer\u2019s note, complete seller terms. Loan caption: \u201cContents inert.\u201d",'refs':refs('purchase-summary')},
   {'id':'proof','kind':'proof','source':'OCTOBER 29, 2026 / STAFF PROOF','title':'Dr. Art E. Fact \u2192 Intake',
    'text':"Seller requires original contents. Lender calls contents inert. Please clarify before opening.",
    'reply':'Unresolved. Keep closed.',
    'strike':'Purchase condition requires original contents to remain.',
    'distribution':'OUTGOING COPIES / Staff: full query, seller attachment, restriction. Press: Reed DeLabel\u2019s marked caption.',
    'refs':refs('press-summary')},
   {'id':'dates','kind':'dates','source':'CLOSURE TREATMENT / RETAINED COPIES','title':'Red paper fitted across stopper',
    'rows':[['SIGNED ORIGINAL','October 30, 2026'],["CHIP\u2019S INSURANCE COPY",'October 29, 2026']],
    'refs':refs('seal-dates')},
   {'id':'collection-register','kind':'register','source':'COLLECTION OFFICE / FILE CHECKS','title':'Labels, claims and access',
    'rows':[
     ['Cupboard lock, after preview','Staff keys: OPEN. Founder\u2019s spare: OPEN.'],
     ['Bowl label correction','\u201cOwnership settled\u201d WITHDRAWN. Supporting papers missing.'],
     ['Ownership file','Claimants\u2019 letter + earlier acquisition advice. No ministry return order enclosed.'],
     ['Lender descriptions','Old rule: publish before supporting papers arrive. Revised rule: review papers first.'],
     ['Press correction','Correction concerns the former owner\u2019s name only. No claim of poison treatment.']
    ],'refs':refs('ownership-records','family-and-claim')+['collection_working_proof/r7','original_source/p1']}
  ]},
  {'title':'The Press Desk Originals','groups':[
   {'id':'recorder','kind':'transcript','source':'PAIGE TURNER / UNTRIMMED RECORDER','title':'The interview begins',
    'lines':bank['pre_method_press_interview_opening'],'refs':['original_interview/dialogue']},
   {'id':'studio','kind':'film','source':'PRODUCTION COPY / RECEIVED BEFORE GALA','title':'Donor Collapse: studio master',
    'text':'Original sound: \u201cJacket take\u201d \u2192 chair scrape \u2192 clatter. Picture and sound received together. Podcast master: same sequence. Teaser starts after \u201cJacket take.\u201d',
    'refs':refs('studio-audio')},
   {'id':'picture-receipt','kind':'receipt','source':'PICTURE EDITOR / CARD RECEIPT','title':'Original import retained',
    'text':'Copied complete card after preview, before returning it. Import: physical bottle on open stand; no toast photograph. Photographer\u2019s agency export supplied later.',
    'aside':'Agency correction: earlier gallery photo was commercial, supplied as news. Public podium visible; disputed purchase cropped out.',
    'refs':refs('photo-history','tour-and-photo')},
   {'id':'install','kind':'checklist','source':'INSTALLATION / COMPLETED CHANGES','title':'Final gallery copy',
    'rows':[
     ['Grant\u2019s place setting','Proposed transparent cover CANCELED on BOTH styling copies.'],
     ['Bottle stand','Proposed glass front NOT INSTALLED.'],
     ['Textile projection','Magnified stitches only.'],
     ['Alcove','Hanging load REMOVED; route CLOSED.']
    ],
    'note':'Docent: \u201cWe returned to the public cases. We never entered Grant\u2019s room or stopped at his place.\u201d',
    'refs':refs('gallery-plan')+['visitor_route/r0','visitor_route/p0','production_originals/r5']}
  ]}
 ]}
(RUN/'artifact-copy.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

INK=HexColor('#202426');RED=HexColor('#741f31');MUTED=HexColor('#596266');LINE=HexColor('#adb2b2');PALE=HexColor('#f1f2ef')
pdf=OUT/'ACT_III_Replacement_Artifacts.pdf'
c=canvas.Canvas(str(pdf),pagesize=(612,792),invariant=1)
c.setTitle('Act III: three replacement artifacts');c.setAuthor('The Last Acquisition')
def rect(x,y,w,h,fill=white,stroke=LINE):
 c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.6);c.rect(x,792-y-h,w,h,fill=1,stroke=1)
def text(s,x,y,w=516,size=16,font='Helvetica',color=INK,leading=None):
 markup=html.escape(s).replace('\n','<br/>')
 p=Paragraph(markup,ParagraphStyle('a',fontName=font,fontSize=size,leading=leading or size*1.2,textColor=color))
 _,h=p.wrap(w,10000);assert y+h<=756,(s[:35],y+h)
 p.drawOn(c,x,792-y-h);return y+h
def markup(s,x,y,w=516,size=16,font='Helvetica',color=INK,leading=None):
 p=Paragraph(s,ParagraphStyle('a',fontName=font,fontSize=size,leading=leading or size*1.2,textColor=color));_,h=p.wrap(w,10000)
 assert y+h<=756,(s[:35],y+h);p.drawOn(c,x,792-y-h);return y+h
def rule(y,x=42,w=528):
 c.setStrokeColor(LINE);c.setLineWidth(.7);c.line(x,792-y,x+w,792-y)
def label(s,y,x=48,w=516):return text(s,x,y,w,10,'Helvetica-Bold',MUTED)+5
def title(s,y,x=48,w=516,size=20):return text(s,x,y,w,size,'Helvetica-Bold',INK)+8
def pagehead(page):
 text('ACT III: METHOD',42,22,528,12,'Helvetica-Bold',RED)
 text(page['title'],42,45,528,25,'Helvetica-Bold',INK)
 rule(84)

# Estate: one private recording, followed by the actual slips, not a narrator's report.
p=data['pages'][0];pagehead(p);g=p['groups'][0]
y=label(g['source']+' / FOR MY EXECUTORS',101)
rect(42,y-2,528,230,PALE)
vy=y+12
for para in g['paragraphs']:
 vy=text(para,56,vy,500,16,'Helvetica',leading=19)+5
assert vy<y+229,('video overflow',vy,y)
y=y+241;g=p['groups'][1];y=label(g['source'],y);y=text(g['text'],48,y,516,15)+12
g=p['groups'][2];y=label(g['source'],y);y=title(g['title'],y,size=18)
for a,z in g['rows']:
 y0=y
 ya=text(a,48,y,180,14,'Helvetica-Bold');yz=text(z,242,y,322,15)
 y=max(ya,yz)+4;rule(y-2,48,516)
print('estate bottom',y);c.showPage()

# Collection file: receiving, correspondence, date slips, and register are separate originals.
p=data['pages'][1];pagehead(p);y=99
g=p['groups'][0];y=label(g['source'],y);y=text(g['text'],48,y,516,16)+12;rule(y);y+=13
g=p['groups'][1];y=label(g['source']+' / DR. ART E. FACT TO INTAKE',y)
y=text(g['text'],48,y,516,16)+7
y=markup('<b>Intake reply:</b> '+html.escape(g['reply']),48,y,516,16)+9
y=text(g['distribution'],48,y,516,13)+9
y=markup('<b>Press proof:</b> Contents inert. <strike color="#741f31">'+html.escape(g['strike'])+'</strike>',48,y,516,16)+15
g=p['groups'][2];y=label(g['source'],y);y=title(g['title'],y,size=17)
ends=[]
for x,(a,z) in zip([48,315],g['rows']):
 rect(x,y,249,63,PALE);e=text(a,x+10,y+8,230,11,'Helvetica-Bold');ends.append(text(z,x+10,e+5,230,19,'BookBold'))
y=y+75
g=p['groups'][3];y=label(g['source'],y)
for a,z in g['rows']:
 ya=text(a,48,y,165,14,'Helvetica-Bold');yz=text(z,225,y,339,15);y=max(ya,yz)+4;rule(y-2,48,516)
print('collection bottom',y);c.showPage()

# Press desk: literal spoken lines, original film frames, import receipt, installed plan.
p=data['pages'][2];pagehead(p);y=99;g=p['groups'][0]
y=label(g['source'],y)
for line in g['lines']:
 speaker,body=line.split(': ',1)
 # Names are speaker labels, not interpretive topic headings.
 y=markup('<b>'+html.escape(speaker)+':</b> '+html.escape(body),48,y,516,15,'Book',leading=17.5)+5
y+=7;g=p['groups'][1];y=label(g['source'],y)
with Image.open(ROOT/'assets/evidence/print-2026-10-24/studio_take.png') as im:
 # Crop viewport selects the existing studio-film row; no image content is altered.
 crop=im.crop((0,0,im.width,int(im.height*.49)));buf=io.BytesIO();crop.save(buf,format='JPEG',quality=94);buf.seek(0)
c.drawImage(ImageReader(buf),48,792-y-94,width=250,height=94,preserveAspectRatio=True,anchor='c')
end=text(g['text'],315,y,249,14)
y=max(y+94,end)+12
g=p['groups'][2];y=label(g['source'],y);y=text(g['text'],48,y,516,14)+6;y=text(g['aside'],48,y,516,14)+12
g=p['groups'][3];y=label(g['source'],y)
for a,z in g['rows']:
 ya=text(a,48,y,165,13,'Helvetica-Bold');yz=text(z,225,y,339,14);y=max(ya,yz)+5
y=text(g['note'],48,y+5,516,14)
print('press bottom',y);c.save()

# Preserve all three approved pages exactly, and the early staged releases.
basekit=Path((ROOT/'docs/playtest/2026-10-25-ACT3-TWO-RECORD-SHEETS-SPOILERS/candidate-kit-path.txt').read_text().strip())
with fitz.open(basekit/'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf') as old,fitz.open(pdf) as new:
 full=fitz.open();full.insert_pdf(old,from_page=3,to_page=4);full.insert_pdf(new);full.insert_pdf(old,from_page=7,to_page=7);full.save(OUT/'ACT_III_Evidence.pdf');full.close()
with fitz.open(OUT/'ACT_III_Evidence.pdf') as full,fitz.open(basekit/'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf') as old:
 assert len(full)==6
 for a,z in [(0,3),(1,4),(5,7)]:assert full[a].get_pixmap().samples==old[z].get_pixmap().samples
staged=fitz.open()
with fitz.open(basekit/'OPEN_FREELY/05_Staged_Evidence_CONFIRMED_22.pdf') as old:staged.insert_pdf(old,from_page=0,to_page=2)
with fitz.open(OUT/'ACT_III_Evidence.pdf') as full:staged.insert_pdf(full)
staged.save(OUT/'03_Staged_Evidence.pdf');staged.close()

# Every original source reference remains assigned; review actual wording separately.
original_refs={r for page in prior['pages'] for block in page['blocks']+page.get('results',[]) for r in block['refs']}
approved_refs={r for page in prior['pages'] if page['layout'] in ['bottle','toast','comparisons'] for block in page['blocks']+page.get('results',[]) for r in block['refs']}
mapped={r for page in data['pages'] for group in page['groups'] for r in group['refs']}
assert not original_refs-(approved_refs|mapped),sorted(original_refs-(approved_refs|mapped))
reviewdir=RUN/'renders';reviewdir.mkdir(exist_ok=True)
with fitz.open(pdf) as doc:
 counts=[]
 for i,page in enumerate(doc):
  content=page.get_text();assert '\ufffd' not in content;counts.append(len(content.split()))
  spans=[s for block in page.get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for s in line['spans']]
  assert all(0<=s['bbox'][0]<s['bbox'][2]<=612 and 0<=s['bbox'][1]<s['bbox'][3]<=760 for s in spans)
  page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(reviewdir/f'artifact-{i+1}.png')
manifest=json.loads((ROOT/'source/connected_release/manifest.json').read_text())
for name,digest in manifest['sha256'].items():assert hashlib.sha256((ROOT/'source/connected_release'/name).read_bytes()).hexdigest()==digest
from public_lock import verify_public_lock
verify_public_lock(ROOT)
report={'status':data['status'],'replacement_pages':3,'act_iii_pages':6,'word_counts':counts,'all_79_source_groups_mapped':len(original_refs)==79,'approved_three_pages_pixel_identical':True,'frozen_source_unchanged':True,'public_lock':True,'visual_review_complete':False,
 'provenance_change':'Grant estate video is a newly authored fictional carrier of existing facts. No recording timestamp, murder prediction, new alibi, cause of death or accusation added. Independent records retained for receipt, staff restriction and original media. Not blind-playtested.'}
(RUN/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report));print(OUT)





