"""Deliver the protected print edition after rejecting the tested rewrite."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(r'C:/Users/dalmo/Documents/Codex/2026-10-24/what/outputs')
RUN=ROOT/'docs/playtest/2026-10-27-ENSEMBLE-BLIND-SPOILERS'
AUTHOR=ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
REPORT=OUT/'ensemble-test-report'
BASE=OUT/'final-party-print-kit'
HANDOFF=OUT/'party-print-handoff'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    data=json.loads((RUN/'summary.json').read_text())
    acceptance=json.loads((RUN/'acceptance-review.json').read_text())
    assert data['completed']==22 and data['score_values']==3872
    assert data['all_journals_and_locks_verified']
    assert not acceptance['fairness_headline_gates_pass']
    HANDOFF.mkdir(exist_ok=True)
    original=BASE/'Print_Today_Current_22.zip'
    recommended=HANDOFF/'PRINT_THIS_Current_22.zip'
    shutil.copy2(original,recommended)
    assert sha(original)==sha(recommended)
    with ZipFile(recommended) as z:assert z.testzip() is None
    finish=HANDOFF/'Finish_Printing_Host_and_Packets.zip'
    instructions='''RECOMMENDED PRINT EDITION / CURRENT 22 GUESTS

This is the protected October 26 printing edition. No rejected rewrite is included.
If you already printed the four unchanged jobs (69 sheets), print ONLY these two remaining jobs:
01_Host_Guide.pdf: ONE copy, 5 sheets.
04_Guest_Packets_PRINT_WITHOUT_READING.pdf: ONE copy, 264 sheets.
Total remaining: 269 sheets.

US Letter, single-sided, 100% / actual size. Do not print on both sides.
Keep private packets facing their player; avoid reading their speech boxes.
Each guest has 12 consecutive pages. Leave page 11 (ballot) loose; staple the other pages in order.
Use the matching host guide in this archive. Do not substitute the rejected ensemble-candidate guide or helper.
'''
    names=['01_Host_Guide.pdf','04_Guest_Packets_PRINT_WITHOUT_READING.pdf']
    with ZipFile(finish,'w',ZIP_DEFLATED) as z:
        for name in names:z.write(BASE/name,name)
        z.writestr('PRINT_FIRST.txt',instructions)
    with ZipFile(finish) as z:
        assert z.testzip() is None
        for name in names:assert hashlib.sha256(z.read(name)).hexdigest()==sha(BASE/name)
    safe='''# Printing decision — October 27, 2026

Print **PRINT_THIS_Current_22.zip**. It is a byte-identical copy of the protected, previously verified October 26 edition. It contains all six required PDF jobs and the original instructions. No rejected dramaturgical revision is included.

| File | Copies | Sheets |
|---|---:|---:|
| 01 Host guide | 1 | 5 |
| 02 Hunt clues | 1 | 16 |
| 03 Staged evidence | 3 | 27 |
| 04 Private guest packets | 1 | 264 |
| 05 Name tents | 1 | 22 |
| 06 Animal draw cards | 1 | 4 |
| **Total** | | **338** |

Print single-sided on US Letter at 100% / actual size. Keep later evidence covered and private packets facing their players. Each guest receives twelve consecutive pages; leave page 11, the ballot, loose and staple the other pages in order. Follow the matching original host guide.

If you already printed **Print_These_Unchanged_Jobs_Now.zip**, those 69 sheets are correct. Use **Finish_Printing_Host_and_Packets.zip** for the remaining 269 sheets. Do not print the full kit as well as the two partial archives.

## Verification result, without story spoilers

The final experimental rewrite completed all 22 blind cases and all 3,872 locked suspicion scores. It returned **20/22 correct accusations, 21/22 endings judged earned, zero early clear culprits, and 6.09/10 mean naturalness**. It failed acceptance and was rejected. The writing target above eight was not achieved.

The protected printing edition retains its earlier **22/22 correct and earned exact-input coverage**, zero early clear culprits, and 6.41/10 naturalness. That earlier coverage combines assessments from successive versions whose player-facing inputs matched; it is not one fresh 22-reader cohort. Neither set estimates human solve rates or guarantees a particular dinner group's experience.

Independent full-cast editorial reviews found only modest improvement in the experimental prose. Their higher literary ratings did not predict the final blind suite. The experiment's raw scores, accusations and unfiltered feedback have been preserved separately; you do not need to read spoilers or judge the writing to use this recommendation.

The complete protected ZIP passes its integrity check. Its six jobs total 338 sheets; the guest book is 264 pages for 22 guests, and Act III remains six pages. Your three approved evidence pages and all other protected evidence remain intact. The website, previously sent assets and canonical game source were not replaced.

The revision effort did not produce the requested writing improvement. This handoff gives you one concrete, previously verified edition to print now. No further automatic rewrite or test cycle is pending.
'''
    (HANDOFF/'PRINTING_DECISION_NO_SPOILERS.md').write_text(safe,encoding='utf-8')
    (HANDOFF/'PRINT_FIRST.txt').write_text('RECOMMENDED: the protected October26 current22 edition.\nNothing printed yet: use PRINT_THIS_Current_22.zip (338 sheets).\nAlready printed the unchanged69-sheet jobs: use Finish_Printing_Host_and_Packets.zip (269 remaining sheets).\nChoose the full kit OR the two partial archives, not both.\nUS Letter, single-sided,100% / actual size.\nKeep private speech boxes unread; follow the included matching host guide.\nThe experimental ensemble rewrite was rejected and is not included.\n',encoding='utf-8')
    receipt={'recommended_edition':'protected2cb64b9','recommended_zip_sha256':sha(recommended),
             'same_as_protected_zip':True,'full_zip_integrity_pass':True,'full_sheets':338,
             'unchanged_jobs_sheets':69,'remaining_jobs_sheets':269,
             'remaining_zip_sha256':sha(finish),'new_candidate_status':'REJECTED',
             'new_candidate_summary':data,'naturalness_aspiration_met':False,
             'no_source_or_site_promotion':True}
    (HANDOFF/'print-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    private='''# Final ensemble experiment rejected

All22 fresh readers completed the one frozen pressure candidate. All3,872 scores, source/input/score/accusation/completion hashes, released image copies and post-vote order traces verified. Interrupted t020 andt021 resumed with their same identities and immutable prior scores; t022 was genuinely fresh. No rerolls or favorable case selection occurred.

Results:20 correct,21 earned,0 early clear,20 unique final culprit leaders. Naturalness6.09 versus protected6.41; arc variety7.05 versus7.18. The two failed accusations were Sue and Justin scenarios, both accused as Elle; Justin's ending was judged unearned. Those results remain failures. No new forensic observation, witness or physical match was invented to rescue them.

The recurring feedback concerns repeated documentary denials and professional breaches, dense compiled evidence, and broad physical opportunity without a unique scrap match. Readers also praised distinctive practical priorities, readable comparisons and interpersonal stakes. The full raw feedback is in all-player-feedback.md. Scores are AI reading diagnostics, not human solve-rate estimates; independent candidate readers versus versioned baseline coverage do not establish a controlled causal effect.

Earlier editorial readings were a screen, not proof: the final matched full-corpus reader narrowly preferred the pressure draft, while judging its overall improvement insubstantial; a fresh whole-cast reader rated naturalness7.6/arc7.3 and found it ready for fair-play testing. The completed fair-play cohort failed. No claim of naturalness above8, substantial whole-cast success or successful revised release is justified.

Print decision:retain the protected2cb64b9 edition. User-facing handoff is outputs/party-print-handoff. It contains an exact copy of the protected338-sheet ZIP and the remaining269-sheet host/packet archive for a user who printed the unchanged69sheet jobs. No new candidate PDF is recommended. No source/site promotion occurred. Automatic revision follow-up is to stop after delivery; no further authoring loops.
'''
    (REPORT/'revision-review.md').write_text(private,encoding='utf-8')
    (REPORT/'READ_RESULTS.md').write_text(private,encoding='utf-8')
    (RUN/'RESULTS.md').write_text(private,encoding='utf-8')
    shutil.copy2(RUN/'acceptance-review.json',REPORT/'acceptance-review.json')
    shutil.copy2(BASE/'ACT_III_Evidence.pdf',REPORT/'tested-ACT_III_Evidence.pdf')
    html=(REPORT/'results.html').read_text(encoding='utf-8')
    html=html.replace('Dramaturgical revision: 22 blind scenarios','Rejected ensemble candidate: complete results')
    html=html.replace('October 26, 2026','October 27, 2026')
    banner='<p><strong>REJECTED — do not print this candidate. Use the protected edition in party-print-handoff. Naturalness above eight was not achieved.</strong></p>'
    while banner+banner in html:html=html.replace(banner+banner,banner)
    if banner not in html:html=html.replace('<div id="cards"',banner+'<div id="cards"',1)
    (REPORT/'results.html').write_text(html,encoding='utf-8')
    (OUT/'ensemble-candidate/CANDIDATE_STATUS.txt').write_text('REJECTED — DO NOT PRINT.\nFull22-case suite failed:20correct,21earned,naturalness6.09.\nUse ../party-print-handoff/PRINT_THIS_Current_22.zip.\nNo revised release or8+writing score achieved.\n',encoding='utf-8')
    with (AUTHOR/'CURRENT_STATE.md').open('a',encoding='utf-8') as f:
        f.write('\nFINAL COHORT COMPLETE/REJECTED:20correct,21earned,zeroearlyclear,20uniqueleaders,naturalness6.09,arc7.05;all3872scores/hashes/images/finaleordersverified. Do notpromote orrunmorevariants. Protected338-sheet kit selected; spoiler-free handoff and exact ZIP in outputs/party-print-handoff. Remaining269-sheet archive supplied forunchanged69alreadyprinted. User neednotjudgeprose/readspoilers. No canonical/sitepromotion. Stop follow-upautomation afterdelivery.\n')
    with (ROOT/'PLAN.md').open('a',encoding='utf-8') as f:
        f.write('\n## Final printing handoff, October27\n\nFullensemble pressurecohort rejected20/22correct,21earned,naturalness6.09. Allrawresultsretained. Recommendprotected2cb64b9 printingedition, copiedbyte-identicallytooutputs/party-print-handoff/PRINT_THIS_Current_22.zip; full338sheets orremaining269afterunchanged69jobs. No newpromotion. Writingaspirationnotmet. No moreautomaticstyle/testcycles; deliverhonestspoiler-freeresultandstopfollow-up.\n')
    print(json.dumps({'handoff':str(HANDOFF),'recommended_zip':str(recommended),'candidate_rejected':True,'zip_integrity_pass':True}))

if __name__=='__main__':main()
