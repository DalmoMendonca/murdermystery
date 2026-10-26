# Candidate 02 independent semantic review — author-only spoilers

Reviewed all 40 hearing fields listed in `change-ledger.json` against the candidate02 baseline-source and candidate-source YAML, candidate01 `semantic-obligations.json` (including exact protected baseline passages), and `source/connected_release/confirmed.yaml`. This is a factual preservation review, not a blind read, score, deduction test, or fairness certification. This reviewer is ineligible for later blind reading.

## Result

One narrow timing-preservation issue was found and is now closed after author revision. No outstanding must-fix findings. No newly invented witness, alibi, exculpatory observation, poison mechanism, or corroborating event found in the reviewed changes. All disputed guilty Method accounts remain disputed accounts, with their existing certainty and knowledge qualifiers; innocent collateral lies remain before the vote and their admissions remain in the unchanged endings.

### Closed finding: 04 Monet Bags / motive_murderer

Both candidate01 (`Friday is payday`) and original canon (`Friday. That's when wages are due.`) explicitly tie the wage deadline to Friday. Candidate02 says `Friday was coming` and later `Wages don't wait for an explanation`, which makes that connection inferential. Retain the explicit deadline in the same branch and stage, for example by changing `Friday was coming` to `Wages were due Friday`. This is a timing-preservation fix, not a claim that the passage creates a new alibi or makes a deduction fail. No source edits made by this reviewer.

Closure verified against the reassembled candidate-source YAML and updated change ledger: the passage now explicitly says `Wages were due Friday.` The ledger exactly matches the revised hearing.

## Verified mechanically

- Exactly 40 hearing values differ between baseline-source and candidate-source.
- The ledger describes that exact set, and all 40 before/after strings match their respective YAML values.
- Every `final_innocent` and `final_murderer` value is unchanged from the candidate02 baseline (candidate01).
- The five restored guilty Method replies—Sue 08, Barb 11, Paige 12, Elon 15, Brie 23—match the original canonical hearing strings exactly.

String equality verifies those facts only. The following stage/branch checks are manual.

## Field-by-field coverage

