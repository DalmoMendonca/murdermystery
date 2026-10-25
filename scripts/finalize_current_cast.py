"""Deadline fallback: publish the tested story with the actual attending cast."""
from pathlib import Path
import copy,json,shutil,yaml
from exhaustive_balance import sha,write
from public_lock import verify_public_lock

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest/2026-10-24-CURRENT-CAST-RELEASE-SPOILERS'
BASE=ROOT/'docs/playtest/2026-10-23-FINAL-RSVP22-SPOILERS'
LIVE=ROOT/'source/connected_release'
assert not RUN.exists(),'Never overwrite a source archive or release receipt.'
latest=ROOT/'docs/playtest/2026-10-24-RESTORED-OPPORTUNITY-SPOILERS'
tested=json.loads((latest/'aggregate.json').read_text(encoding='utf-8'))
assert tested['completed']==2 and tested['invalid']==0
assert any(not t['metrics']['e3_ready'] for t in tested['trials']),'Use the accepted-source path if the candidate passes.'
verify_public_lock(ROOT)
RUN.mkdir();shutil.copytree(LIVE,RUN/'published-source-before')
out=RUN/'candidate-source';out.mkdir()
all_bank=yaml.safe_load((LIVE/'all.yaml').read_text(encoding='utf-8'))
event=yaml.safe_load((BASE/'frozen-source/confirmed.yaml').read_text(encoding='utf-8'))
for bank in [all_bank,event]:
    bank['status']='deadline_current_cast_published_story'
for label,bank in [('all',all_bank),('confirmed',event)]:
    (out/(label+'.yaml')).write_text(yaml.safe_dump(bank,allow_unicode=True,sort_keys=False),encoding='utf-8')
for name in ['playable-evidence.yaml','voice-story-bible.yaml']:shutil.copy2(LIVE/name,out/name)
# Preserve ALL branches, including deliberately false murderer statements.
# Monet's impossible early visit is intentional and explained in her confession.
original=yaml.safe_load((BASE/'frozen-source/confirmed.yaml').read_text(encoding='utf-8'))
assert original['question_rounds']==event['question_rounds']
assert original['pre_method_press_interview_opening']==event['pre_method_press_interview_opening']
for old,new in zip(original['characters'],event['characters']):
    assert old['id']==new['id']
    assert old['coming_clean']==new['coming_clean']
    for field,text in old['hearings'].items():
        assert text==new['hearings'][field]
record={'revision':'current-rsvp22-deadline-release-2026-10-24','baseline_commit':'4af7056',
        'tests':[str(BASE.relative_to(ROOT))],
        'confirmed_ids':[c['id'] for c in event['characters']],
        'changes':'Attendance substitutions from the tested published-story baseline only. All30 original story branches preserved; no rejected balance rewrites.',
        'limitations':'Two targeted new-role text cases, not exhaustive coverage or human solve rates. Current baseline midgame counts3/2 and final innocent alternatives0/1 miss desired balance. Three later experimental rounds rejected; their scores do not describe this release.',
        'sha256':{p.name:sha(p) for p in out.iterdir()}}
write(out/'manifest.json',record)
for p in out.iterdir():shutil.copy2(p,LIVE/p.name)
write(RUN/'source-equivalence.json',{'published_story_preserved':True,'all30_story_branches_unchanged':True,'all_current22_baseline_words_unchanged':True,'current_adult_count':22,'removed':['03','10'],'added':['24','27'],'nonplaying_child_excluded':True,'all16_clues_and_every_evidence_exhibit_unchanged':True,'already_sent_assets_locked':True})
status={'release_date':'2026-10-24','edition':record['revision'],'characters':30,'confirmed_guest_packet_edition':22,'complete_player_packet_pages':12,
        'status':'Current-attendance deadline fallback. Published story preserved; recent balance experiments rejected. No claim that balance goals are met.',
        'confirmed_changes':'Hugh and Tess removed; Cary and Robin added. Belle is not an adult suspect.',
        'sent_assets':'unchanged','balance_report':'docs/playtest/2026-10-24-RESTORED-OPPORTUNITY-SPOILERS/RESULTS.md'}
write(ROOT/'site/downloads/Release_Status.json',status)
(RUN/'DECISION.md').write_text('''# Deadline release: current attendance, published story

The bounded restored-opportunity candidate is rejected: Cary's reader scored him3 before the final statements and9 afterward, with one midgame suspect above5 and no final innocent alternatives. Robin's reader met the desired distribution:6 before the final statements,9 afterward,8 midgame suspects and6 innocent final alternatives. Both accusations were correct, earned, and not clear prematurely. One successful scenario does not validate the shared kit for every selected culprit.

Do not publish that mixed candidate or transfer its scores onto this release. This release preserves the published story and uses the previously tested current22 attendance edition. Its two original baseline cases scored Cary6->10 and Robin7->9, with3/2 midgame suspects and0/1 final innocent alternatives. Those balance shortcomings remain. The purpose is a coherent printable kit for the real attending cast while preserving the best proven fallback; it is not an advertised balance upgrade.

Hugh and Tess are absent; Cary and Robin attend. The nonplaying child does not enter suspect selection. Day-of relationship bullets and all question targets follow attendance. Sent invitations and character sheets remain byte-locked. ALL original story branches are preserved, including Monet's deliberately false early-visit statement; her confession explains that lie. No untested branch correction is included.

All30 proof routes remain available in the full-cast edition. Only the two baseline current-cast worlds were specifically tested; no human solve rates or live rehearsal are claimed. The old source is archived here. Final PDF rendering, visual review, packaging and live hashes must be recorded before declaring deployment complete.
''',encoding='utf-8')
print('Deadline current-cast source prepared; no rejected balance scenes promoted.')
