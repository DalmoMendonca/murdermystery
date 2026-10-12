"""Replace stale prompts while preserving the existing named target groups."""
from pathlib import Path
import json, argparse

ROOT = Path(__file__).resolve().parents[1]
args=argparse.ArgumentParser()
args.add_argument('--apply-source',action='store_true',help='Only use when integrating an accepted candidate and rebuilding PDFs.')
options=args.parse_args()
source = ROOT / 'source/question_rounds.json'
path = source if options.apply_source else ROOT / 'docs/baseline-improvement-02-SPOILERS/question_rounds.json'
rounds = json.loads(source.read_text(encoding='utf-8'))
questions = {
    'motive': [
        "What was at stake in Grant's proposed deal?",
        'What did Grant want you to approve?',
        'What business did you have with Grant?',
        'How had Grant interfered with your work?',
        'Why did Grant object to what you had written?',
        'What was Grant trying to keep private?',
        'What was going wrong with your commission?',
        'What claim did you want the museum to recognize?',
        'Why was your past business with Grant a problem tonight?',
        "What part of Grant's gala plans did you object to?",
    ],
    'opportunity': [
        'What did you try to control or keep from Grant before the toast?',
        'What did you change or conceal during the reception?',
        'What were you trying to keep out of the announcement?',
        "What happened when you challenged Grant's demands?",
        'What problem were you dealing with while guests mingled?',
        'What did you do after Grant challenged your plans?',
        'What did you try to correct or withdraw tonight?',
        'What change did you make to the gala arrangements?',
        'How did you make your dispute public, or keep it private?',
        'What did you circulate or keep without permission?',
    ],
    'method': [
        'What does the original version show?',
        'What became of the plan you described?',
        'What can you show us about that transaction?',
        'What was kept from the work or delivery?',
        'What remains of the work Grant wanted to use?',
        'What do the papers you kept actually say?',
        'What exactly did you handle, and why?',
        'What survived from the material Grant wanted changed?',
        'What became of the change you made?',
        'What are you willing to put on the record now?',
    ],
}
for rd in rounds:
    assert len(rd['groups']) == len(questions[rd['key']]) == 10
    for group, question in zip(rd['groups'], questions[rd['key']]):
        group['question'] = question
path.write_text(json.dumps(rounds,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Aligned thirty prompts; named targets unchanged. '+('Canonical source updated; rebuild required.' if options.apply_source else 'Private candidate only; canonical PDFs/source unchanged.'))
