"""Freeze the repaired fifteen-role follow-up; never reroll or overwrite a trial."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
original = (ROOT / 'scripts/freeze_balance_slice.py').read_text(encoding='utf-8')
prior = ROOT / 'docs/connected-story-01-SPOILERS/balance-slice-01'
selection = json.loads((prior / 'private-selection.json').read_text(encoding='utf-8'))
code = original.replace("OUT = LAB / 'balance-slice-01'", "OUT = LAB / 'balance-slice-02'")
code = code.replace("ids = [str(r['id']).zfill(2) for r in available]", "ids = " + repr([r['id'] for r in selection['cast']]))
code = code.replace('killer = random.SystemRandom().choice(ids)', 'killer = ' + repr(selection['killer_id']))
code = code.replace("for which in ('old','new'):", "for which in ('new',):")
code = code.replace("'Single uniform random draw from the fifteen complete routes, shared between versions; no reselection.'", "'Reuse the earlier hidden random selection and same fifteen roles; no reroll. Reader does not receive selection.'")
code = code.replace("'EXHIBITION CATALOG PROOF, DATED BEFORE GALA: Bottle working entry", "'EXHIBITION CATALOG PROOF, DATED BEFORE GALA: The full working proof was sent to intake; an unresolved reply instructs staff to keep the bottle closed. Full proof and reply went to staff; the shortened entry went to press. Bottle working entry")
code = code.replace("print('Frozen two seven-stage inputs with the same fifteen roles and one hidden uniform selection. Identity not printed.')", "print('Frozen one current seven-stage input, same prior fifteen roles and hidden culprit; hunt omitted. No production changes.')")
exec(compile(code, str(ROOT / 'scripts/freeze_balance_slice.py'), 'exec'))
