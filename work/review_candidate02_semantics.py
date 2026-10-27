import hashlib
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
run = root / 'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
source = root / 'source/connected_release/confirmed.yaml'
candidate = run / 'candidate02-source/confirmed.yaml'
a = yaml.safe_load(source.read_text(encoding='utf-8'))
b = yaml.safe_load(candidate.read_text(encoding='utf-8'))
guard = json.loads((run / 'fact-guard.json').read_text(encoding='utf-8'))
ledger = json.loads((run / 'candidate02-change-ledger.json').read_text(encoding='utf-8'))
old = {c['id']:c for c in a['characters']}
new = {c['id']:c for c in b['characters']}
frozen = {p['passage_key']:p for p in guard['passages']}
changes = []
allchanges = []
for cid,c in new.items():
    for section in ('hearings','coming_clean'):
        for key,text in c[section].items():
            gkey = cid + '.' + (key if section == 'hearings' else 'final_' + key)
            assert old[cid][section][key] == frozen[gkey]['baseline_quote']
            if text != old[cid][section][key]:
                row={'id':cid,'section':section,'field':key,'before':old[cid][section][key],'after':text}
                allchanges.append(row)
                if section == 'hearings': changes.append(row)
assert len(changes)==19 and len(allchanges)==27
assert [{k:v for k,v in x.items() if k!='name'} for x in ledger['changes']] == allchanges
assert all(old[cid]['hearings']['evidence_murderer']==new[cid]['hearings']['evidence_murderer'] for cid in old)
assert all(old[cid]['coming_clean']['murderer']==new[cid]['coming_clean']['murderer'] for cid in old)
assert a['question_rounds']==b['question_rounds']
assert a['pre_method_press_interview_opening']==b['pre_method_press_interview_opening']
finaldraft=yaml.safe_load((run/'draft-finales.yaml').read_text(encoding='utf-8'))
assert all(new[cid]['coming_clean']['innocent']==v['innocent'] for cid,v in finaldraft.items())

