import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source/connected_release/confirmed.yaml'
EVIDENCE = ROOT / 'source/connected_release/playable-evidence.yaml'
PRIOR = ROOT / 'docs/playtest/2026-10-26-DRAMATURGICAL-01-SPOILERS/semantic-obligations.json'
OUT = ROOT / 'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
data = yaml.safe_load(SOURCE.read_text(encoding='utf-8'))
prior = json.loads(PRIOR.read_text(encoding='utf-8'))
prior_chars = {c['id']: c for c in prior['characters']}
evidence = yaml.safe_load(EVIDENCE.read_text(encoding='utf-8'))
stages = {'motive': 'motive', 'where': 'opportunity', 'evidence': 'method', 'final': 'coming_clean'}

# These are constraints, not alternate prose or a repaired chronology.
focus = {
 '01': ['Naming, departmental votes and resignation remain proposed donor terms; Monet/payroll and Sue/objecting remain attributed.', 'Public refusal and private access remain distinct; innocent board call is alone by request to Barb; murderer straightens chair beside waiting glass.'],
 '02': ['Earlier bowl approval and Reed challenging teacher remain Claire\'s own fault; murderer Grant retains signature and leverage.', 'Bowl label removed, bowl stays; Reed keeps old text; bottle papers move to intake under hold; murderer personally moves glass off paper.'],
 '04': ['Wages Friday; donor inspection of transfers; murderer restricted transfers face board scrutiny, not an accepted rescue.', 'Innocent takes donor ticket personally and removes transfer slip; murderer sends ticket back with manager then makes separate signature visit.'],
 '05': ['Recent repair versus demanded ancient description; insurance date leverage remains branch specific.', 'Band fitted before preview; condition sheet distinct from insurance copy; murderer visits after preview, lifts glass, returns it, then attends mount problem.'],
 '06': ['Film is empty jacket falling; credit/ownership dispute with Grant; Vincent knows earlier work, not homicide.', 'Innocent shows coordinator film privately at set place; murderer claims gallery-only showing and denies private chair/glass visit.'],
 '07': ['Early painting, bottle-study publicity and withheld reproduction permission; murderer final-payment leverage remains explicit.', 'Sale photograph and separate studio lighting model; murderer preview attendance then private delivery of unsigned release beside waiting glass.'],
 '08': ['Unsigned gift before board vote; future acquisition control; earlier ownership advice carries murderer leverage.', 'Public master withdrawal and private donor copy remain different documents; murderer physically lifts glass to retrieve donor copy.'],
 '09': ['Reed\'s citation finding; Grant wants early press copies; Dada interest is speaker\'s own feeling, not Dada\'s reply.', 'Innocent knows original-contents/cyanide conflict and allows preview; murderer query retained then private speech-card visit, glass present, Grant absent.'],
 '11': ['Privacy exception; murderer false-fault log as donor leverage; visiting crews differ from permitted staff.', 'Museum/catering access remains; innocent admits fault entry and Artie use; murderer alone room/latch check, door reopened, no new recording.'],
 '12': ['Unsupported sentence needs correction; source protection; Justin folder; no source identification.', 'Recorder retrieved from Grant coat without permission; editor keeps original, critic gets short export; murderer asserts cloakroom-only checking.'],
 '13': ['Uncalculated mount, naming plaque and next commission/insurer pressure; chair-position habit does not add an observed event.', 'Closed alcove distinct from preview bench; innocent turns away Elle/Al/Anne; murderer separate empty-room seated visit.'],
 '14': ['Innocent asserts ministry authority; murderer knows claim letter and supplier commission provide leverage; Sue questions authority.', 'Sealed water requested; innocent circulates letter and defends heading; murderer brings letter privately, puts under glass edge, Grant elsewhere.'],
 '15': ['Platform/collection/customer-list proposal; dealer purchase photo exclusion; murderer installation/demo gap and funding exposure.', 'Phone sample/demonstration distinct from actual camera connection; innocent also tries panel at unattended prepared place; murderer does same seeking approval.'],
 '18': ['Pattern rights for early payment; innocent denies diverted advance, murderer admits diversion; no rewrite repays debt at an invented time.', 'Panel removed after alcove closure, lamp close; transported through private room and rolled beside prepared place; murderer separate pattern slides retained.'],
 '19': ['Missing bowl document/correction and desired credit; doctorate threat in murderer branch; teacher approval is not new evidence.', 'Innocent deliberately cuts original-contents warning for publicity disgrace, not space; full intake file remains; murderer caption visit beside glass, paper removed again.'],
 '20': ['Cold-cast resin with metal powder versus bronze publicity; final payment, donor credit, home caregiving stakes.', 'Label correction and closed alcove remain; murderer private visit after preview sits beside glass, leaves before Grant returns.'],
 '23': ['Extra cheese course is unfunded/disputed, original private toast paid; supplier liability belongs to Brie.', 'Innocent personally flavors glass alone and retains container with service; murderer takes flavoring to place, later retains container; no invented supervisor.'],
 '24': ['Frame-report leverage and demand for unchecked signature; previous job loss; innocent calls damage old, murderer admits own crack.', 'Sealed bottle delivered to intake with frames; shop gifts to service; label inert is lender report; private report retrieval and waiting glass; murderer handles carton.'],
 '25': ['School promise precedes approval; patron-preview replacement; murderer continuing budget threat is not solved by one visit.', 'Innocent handout retains Reed footnotes and admits unmet funding; tour turns at alcove; murderer also makes separate private handout visit.'],
 '27': ['Intact bowl return OR hearing; exclusion/disruption stakes, not permission to destroy; Barb removal history remains.', 'Innocent petition interrupts Paige and retains bowl card; murderer asserts public-podium interview and denies private entry; do not make this narration true.'],
 '28': ['Family valuation versus dealer price; innocent says damaged piece, murderer admits intact object and dishonest comparison.', 'Innocent collar impression corrected by Chip during preview, no request to open; murderer preview then private comparison beside waiting glass.'],
 '29': ['Settlement omitted from headline; deed/purchase/missing payment remain; murderer records/confidentiality pressure, not erased historical wrong.', 'Deed AND settlement reach counsel; old clipping circulated; murderer privately brings folder, writes/tosses note, takes folder away; no new witness.'],
}