| Character | Field | Finding |
|---|---|---|
| 04 Monet Bags | `motive_innocent` | Friday/payroll, inspection terms, Artie contrast and rejected check retained. |
| 04 Monet Bags | `motive_murderer` | CLOSED: revised candidate explicitly says wages were due Friday; moved wages, mother, books, board and urgency retained. |
| 04 Monet Bags | `where_innocent` | Ticket/account crossing, donor copy, waiting glass/absence, slip removal and board-authorization lie retained. |
| 04 Monet Bags | `where_murderer` | Manager ticket, sent-back donor copy, off-agenda restricted transfer, books/signature, absence and wait retained. |
| 04 Monet Bags | `evidence_innocent` | Booked original toast, service instruction, donor extra-course payment and collateral payroll-authority lie retained. Personal service instruction restores original canon. |
| 04 Monet Bags | `evidence_murderer` | 6:15/6:32 dispute, unwrapped glass, claimed return before preview/no later return and separate cheese errand retained. |
| 06 Dada DiCapo | `motive_innocent` | Authorship, empty dinner jacket/gilded chair, commission/credit dispute, Vincent and planned discomfort retained; remembered-as-mine restores original. |
| 06 Dada DiCapo | `motive_murderer` | Foundation acquisition/name erasure, imposed gratitude, jacket film, Vincent knowledge and planned discomfort retained. |
| 06 Dada DiCapo | `where_innocent` | Private-room/coordinator visit, phone film, canceled cue, refusal again, prepared place and toast screen retained. |
| 06 Dada DiCapo | `where_murderer` | Coordinator refusal, gallery film/remaining there, private-room/chair/glass denial, toast screen and separate private version retained. |
| 06 Dada DiCapo | `evidence_innocent` | Empty-jacket film, rejection/persistence and intended alive/furious humiliation retained. |
| 06 Dada DiCapo | `evidence_murderer` | Taking contents for film, thought-inert qualifier, claimed agreed private live version after toast, public-only cancellation, no glass rehearsal and expected rise retained. |
| 08 Sue Venir | `evidence_murderer` | Exact canonical restoration: manager room pour, sole visit, glass lifted off agreement, remained through filling and public hospitality markup. |
| 11 Barb Dwyer | `motive_innocent` | Privacy request/agreement, donor exception, security consequences, Artie and outside-crew priorities retained. |
| 11 Barb Dwyer | `motive_murderer` | False fault, monitor removal, Grant knowing privacy and future coercion retained. |
| 11 Barb Dwyer | `where_innocent` | Camera/crew restriction with staff access, room check/set place, room clearing/Artie use, false log and lost record retained. |
| 11 Barb Dwyer | `where_murderer` | Monitor removal/access exceptions, empty prepared room, brief latch closure/reopening, false fault and technician-only exception retained. Museum staff restores original specificity. |
| 11 Barb Dwyer | `evidence_innocent` | Power removed/network attached/no footage, technician false-fault instruction, Paige recorder request and staff release retained. |
| 11 Barb Dwyer | `evidence_murderer` | Exact canonical restoration: false local-footage claim including glass, network-not-power assertion, privacy log and storage direction. |
| 12 Paige Turner | `evidence_murderer` | Exact canonical restoration: no drink/yesterday-office claim, tonight cloakroom retrieval/export, protective cut and editor original. |
| 15 Elon Mosaic | `evidence_murderer` | Exact canonical restoration: live existing-camera panel, presentation-label qualification, surviving private feed, prepared-place observation and trial funding. |
| 18 Elle Loominate | `motive_innocent` | Early payment for all future pattern uses, other-advance collateral lie and Chip contrast retained. Rescue phrasing restores original. |
| 18 Elle Loominate | `motive_murderer` | Spent advance, disclosure with early-payment request, all future uses as rescue price and incremental fabric buying retained. |
| 18 Elle Loominate | `where_innocent` | Closed alcove/close lamp, panel removal, private-room rolling beside set place, Grant absent, exit with panel, fabric bill and separate-advance lie retained. |
| 18 Elle Loominate | `where_murderer` | Top panel, closed alcove/lamp, separate production slides, private-room panel handling/rolling, absence/exit and refused rights transfer retained. Frank instruction restores original. |
| 18 Elle Loominate | `evidence_innocent` | Enlarged stitches, real loan, private-room packing/rolling, wrong-job and unused-advance collateral lies retained. Changed request framing introduces no factual proof. |
| 18 Elle Loominate | `evidence_murderer` | Projection between slides, cupboard physical loan, lit-image memory and pattern-rights amendment retained. Changed help request is emotional framing. |
| 23 Brie DeVivre | `evidence_murderer` | Exact canonical restoration: closed container left with service, pre-toast shared-pitcher flavoring by manager, disputed food versus paid booked drink. |
| 24 Cary Crates | `motive_innocent` | Old-damage report, receiving photos/frame report, unchecked next delivery, deferred resolution and job-loss fear retained. Frame report possession restores original. |
| 24 Cary Crates | `motive_murderer` | Personal delivery damage/false old-damage report, unchecked signature versus employer exposure, prior dismissal and job threat retained. Photograph delivery/employer wording restores original. |
| 24 Cary Crates | `where_innocent` | Sealed bottle/intake/frames, label-only inert qualifier, gifts to service, later report visit, unattended glass and subsequent packing-bin cleanup retained. |
| 24 Cary Crates | `where_murderer` | Sealed intake handover/lender inert label, service gifts, stuck lift, first-report retrieval, unattended glass, carton off chair, wait and departure retained. |
| 24 Cary Crates | `evidence_innocent` | Preexisting-crack/lighting lies, service unpacking of crest glass and drinking-photo engraving retained. |
| 24 Cary Crates | `evidence_murderer` | Preview stopper/packing check, label inert qualifier, boxed engraved glass, firsthand plain-spare drinking claim, tested gift distinction and corrected report retained. |
| 27 Robin Banks | `motive_innocent` | Intact return or hearing, applause first, conditional interruption, Barb removal history and desired answer retained. Refusal condition restores original. |
| 27 Robin Banks | `motive_murderer` | Claimants hearing/exclusion, applause, announcement disruption, security threat and Barb history retained. |
| 27 Robin Banks | `where_innocent` | Petition search/interruption during Paige gift questions, intake ownership card inside petition, prior warning and staying after dismissal retained. |
| 27 Robin Banks | `where_murderer` | Petition after security warning, public-podium interview handoff, later signature-page desk return, signature demand and private-room denial retained. |
| 27 Robin Banks | `evidence_innocent` | Private petition handoff while Paige records, podium correction/knowledge, bowl card and Barb dismissal defiance retained. |
| 27 Robin Banks | `evidence_murderer` | Preview sample/proof motive, no sample in private room, announcement-desk page and recorded public-podium claim/Paige corroborator retained. |

## Limits and disposition

The narrow deadline edit above has been verified in the reassembled candidate and ledger; no semantic must-fix remains from this review. Canon-restoring details were checked against the original rather than rejected merely because candidate01 compressed them. Emotional address, requests, ordering within a hearing answer, and rhetorical emphasis were treated as permissible where they did not alter an event or protected claim. No proof was added to repair any route. These findings do not establish whether players can solve any route or whether the six voices meet the dramaturgical objective.
