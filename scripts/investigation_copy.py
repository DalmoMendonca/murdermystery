"""Canonical private testimony; public character copy is independently locked."""
import yaml,re
HEARING_KEYS={base+'_'+branch for base in ['motive','where','evidence'] for branch in ['innocent','murderer']}
def apply_investigation(characters,root):
    data=yaml.safe_load((root/'source/investigation_copy.yaml').read_text(encoding='utf-8'))
    assert data['schema_version']==2
    rows=data['characters'];by_id={c['id']:c for c in characters}
    assert len(rows)==len(by_id) and {r['id'] for r in rows}==set(by_id)
    for row in rows:
        c=by_id[row['id']];h=row['hearings'];proof=row['exclusion']
        assert set(h)==HEARING_KEYS and all(isinstance(v,str) and v.strip() for v in h.values())
        assert all(h[b+'_innocent']!=h[b+'_murderer'] for b in ['motive','evidence'])
        # Shared Opportunity facts keep ordinary activity from becoming a branch tell.
        c['private'].update(row['briefing'])
        c['hearing']=h.copy();c['testimony_clearance']=proof.copy();c['testimony_suspicion']=row['suspicion']
        for branch in ['innocent','murderer']:
            c['private']['final_'+branch]=row['coming_clean'][branch]
            c['private'][branch]=row['coming_clean'][branch]
        c['case_facts']={branch:derive_account(h,branch,proof) for branch in ['innocent','murderer']}
        trace=row.get('positive_trace')
        if trace:
            for branch in ['innocent','murderer']:
                c['case_facts'][branch]['source_glass_trace']=trace['anchor'] in h['evidence_'+branch]
                c['case_facts'][branch]['trace_argument']=trace['meaning']
    return characters

def derive_account(hearings,branch,proof):
    """Read start/completion claims from speeches, then apply the fixed crime windows.
    Assumes printed claims are factual. It does not authenticate a speaker's identity.
    """
    motive=hearings['motive_'+branch];method=hearings['evidence_'+branch]
    start_account=method if proof['family']=='first_admission' else motive
    starts=re.findall(r'6:(\d{2})',start_account);ends=re.findall(r'6:(\d{2})',method)
    if proof['family']=='contextual':
        claims=proof['claim_fragments']
        complete=all(x['text'] in hearings[x['round']+'_'+branch] for x in claims)
        return {'claimed_start':None,'claimed_end':None,'first_admission':False,
                'excluded_actions':[],'excluded_action':None,'proof_family':'contextual',
                'contextual_rebuttal_disclosed':complete,
                'inference':'Explains suspicious evidence without a complete alibi.'}
    if proof['family'] in ['route','guard','sequence']:
        # Bespoke wording must disclose every authored premise. This verifies
        # coverage only. An independent reader must assess the physical inference.
        claims=proof['claim_fragments']
        assert claims and {x['round'] for x in claims}=={'where','evidence'}
        complete=all(x['text'] in hearings[x['round']+'_'+branch] for x in claims)
        excluded=[proof['action']] if complete else []
        return {'claimed_start':None,'claimed_end':None,'first_admission':False,
                'excluded_actions':excluded,'excluded_action':excluded[0] if excluded else None,
                'inference':'Authored premise coverage; independent semantic review required.',
                'proof_family':proof['family']}
    if not starts and proof['family']=='continuous_activity':
        assert len(ends)>=2,('Start and completion facts missing in Method',branch)
        starts=[ends[0]];ends=ends[1:]
    assert starts,('Timed account missing its disclosed start',branch)
    start=int(starts[-1]);excluded=[]
    first_admission=bool(re.search(r'first entered|first time',start_account,re.I))
    if first_admission:
        end=None
        if start>=28:excluded.append('acquire_sample')
    else:
        assert ends,('Completion fact missing',branch)
        end=int(ends[0]);assert start<end,('Impossible work interval',start,end)
        for action,lo,hi in [('acquire_sample',20,28),('contaminate_coupe',40,44)]:
            if start<=lo and end>=hi:excluded.append(action)
    return {'claimed_start':start,'claimed_end':end,'first_admission':first_admission,'excluded_actions':excluded,'excluded_action':excluded[0] if excluded else None}