collateral_stages = {
 '04': ['where', 'evidence'], '05': ['where', 'evidence'],
 '14': ['motive', 'where', 'evidence'], '15': ['where', 'evidence'],
 '18': ['motive', 'where', 'evidence'], '24': ['motive', 'where', 'evidence'],
 '28': ['motive', 'evidence'],
}
early_murderer_lies = {
 '06': 'Gallery-only coordinator encounter and denied private-room visit remain deliberate cover, not a true alibi.',
 '12': 'Cloakroom-only checking/private-place denial remains a deliberate cover claim, not independently witnessed fact.',
 '27': 'Public-podium interview and denial of private entry remain deliberate cover; original recording contradicts location.',
}

records = []
for c in data['characters']:
    old = prior_chars[c['id']]
    passages = dict(c['hearings'])
    passages.update({'final_' + b: t for b, t in c['coming_clean'].items()})
    for key, quote in passages.items():
        assert old['protected_baseline_passages'][key] == quote, (c['id'], key)
        prefix, branch = key.split('_', 1)
        stage = stages[prefix]
        path = f"characters[{c['id']}]." + (f'coming_clean.{branch}' if prefix == 'final' else f'hearings.{key}')
        # Conservatively retain every source statement, including fragments, vocatives,
        # qualifications and rhetorical questions. These are quoted claims, not verdicts.
        units = re.split(r'(?<=[.!?])\s+(?=[A-Z“\"\'])', quote)
        nonnegotiables = [
            {'ordinal': n, 'claim_as_originally_spoken': unit,
             'requirement': 'Retain its proposition, negation, tense, modality, attribution, speaker and branch at this stage; quoted assertions are not automatically true.'}
            for n, unit in enumerate(units, 1)
        ]
        status = []
        if prefix == 'evidence' and branch == 'murderer':
            status.append('Contains deliberate homicide-cover lie specified in murderer_method_guard; preserve true concessions as true concessions.')
        if branch == 'innocent' and prefix in collateral_stages.get(c['id'], []):
            status.append('Contains or sustains the innocent collateral deception specified below; do not turn it into honest uncertainty or retract before finale.')
        if prefix == 'where' and branch == 'murderer' and c['id'] in early_murderer_lies:
            status.append(early_murderer_lies[c['id']])
        if prefix == 'final':
            status.append('Post-vote admission/correction and emotional consequence; cannot be moved into an earlier hearing or another branch.')
        if not status:
            status.append('Preserve claim-level mixture exactly; do not infer global truth from branch or replace attributed belief with objective fact.')
        required = focus[c['id']][0 if prefix == 'motive' else 1] if prefix in ('motive', 'where') else (
            old['guilty_method']['protected_claims'] if branch == 'murderer' and prefix == 'evidence' else
            old['guilty_method']['post_vote_resolution'] if branch == 'murderer' and prefix == 'final' else
            'All quoted source assertions below remain binding; homicide innocence does not erase personal fault, prior concealment, restricted access, or stated evidence limits.')
        records.append({
            'passage_key': f"{c['id']}.{key}", 'source_path': path,
            'character_id': c['id'], 'speaker': c['name'], 'branch': branch,
            'stage': stage, 'vote_timing': 'post_vote' if prefix == 'final' else 'pre_vote',
            'baseline_quote': quote,
            'baseline_quote_sha256_utf8': hashlib.sha256(quote.encode('utf-8')).hexdigest(),
            'concrete_stage_obligation': required,
            'non_negotiable_claims': nonnegotiables,
            'speaker_certainty': 'Exact original qualifiers in each quoted claim control: firsthand I saw/did/checked, attributed label/document/source, I thought/believed/looked, requests, denials and rhetorical questions must retain distinct force. Bare assertions stay categorical; a lie cannot become a guess.',
            'knowledge_ownership': f"{c['name']} owns the first-person actions, memory, beliefs and admissions. Named addressees do not thereby witness or know those actions. Quoted third-party/document claims stay attributed to that party/document; do not promote a report or request into corroboration.",
            'admissions_vs_lies': status,
            'murderer_method_guard': old['guilty_method'] if prefix == 'evidence' and branch == 'murderer' else None,
            'innocent_collateral_guard': old['innocent_collateral_lie'] if branch == 'innocent' and c['id'] in collateral_stages else None,
            'finale_guard': {'preserve_all_assertions': True, 'no_early_reveal': True,
                             'murderer_resolution': old['guilty_method']['post_vote_resolution'] if branch == 'murderer' else None}
                            if prefix == 'final' else None,
        })

