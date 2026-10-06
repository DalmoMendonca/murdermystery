"""Editable organizer-only testimony; public character copy remains independent."""
import yaml

HEARING_KEYS={'motive_innocent','motive_murderer','where_innocent','where_murderer','evidence_innocent','evidence_murderer'}

def apply_investigation(characters,root):
    data=yaml.safe_load((root/'source/investigation_copy.yaml').read_text(encoding='utf-8'))
    assert data['schema_version']==1
    rows=data['characters'];by_id={c['id']:c for c in characters}
    assert len(rows)==len(by_id) and {r['id'] for r in rows}==set(by_id)
    for row in rows:
        c=by_id[row['id']];h=row['hearings']
        assert set(h)==HEARING_KEYS and all(isinstance(v,str) and v.strip() for v in h.values()),c['name']
        for base in ['motive','where','evidence']:
            assert h[base+'_innocent']!=h[base+'_murderer'],(c['name'],base,'identical branches')
        c['hearing']=h.copy();c['testimony_clearance']=row['clearance'].copy();c['testimony_suspicion']=row['suspicion']
        for branch in ['innocent','murderer']:
            c['private']['final_'+branch]=row['coming_clean'][branch]
            c['private'][branch]=row['coming_clean'][branch]
        c['case_facts']={
            'innocent':{'cleared_by':row['id'],'evidence_discovery':row['clearance']['discovery'],'actual_interval':[39,45]},
            'murderer':{'cleared_by':None,'actual_poisoning_interval':[40,44]}}
    return characters
