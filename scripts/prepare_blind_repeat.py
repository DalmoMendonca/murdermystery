"""Create a prospectively declared byte-identical fresh-reader comparison."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

def make(version, parent, label):
    assert parent.isalnum() and label.isalnum() and parent != label
    root = ROOT / f'build/story-pass{version}'
    assert (root / 'private-manifest.json').exists(), 'Freeze the main trials first'
    source = root / parent
    destination = root / label
    assert not destination.exists(), 'A repeat cannot overwrite an existing reader'
    files = [source / f'checkpoint_{i:02}.txt' for i in range(1, 9)]
    assert all(p.is_file() for p in files)
    selection = json.loads((source / 'private-selection.json').read_text(encoding='utf-8'))
    destination.mkdir()
    hashes = {}
    for path in files:
        target = destination / path.name
        shutil.copy2(path, target)
        assert target.read_bytes() == path.read_bytes()
        hashes[path.name] = hashlib.sha256(target.read_bytes()).hexdigest()
    selection['trial'] = label
    (destination / 'private-selection.json').write_text(json.dumps(selection, indent=2) + '\n', encoding='utf-8')
    note = {'trial': label, 'parent_trial': parent,
            'reason': 'Prospectively declared fresh unanchored reader on byte-identical inputs',
            'sha256': hashes}
    (root / f'supplemental-{label}.json').write_text(json.dumps(note, indent=2) + '\n', encoding='utf-8')
    print('Fresh comparison created; eight input hashes match. No identity or scores printed.')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--version', type=int, required=True)
    p.add_argument('--parent', default='B')
    p.add_argument('--trial', default='D')
    args = p.parse_args()
    make(args.version, args.parent, args.trial)
