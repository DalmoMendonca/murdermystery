---
title: Round 18 continuity and dialogue review
status: partial-candidate-audit
scope: ten complete core roles and twelve available other roles
---

# Continuity review — spoilers

The candidate needs revision before freezing. This review covers all eight speeches for core IDs 01, 04, 05, 06, 09, 10, 11, 12, 20 and 23, and the available eight speeches for other IDs 02, 03, 07, 08, 13, 14, 15, 16, 17, 18, 19 and 21. Other-dialogue was marked incomplete and ended at Ella on the final read. No conclusion is made about the eight unavailable roles. No build selections, test identities or reader scores were inspected for this audit.

The Game Narrative, Genre Craft mystery fair-play, Line Editing and Voice & Style guidance informed the checks. Public character copy and the public fields of source/characters.json remain the canon; this report proposes private changes only.

## Blocking issues

1. **Act II has a guilty-only identifying template.** Every core murderer opportunity speech volunteers a broken favor: Artie lines 28–29, Monet 88–89, Chip 149–150, Dada 214, Art 277–278, Tess 340–341, Barb 404–406, Paige 469–470, Al 536–537 and Brie 605–607. None of the innocent counterparts volunteers the same explanation. All twelve available other murderer opportunity speeches do it too. Avoiding the fragment's color and recovery location does not remove this tell: one guest still supplies the same conspicuous bottle accident in every selected world. The candidate's retained exhibit-before-Method order is an explicit choice in STORY.md, not an accidental sequence error; its early planting nevertheless makes this structural problem unavoidable in the present text. **Fix:** plant several consequential, nonexclusive ordinary gift/material incidents in both branches, with a later role-specific contradiction; or follow the architecture's fallback and make the fracture identify only the route while a separate, preplanted account supplies contested attribution. Merely moving or rephrasing the unique aside is insufficient.

2. **Vincent's ending contradicts death after the toast.** other-dialogue.yaml lines 169–170: “I killed him before he drank that clean punch.” F2 says he became ill after drinking, and the fixed chronology has punch at 6:46 and toast at 6:49. **Fix:** “I poisoned his empty glass before the clean punch was poured. He drank it at the toast.”

3. **Several available other Method speeches confess the deception before Coming Clean.** Claire lines 52–54 says she called the gift broken to explain the mess and wants to stop evading; Mona 323–326 identifies her “other concealment” behind the sideboard; Elon 382 calls the broken-gift story deliberate distraction; Anya 439–441 says she kept quiet about what she did and invented an explanation for damage; Hugh 103–106 virtually abandons his miniature explanation. In combination with known contaminated objects and target-side bottle handling, these become author-supplied answers, rather than accounts players weigh. **Fix:** retain defensible, limited denials or competing explanations through Method; reserve explicit cover-story admissions for Coming Clean. Keep differences in how they evade, rather than making all eight collapse into the same increasingly candid confession.

4. **Sue personalizes an anonymous recovered bottle.** other-dialogue.yaml 209–212 moves directly from “I opened my miniature” to “It cannot be the broken object ... the recovered one is intact.” F5 expressly gives the recovered miniature no recipient name; F4 establishes intact condition only for that recovered object. The report cannot establish it was Sue's miniature or that no other favor broke. **Fix:** make her state her own claimed bottle condition or provenance, and leave the recovered bottle's ownership disputed. For example, “That recovered miniature is intact. You haven't established whose it was. I said I cleared broken material from my case.” Do not turn that proposed defense into an objectively certified fact.

## Candidate questions and future integration

Round18's actual input is packet-questions.yaml. Its broader Motive and Opportunity questions generally accommodate the new accounts; the former preparation-department prompts below are not active candidate defects. All Method questions are now identical: “What did you bring to the reception desk, and what was it for?” This produces conversational monotony and several indirect answers. Barb I begins with camera/alarm distinctions before eventually describing her officer's notebook; Brie I discusses Casey's collection and laboratory results before discussing the towel. Start with the requested object/action and let the forensic response follow, or give them a targeted service/record question.

Claire and Vincent's Opportunity prompt asks what they changed “while the unveiling was held.” Vincent describes taking the painting off its stand before opening, then placing the label at reception; distinguish the earlier removal from the later label errand. Claire's packet account does not firmly time label substitution; add a brief ordering phrase if it should occur during the hold.

Future integration must replace source/question_rounds.json, which still asks Sue about preparation contact and Hugh/Anya about first arrival. Those facts are absent from the new Opportunity replies. These are future source-integration mismatches, not mismatches in packet-questions.yaml.

