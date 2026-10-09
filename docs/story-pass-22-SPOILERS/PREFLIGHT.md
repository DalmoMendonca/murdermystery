# Round 22 editorial preflight

**Verdict: coherent enough to run the proposed limited release-timing experiment.** No blocking contradiction or unfair concealment is introduced by the F2 change. This is an editorial consistency finding, not a finding that the mystery is uniquely solvable, meets any rating threshold, or is ready for integration.

## Scope verified

I inspected `TEST_PROTOCOL.md`, `change-audit.json`, both round22 YAML files, and their round21 counterparts. `investigation_copy.yaml` is byte-identical between rounds21 and22. A textual diff of `evidence_design.yaml` is confined to F2 text. Parsing the two evidence files and substituting round22's F2 text into round21 produces equal full data structures. Thus all reports, discoveries, evidence rows, captions, testimony and underlying authored crime outside that field are unchanged.

The only substantive replacement is:

- Round21: “The examination identifies cyanide poisoning.”
- Round22: “Poisoning is suspected; the substance has not yet been identified. Toxicology results are pending.”

No new test inputs or scores were created for this review.

## Earlier player information

I scanned preserved round21 A/B/C/D checkpoint text through stage6 and all 120 motive/where testimony fields in the unchanged 30-character investigation file for chemical identification or completed toxicology findings. The only pre-Method explicit cyanide identification in those player releases is the round21 F2 sentence that round22 replaces. There is no earlier testimony saying cyanide is known, or claiming the laboratory has already cleared a particular substance. Introductions and the 16 discoveries provide no chemical-species identity.

Discovery13 establishes a historical poison bottle with original contents retained and required hazard assessment. Discovery14 records its theft and Grant's unverified claim that it was emptied. These establish potential danger, not the substance that killed Grant. Dr. Art's stage6 question about whether the Eleanor Vale bottle still contained poison concerns the historical object; it does not identify Grant's toxicology. The later reference to a coroner's report is naturally the historical case's lecture material, not a preexisting report on Grant.

Poison remains strongly suggested before Method. That is legitimate available evidence and may limit the experiment's effect. The change does not promise that readers will regard every method as equally plausible.

## Toxicology consistency

F2's existing “Laboratory results / Pending” row now agrees particularly clearly with its revised text. F3 describes recovery and pending object comparison without supplying chemistry. F4 supplies physical identification, fracture matching and service photographs, not a prior laboratory result. F5 first reports cyanide in the original, fragment, miniature and target glass, plus negative tests for the other sampled substances.

The final evidence testimony's references to clear punch, food, PROP, brush-water or FIXER come after F5 in the sequential release order. They therefore do not contradict pending toxicology at F2. F5's negative findings remain chemical-specific; they do not establish absence of every conceivable toxin or every mechanism. That limitation is inherited rather than introduced by round22.

## Fair play and fictional timing

The revised initial report openly says the result is pending. It does not tell players a known positive is negative, disguise an authenticated result, or change the actual poison retroactively. The initial death after a drink, missing hazardous object and retained contents are a reasonable basis for suspected poisoning while chemical identification is unresolved. Players retain enough evidence to investigate that hypothesis before confirmation.

F5 then advances the investigation with a completed result. No supplied report assigns a clock time or mandatory real-world turnaround interval to the laboratory work between releases. The game's compression of investigation time is an existing abstraction; the revision does not newly assert that a full toxicology examination happens in a specified number of minutes. If a later production script explicitly treats all hearings as uninterrupted immediate conversation, that would require a separate timing review. It is not a blocker in this transcript prototype.

The stolen historical poison and pre-toast security negligence remain plausible in the same heightened museum fiction as round21. Deferring investigators' chemical identification does not imply that staff had no reason to treat the stolen original as hazardous.

## Interpretation limit

The revision is a single-field change, but semantically it defers **both confirmed poisoning and cyanide identity**. Round21 states established cyanide poisoning; round22 states suspected poisoning of unknown substance. Results should therefore be described as testing the timing of early diagnostic certainty, not as cleanly isolating the word “cyanide” while certainty of poisoning stays fixed. This is a reporting qualification, not a request to alter the prospective input.

The protocol appropriately retains the other veto criteria. Anonymous miniature attribution, original/copy ambiguity, repeated glass contacts and broader guilty-world coverage remain independent questions. I recommend proceeding with the stated fresh-reader experiment, retaining all outcomes and verifying the promised per-release byte comparison at freeze. This reviewer has prior round21 exposure and must not serve as a fresh round22 blind player.
