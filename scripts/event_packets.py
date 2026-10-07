"""Attendance-specific packets: replace only question pages; preserve all story facts."""
import json,yaml,fitz
from pathlib import Path

def build_event(chars,b):
    active=set(yaml.safe_load((b.ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    attendees=[c for c in chars if c['id'] in active];names={c['name'] for c in attendees}
    rounds=json.loads((b.ROOT/'source/question_rounds.json').read_text(encoding='utf-8'))
    from printable_v2 import questions
    combined=fitz.open()
    temporary=b.KIT/'PRINT_WITHOUT_READING/_event_question_work.pdf'
    for c in attendees:
        with fitz.open(b.KIT/'PRINT_WITHOUT_READING/Secret_Individual'/f'{c["slug"]}_SECRET.pdf') as master:
            event=fitz.open();event.insert_pdf(master)
            for rd,pn in zip(rounds,[5,7,9]):
                filtered=dict(rd);filtered['groups']=[dict(g,targets=[n for n in g['targets'] if n in names]) for g in rd['groups']]
                # Keep empty group spaces for stable two-column measures; omit their contents.
                s=b.Sheet(temporary,c['name']+' / attending guest questions');s.page=pn
                questions(s,c,filtered,b);s.save()
                with fitz.open(temporary) as q:
                    assert len(q)==1
                    event.delete_page(pn-1);event.insert_pdf(q,start_at=pn-1)
            assert len(event)==12
            combined.insert_pdf(event);event.close()
    dest=b.KIT/'PRINT_WITHOUT_READING'/f'03A_Confirmed_{len(attendees)}_Guest_Packets_PRINT_DO_NOT_READ.pdf'
    combined.save(dest,garbage=4,deflate=True,no_new_id=True);combined.close()
    assert temporary.resolve().is_relative_to(b.KIT.resolve());temporary.unlink()
    (b.WORK/'event-roster.json').write_text(json.dumps({'count':len(attendees),'characters':[c['name'] for c in attendees],'packet_file':str(dest.relative_to(b.KIT))},indent=2)+'\n',encoding='utf-8')
    return dest
