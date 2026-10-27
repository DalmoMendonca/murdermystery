"""Assemble manually authored selective edits; never alter protected sources."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, yaml

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
SOURCE = ROOT/'source/connected_release'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def export(bank, target, procedure=None):
    """Stage order makes ensemble rhythms visible without duplicating 22 worlds."""
    pieces = ['# Complete ensemble manuscript\n',
        'There are22active roles. All22 answer each of3rounds, in the listed group order. Exactly one guest uses murderer alternatives, the others use innocent alternatives. The alternatives are NOT additional public testimony. Do not concatenate22 murderer readings as if one room heard them.\n',
        'After all votes lock, only the top THREE voted suspects read Coming Clean, descending votes, alphabetical full-name ties. All called innocents finish even after a confession. If none confesses, the selected animal murderer reads fourth. Nobody improvises new facts or reads another role’s private alternatives.\n']
    if procedure is not None:
        pieces=['# Complete ensemble manuscript\n',procedure,
                '\nAll22roles and176 passage alternatives are supplied for complete review. In a played world exactly one role uses its murderer alternatives. Do not concatenate22 murderer readings as one scene. The grouped presentation below is an analytical reading order; the actual guest-chooses-next chain can visit any unheard guest.\n']
    names = {c['name']: c for c in bank['characters']}
    for round_ in bank['question_rounds']:
        field = {'motive':'motive','opportunity':'where','method':'evidence'}[round_['key']]
        pieces.append(f"\n## {round_['key']}\n")
        for group in round_['groups']:
            pieces.append('\nQuestion: '+group['question']+'\n')
            for name in group['targets']:
                c = names[name]
                for branch in ['innocent','murderer']:
                    pieces.append(f"### {c['id']} {name} / {branch}\n\n{c['hearings'][field+'_'+branch]}\n")
    pieces.append('\n## Possible finale readings: only selected top3 plus possible fallback are heard\n')
    for c in bank['characters']:
        for branch in ['innocent','murderer']:
            pieces.append(f"### {c['id']} {c['name']} / {branch}\n\n{c['coming_clean'][branch]}\n")
    target.write_text('\n'.join(pieces), encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', default='01')
    parser.add_argument('--draft', default='draft-pre-vote.yaml')
    parser.add_argument('--finales', default='draft-finales.yaml')
    parser.add_argument('--procedure')
    args = parser.parse_args()
    assert args.version.isdecimal() and len(args.version)==2
    dest = RUN/f'candidate{args.version}-source'
    assert not dest.exists(), 'Preserve every candidate snapshot; use a new version for repairs.'
    base = yaml.safe_load((SOURCE/'confirmed.yaml').read_text(encoding='utf-8'))
    provenance = json.loads((RUN/'baseline-provenance.json').read_text())
    assert sha(SOURCE/'confirmed.yaml') == provenance['sha256']
    pre = yaml.safe_load((RUN/args.draft).read_text(encoding='utf-8')) or {}
    post = yaml.safe_load((RUN/args.finales).read_text(encoding='utf-8')) or {}
    assert sum(len(v) for v in pre.values()) <= 50
    byid = {c['id']:c for c in base['characters']}
    assert set(pre) <= set(byid) and set(post) <= set(byid)
    for ident, fields in pre.items():
        assert set(fields) <= set(byid[ident]['hearings'])
        assert 'evidence_murderer' not in fields, 'Preserve all22 pivotal murderer claims verbatim.'
    for ident, fields in post.items():
        assert set(fields) <= {'innocent'}, 'All22 murderer finales remain protected in this pass.'
    dest.mkdir()
    ledger = []
    for edition in ['all','confirmed']:
        bank = yaml.safe_load((SOURCE/(edition+'.yaml')).read_text(encoding='utf-8'))
        for c in bank['characters']:
            old = copy.deepcopy(c)
            c['hearings'].update(pre.get(c['id'],{}))
            c['coming_clean'].update(post.get(c['id'],{}))
            assert c['hearings']['evidence_murderer'] == old['hearings']['evidence_murderer']
            assert c['coming_clean']['murderer'] == old['coming_clean']['murderer']
            if edition == 'confirmed':
                for section in ['hearings','coming_clean']:
                    for key, after in c[section].items():
                        before = old[section][key]
                        if after != before:
                            ledger.append(dict(id=c['id'],name=c['name'],section=section,field=key,before=before,after=after))
        bank['status'] = f'isolated_ensemble_candidate{args.version}_pending_semantic_and_editorial_review'
        (dest/(edition+'.yaml')).write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
        if edition == 'confirmed':
            current = bank
    for name in ['playable-evidence.yaml','voice-story-bible.yaml']:
        shutil.copy2(SOURCE/name, dest/name)
    procedure=None
    if args.procedure:
        procedure=(RUN/args.procedure).read_text(encoding='utf-8')
        (dest/'procedure.txt').write_text(procedure,encoding='utf-8')
        (dest/'performance.yaml').write_text(yaml.safe_dump({'metadata':{'group_index_base':1,'numbering_is_spoken':False,'schedules':[]},'fields':{}},sort_keys=False),encoding='utf-8')
    words = sum(len(s.split()) for c in current['characters'] for s in c['hearings'].values())
    assert words <= 8040, words
    report = dict(changes=ledger,changed_passages=len(ledger),pre_vote_words=words,baseline_pre_vote_words=8040,
                  pivotal22_murderer_method_fields_verbatim=True,all22_murderer_finales_verbatim=True,
                  question_rounds_unchanged=current['question_rounds']==base['question_rounds'],
                  status='pending independent semantic and whole-ensemble literary review',
                  version=args.version,sha256={p.name:sha(p) for p in dest.iterdir()})
    (RUN/f'candidate{args.version}-change-ledger.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if not (RUN/'baseline-stage-order.md').exists():
        export(base, RUN/'baseline-stage-order.md')
    export(current, RUN/f'candidate{args.version}-stage-order.md',procedure)
    print(json.dumps({k:v for k,v in report.items() if k not in ['changes','sha256']}))

if __name__ == '__main__':
    main()
