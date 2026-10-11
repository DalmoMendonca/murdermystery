"""Private one-page evidence proof, never a kit/public export."""
from pathlib import Path
import yaml
import fitz
import build as b
import evidence_design as design

def main():
    candidate=b.ROOT/'docs/story-pass-18-SPOILERS'
    report=next(r for r in yaml.safe_load((candidate/'evidence_design.yaml').read_text(encoding='utf-8'))['reports'] if r['id']=='F2')
    b.KIT=b.ROOT/'build/proof18'
    b.fonts()
    path=b.KIT/'Evidence_2_DRAFT.pdf'
    s=b.Sheet(path,report['title'])
    y=design.heading(s,report['title'],'EVIDENCE 2 / INITIAL FINDINGS',b)
    y=design.receiving(s,report,y,b)
    s.block(report['text'],42,y,528,18,bottom=724)
    s.footer('Private draft / The Meridian Museum / Evidence 2')
    s.save()
    with fitz.open(path) as pdf:
        assert len(pdf)==1
        pdf[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(b.KIT/'Evidence_2_DRAFT.png')
    print(str(path))

if __name__=='__main__':main()
