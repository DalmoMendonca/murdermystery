import hashlib
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
run = root / 'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
source = root / 'source/connected_release/confirmed.yaml'
canon = yaml.safe_load(source.read_text(encoding='utf-8'))
draft_path = run / 'draft-finales.yaml'
draft = yaml.safe_load(draft_path.read_text(encoding='utf-8'))
guard = json.loads((run / 'fact-guard.json').read_text(encoding='utf-8'))
originals = {c['id']: c for c in canon['characters']}
frozen = {p['passage_key']: p for p in guard['passages']}
assert len(draft) == 8
assert all(list(branches) == ['innocent'] for branches in draft.values())
assert all(originals[cid]['coming_clean']['innocent'] == frozen[cid + '.final_innocent']['baseline_quote'] for cid in draft)

reviews = {
 '07': ('RISK (non-evidentiary wording only)',
        'The homicide denial, wooden model/glass loan, delivery-list distinction, withheld reproduction permission despite outstanding payment, and inflated early-work story remain word-for-word. The debt of a conversation remains. Replacing a request to bring paintings with a wish is within the authorized social-aftermath revision.',
        '“I\'d been hoping to see the bad student paintings again” adds a prior hope and the implication of having seen these paintings before. Canon establishes an interest in recovering student-era effort, not that specific prior viewing. This is no new murder clue, witness or materially different motive; it is a small autobiographical addition. For strict minimality, remove “again” or use “I had wanted to remember what trying felt like.” Do not describe the new past-perfect hope as an exact retained fact.'),
 '08': ('ACCEPTABLE',
        'The denial, master withdrawn at the public desk, continuing private service, board objection carrying earlier bad advice, and admission of delayed challenge are unchanged. Continued dispute over the letter is already explicit in the innocent Opportunity and preserves Sue\'s own judgment rather than granting her new knowledge of Mona\'s confession.',
        'The trip home changes from a present desire to a dislocated wish; neither version establishes a completed trip. “We ought to be going home together” does not claim that Mona is free to leave. The new uncertainty is Sue\'s emotional state, not uncertainty about the legal objection or crime facts.'),
 '09': ('ACCEPTABLE',
        'The dated query, original-contents condition, unresolved intake response, decision to allow entry and Reed\'s deserved credit remain unchanged. The dinner disclosure remains in the innocent post-vote finale. Recasting the disguised invitation as an embarrassed account of trying to invite Dada preserves the existing fact and ownership of the intention.',
        'The original “You need not answer it tonight” is replaced by “This is hardly the moment”; there is no new answer, acceptance, prior dinner, mutual attraction or corroborating event. This is an authorized change in social posture, not a changed source-knowledge claim.'),
 '13': ('ACCEPTABLE',
        'The plan/installed-room distinction, open adjoining bench, absent glass front, uncalculated mount approval and subsequent load removal all remain exactly. Elle\'s retrieval remains conditional on safe movement. The instruction to leave the space empty also remains.',
        'Removing the “Production” vocative changes the instruction\'s addressee specificity, not the identity of a witness, safety finding or past action. Do not stage the instruction as newly obeyed or as proof that Elle can lawfully leave after a confession.'),
 '18': ('MUST-FIX (narrow sequence/destination omission)',
        'The homicide denial, weave passing the glass, real preview bottle, correct merchant line, diverted other-client advance, repeated denial and unrepaid debt remain exactly. Removing Chip\'s offered packing role is within authorized social-request changes and does not affect the earlier glass access.',
        'The canonical statement is “I have to go home with the thing I actually made, then call the person who paid for something else.” The draft instead says “The fabric still needs packing. Then I have to call the person who paid for something else.” Packing now supplies the antecedent of “Then”; the explicit departure home with the fabric before the call is lost. Under the instruction that sequence remain, restore that destination/ordering without restoring a social assumption about Chip. Minimal repair: “The fabric still needs packing. I have to take it home, then call the person who paid for something else. I don\'t know how to begin that call.” This does not invent a return: it retains the original stated intention, not a completed journey.'),
 '19': ('ACCEPTABLE WITH DISCLOSED AMBIGUITY RESOLUTION',
        'The marked proof\'s full-intake/shortened-press distribution remains. The removed warning, completed page, credit claim, wish to stop depending on Claire\'s approval and intended uncut transmission remain. “It wasn\'t a space problem” repeats innocent Opportunity exactly; “I wanted Grant humiliated” paraphrases the already disclosed intended “public disgrace” and deliberate harmful-caption publicity, not an invented motive.',
        '“I removed a warning to finish a page” grammatically gives finishing as a purpose; “I finished that page by removing a warning” makes removal the means and avoids that purposive reading. The revised finale therefore is not proposition-for-proposition identical in its treatment of the isolated ambiguous purpose phrase. It preserves the full arc\'s already explicit non-space, retaliatory intention and introduces no new action, knowledge, evidence or chronology. Given the current express authorization to repair this tension, acceptable; report it as an ambiguity resolution, not proof that the old ambiguity was untouched. Removing “Those are separate things” does not merge credit with moral judgment: the two desires remain separate sentences.'),
 '23': ('ACCEPTABLE',
        'The innocence claim, individual drink flavoring under the paid order, distinction between ingredient/pitcher tests and another person\'s contamination, unpaid extra-course purchase, staff transport needs and earned release remain exactly. The draft does not retract her unsupervised preparation or turn the ordinary ingredient into poison.',
        'The assumed next-day argument with Monet becomes the continuing existence of the bill tomorrow, already entailed by the explicitly unpaid purchase. No payment, liability transfer, new funding or canceled private service is introduced.'),
 '29': ('ACCEPTABLE',
        'The corrected name rather than contents, knowingly omitted settlement, current-theft headline and completed public correction/full-folder inclusion remain exactly. Both former occupants and settlement still belong in the tour; the longer version still requires time.',
        'The original promises a shared earlier start; the draft requests sufficient time without requiring a future outing with Anne. “Those people don\'t owe me a brilliant headline” remains Justin\'s ethical judgment, matching his wish for remembrance beyond a dramatic story. It supplies no new historical fact or claimant permission.'),
}

