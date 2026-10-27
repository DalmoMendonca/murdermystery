from pathlib import Path
import hashlib,json,copy
import yaml

root=Path(__file__).resolve().parents[1]
run=root/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
src=root/'source/connected_release'
dst=run/'candidate04-source'
canonical=yaml.safe_load((src/'confirmed.yaml').read_text(encoding='utf-8'))
candidate=yaml.safe_load((dst/'confirmed.yaml').read_text(encoding='utf-8'))
perf=yaml.safe_load((dst/'performance.yaml').read_text(encoding='utf-8'))
ledger=json.loads((run/'candidate04-change-ledger.json').read_text(encoding='utf-8'))
old={c['id']:c for c in canonical['characters']}
new={c['id']:c for c in candidate['characters']}
changes=[]
for cid,c in new.items():
 for sec in ('hearings','coming_clean'):
  for field,text in c[sec].items():
   if old[cid][sec][field]!=text: changes.append({'id':cid,'section':sec,'field':field,'before':old[cid][sec][field],'after':text})
assert changes==ledger['changes'] and len(changes)==29
assert sum(x['section']=='hearings' for x in changes)==27
assert canonical['question_rounds']==candidate['question_rounds']
assert canonical['pre_method_press_interview_opening']==candidate['pre_method_press_interview_opening']
for cid in old:
 assert old[cid]['coming_clean']['murderer']==new[cid]['coming_clean']['murderer']
 expected=new[cid]['hearings']['evidence_murderer']
 if cid=='11': expected=expected.replace("Brie, there's footage. ",'')
 assert old[cid]['hearings']['evidence_murderer']==expected
assert (src/'playable-evidence.yaml').read_bytes()==(dst/'playable-evidence.yaml').read_bytes()
assert (src/'voice-story-bible.yaml').read_bytes()==(dst/'voice-story-bible.yaml').read_bytes()
prefix={'motive':'motive','opportunity':'where','method':'evidence'}
fieldkeys=[]
for cid,fields in perf['fields'].items():
 for key,parts in fields.items():
  assert ' '.join(p['speech'] for p in parts)==new[cid]['hearings'][key],(cid,key)
  assert [p['part'] for p in parts]==list(range(1,len(parts)+1))
  fieldkeys.append((cid,key))
assert len(fieldkeys)==22
case_rows=[]
for culprit in new:
 row=[culprit+' '+new[culprit]['name']]
 for sched in perf['metadata']['schedules']:
  group=candidate['question_rounds'][list(prefix).index(sched['round_key'])]['groups'][sched['group_index']-1]
  groupids={cid for cid,c in new.items() if c['name'] in group['targets']}
  assert set(t['id'] for t in sched['turns'])==groupids
  seen=[]
  for t in sched['turns']:
   branch='murderer' if t['id']==culprit else 'innocent'
   key=prefix[sched['round_key']]+'_'+branch
   part=next(p for p in perf['fields'][t['id']][key] if p['part']==t['part'])
   seen.append((t['id'],key,t['part'],part['speech']))
  for cid in groupids:
   key=prefix[sched['round_key']]+'_'+('murderer' if cid==culprit else 'innocent')
   spoken=[(x[2],x[3]) for x in seen if x[0]==cid]
   assert spoken==[(p['part'],p['speech']) for p in perf['fields'][cid][key]]
  row.append('Guilty '+culprit if culprit in groupids else 'All innocent')
 case_rows.append(row)

