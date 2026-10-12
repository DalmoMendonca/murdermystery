"""Single-variable private experiment: defer identified poison until Method."""
from pathlib import Path
import copy
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-22-SPOILERS'
OLD = ROOT / 'docs/story-pass-21-SPOILERS'

def main():
    assert not (ROOT / 'build/story-pass22/private-manifest.json').exists(), 'Frozen trial cannot be rewritten'
    OUT.mkdir(exist_ok=True)
    # Preserve testimony bytes, including the explicit three-prototype guard.
    (OUT / 'investigation_copy.yaml').write_bytes((OLD / 'investigation_copy.yaml').read_bytes())
    before = yaml.safe_load((OLD / 'evidence_design.yaml').read_text(encoding='utf-8'))
    after = copy.deepcopy(before)
    report = next(r for r in after['reports'] if r['id'] == 'F2')
    old = 'Grant Larceny became ill after drinking his toast and died at the gala. The examination identifies cyanide poisoning.'
    new = 'Grant Larceny became ill after drinking his toast and died at the gala. Poisoning is suspected; the substance has not yet been identified. Toxicology results are pending.'
    assert old in report['text']
    report['text'] = report['text'].replace(old, new)
    restored = copy.deepcopy(after)
    next(r for r in restored['reports'] if r['id'] == 'F2')['text'] = next(r for r in before['reports'] if r['id'] == 'F2')['text']
    assert restored == before, 'Only F2 text may change'
    (OUT / 'evidence_design.yaml').write_text(yaml.safe_dump(after, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    (OUT / 'change-audit.json').write_text(json.dumps({'changed_fields': ['reports.F2.text'],
       'same_testimony_bytes': True, 'actual_crime_changed': False,
       'chemical_identification_release': 'Act III / F5',
       'scope': 'Only Ella/Justin/Elon prototypes eligible; other27 unvalidated'}, indent=2) + '\n', encoding='utf-8')
    print('One evidence field changed. Testimony, actual crime and all other evidence retained.')

if __name__ == '__main__':
    main()
