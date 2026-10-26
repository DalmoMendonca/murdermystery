"""Report the approved candidate's actual gates without redefining a miss."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-26-DRAMATURGICAL-02-BLIND-SPOILERS'
BASE=ROOT/'docs/playtest/2026-10-26-SURGICAL-FINAL-COVERAGE-SPOILERS'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
if __name__=='__main__':
    new=read(RUN/'summary.json');old=read(BASE/'summary.json')
    gates={
      'all22_complete':new['completed']==22,
      'all22_correct':new['correct']==22,
      'all22_earned':new['earned']==22,
      'zero_early_clear':new['clear_before_method_testimony']==0,
      'all22_unique_final_culprit_leaders':new['unique_final_culprit_leader']==22,
      'naturalness_above8_aspiration':new['ratings']['naturalness']['mean']>8,
      'arc_variety_at_least8_aspiration':new['ratings']['arc_variety']['mean']>=8,
      'no_naturalness_or_arc_rating_below6':all(new['ratings'][k]['min']>=6 for k in ['naturalness','arc_variety']),
    }
    fairness=all(gates[k] for k in ['all22_complete','all22_correct','all22_earned','zero_early_clear','all22_unique_final_culprit_leaders'])
    payload={'candidate':'dramaturgical02','gates':gates,'fairness_headline_gates_pass':fairness,
      'naturalness_mean':new['ratings']['naturalness']['mean'],'baseline_naturalness_mean':old['ratings']['naturalness']['mean'],
      'arc_variety_mean':new['ratings']['arc_variety']['mean'],'baseline_arc_variety_mean':old['ratings']['arc_variety']['mean'],
      'distribution_review':{k:{'baseline':old[k],'candidate':new[k],'change':new[k]-old[k]} for k in ['act2_suspects_above5_median','final_innocents_5to7_median']},
      'promotion':'Not authorized until user reviews the candidate and results. Failed fairness gates block promotion.',
      'limitations':'Fresh22 candidate readers versus versioned prior coverage, not a randomized matched experiment. AI readings do not estimate human solve rates. Inspect all qualitative feedback; mean ratings do not establish freedom from repeated arcs.'}
    (RUN/'acceptance-review.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload))