hashes={name:hashlib.sha256((dst/name).read_bytes()).hexdigest() for name in ('confirmed.yaml','performance.yaml','procedure.txt','playable-evidence.yaml','voice-story-bible.yaml')}
for name,h in hashes.items(): assert ledger['sha256'][name]==h
reports={
 '01.motive_innocent':'PASS. Six years, replacement, proposed donor terms, payroll and Sue objection remain. Address to Sue adds no answer or historical knowledge.',
 '01.motive_murderer':'PASS. Same replacement assertion as innocent branch; practiced/could-not-get-through remain completed past states despite contractions.',
 '04.motive_innocent':'PASS. Friday identifies wage due date; funding/control, cleaners, payroll preference and rejected terms remain. Replacement fragment echoes immediately preceding Artie part2; it is not independent confirmation.',
 '04.motive_murderer':'PASS. Same public replacement echo; mother/payday, moved money, books-before-check, board scrutiny, hated lost authority and no time remain. No new admission of unauthorized transfer is substituted for the original branch.',
 '08.motive_innocent':'PASS. Full canonical paragraph, one turn; no assent to Artie or Monet is scripted.',
 '08.motive_murderer':'PASS. Full canonical paragraph, one turn; retains earlier-advice leverage and no new threat.',
 '02.where_innocent':'PASS. Previously reviewed canonical paraphrase: separate bowl/bottle files, hold, removal/movement, both on desk; no new document or evidence handling.',
 '02.where_murderer':'PASS. Verbatim canonical paragraph; glass moved off paper remains Claire\'s own claim, not Reed\'s observation.',
 '05.where_innocent':'PASS. Verbatim canonical paragraph. Existing load-down imperative is unchanged, not a newly reported compliance or an instruction to reset the current scene.',
 '05.where_murderer':'PASS. Verbatim canonical paragraph, including held glass/put-back sequence and timing after preview. No new partner response.',
 '09.where_innocent':'MUST-FIX: sequence ambiguity. Original asks Reed to hold early press copies before narrating Grant\'s reply and allowing preview; revised performance places the request after Reed part1 and after Art\'s “I let the preview go ahead.” Past “I asked you” does not become a present command, but the original pre-preview timing is no longer clear. Preserve it explicitly in the retrospective cue, e.g. “Reed, before the preview I asked you to hold the early press copies.” All other source assertions remain.',
 '09.where_murderer':'MUST-FIX: sequence ambiguity. Original request to restore attachment precedes draft/query and preview attendance. Revised part2 reports it after “I attended the preview.” Retain the historical request and its before-preview position explicitly, e.g. “Reed, before the preview I asked you to restore the collection attachment.” Do not turn it into “restore it now” or make Reed claim compliance. Private speech-card visit and other admissions remain.',
 '19.where_innocent':'PASS. Intake-full-query sentence moves into part1; omitted warning, non-space motive, Grant publicity insult, intended public disgrace and unexamined harm remain. It neither says Art just ordered the edit nor claims he consented.',
 '19.where_murderer':'PASS. Previously reviewed paraphrase with restored “apparently”; full intake attachment, shortened press entry, Grant approval demand and private caption handling remain. Response contains no claim of obeying Art\'s past request.',
 '06.evidence_innocent':'PASS. Prior reviewed prohibition-to-wish change preserves intended alive/furious humiliation and film/rejection. No new Vincent reply.',
 '06.evidence_murderer':'PASS. All original sentences verbatim; live-stunt consent and inert-belief cover remain lies at their original strength. Nobody in the exchange validates them.',
 '11.evidence_innocent':'PASS. Entire canonical text retained, split only. Power/no-recording and false-log admission precede Brie; staff-release permission follows Brie\'s staff request, present permission already in canon. No release or questioning is newly reported as accomplished.',
 '11.evidence_murderer':'PASS within expressly authorized repetition. Every original sentence retained. “Brie, there\'s footage” only repeats the same categorical false claim from part1. Following Brie\'s lone preparation account it is still Barb\'s assertion, not a factual answer endorsed by Brie. Preserve its false status and do not stage a confirming reaction.',
 '23.evidence_innocent':'PASS. Canonical text verbatim, split. Lone individual preparation, retained ingredient, washed measure, staff request and unpaid food remain; no reply accepts footage or a new witness.',
 '23.evidence_murderer':'PASS. Canonical text verbatim, split. Closed-container/flavored-pitcher lie and true paid-toast/disputed-food distinction stay with Brie. Later billing statement does not corroborate Barb\'s power account.',
 '24.evidence_innocent':'PASS. Canonical paragraph after completed Barb/Brie block: same engraved glass and collateral frame-damage lie. No new statement about previous speakers\' truthfulness.',
 '24.evidence_murderer':'PASS. Canonical paragraph; original bottle-opening concession, inert label report, boxed-glass/plain-spare lie, watched claim and corrected report remain. It does not claim Barb\'s footage establishes its story.',
}
assert set(reports)=={cid+'.'+field for cid,field in fieldkeys}
lines=['# Candidate04 semantic and exchange-schedule review','',
 '**Verdict: FAIL pending two narrow historical-sequence clarifications in Art09 Opportunity.** No new witness, physical act, forensic inference or cross-speaker admission was found in the exchanges. The format is genuinely a split-turn performance change; it is not certified as having any particular solve rate or literary quality.','',
 'Reviewed the actual assembled confirmed.yaml, performance.yaml, procedure.txt and exact change ledger against canonical full arcs and the frozen fact guard, carrying forward the prior semantic review of unchanged candidate03 edits. No source/candidate was edited. No prior literary ratings, trial scores or author rationale were used as evidence.','',
 '## Reviewed snapshot hashes','']
