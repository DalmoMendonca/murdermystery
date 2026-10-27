from pathlib import Path
import yaml,json,hashlib

root=Path(__file__).resolve().parents[1]
run=root/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
base=root/'source/connected_release'
src=run/'candidate06-source'
canonical=yaml.safe_load((base/'confirmed.yaml').read_text(encoding='utf-8'))
actual=yaml.safe_load((src/'confirmed.yaml').read_text(encoding='utf-8'))
ledger=json.loads((run/'candidate06-change-ledger.json').read_text(encoding='utf-8'))
guard=json.loads((run/'fact-guard.json').read_text(encoding='utf-8'))
a={c['id']:c for c in canonical['characters']}
b={c['id']:c for c in actual['characters']}
frozen={x['passage_key']:x for x in guard['passages']}
diff=[]
for cid,c in b.items():
 for sec in ('hearings','coming_clean'):
  for k,t in c[sec].items():
   fk=cid+'.'+(k if sec=='hearings' else 'final_'+k)
   assert frozen[fk]['baseline_quote']==a[cid][sec][k]
   if t!=a[cid][sec][k]:diff.append({'id':cid,'section':sec,'field':k,'before':a[cid][sec][k],'after':t})
assert diff==[{k:v for k,v in x.items() if k!='name'}for x in ledger['changes']]
pre=[x for x in diff if x['section']=='hearings']
assert len(pre)==35 and len(diff)==37
assert len({x['id'] for x in pre})==18
for cid in a:
 for k in ('evidence_innocent','evidence_murderer'):assert a[cid]['hearings'][k]==b[cid]['hearings'][k]
 assert a[cid]['coming_clean']['murderer']==b[cid]['coming_clean']['murderer']
