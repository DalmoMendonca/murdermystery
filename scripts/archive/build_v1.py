#!/usr/bin/env python3
"""Build all printable assets and the downloadable ZIP from editable source.

The purpose of this pipeline is iteration, not pixel-perfect preservation of the first
ChatGPT-generated PDFs. Edit source/v1 first; this script regenerates individual and
combined PDFs, then assembles the complete kit under site/downloads.
"""
from pathlib import Path
import json, zipfile, html, shutil, re
from weasyprint import HTML
from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source' / 'v1'
SITE = ROOT / 'site'
WORK = ROOT / 'build'
KIT_ROOT = SITE / 'downloads' / 'current' / 'The_Last_Acquisition_Complete_Kit'

CSS = r'''
@page { size: Letter; margin: .58in; @bottom-right { content: "Page " counter(page); font: 8.5px Arial; color:#766f64; } }
*{box-sizing:border-box} body{font-family:Georgia,"Times New Roman",serif;color:#171512;font-size:10.5pt;line-height:1.36}
h1,h2,h3,.sans{font-family:Arial,Helvetica,sans-serif} h1{font-size:25pt;line-height:1.02;margin:0 0 4pt;letter-spacing:-.02em} h2{font-size:13pt;margin:17pt 0 6pt;border-bottom:1px solid #b8aa90;padding-bottom:3pt} h3{font-size:10.5pt;margin:12pt 0 4pt;text-transform:uppercase;letter-spacing:.08em;color:#705f45}
.kicker{font:700 7.5pt Arial;text-transform:uppercase;letter-spacing:.15em;color:#705f45;margin-bottom:8pt}.role{font:10pt Arial;color:#5f584e;margin-bottom:16pt}.rule{height:1px;background:#b8aa90;margin:12pt 0}.note{font:8.5pt Arial;color:#665f55}.card{border:1px solid #b8aa90;padding:11pt;margin:0 0 10pt;break-inside:avoid}.columns{display:grid;grid-template-columns:1fr 1fr;gap:16pt}.page{break-after:page}
pre{white-space:pre-wrap;font:10.3pt/1.38 Georgia,"Times New Roman",serif;margin:0}.namecard{display:inline-flex;width:47%;height:2.15in;border:1px solid #8f8068;margin:1%;padding:18pt;vertical-align:top;flex-direction:column;justify-content:center;break-inside:avoid}.namecard strong{font:20pt Arial}.namecard span{font:9pt Arial;color:#665f55;margin-top:6pt}.spoiler{border:2px solid #6f1f24;padding:10pt;color:#6f1f24;font:700 10pt Arial;text-transform:uppercase;letter-spacing:.08em}
'''

def html_doc(body, title='The Last Acquisition'):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'

def write_pdf(body, out, title='The Last Acquisition'):
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_doc(body,title), base_url=str(ROOT)).write_pdf(out)

def clean_source_for_display(text):
    # Source was recovered from v1 PDFs; remove repeated document title/page artifacts where present.
    lines=[]
    for line in text.replace('\f','\n').splitlines():
        s=line.strip()
        if not s: lines.append(''); continue
        if s == 'Treasures of the World': continue
        if s.startswith('The Meridian Museum of Art & World Cultures - Treasures of the World'): continue
        if re.fullmatch(r'Page \d+', s): continue
        lines.append(s)
    return '\n'.join(lines).strip()

def markdownish_body(text, kicker=None):
    text=clean_source_for_display(text)
    top=f'<div class="kicker">{html.escape(kicker)}</div>' if kicker else ''
    return top + '<pre>' + html.escape(text) + '</pre>'

def merge_pdfs(paths, out):
    w=PdfWriter()
    for p in paths: w.append(str(p))
    out.parent.mkdir(parents=True,exist_ok=True); w.write(str(out)); w.close()

def render_characters(chars):
    pre_paths=[]; sec_paths=[]
    pre_dir=KIT_ROOT/'OPEN_FREELY'/'PreParty_Individual'
    sec_dir=KIT_ROOT/'PRINT_WITHOUT_READING'/'Secret_Individual'
    for c in chars:
        pre_body=(f'<div class="kicker">Treasures of the World</div><h1>{html.escape(c["name"])}</h1>'
                  f'<div class="role">{html.escape(c["role"])} | Age {c["age"]}</div>'
                  f'<pre>{html.escape(clean_source_for_display(c["preparty_markdown"]))}</pre>')
        pp=pre_dir/f'{c["slug"]}.pdf'; write_pdf(pre_body, pp, c['name']); pre_paths.append(pp)
        sec_body=(f'<div class="spoiler">Party-night packet - keep private</div><h1 style="margin-top:14pt">{html.escape(c["name"])}</h1>'
                  f'<div class="role">{html.escape(c["role"])}</div>'
                  f'<pre>{html.escape(clean_source_for_display(c["secret_markdown"]))}</pre>')
        sp=sec_dir/f'{c["slug"]}_SECRET.pdf'; write_pdf(sec_body, sp, c['name']+' secret'); sec_paths.append(sp)
    merge_pdfs(pre_paths, KIT_ROOT/'OPEN_FREELY'/'02_PreParty_Character_Sheets_ALL.pdf')
    merge_pdfs(sec_paths, KIT_ROOT/'PRINT_WITHOUT_READING'/'03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf')