findings={
 '02.where_innocent': ('PASS','Bowl remains while label is removed; Reed retains old wording. The bottle\'s separate papers, public-display-to-intake movement, hold reason and both files on desk remain. “Own file” makes explicit the already stated two-file distinction without adding a new record. Self-critical motive and correction request remain; no new act by Reed.'),
 '04.where_innocent': ('PASS','Present request to Brie moves to the front; it is not a historical service event. Ticket arrives in accounts, account is crossed out, donor copy taken privately, Grant absent and glass waiting, transfer slip removed. Categorical board-authorization lie survives verbatim; no actual authorization is granted by this revision.'),
 '06.evidence_innocent': ('PASS','Only the address changes from a prohibition to a stated wish against Vincent softening the insult. Empty-jacket film, rejection, persistence, intended living/furious audience target and cruelty remain. Neither text establishes that Vincent actually responded or softened it.'),
 '07.where_innocent': ('PASS','The painting-from-sale-photo relation is explicit in the canonical innocent Method; clarifying the elliptical “bottle came from a sale photograph” imports no new event or knowledge. Model remains a studio lighting aid, actual acquired bottle is seen at preview, and studio things are excluded from loan. Reproduction crossing, collector showing, dealer scope and permission request remain.'),
 '07.where_murderer': ('PASS','Joining the private delivery and placement sentences preserves preview before later private visit, unsigned release, placement beside glass, catching light and Grant absence. Nothing makes him witnessed or reduces handling/access. Model and payment/permission context remain in the full paired arc.'),
 '08.where_murderer': ('PASS','Public announcement stop with Artie, kept running order and earlier attached advice remain. Private donor copy remains distinct; glass stands on it and Sue lifts glass/pulls paper free. The desire for that copy absorbs the rhetorical “you can see why”; no new witness or private supervision appears. Apology and anti-binding-agreement purpose remain.'),
 '13.where_innocent': ('PASS','Closure, lights, three parties\' requests, tour arrival/turnaway and preview elsewhere remain. Hearing production\'s complaint is still Frank\'s firsthand hearing of the same claim; removing a vocative does not create a named witness or a second conversation. No access to the closed alcove is granted.'),
 '13.where_murderer': ('PASS; chronology wording watch','The same ordered narration survives: Chip objection/closure, others\' exception requests, Grant\'s reopening request, private refusal visit, empty chair/set-out glass, sitting in other chair then rising before Grant arrives. “Then” makes the existing narrated transition explicit; it supplies no clock time or witness. It must not be staged as evidence of a newly timed message. Months of design, closed-door result and lack of graciousness remain; removing Production vocative adds no knowledge.'),
 '14.where_murderer': ('PASS','Unattributed circulation, Sue\'s authority question, Grant\'s knowledge, sealed-water request, private letter delivery, glass already there, Grant elsewhere, letter under glass edge to stop sliding, and desire for a private reading all remain. No water consumption or actual audience laughter is newly claimed.'),
 '15.where_innocent': ('PASS','Launch agreement is still intended for tonight, not completed. Phone demonstration includes private-room panel; preview explicitly precedes prepared-place display test; Grant absent. The proposal/no-invoice collateral deception remains categorical, not softened or admitted early.'),
 '18.where_innocent': ('PASS','The current refusal/request to Frank moves ahead of the historical narration, not into the event chronology. Alcove closure and close lamp precede removal/transport; panel rolled beside prepared place, Grant absent, speaker leaves with panel. Merchant bill identifies this fabric; false claim about the other advance remains intact. No help, witness or new transfer is invented.'),
 '19.where_murderer': ('MUST-FIX 2: restore qualification','Both labels, shortened press entry, full intake attachment, Grant\'s approval demand, private visit, Grant absence, caption placement and withdrawal before departure remain. However, original “and apparently I was supposed to find wording that satisfied both” becomes categorical “I was supposed to find wording to keep the program from getting longer and the donor from looking foolish.” Under the explicit certainty guard, preserve “apparently” (e.g. “Claire, apparently I was supposed ...”). It can be read as sarcasm rather than literal doubt, but deleting it needlessly strengthens the speaker\'s asserted knowledge of the assignment. Do not treat it as evidence that an actual instruction was corroborated. “I took him” is immediately qualified by “He wasn\'t there,” so it does not establish a successful handover.'),
 '20.where_murderer': ('MUST-FIX 1: restore payment/modifier scope','Refused replacement, corrected bronze description, Cary\'s installed contracted work, alcove closure, after-preview private payment visit, set-out glass, sitting, nobody arriving and departure remain. But original “make him a second sculpture for free” becomes “Grant\'s second free sculpture.” The latter implies an earlier free sculpture, which is not the original assertion and conflicts with the contracted work/outstanding last payment framing. Restore “make him a second sculpture for free,” or “for a second sculpture for Grant for free” with unambiguous scope. No authority to change the financial history exists. The final heavy-object metaphor changes wording but supplies no new physical movement of Grant.'),
 '24.where_innocent': ('PASS','Job request remains present, not an already assigned job. Signed sealed bottle/intake/frame handover, label-as-label inert report, service gifts, later report visit, set-out glass/Grant absence, subsequent bin emptying and normal-cleanup explanation remain. The prior-damage lie remains categorical and is still retracted only in innocent finale.'),
 '24.where_murderer': ('PASS','Signing then handing over makes the same handover sequence explicit; sealed incoming bottle, frame delivery and inert attribution to lender remain. Service gifts, stuck lift, report-retrieval motive, absent Grant/glass, carton lifted to clear chair, wait/departure and fear of “old” remain. No new packing check, opening or witness is introduced before Method.'),
 '25.where_innocent': ('PASS; canonical story conflict retained','Handout replacement retains Reed footnotes, removes Grant language, admits funding need; tour reaches closed alcove and turns back. The public consequence of her promise and unapproved plan remain. “I\'d made” is retrospective completion of that already narrated public handout act, not a new public announcement or a changed timing of school funding. No private visit or group presence at a private glass is added.'),
 '25.where_murderer': ('PASS; canonical story conflict retained','Same short tour, complaint to Frank, reception private handout visit, waiting glass, staying beside table rather than chasing Grant, wish to show crossed-out school program, unauthorized route and access grievance remain. Reordering desire after action changes narration, not who was present. It still does not expressly say she was alone in this paragraph; the separate unsupervised visit is established in the canonical murderer finale.'),
 '28.evidence_innocent': ('PASS','Only initial conversational “No” is removed. Band crossing stopper, Chip correction at preview, categorical false damaged-family-object/correct-comparison claims, no call received, continued looking and desire to speak before handout is read all remain. No identity, content or timing of a new call appears.'),
 '29.where_murderer': ('PASS','Sentence splits retain counsel receiving deed plus settlement together, Anne\'s request, circulated clipping, Grant\'s folder demand, private visit, waiting glass/Grant absence, note-writing then tearing and folder removal. Removing causal “so” does not erase the stated request/visit-purpose in context; no successful delivery or extra visit is added. Exposure/rebuttal stakes unchanged.'),
}
assert set(findings)=={r['id']+'.'+r['field'] for r in changes}

