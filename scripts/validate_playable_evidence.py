"""Reject silently converted clock labels before freezing player-visible evidence."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
def validate(path=None):
    path = path or ROOT/'docs/connected-story-01-SPOILERS/playable-evidence.yaml'
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    assert [r['number'] for r in data['hunt']] == list(range(1,17))
    all_exhibits = data['hunt'] + [x for release in data['releases'] for x in release['exhibits']]
    for exhibit in all_exhibits:
        for row in exhibit.get('rows',[]):
            assert all(isinstance(cell,str) for cell in row), f"Non-text visible table cell in {exhibit['title']}: {row!r}"
        for paragraph in exhibit.get('paragraphs',[]):
            assert isinstance(paragraph,str), exhibit['title']
    ids = {x['id'] for release in data['releases'] for x in release['exhibits']}
    assert len(ids)==sum(len(r['exhibits']) for r in data['releases'])
    checks = data['releases'][-1]['route_checks']
    assert set(checks)=={f'{i:02}' for i in range(1,31)}
    assert all(set(dependencies)<=ids for dependencies in checks.values())
    return data


if __name__=='__main__':
    validate()
    print('All16 hunt exhibits, staged exhibit IDs,30 route references and visible text cells validated. No balance claim.')
