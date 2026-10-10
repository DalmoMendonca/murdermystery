"""Belle uses the cast's existing public design without joining the mystery cast."""
from pathlib import Path
import shutil,fitz
import build as b
from after_hours_print import poster
from printable_v2 import tents

def create_public(data,kit,downloads):
    folder=kit/'OPEN_FREELY/Belle_Tament';folder.mkdir(parents=True,exist_ok=True)
    stage=b.WORK/'belle-public';stage.mkdir(parents=True,exist_ok=True)
    portraits=b.ROOT/'assets/portraits/31_Belle_Tament'
    c={'name':data['name'],'slug':'Belle_Tament_Character_Sheet','role':data['role'],
       'portrait_path':portraits/'van_gogh.png','chibi_path':portraits/'chibi.png',
       'card_name':{'first_middle':'Belle','last':'Tament'},
       'preparty':{'description':data['backstory'],
                   'relationships':data['preparty_relationships'],
                   'acting':data['acting_tips'],'costume':data['costume_suggestions']}}
    original=b.KIT
    try:
        b.KIT=stage
        poster([c],b,output_dir=stage,merged_path=stage/'merged.pdf')
        public=stage/'Belle_Tament_Character_Sheet.pdf'
        shutil.copy2(public,folder/public.name)
        doc=fitz.open(public);page=doc[0]
        page.get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).pil_save(str(folder/'Belle_Tament_Character_Sheet.jpg'),format='JPEG',quality=95)
        doc.close()
        poster([c],b,print_mode=True,output_dir=stage/'print',merged_path=stage/'print-merged.pdf')
        shutil.copy2(stage/'print/Belle_Tament_Character_Sheet.pdf',folder/'Belle_Tament_Character_Sheet_PRINT.pdf')
        tents([c],b)
        shutil.copy2(stage/'OPEN_FREELY/09_Host_Safe_Name_Cards.pdf',folder/'Belle_Tament_Tent_Card.pdf')
    finally:b.KIT=original
    for file in folder.iterdir():shutil.copy2(file,downloads/file.name)
    return folder
