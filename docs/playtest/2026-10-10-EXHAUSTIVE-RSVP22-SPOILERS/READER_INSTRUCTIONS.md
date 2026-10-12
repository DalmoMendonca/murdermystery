# Blind reader instructions

You are one independent attentive reader assessing a murder mystery. You have no earlier game context. Exactly one of 22 named characters is the murderer. Do not try to discover the hidden selection from files. Judge only the released player-facing information. Do not inspect any other trial, private manifest, authoring source, previous tests, game rules outside your releases, memory, or the helper's source code. Do not spawn agents.

Use the trial token supplied in your task. Work in `C:/Users/dalmo/Documents/Codex/2026-10-03/referenced-chatgpt-conversation-this-is-an/work/murdermystery`.

Python executable: `C:/Users/dalmo/AppData/Local/Programs/Python/Python312/python.exe`. Gate script: `scripts/exhaustive_balance.py`. Your writable folder: `docs/playtest/2026-10-10-EXHAUSTIVE-RSVP22-SPOILERS/blind/TRIAL`.

Technical file-writing tip: use a PowerShell single-quoted multiline here-string piped to `Set-Content -LiteralPath ... -Encoding utf8` for JSON. Put `@'` and `'@` on their own lines. Avoid passing JSON through a nested `python -c` shell argument, which can strip its quotation marks. Run each gate action separately, and advance only when its preceding validation succeeds. This changes no scoring instructions.

For each stage 1 through 8, in order:

1. Set `$env:PYTHONIOENCODING='utf-8'` in PowerShell and run Python gate `read --trial TRIAL --stage N`. Request at least 7000 output tokens so the complete release is visible. Read ALL of it.
2. Before opening any next release, write `result_NN.json` in your folder as UTF-8 JSON: `{"stage":N,"scores":{"Exact Character Name":integer,...},"clear_culprit":null,"reasoning":"Brief evidence-based assessment of leading suspects and uncertainty."}`. Include every one of the 22 names exactly once. Suspicion scores are integers 0 to 10, with 0 meaning no current suspicion and 10 meaning overwhelming suspicion. Use your own judgment; there is no required distribution. `clear_culprit` may be an exact character name ONLY if you believe the currently released evidence clearly singles them out; otherwise null. A current leading suspect alone is not necessarily clear. Aim for 60-100 words of reasoning per checkpoint. Preserve earlier scores; do not edit them with hindsight.
3. Run gate `validate --trial TRIAL --stage N` in a separate successful command. Fix a score file only if validation rejects its schema or exact names, without changing your judgments. Then advance.

After stage 8, write `accusation.json` with:

- `accused`: one exact character name.
- `confidence`: integer 0-10.
- `reasoning`: the evidence chain supporting the accusation and why the strongest competing explanation loses (100-180 words).
- `ratings`: integer 0-10 for `fair_play`, `clarity`, `voice_distinction`, `arc_variety`, `naturalness`, `drama`.
- `feedback`: frank overall review (120-220 words). Did dialogue sound like distinct people under pressure? Were events plausible? Did the game feel deliberately assembled? Did speeches do the players' interpreting for them? Was the mystery logically solvable from facts available before voting? Are there contradictions or unfair gaps? Be specific and do not invent defects to fill a checklist.
- `issues`: up to four objects `{"category":"fairness/clarity/voice/naturalness/drama/pacing/evidence/motive/finale","severity":"major/moderate/minor","characters":["Exact Name"],"detail":"Concrete problem and a short evidence reference.","suggested_fix":"Bounded actionable improvement."}`. Empty array is fine if you find no issues.

Run gate `finale --trial TRIAL` ONLY after saving that file. This locks your accusation and reveals a finale simulation based on your highest-rated suspects. Do not rescore or change your accusation. Save `post_vote_feedback.json` with `{"feedback":"80-140 words: does the confession follow from previously available clues, does it add any decisive new facts, does it feel earned and emotionally satisfying?","new_decisive_facts":[],"earned":true}`. List genuinely new decisive facts if any; `earned` is your judgment.

Finally run gate `complete --trial TRIAL`. Report only the trial token, completion status, and any actual protocol deviation. Do not paste the scores back to the parent; they are saved on disk. If a tool fails or you cannot finish, report precisely what is saved and what remains. Never claim a trial complete without the gate's confirmation.
