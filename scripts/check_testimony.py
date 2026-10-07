"""Check authored constraints and release coverage; not a human difficulty test."""
import json,re,yaml
from pathlib import Path
from character_copy import load_characters,ROOT
from public_lock import verify_public_lock

def check_testimony():
    verify_public_lock(ROOT)
    chars=load_characters();data=yaml.safe_load((ROOT/'source/investigation_copy.yaml').read_text(encoding='utf-8'))
    design=yaml.safe_load((ROOT/'source/case_design.yaml').read_text(encoding='utf-8'))
    evidence=yaml.safe_load((ROOT/'source/evidence_design.yaml').read_text(encoding='utf-8'))
    reports={r['id']:r for r in evidence['reports']}
    assert not any(r.get('archive') for r in reports.values())
    actions={a['id']:a for a in design['crime']['necessary_actions']}
    assert set(actions)=={'acquire_sample','contaminate_coupe'}
    assert actions['acquire_sample']['interval']==[20,28] and actions['contaminate_coupe']['interval']==[32,44]
    all_words=[t for c in chars for t in c['hearing'].values()]
    endings=[c['private']['final_'+b] for c in chars for b in ['innocent','murderer']]
    assert len(all_words)==180
    for key in ['motive_innocent','motive_murderer','where_innocent','where_murderer','evidence_innocent','evidence_murderer']:
        assert len({c['hearing'][key] for c in chars})==30,('Repeated speech across characters',key)
    assert len(endings)==len(set(endings))==60
    audit=[]
    for c,row in zip(chars,data['characters']):
        assert c['id']==row['id']
        proof=row['exclusion'];assert proof['action'] in actions or (proof['family']=='contextual' and proof['action'] is None)
        assert proof['activity_premise'] in ' '.join(c['hearing'][k+'_innocent'] for k in ['motive','where','evidence'])
        # Physical restrictions may be delayed until Method for pacing.
        assert c['case_facts']['innocent']['excluded_actions']==([] if proof['family']=='contextual' else [proof['action']]),(c['name'],'Printed chronology does not establish designed exclusion')
        assert not c['case_facts']['murderer']['excluded_actions'],(c['name'],'Guilty chronology supplies a murder exclusion')
        innocent=' '.join(c['hearing'][b+'_innocent'] for b in ['motive','where','evidence']).casefold()
        guilty=' '.join(c['hearing'][b+'_murderer'] for b in ['motive','where','evidence']).casefold()
        missing=[a for a in proof['anchors'] if a.casefold() not in innocent]
        assert not missing,(c['name'],'missing claimed exclusion language',missing)
        assert not all(a.casefold() in guilty for a in proof['anchors']),(c['name'],'full exclusion wording in guilty account')
        for branch in ['innocent','murderer']:
            spoken=' '.join(c['hearing'][b+'_'+branch] for b in ['motive','where','evidence']).casefold()
            assert row['suspicion'].casefold() in spoken,(c['name'],'scandal not disclosed',branch)
            assert not re.search(r'\bi (?:poisoned|killed|murdered|took cyanide|coated his glass)\b',spoken),(c['name'],'premature confession')
        final=c['private']['final_murderer'].casefold()
        assert 'cyanide' in final and 'uncovered' in final and 'glass' in final,c['name']
        trace=row.get('positive_trace')
        if trace:
            assert trace['anchor'] in c['hearing']['evidence_murderer']
            assert trace['anchor'] not in ' '.join(c['hearing'][k+'_innocent'] for k in ['motive','where','evidence'])
        audit.append({'character':c['name'],'excluded_required_action':proof['action'],'argument':proof['explanation'],'references':actions[proof['action']]['facts'] if proof['action'] else ['F3','F5'],'assumption':'Printed account coverage is not an independent forensic proof or a measured suspicion score.'})
    active=set(yaml.safe_load((ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['active_character_ids'])
    # Enumerate every selected culprit under five attendance families. No all-subsets claim.
    cases=0
    for killer in chars:
        for present in [set(c['id'] for c in chars),active|{killer['id']},set(c['id'] for c in chars[:15])|{killer['id']},set(c['id'] for c in chars if int(c['id'])%2)|{killer['id']},set(c['id'] for c in chars if int(c['id'])%3)|{killer['id']}]:
            candidates=[]
            for c in chars:
                if c['id'] not in present:continue
                account=c['case_facts']['murderer' if c['id']==killer['id'] else 'innocent']
                if account['excluded_action'] is None:candidates.append(c['id'])
                else:assert account['excluded_action'] in actions
            residual={r['id'] for r in data['characters'] if r['exclusion']['family']=='contextual'}
            assert set(candidates)==({killer['id']}|residual)&present
            positive=[c['id'] for c in chars if c['id'] in present and c['case_facts']['murderer' if c['id']==killer['id'] else 'innocent'].get('source_glass_trace')]
            assert positive==[killer['id']];cases+=1
    report={'passed':True,'revision':design['revision'],'hearing_speeches':180,'coming_clean_speeches':60,'culprit_attendance_scenarios':cases,'confirmed_cast_size':len(active),'characters':audit,'human_or_blind_agent_playtest':False,'limitation':'Anchor and constraint checks validate the authored model. Independent reading and blind trials are needed for inference quality and difficulty.'}
    (ROOT/'build/testimony-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'Passed 180 speech boxes across all thirty roles, 60 endings and {cases} authored-world scenarios; independent inference review remains separate.')
    return cases
if __name__=='__main__':check_testimony()