assert len(records) == 176
assert len({r['passage_key'] for r in records}) == 176
assert sum(r['vote_timing'] == 'pre_vote' for r in records) == 132
assert sum(r['murderer_method_guard'] is not None for r in records) == 22
assert len(collateral_stages) == 7
guard = {
 'schema_version': 1, 'visibility': 'private_author_only_spoilers',
 'purpose': 'Independent semantic guard for fact-preserving ensemble rescue. Canonical source only; no rejected candidate, judge review or reader scores consulted.',
 'baseline': {'path': 'source/connected_release/confirmed.yaml',
              'sha256_bytes': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'passage_count': 176, 'pre_vote_count': 132, 'finale_count': 44,
              'evidence_path': 'source/connected_release/playable-evidence.yaml',
              'evidence_sha256_bytes': hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
              'quote_crosscheck': 'All 176 canonical source strings equal protected_baseline_passages in prior semantic obligations; prior candidate strings were not read or used.'},
 'scope_and_limits': 'Exact original quotes and enumerated source statements are exhaustive claim retention constraints, not a logical proof or a fully normalized truth table. Sentence units deliberately retain fragments, rhetorical and emotional claims. Manual stage constraints and lie guards supplement the quotes. Ambiguities are preserved, not adjudicated.',
 'global_non_negotiables': [
   'Keep 22 routes, six pre-vote and two post-vote passages per speaker. The selected innocent/murderer box remains branch-local; do not expose both branches as one testimony.',
   'Do not move assertions to another speaker or stage. Addressing Claire/Chip/Monet/etc is not permission to give that person firsthand knowledge, agreement, a reply or a witnessed alibi.',
   'Public announcement desk, private donor room, kitchen, cloakroom, closed alcove, open adjoining preview bench and staff-accessible cupboard remain distinct places.',
   'Preview 6:20–6:28 precedes 6:32 glass setup; 7:04 collection, 7:06 kitchen pour, 7:09 direct service; the 6:15 Monet story is false, not an alternate clock.',
   'Gift unsigned/unaccepted; donor proposals not enacted decisions. Refusal/public announcement cancellation does not cancel paid private hospitality or cheese charge.',
   'Seller requires original contents and fulfills sale; lender says inert; intake has unresolved query/keep-closed restriction. Empty, inert, original contents and verified harmless are not interchangeable.',
   'Physical historical bottle on open preview support; no fixed glass front, wooden replacement or bottle projection. Rear band split differs from front view. Red foil-backed paper is similar stock, never a unique torn-edge fingerprint.',
   'Cyanide in individual crest glass and bottle residue; not shared punch/food. Ordinary flavoring in glass and retained ingredient, absent pitcher; ingredient is not itself proven poison.',
   'Engraved glass unwrapped and used; water remains sealed. Power removed and network left: no local recording, no live camera panel. Saved demo image is not a witness.',
   'All 22 murderer Method claims retain deliberate-cover status and same strength, concessions and contradictions; all seven innocent collateral lies retain denial then post-vote correction.',
   'Murderer finales retain preview extraction followed by private-glass poisoning and their specific false account/rebuttal. No new timing, witness, access exclusivity, clue or forensic certainty.',
 ],
 'preserved_ambiguities': [
   'Reed innocent opportunity denies a space problem and calls omission deliberate; innocent finale says removed a warning to finish a page. Preserve both original assertions; do not repair intent by choosing one.',
   'Grant summons/requests and undocumented feelings are speaker claims, not newly corroborated communications.',
   'The institutional risk, staff access and ordinary cupboard keys do not single out a culprit. Scrap similarity is not a unique match.',
   'Dates in treatment and proof exhibits remain exact source dates, even when apparently awkward against external calendar context; no chronology repair authorized.',
   'Full future certainty, apology, emotional motive and hypothetical reactions remain claims at their existing strength; do not materialize them into offstage events.',
 ],
 'innocent_collateral_character_ids': list(collateral_stages),
 'passage_keys': [r['passage_key'] for r in records],
 'passages': records,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'fact-guard.json').write_text(json.dumps(guard, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'passages': len(records), 'pre_vote': 132, 'finales': 44, 'method_lies': 22, 'innocent_collateral_lies': 7, 'sha256': guard['baseline']['sha256_bytes']}))
