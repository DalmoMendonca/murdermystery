"""Explicitly promote a tested published-baseline revision, retaining rollback sources."""
from pathlib import Path
import hashlib,json,shutil,yaml
from compile_connected_story import ROOT,LAB,compile_bank
from validate_playable_evidence import validate
from public_lock import verify_public_lock

def promote(rsvp_case):
    cases=[LAB/'balance-dramatic-30-03',LAB/rsvp_case]
    metrics=[m for case in cases for m in json.loads((case/'metrics.json').read_text(encoding='utf-8')).values()]
    assert len(metrics)==6
    assert all(m['correct_final_leader'] and m['final_culprit_score']>=9 and m['e3_culprit_score']>=5
               and not m['early_obvious_culprit'] and not m['early_large_lead'] for m in metrics)
    assert sum(m['act_ii_above_five']>= (10 if i<3 else 8) for i,m in enumerate(metrics))>=4,'Midpoint target coverage regressed'
    dest=ROOT/'source/connected_release'
    original=yaml.safe_load((dest/'all.yaml').read_text(encoding='utf-8'))
    baseline={r['id']:r for r in original['characters']}
    banks={active:compile_bank(active) for active in ('all','confirmed')}
    for row in banks['all']['characters']:
        for field in ('motive_innocent','where_innocent','evidence_innocent'):
            assert row['hearings'][field]==baseline[row['id']]['hearings'][field]
        assert row['coming_clean']==baseline[row['id']]['coming_clean']
    # Full-cast test need not be repeated for an unseen Al guilty-box change:
    # verify every delivered selected speech, question and opening is identical.
    for case,active in zip(cases,('all','confirmed')):
        manifest=json.loads((case/'private-selection.json').read_text(encoding='utf-8'))
        for relative,expected in manifest['sha256'].items():
            assert hashlib.sha256((case/relative).read_bytes()).hexdigest()==expected,relative
        frozen=yaml.safe_load((case/'frozen-source/compiled-bank.yaml').read_text(encoding='utf-8'))
        old={r['id']:r for r in frozen['characters']}
        current=banks[active]
        assert current['question_rounds']==frozen['question_rounds']
        assert current['pre_method_press_interview_opening']==frozen['pre_method_press_interview_opening']
        for row in current['characters']:
            branch='murderer' if row['id']==manifest['killer_id'] else 'innocent'
            for act in ('motive','where','evidence'):
                field=act+'_'+branch
                assert row['hearings'][field]==old[row['id']]['hearings'][field],(active,row['id'],field)
        assert (LAB/'playable-evidence.yaml').read_bytes()==(case/'frozen-source/playable-evidence.yaml').read_bytes()
    validate();verify_public_lock(ROOT)
    archive=LAB/'published-fallback-2026-10-10-source'
    if not archive.exists():shutil.copytree(dest,archive)
    # Preserve prior generated PDFs for image comparison; copying requires no
    # changes to the published site or to the immutable pre-party assets.
    oldkit=ROOT/'build/connected-release-kit/The_Last_Acquisition_Complete_Kit'
    review=ROOT/'build/revision03-before'
    if not review.exists():
        review.mkdir()
        for path in oldkit.rglob('*.pdf'):
            target=review/path.relative_to(oldkit);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    for active,label in [('all','all'),('confirmed','confirmed')]:
        banks[active]['status']='tested_published_baseline_revision03'
        (dest/(label+'.yaml')).write_text(yaml.safe_dump(banks[active],sort_keys=False,allow_unicode=True),encoding='utf-8')
    shutil.copy2(LAB/'playable-evidence.yaml',dest/'playable-evidence.yaml')
    record={'revision':'published-baseline-opportunity-2026-10-10',
            'baseline_tested_commit':'e29371c','tests':[str(p.relative_to(ROOT)) for p in cases],
            'limitations':'Two same-culprit text cases; not all30 worlds or human solve rates. Final alternative suspicion varies. Innocent readings and endings retained exactly.',
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file() and p.name!='manifest.json'}}
    (dest/'manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('Explicit promotion prepared; old pinned sources archived; PDFs still require rebuild/review before deployment.')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--rsvp-case',required=True);args=parser.parse_args()
    assert args.rsvp_case in ('balance-dramatic-22-03','balance-dramatic-22-04')
    promote(args.rsvp_case)