def load_doc(doc_key):
    single=SOURCE/f'{doc_key}.md'
    if single.exists():
        return single.read_text(encoding='utf-8')
    parts=sorted((SOURCE/doc_key).glob('*.md'))
    if not parts:
        raise FileNotFoundError(f'No source document found for {doc_key}')
    return '\n'.join(part.read_text(encoding='utf-8') for part in parts)

def render_doc(doc_key, out_rel, title, spoiler=False):
    text=load_doc(doc_key)
    prefix='<div class="spoiler">Spoiler material - do not read if you are playing</div>' if spoiler else '<div class="kicker">The Last Acquisition</div>'
    write_pdf(prefix+f'<h1>{html.escape(title)}</h1>'+markdownish_body(text), KIT_ROOT/out_rel, title)

def render_namecards(chars):
    cards=[]
    for c in chars:
        cards.append(f'<div class="namecard"><strong>{html.escape(c["name"])}</strong><span>{html.escape(c["role"])}</span></div>')
    write_pdf('<div class="kicker">Host-safe name cards</div><h1>Guest name cards</h1>'+''.join(cards), KIT_ROOT/'OPEN_FREELY'/'09_Host_Safe_Name_Cards.pdf','Name Cards')

def build_kit():
    if WORK.exists(): shutil.rmtree(WORK)
    if KIT_ROOT.parent.exists(): shutil.rmtree(KIT_ROOT.parent)
    KIT_ROOT.mkdir(parents=True, exist_ok=True)
    chars=[]
    for part in sorted((SOURCE/'characters').glob('*.json')):
        chars.extend(json.loads(part.read_text(encoding='utf-8')))
    render_characters(chars)
    render_doc('README','00_READ_ME_FIRST.pdf','Read Me First')
    render_doc('facilitator','OPEN_FREELY/01_Facilitator_Guide_SPOILER_SAFE.pdf','Facilitator Guide')
    render_doc('host_safe_props','OPEN_FREELY/04_Host_Safe_Props.pdf','Host-Safe Props')
    render_doc('invitation_arrival','OPEN_FREELY/06_Invitation_and_Arrival_Guide.pdf','Invitation & Arrival Guide')
    render_doc('exhibits_decor','OPEN_FREELY/07_Museum_Exhibits_and_Decor.pdf','Museum Exhibits & Decor')
    render_doc('awards_scoring','OPEN_FREELY/08_Awards_and_Scoring.pdf','Awards & Scoring')
    render_namecards(chars)
    render_doc('clues_forensics','PRINT_WITHOUT_READING/04B_Clues_and_Forensics_PRINT_DO_NOT_READ.pdf','Clues & Forensics',True)
    render_doc('evidence_cards','PRINT_WITHOUT_READING/05_Character_Evidence_Cards_PRINT_DO_NOT_READ.pdf','Character Evidence Cards',True)
    render_doc('spoiler_bible','SPOILERS_DO_NOT_OPEN/99_SPOILER_BIBLE_DO_NOT_OPEN.pdf','Spoiler Bible',True)
    (KIT_ROOT/'README.txt').write_text('The Last Acquisition - generated from editable repository source.\n',encoding='utf-8')

    zip_out=SITE/'downloads'/'The_Last_Acquisition_Complete_Kit.zip'
    with zipfile.ZipFile(zip_out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in KIT_ROOT.rglob('*'):
            if p.is_file(): z.write(p, Path('The_Last_Acquisition_Complete_Kit')/p.relative_to(KIT_ROOT))

    src_out=SITE/'downloads'/'The_Last_Acquisition_Source.zip'
    with zipfile.ZipFile(src_out,'w',zipfile.ZIP_DEFLATED) as z:
        for base in [ROOT/'source',ROOT/'docs',ROOT/'scripts',ROOT/'templates',ROOT/'site']:
            if not base.exists():
                continue
            for p in base.rglob('*'):
                if p.is_file() and 'downloads' not in p.parts:
                    z.write(p,p.relative_to(ROOT))
        for p in [ROOT/'README.md', ROOT/'CHANGELOG.md', ROOT/'requirements.txt', ROOT/'netlify.toml']:
            if p.exists(): z.write(p,p.relative_to(ROOT))
    return zip_out,src_out

if __name__=='__main__':
    a,b=build_kit(); print(a); print(b)