for name,h in hashes.items(): lines.append(f'- `{name}`: `{h}`')
lines+=['','Ledger hash: `'+hashlib.sha256((run/'candidate04-change-ledger.json').read_bytes()).hexdigest()+'`. All listed file hashes match the ledger.','',
 '## Exact structural checks','',
 'The actual canonical-to-candidate diff contains 29 changed passages: 27 hearings and two innocent finales. It exactly matches the ledger. All 22 murderer Method originals remain verbatim, with only the authorized Barb repeated sentence inserted. All 22 murderer finales remain exact baseline. The evidence and voice-bible files inspected are byte-identical to canonical; the nine-underlying-source-byte claim was not separately expanded into a nine-file audit here. Question rounds and recorded interview opening are unchanged.','',
 'All 22 performance fields (11 speaker/act assignments, both branches) concatenate exactly into the actual candidate confirmed paragraphs. Part numbers are sequential; each speaker\'s complete paragraph is delivered once and in its internal part order. Each chosen group contains exactly the active members of its existing shared-question group. The performance schedules add two speaker entries per act, not duplicate testimony. Repeated turns do not grant a second branch.','',
 '## Full 22-culprit branch application','',
 'For each possible sole selected culprit, the three complete fixed schedules were applied. Every part used only that character\'s selected branch; all other speakers used innocent branches. All parts appeared exactly once per speaker in original internal order, without truncation or branch leakage. Group entry by any of its members produces the same sequence and completion set. The generic procedure lets the last scheduled speaker choose an unheard guest outside that group; it does not force a different order among the remaining original single-turn speakers.','',
 '| Selected culprit | Motive group | Opportunity group | Method group |',
 '|---|---|---|---|']
for row in case_rows: lines.append('| '+' | '.join(row)+' |')
lines+=['','## Public-response licensing','',
 'Motive: Artie part1 publicly supplies donor resignation/payroll/objection context in both branches. Sue\'s full paragraph neither answers a secret nor grants consent. Artie part2 publicly supplies “my own replacement” in both branches immediately before Monet part2 echoes “Your replacement, Artie.” This repeats a heard claim, not an independently witnessed replacement decision. The proposed gift remains unaccepted.','',
 'Opportunity: Art part1 publicly supplies the inert/original-contents conflict or retained query; Reed part1 publicly supplies full intake materials in both branches. Art part2\'s “I asked you” remains retrospective in both variants, but its pre-preview position needs the two clarifications above. Reed part2 gives only his own previously authored account; it never says he complied with Art, knew Art\'s private visit, or witnessed his handling. Claire and Chip add no assent. An existing vocative is not a new witness.','',
 'Method: Barb part1 establishes either her truthful power/no-recording account or her false local-footage account. Brie part1 says either “prepared ... alone” plus staff request, or her original pitcher/container cover plus staff request. Barb innocent part2 repeats canonical staff-release permission; Barb murderer part2 repeats her own footage lie and canonical storage request. Brie part2 returns to bills in either branch; she does not accept the asserted footage or the technician story. Dada and Cary perform their original branch claims without corroborating the exchange. All alternative pairings relevant to each sole-culprit case therefore work as assertions and requests, not confirmed history.','',
 '## Per-field full exchange review','']