parts = [
 '# Finale semantic review — eight selective innocent endings',
 '',
 'Reviewed 2026-10-27. Independent semantic scope only: every revised finale was compared with its complete canonical innocent/murderer arc and its frozen fact-guard quote. The draft notes were read for the stated change scope. No literary grading, prior trial scores, other judge reports or new clues were used. No canonical source was edited.',
 '',
 'The supplied verified host procedure is the governing context: top three suspects read in descending vote order (alphabetical tie-break), innocent endings continue after a confession, with the stated fallback where required. This review does not assume all 21 innocent endings are performed. It assesses the proposed social-aftermath revisions under the express permission to alter future wishes/requests while preserving material facts, mechanism, collateral retractions, certainty and sequence.',
 '',
 f'Canonical byte SHA256: `{hashlib.sha256(source.read_bytes()).hexdigest()}`. Draft byte SHA256 at review: `{hashlib.sha256(draft_path.read_bytes()).hexdigest()}`. All eight canonical finale quotes equal their fact-guard originals. Every draft entry is an innocent finale; no murderer ending or pre-vote entry is included in this draft.',
 '',
 'Result: one narrow must-fix (Elle\'s home/fabric-before-call sequence), one non-evidentiary wording risk (Vincent\'s added “again”), five straightforward acceptances, and one acceptance requiring candid disclosure that an existing ambiguity is being resolved (Reed). All eight retain their innocence assertions and the homicide-relevant assertions present in their original finales. Elle\'s collateral retraction remains intact; its later stated departure/call order needs restoration.',
 '',
 'Draft-notes accuracy: the notes correctly distinguish post-vote social posture from mechanics and do not justify a blanket finale rewrite. Their blanket claim that staging remains protected should be narrowed until Elle\'s explicit homeward sequence is restored. Their Reed rationale is supported by the full canonical innocent arc, but should say this resolves a purposive ambiguity rather than claiming no semantic interpretation has changed.',
 '',
]
for cid, branches in draft.items():
    verdict, retained, concern = reviews[cid]
    parts.extend([
       f"## {cid} — {originals[cid]['name']} — {verdict}", '',
       '**Original innocent finale**', '', '> ' + originals[cid]['coming_clean']['innocent'], '',
       '**Proposed innocent finale**', '', '> ' + branches['innocent'], '',
       '**Preservation assessment:** ' + retained, '',
       '**Risk / required action:** ' + concern, '',
    ])
parts.extend([
 '## Scope limit', '',
 'This is a semantic review of the eight saved proposals at the recorded hash. It neither approves pre-vote ensemble changes nor validates a later edited draft automatically. The limited social-posture permission overrides the frozen guard\'s literal retention of future requests; it does not permit new past events, forensic certainty, alibis, admissions, witness knowledge or a changed crime sequence. Suggested wording is review advice only and has not been inserted into canon or the draft.', '',
])
(run / 'finale-semantic-review.md').write_text('\n'.join(parts), encoding='utf-8')
print('Saved finale-semantic-review.md; 8 originals/drafts, 1 must-fix, 1 risk, 6 acceptable including Reed qualified acceptance.')
