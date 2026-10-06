"""Cross-check authored testimony against printed proof, clocks and attendance.

This verifies the elimination rule. It does not simulate or measure human guesses.
"""
import json,re,yaml
from pathlib import Path
from character_copy import load_characters,ROOT

def check_testimony():
    characters=load_characters();copy=yaml.safe_load((ROOT/'source/investigation_copy.yaml').read_text(encoding='utf-8'))
    docs=json.loads((ROOT/'source/discoveries.json').read_text(encoding='utf-8'))
    rows={r['id']:r for r in copy['characters']}
    speeches=[t for c in characters for t in c['hearing'].values()]
    assert len(speeches)==len(set(speeches))==180
    endings=[c['private']['final_'+b] for c in characters for b in ['innocent','murderer']]
    assert len(endings)==len(set(endings))==60
    catalog={d['number']:d for d in docs}
    assert len(catalog)==16 and not any(d.get('records') for d in docs)
    reports=json.loads((ROOT/'source/investigation.json').read_text(encoding='utf-8'))
    archive=next(r for r in reports if r['id']=='F4')['archive']
    sources={s for g in archive['groups'] for s in g['sources']}
    assert len(sources)==30
    audit=[]
    for c in characters:
        row=rows[c['id']];proof=row['clearance'];base={'motive':'motive','opportunity':'where','method':'evidence'}[proof['round']]
        text=c['hearing'][base+'_innocent']
        assert proof['anchor'].casefold() in text.casefold(),(c['name'],'clearing detail missing from designated innocent round')
        assert proof['report']=='F4' and proof['source'] in sources,c['name']
        stamps=proof['interval']
        assert archive['brass_interval' if proof['clock']=='BRASS' else 'security_interval']==f'6:{stamps[0]:02}–6:{stamps[1]:02}'
        offset=10 if proof['clock']=='BRASS' else 0
        start,end=stamps[0]-offset,stamps[1]-offset
        assert start<=40 and end>=44,(c['name'],'record does not cover contamination')
        # A murderer may mention the same prop, but must not assert its valid
        # complete alibi tuple. Read the full sentences in the semantic review.
        guilty=' '.join(c['hearing'][b+'_murderer'] for b in ['motive','where','evidence'])
        assert not (proof['anchor'].casefold() in guilty.casefold() and
                    all(f'6:{n:02}' in guilty for n in stamps[:2])),(c['name'],'complete clearing tuple leaked into guilty testimony')
        innocent=' '.join(c['hearing'][b+'_innocent'] for b in ['motive','where','evidence'])
        for b in ['innocent','murderer']:
            spoken=' '.join(c['hearing'][k+'_'+b] for k in ['motive','where','evidence'])
            assert row['suspicion'].casefold() in spoken.casefold(),(c['name'],'suspicious disclosure absent',b)
            assert not any(phrase in spoken.casefold() for phrase in ['i poisoned','i killed him','i wiped grant’s coupe','i took the toxin','i coated his coupe']),c['name']
        audit.append({'character':c['name'],'round':proof['round'],'report':'F4','source':proof['source'],'anchor':proof['anchor'],'record_interval_security':[start,end],'suspicion':row['suspicion'],'valid_innocent_clearance':True,'valid_murderer_clearance':False})
    active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    cases=0
    for killer in characters:
        attendance=[{c['id'] for c in characters},active|{killer['id']},
                    {c['id'] for c in characters[:15]}|{killer['id']},
                    {c['id'] for c in characters if int(c['id'])%2}|{killer['id']},
                    {c['id'] for c in characters if int(c['id'])%3}|{killer['id']}]
        for present in attendance:
            unresolved=[]
            for c in characters:
                if c['id'] not in present:continue
                facts=c['case_facts']['murderer' if c['id']==killer['id'] else 'innocent']
                if facts['cleared_by'] is None:unresolved.append(c['id'])
                else:
                    assert facts['cleared_by']==c['id'] and facts['evidence_report']=='F4'
                    assert facts['actual_interval'][0]<=40 and facts['actual_interval'][1]>=44
            assert unresolved==[killer['id']]
            cases+=1
    evidence={'revision':'three branched rounds','hearing_speeches':180,'coming_clean_speeches':60,'culprit_attendance_scenarios':cases,'confirmed_cast_size':len(active),'characters':audit,'passed':True,'human_or_blind_agent_playtest':False}
    (ROOT/'build/testimony-check.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Passed180distinct hearing speeches,60endings,30linked clearances and{cases}culprit/attendance scenarios including current{len(active)}guest cast.')
    return cases

if __name__=='__main__':check_testimony()