for cid,key in fieldkeys:
 lines += [f'### {cid}.{key}', '', '**Canonical**', '', '> '+old[cid]['hearings'][key], '', '**Actual candidate, performed in scheduled parts**', '', '> '+new[cid]['hearings'][key], '', reports[cid+'.'+key], '']
lines+=['## Remaining prior edits and collateral arcs','',
 'Candidate03-to-candidate04 differences were inspected directly, not assumed. The remaining candidate03 hearing paraphrases stay unchanged: Monet innocent ticket/authorization; Vincent both Opportunity branches; Sue murderer donor copy/glass; Frank both Opportunity branches; Mona murderer letter/glass; Elon innocent demonstration/invoice denial; Elle innocent panel/advance denial; Al murderer sculpture/payment with fixed “second sculpture for free”; Cary both Opportunity branches; Anne both Opportunity branches; Penny innocent Method; Justin murderer folder/note. Claire innocent, Dada innocent Method and Reed murderer Opportunity are also unchanged from their earlier semantic pass and are included above because they are now performed inside the exchanges. Al\'s financial modifier and Reed\'s “apparently” fix remain present.','',
 'The seven innocent collateral lies remain intact: Monet authorization, Chip insurance date, Mona ministry authority, Elon invoice, Elle advance, Cary damage, Penny valuation. Their original post-vote retractions remain. Barb\'s admitted false log is not converted into an eighth delayed collateral reveal; Reed\'s deliberate warning omission is already public in Opportunity and remains so. Anne\'s original Opportunity/Method tour conflict and murderer retrospective false group alibi remain unchanged; no route harmonization or new escort is authorized.','',
 '## Finale and procedure','',
 'All original warm innocent finales are restored except Frank\'s already reviewed removal of the Production vocative and Reed\'s already reviewed, expressly authorized ambiguity repair. Art\'s dinner invitation remains post-vote only. No material finale assertion, murderer mechanism or collateral retraction is newly changed by this version.','',
 'Procedure explicitly locks every ballot before any finale, keeps the original top-three tally, announces all names together, lets only named innocents speak first in any order, waits the named murderer, and always gives the actual murderer the last speech even outside the top three. It explicitly forbids substituting fourth place and retains Escaped Justice against the original locked tally. This is a procedural change, not evidence or a voting-feedback change. Maximum speeches is four: three named innocents plus an unlisted murderer, or two named innocents plus a listed murderer. The restored future social requests now precede the confession; they are wishes/permissions, not completed departure, agreement or assistance.','',
 'The sentence requiring host and all private instructions to match before printing is an integration condition. This review covers these prototype files; it does not certify a future compiled packet with inherited host/private instructions. Do not mark a protected printing release as matched until those actual artifacts are checked.','',
 '## Required action','',
 'In both Art09 Opportunity branches preserve that the reported request to Reed preceded the preview, while retaining past-tense ownership: “Reed, before the preview I asked you ...”. This resolves the sequencing ambiguity without creating a current instruction, new compliance, or a witness. Update both confirmed and performance representations together, reassemble and recheck exact concatenation/hash. No other semantic must-fix was found in this snapshot.','']
(run/'candidate04-semantic-review.md').write_text('\n'.join(lines),encoding='utf-8')
print('Saved candidate04-semantic-review.md; 22 performance fields, 22 culprit schedules, 29 actual changed passages; 2 narrow sequence must-fixes.')