Tess answers first entry in I and distinguishes earlier entry from later ticket collection in G. That is physically possible, but the branch difference is unusually explicit. Do not add a fixed receipt exhibit certifying first entry for both worlds.

## Core-role causal and suspicion checks

Each reviewed core innocent branch contains both damaging conduct and a contextual fact. These facts limit particular theories; none should be announced as whole-person clearance.

| Core role | Surviving suspicion | Mitigating fact |
|---|---|---|
| Artie | Forgery, substituted speech, unauthorized toast delay | Retained competing speeches and chair's refusal; gift remains subject to approval |
| Monet | Restricted-fund transfer, financial concealment, deliberate service gap | Supplier hold and unserved extra course; clean punch only narrows route |
| Chip | Altered insurance date, withheld receiving information, shove, tools at reception | Real photographed mount failure and harmless open-bottom replica |
| Dada | Threatening note, false cue authorization, staged collapse | Canceled cue and clear PROP glass distinguish performance from poisoning |
| Art | Prior poison knowledge, hidden request, delayed correction | Complete request seeks replica; opening refused; correction has a record |
| Tess | Trustee bluff, hidden rental stem, stolen signing pen | Claimed first-entry receipt after theft and removed rental stem; receipt remains contestable |
| Barb | Camera exception, suppressed incident detail, delayed hazard response | Independent alarm and retained collections objection |
| Paige | Threat, unauthorized search, withheld source page | Recorder preserves coercion; editor retains unredacted page; recorder supplies no hand alibi |
| Al | Altered support, threat to remove sculpture, actual target handling | Crew's earlier drawing and genuine invoice; unopened-favor claim is inspectable, not certified |
| Brie | Menu substitution, threat to halt service, deliberate vacancy and target handling | Supplier label and clear food narrow fraud/communal-route theories; towel explains outside fibers |

No reviewed core G branch imposes a continuous alibi excluding the 6:12 theft or 6:32–6:44 glass exposure. Their errands can follow the 6:35–6:37 mount hold and still reach the sideboard before collection at 6:44. No speech requires access through a valid cabinet key; forcing the lock and secondary case remains consistent. The source, transport in a common favor, exposed individual glass, later clean punch, and hiding place fit the stated crime. There are no preparation instructions in the reviewed dialogue.

Barb's “afterward” in I and “later” in G are vague about whether Casey was still at reception. Clarify that the request to clear the sideboard preceded Casey's kitchen trip or was delivered by radio. This is staging ambiguity, not an established impossible alibi.

Paige's Method account places an argument with Grant's assistant after recorder recovery although Opportunity places the coat search earlier. A second exchange is possible; add “again” to the later argument if that is intended.

## Naturalism and locked voice

Occupational concerns differ, but Method and innocent endings repeatedly adopt the same articulate evidence counsel voice: “not an alibi,” “doesn't clear me,” “retained record,” and a tidy commitment to disclose wrongdoing. This exposes the author's balancing instructions. Other Anya explicitly tells players not to turn age into an alibi; Elon measures his phone message against twelve minutes; Frank explains how to distinguish console and reception access. These lines should become concrete conversational resistance rather than explanations of game inference.

Use the sent acting tips to change behavior: Sue narrows one question; Barb supplies a brief remembered instruction; Paige asks who has heard the recording; Hugh bargains about which document is released; Elon talks too confidently about what he can arrange; Anya interrupts an indulgent premise rather than announcing the alibi rule. Keep Art's professorial expansion and Dada's theatricality because those are specific public traits. Brie's reply should issue a service instruction or demand the balance, rather than close with a general moral about workers.

No direct contradiction with locked public roles, relationships or Paige's reporting integrity was established in these twenty-two roles. Do not rewrite sent invitations or character sheets to solve the private dialogue problems. All I statements remain contestable claims. A fair-play review does not require promising innocent guests tell the truth.

F4/F5 correctly establish source material, contamination and intact condition for the recovered miniature. They do not establish a recipient, exclusive custody, theft by the person describing a parcel, or poisoning by that person. Final accusation reasoning must compare personal statements to those limited exhibits and admit the surviving transfer/clutter alternatives. The speech template presently supplies more identifying certainty than the objects do.


## Additional available rows

Saul, Elle, Reed and Ella also have suspicious innocent actions and limited contextual support: omitted discretion fee with an unabridged invoice; unauthorized textile removal with a prior family return demand; forged correction and poison-inventory inquiry with a dated research scan/refusal; sold promised painting and altered card with registrar correspondence. Ella explicitly admits glass contact in I. None of these records excludes either crime window, and none should be presented as chemical or temporal clearance. No further hard physical contradiction was established in these four rows.