parts=[
 '# Candidate 02 semantic review - 19 changed pre-vote passages', '',
 'Reviewed the actual assembled candidate02-source/confirmed.yaml against canonical confirmed.yaml, all full paired arcs and fact-guard.json. Exact ledger correspondence was independently checked; ledger assertions alone were not treated as proof. No earlier draft, author literary preference, literary judge score or prior trial score was used. Source/candidate files were not edited.', '',
 f"**Verdict: FAIL pending two narrow fixes.** Candidate confirmed.yaml byte SHA256: `{hashlib.sha256(candidate.read_bytes()).hexdigest()}`. Canonical byte SHA256: `{hashlib.sha256(source.read_bytes()).hexdigest()}`.", '',
 'Must-fix 1: Al 20.where_murderer changes “a second sculpture for free” into “second free sculpture,” adding an unsupported first-free-work implication. Restore the original modifier scope. Must-fix 2: Reed 19.where_murderer drops “apparently” from his account of the wording assignment; restore the qualification under the exact certainty constraint. Neither requires changing canon, a lie, a clue, a witness or a crime mechanism.', '',
 '## Independently verified coverage', '',
 '- Exactly 19 changed pre-vote fields and eight changed innocent finales, 27 total, with exact before/after agreement to candidate02-change-ledger.json.',
 '- All 176 canonical fact-guard quotes agree with canonical text. All 22 murderer Method passages and all 22 murderer finales are verbatim baseline. Question rounds and the pre-Method press-interview opening are unchanged.',
 '- The assembled eight finales match the current reviewed draft-finales.yaml exactly. Their previously closed review is carried forward; Reed\'s explicitly authorized finale ambiguity-resolution caveat remains, separate from this new pre-vote qualification issue.',
 '- All seven collateral deception arcs were checked: Monet authorization, Chip insurance date, Mona ministry authority, Elon invoice/estimate, Elle advance diversion, Cary frame damage, Penny family valuation. Changed denials remain denials; unchanged denials/finale retractions remain exact baseline except the already reviewed Elle social aftermath. No accidental early collateral confession was found.',
 '- No changed passage gives another player a new observed reaction, alibi, supervision, private knowledge, sample, object transfer or physical access. No new clock time or forensic match was found. The two issues concern financial assertion scope and testimony qualification.', '',
 '## Pair parity and Anne conflict', '',
 'Both opportunity branches changed for Vincent, Frank, Cary and Anne; the two branches still differ in exactly the original substantive access/cover-story ways, aside from the isolated issues recorded above in other routes. Claire, Monet, Dada, Sue, Mona, Elon, Elle, Reed, Al, Penny and Justin have selective changes, but unchanged counterparts were compared in full: no new binary innocence marker, shared-witness assertion or branch-exclusive new clue was found. This is semantic parity review, not a judgment of voice, polish, length balance or reader difficulty.', '',
 'Anne innocent Opportunity retains turning the tour back from the closed alcove; innocent Method still places the group at public cases, never in Grant\'s room. Murderer Opportunity still admits taking the handout privately during reception and standing by the waiting glass. Her unchanged murderer Method still claims the group visited that room, was with her, and that this was her only visit; the unchanged murderer finale still explains the private poisoning without the group. That tension and later lie are canonical, not introduced or repaired here. The draft does not invent a group escort in Opportunity and does not remove the later false alibi. Do not “harmonize” the accounts into a new tour route.', '',
 '## Passage-by-passage audit', '',
]
for r in changes:
    key=r['id']+'.'+r['field']
    verdict,reason=findings[key]
    parts += [f"### {key} - {old[r['id']]['name']} - {verdict}", '', '**Canonical**', '', '> '+r['before'], '', '**Actual assembled candidate**', '', '> '+r['after'], '', '**Assessment:** '+reason, '']
parts += ['## Limits and closure requirements','',
 'The original quotes above govern over concise paraphrases. The report does not normalize ambiguities, infer truthful innocence from branch labels, or strengthen scrap similarity into unique identification. Acceptance of the remaining 17 changes means no material semantic change was found in their full-arc context, not a mathematical proof that every word has identical rhetorical force. Restoring Al\'s modifier scope and Reed\'s qualification requires a new assembled hash and a narrow recheck; this failing snapshot cannot be silently treated as passed.', '']
(run/'candidate02-semantic-review.md').write_text('\n'.join(parts),encoding='utf-8')
print(json.dumps({'reviewed_pre_vote':len(changes),'changed_total':len(allchanges),'verdict':'FAIL','mustfixes':2,'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest()}))