assert actual['question_rounds']==canonical['question_rounds']
assert actual['pre_method_press_interview_opening']==canonical['pre_method_press_interview_opening']
perf=yaml.safe_load((src/'performance.yaml').read_text(encoding='utf-8'))
assert perf['metadata']['schedules']==[] and perf['fields']=={}
assert (src/'playable-evidence.yaml').read_bytes()==(base/'playable-evidence.yaml').read_bytes()
hashes={n:hashlib.sha256((src/n).read_bytes()).hexdigest()for n in ('confirmed.yaml','performance.yaml','procedure.txt')}
assert all(ledger['sha256'][n]==v for n,v in hashes.items())
keys=', '.join('`'+x['id']+'.'+x['field']+'`'for x in pre)
text='''# Candidate06 semantic review

**FAIL pending material-claim repairs.** Reviewed all 35 actual changed pre-vote fields against canonical full paired arcs and fact-guard; the exact 37-entry diff matches the ledger (35 hearings across 18 roles, two reviewed finales). No pressure-note classification, literary rating or trial score was used as proof. No source/candidate edits.

## Snapshot

'''
for n,h in hashes.items():text+=f'- `{n}` SHA256: `{h}`.\n'
text+='''
Hashes match the ledger. All 44 Method paragraphs (innocent and murderer), all 22 murderer finales, questions and press-interview opening are exact baseline. Evidence bytes are unchanged. The seven collateral deception arcs retain their original categorical denials and later corrections; altered surrounding rhetoric does not retract them early. Performance schedules/fields are empty. Procedure retains the original one-complete-answer guest chain and the already reviewed locked-ballots, named-innocents-first, murderer-last finale procedure.

## Must-fix material drift

1. **01.where_murderer — action ownership:** “I sent my refusal to the board” becomes “My refusal went to the board.” Delivery still occurs, but Artie's own sending action is no longer asserted. Restore “I sent”; do not substitute unknown delivery agency. The new present difficulty and cut tidying commentary are permitted emotional changes.

2. **06.motive_innocent — medium and attribution:** “I made the film” becomes “I made Donor Collapse,” losing the explicit film medium at Motive. A falling jacket could now denote a live work until later disclosure; film versus live stunt is materially important to this route. Restore “film” here. “Grant ... thought my name distracted” also becomes “apparently my name distracted,” dropping the attributed owner of that thought and changing its epistemic framing. Preserve Grant's stated attitude rather than supply unattributed apparent fact.

3. **07.motive_innocent — repeated historical act:** “He kept exhibiting the early picture” becomes “the early picture Grant exhibited.” Repeated invitations to explain it survive, but repeated exhibiting does not. Restore “kept exhibiting”; this is ongoing donor leverage, not merely a clever coda.

4. **13.where_innocent — closure sequence:** Canon closes/lights off before the requests, Anne's arrival and turning everyone away. Draft opens with the turnaway, recounts requests/arrival, then says “I closed the alcove.” That can put closure after the encounter. Retain the earlier closure explicitly, e.g. “I had closed ...,” without changing the turnaway or supplying an extra visit.

5. **13.where_murderer — action ownership:** “I closed the alcove and killed the lights” becomes “The alcove was closed and the lights were off.” State that Frank performed both actions. Preserving the resulting state and Chip's causal objection is insufficient to preserve the actor.

6. **18.where_murderer — specific handling:** “I unfastened the top panel” becomes “I took the top panel down.” Retain the stated unfastening; unspecified removal does not preserve the particular handling action. Transport, rolling beside the place, absent Grant, departure and Frank's historical instruction otherwise survive. The borrowed-maker metaphor may become a present stance as authorized.

7. **19.where_murderer — qualification:** “apparently I was supposed to find wording” becomes “I was supposed to satisfy both.” Restore “apparently.” It may be sarcastic, but deleting it strengthens the asserted assignment. This is the same certainty defect previously identified, independently present in this new draft. All caption/intake handling survives.

8. **20.where_innocent — new simultaneity:** Draft makes refusal and crossing out bronze occur “while Frank shut the alcove.” Canon specifies only the credit argument as simultaneous with closure; refusal/correction are separately narrated before it. Remove the newly attached simultaneity and retain the original action relationship. The replacement crew's cost and historical “reopen ...” demand survive; that demand stays reported speech, not a live instruction.

9. **29.where_innocent — action ownership:** “I gave counsel the deed and the settlement together” becomes “Counsel got ... together.” Restore Justin as the person giving them. Receipt alone allows an unprovided intermediary. The added current desire to tell the interesting part is permitted.

## Two narrower implication risks

- **09.where_murderer:** “A glass and the speech card” becomes “speech card beside a glass.” This adds a precise spatial relationship rather than simply listing objects found at the place. Prefer the original object list; do not build an inference from newly asserted adjacency. The request remains before preview, and the new desire to discuss the query is an allowed present stance.
- **28.where_murderer:** “what that silence was going to cost” becomes “what his silence would cost.” The possessive narrows the original ambiguous silence toward Grant's withheld disclosure rather than the unanswered waiting scene. Avoid implying a new price-for-confidentiality negotiation; retain “that silence” unless explicitly authorizing this interpretive change. No new actual demand or transaction is otherwise asserted.

## Accepted scope and branch risks

The remaining changes preserve material propositions in their full arcs. Claire's new present avoidance, Art's wish not to explain, Barb's wish for a useful task, Robin's present anger, and shortened moral self-analysis need not restore every original rhetorical clause. Al's metaphor about moving Grant and Justin's rebuttal self-judgment may likewise be cut without inventing actions. Dada's revised rehearsal remains a past cruel answer, not a delivered reply. Mona's “when I circulated” keeps the same questioning occasion. Anne's existing tour/Method conflict remains untouched; no group alibi is repaired into truth.

No new witness, supervision, alibi, physical transfer, forensic certainty or historical conversational reply was found beyond the specific drift/implication issues above. Changing a speaker's present stance does not license another actor's reaction. Single-turn delivery means no response may rely on another guest having spoken first.

Branch-style risk is unproven, not a semantic failure: selective new present-tense codas and shortened metaphor differ between paired branches (notably Artie, Claire, Art, Barb and Justin). They do not consistently identify the murderer, but an independent blinded whole-cast review should check that current emotional stance or narrative tidiness has not become a branch label. This report supplies no aesthetic grade or solve-rate prediction.

## All 35 covered keys

'''+keys+'''

The two changed finales remain the already reviewed Frank vocative removal and Reed's expressly authorized ambiguity resolution. That permission does not waive historical-action or certainty requirements elsewhere. Repair into a new frozen snapshot and recheck its actual assembled hash; this snapshot is not passed.
'''
assert len(text.split())<=1400,len(text.split())
(run/'candidate06-semantic-review.md').write_text(text,encoding='utf-8')
print('Saved candidate06-semantic-review.md;',len(text.split()),'words; 35 fields; FAIL; 9 must-fix items plus 2 implication risks.')