This is a snapshot of files under active writing. Root has elected to remove the guilty-only broken-favor aside from all Opportunity speeches and keep later attribution contestable. That change will address finding 1 only when the actual new speeches are audited; this report does not certify edits it has not read.

## Revised audit of compiled thirty-role candidate

This addendum supersedes the initial snapshot where edits have resolved its findings. Read input: compiled dialogue.yaml, compiled investigation_copy.yaml, and line_edits.yaml; all thirty guilty Opportunity speeches and the remaining eight complete roles (22, 24–30) were checked. No selection or reader result was used.

**Remaining freeze blocker:** Anya's compiled Method reply, dialogue.yaml lines 713–717, still says she kept quiet about what she had done that evening and that the broken gift explained damage she hoped nobody would examine. This retains the premature deliberate-cover admission identified above. Replace it with a resistant account of moving the ledger/glass and handling ordinary materials, without acknowledging concealment of the crime. Reserve that acknowledgment for Coming Clean.

**Small corrections:** Hugh's compiled Method begins “I arrived before collecting the ticket. I said so.” Neither earlier compiled speech says that. Remove “I said so” rather than inventing an earlier exchange. Faye's Method says the editor's dated saved preview establishes that the print existed; a saved image establishes the image/file existed, not the physical print. Change to “Its date establishes the image existed.” Neither correction affects the opportunity windows.

The guilty-only broken-gift account is absent from all thirty Opportunity replies. No dangling early scraps/gift cleanup reference remains from the removed sentences. Tess still breaks a rental glass in both branches, which is an ordinary shared event; it is not a guilty-only favor incident. Vincent now distinguishes the earlier painting removal from the later label visit, and his ending describes poisoning the empty glass before clean punch was poured. Sue now expressly disputes ownership of the anonymous intact miniature. The seven revised Method accounts no longer explicitly confess deliberate deceptive cover.

No new hard contradiction with the 6:12 forced-cabinet theft, the 6:32–6:44 individual-glass window, clean punch at 6:46 or toast at 6:49 was established. The reviewed guilty accounts do not create an impossible continuous alibi. Claims denying original possession or criminal handling in Method are suspect defenses, not objective facts binding Coming Clean. No preparation instructions were introduced.

| Final eight roles | Murder-related innocent mitigation, with limits |
|---|---|
| Drew | Editor's prior proof/withdrawal supplies a reason for secretive page retrieval; does not locate him continuously |
| Cary | Courier picture identifies frame damage; original receiving image distinguishes legitimate trolley work from later theft |
| Anne | Petition versions support political obstruction and explain altered endorsement; bookings do not certify attendance |
| Faye | Prior saved full image explains print retrieval and cropping; clear FIXER excludes only that proposed material |
| Robin | Printer order and board refusal substantiate a planned unauthorized paper protest; legal exposure continues after death |
| Penny | Earlier solicitor receipt and full fourth letter explain selective family evidence; intermediary detail complicates the ownership dispute without clearing target access |
| Justin | Full audio identifies the threatened object as a wall; prior corrected lease explains his errand and his concealed source |
| Minnie | Console records show the blackout canceled at 6:37; florist's note supplies payment context; neither eliminates her admitted glass contact |

All thirty innocent branches now have damaging conduct and at least some contextual mitigation. No full alibi or innocent-truth guarantee is required or asserted. The last eight preserve their sent occupations and character premises: critic/podcaster, handler, educator, photographer, nonprofit organizer, collector, local-history blogger and event producer. No direct locked-public-canon contradiction was established.

The revised attribution mechanism is weaker and later than the initial draft: the selected guest claims miniature access and target handling after the forensic reports, while contextual records corroborate limited ordinary actions. Those admissions can increase suspicion; they do not independently establish whose common miniature was contaminated, who owned the favor paper, or who carried the source fragment. In several worlds there is no prior individualized false account that the fracture objectively contradicts. The fracture establishes the source and supports the route, and a suspect can plausibly argue another person's discarded material or earlier contact. Any final leader is therefore a comparative inference from claims, motives and opportunity, not an independently proven physical match. The candidate must describe that limitation honestly; a fresh reader may reasonably remain undecided.

The repeated polished forensic defenses remain a naturalism risk, especially the all-role distinction between a limited record and a whole-person alibi. That is a craft/test concern rather than a newly established physical blocker. Root's future source-question integration remains separate from the active packet-questions.yaml input.
