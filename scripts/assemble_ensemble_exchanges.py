"""Freeze a different, cue-aware author candidate before independent review."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, yaml

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
CANON = ROOT/'source/connected_release'
FIELD = {'motive':'motive','opportunity':'where','method':'evidence'}
norm = lambda x:' '.join(x.split())
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

PROCEDURE = '''Each guest knows their own branch from the animal draw. Before voting, never read the other branch or improvise a historical fact.
The existing guest-chooses-next chain continues, with ONE marked exchange group in each act. Choosing any person in that marked group starts the whole group's exchange. Ask its existing shared question, then follow the short printed part schedule. Everyone in that group uses only their own branch and stops after the numbered part; all other group members wait. Only the final speaker, after the final part, chooses an unheard guest outside the completed group. The host marks all group members heard only when the exchange finishes. If no unheard names remain, end the act instead of choosing anyone. Other guests have the existing single-turn answer. Group blocks may occur anywhere in the act, but their internal part order is fixed. No extra question or factual improvisation is required. All guests still supply their complete answer in every act.
After ALL ballots are locked, tally the same top three suspects. Announce all three names together. Only named INNOCENT guests read their Coming Clean boxes now, one at a time, in any order. A named murderer waits. When the named innocents finish, the selected-animal murderer stands and reads the murderer box, whether or not in the top three. Do not replace a waiting murderer with a fourth-ranked innocent. Escaped Justice still depends on the ORIGINAL locked top-three tally. Maximum four speeches; the murderer always speaks last. Host and all private instructions must match this prototype before any printing release.'''

def export(bank, performance, target):
    people = {c['id']:c for c in bank['characters']}
    byname = {c['name']:c['id'] for c in bank['characters']}
    schedules = {(s['round_key'],s['group_index']):s for s in performance['metadata']['schedules']}
    text = ['# Full ensemble, cue-aware prototype\n', PROCEDURE,
            '\nExactly one murderer alternative is used in a performed world. Both alternatives below are supplied for complete editorial review, not read consecutively to a table. All22 roles and176 passage alternatives are present. Numbered parts are one answer divided into turns, not new facts.\n']
    for rd in bank['question_rounds']:
        text.append(f"\n## {rd['key']}\n")
        field = FIELD[rd['key']]
        for index, group in enumerate(rd['groups'],1):
            text.append('\nShared question: '+group['question']+'\n')
            schedule = schedules.get((rd['key'],index))
            if schedule:
                text.append('Exchange cue: '+' → '.join(people[t['id']]['name']+' '+str(t['part']) for t in schedule['turns'])+'\n')
                for turn in schedule['turns']:
                    c = people[turn['id']]
                    text.append(f"### {c['id']} {c['name']} / part {turn['part']}\n")
                    for branch in ['innocent','murderer']:
                        part = performance['fields'][c['id']][field+'_'+branch][turn['part']-1]
                        text.append(f"**{branch}:** {part['speech']}\n")
            else:
                for name in group['targets']:
                    c = people[byname[name]]
                    for branch in ['innocent','murderer']:
                        text.append(f"### {c['id']} {name} / {branch}\n\n{c['hearings'][field+'_'+branch]}\n")
    text.append('\n## Possible finales: only named innocents followed by the murderer are performed\n')
    for c in bank['characters']:
        for branch in ['innocent','murderer']:
            text.append(f"### {c['id']} {c['name']} / {branch}\n\n{c['coming_clean'][branch]}\n")
    target.write_text('\n'.join(text),encoding='utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--version',default='04')
    parser.add_argument('--draft',default='draft-exchanges-v2.yaml')
    args=parser.parse_args()
    assert args.version.isdecimal() and len(args.version)==2
    dest=RUN/f'candidate{args.version}-source'
    assert not dest.exists(), 'Never overwrite a snapshot or reroll a judged input.'
    performance = yaml.safe_load((RUN/args.draft).read_text(encoding='utf-8'))
    base = yaml.safe_load((CANON/'confirmed.yaml').read_text(encoding='utf-8'))
    canonical = {c['id']:c for c in base['characters']}
    stage03 = yaml.safe_load((RUN/'candidate03-source/confirmed.yaml').read_text(encoding='utf-8'))
    people03 = {c['id']:c for c in stage03['characters']}
    for schedule in performance['metadata']['schedules']:
        rd = next(r for r in base['question_rounds'] if r['key']==schedule['round_key'])
        group = rd['groups'][schedule['group_index']-1]
        ids = [next(c['id'] for c in base['characters'] if c['name']==n) for n in group['targets']]
        first = list(dict.fromkeys(t['id'] for t in schedule['turns']))
        assert first == ids
        assert len(schedule['turns'])-len(ids)<=5
        field = FIELD[schedule['round_key']]
        for ident in ids:
            parts = [t['part'] for t in schedule['turns'] if t['id']==ident]
            assert parts == list(range(1,len(parts)+1))
            for branch in ['innocent','murderer']:
                values = performance['fields'][ident][field+'_'+branch]
                assert [v['part'] for v in values] == parts
    editions = {}
    ledger = []
    for edition in ['confirmed','all']:
        bank = yaml.safe_load((CANON/(edition+'.yaml')).read_text(encoding='utf-8'))
        for c in bank['characters']:
            if c['id'] not in people03:
                continue
            old = copy.deepcopy(c)
            c['hearings'] = copy.deepcopy(people03[c['id']]['hearings'])
            for field, parts in performance['fields'].get(c['id'],{}).items():
                c['hearings'][field] = ' '.join(p['speech'] for p in parts)
            # Retain the canonical warmth; the finale order now resolves the clash.
            if c['id'] in ['13','19']:
                c['coming_clean']['innocent'] = people03[c['id']]['coming_clean']['innocent']
            assert c['coming_clean']['murderer'] == old['coming_clean']['murderer']
            expect = canonical[c['id']]['hearings']['evidence_murderer']
            actual = c['hearings']['evidence_murderer']
            if c['id']=='11':
                actual = actual.replace("Brie, there's footage. ",'')
            assert norm(actual)==norm(expect), c['id']
            if edition=='confirmed':
                for section in ['hearings','coming_clean']:
                    for field,value in c[section].items():
                        if value!=old[section][field]:
                            ledger.append(dict(id=c['id'],section=section,field=field,before=old[section][field],after=value))
        bank['status']=f'isolated_ensemble_exchange_candidate{args.version}_pending_independent_review'
        editions[edition]=bank
    words = sum(len(s.split()) for c in editions['confirmed']['characters'] for s in c['hearings'].values())
    assert words<=8040,words
    dest.mkdir()
    for edition, bank in editions.items():
        (dest/(edition+'.yaml')).write_text(yaml.safe_dump(bank,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
    for name in ['playable-evidence.yaml','voice-story-bible.yaml']:
        shutil.copy2(CANON/name,dest/name)
    (dest/'performance.yaml').write_text(yaml.safe_dump(performance,sort_keys=False,allow_unicode=True,width=100),encoding='utf-8')
    (dest/'procedure.txt').write_text(PROCEDURE+'\n',encoding='utf-8')
    report = dict(version=args.version,status='pending semantic, cue and independent whole-cast review',
                  changed_passages=len(ledger),pre_vote_words=words,baseline_pre_vote_words=8040,
                  all_murderer_method_sentences_retained_verbatim=True,barb_repeats_existing_footage_claim=True,
                  all22_murderer_finales_verbatim=True,all9_evidence_source_bytes_unchanged=True,
                  extra_entries_per_act={s['round_key']:len(s['turns'])-len(set(t['id'] for t in s['turns'])) for s in performance['metadata']['schedules']},
                  changes=ledger,sha256={p.name:sha(p) for p in dest.iterdir()})
    (RUN/f'candidate{args.version}-change-ledger.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    export(editions['confirmed'],performance,RUN/f'candidate{args.version}-stage-order.md')
    print(json.dumps({k:v for k,v in report.items() if k not in ['changes','sha256']}))

if __name__=='__main__': main()
