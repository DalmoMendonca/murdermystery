"""Compile the isolated connected-story authoring bank, never production source."""
from pathlib import Path
import argparse
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'docs/connected-story-01-SPOILERS'


def compile_bank(active):
    public = yaml.safe_load((ROOT / 'source/character_copy.yaml').read_text(encoding='utf-8'))
    known = {str(r['id']).zfill(2): r for r in public['characters']}
    if active == 'all':
        selected = set(known)
    elif active == 'confirmed':
        selected = {str(i).zfill(2) for i in public['active_character_ids']}
    else:
        selected = {i.strip().zfill(2) for i in active.split(',') if i.strip()}
    if not selected or not selected <= set(known):
        raise ValueError('Use all, confirmed, or known comma-separated character IDs.')
    first = yaml.safe_load((LAB / 'five-role-bank.yaml').read_text(encoding='utf-8'))
    second = yaml.safe_load((LAB / 'production-family-scenes.yaml').read_text(encoding='utf-8'))
    rules = yaml.safe_load((LAB / 'attendance-edits.yaml').read_text(encoding='utf-8'))['rules']
    rows = first['characters'] + [
        {k: row[k] for k in ('id', 'name', 'hearings', 'coming_clean')}
        for row in second['characters']
    ]
    seen = set()
    for row in rows:
        ident = str(row['id']).zfill(2)
        if ident in seen or known[ident]['name'] != row['name']:
            raise ValueError(f'Duplicate or changed public identity: {ident}')
        seen.add(ident)
        if len(row['hearings']) != 6 or set(row['coming_clean']) != {'innocent', 'murderer'}:
            raise ValueError(f'Incomplete paired route: {ident}')
        for act in ('motive', 'where', 'evidence'):
            if row['hearings'][act + '_innocent'] == row['hearings'][act + '_murderer']:
                raise ValueError(f'Identical branches: {ident}/{act}')
        for section in ('hearings', 'coming_clean'):
            for field, speech in row[section].items():
                for rule in rules:
                    if str(rule['absent']).zfill(2) not in selected:
                        speech = speech.replace(rule['find'], rule['replace'])
                row[section][field] = speech
    result = [r for r in rows if str(r['id']).zfill(2) in selected]
    result.sort(key=lambda r: int(r['id']))
    # These drafted paragraphs use unique first names for guest references.
    # Reject a new absent-person mention until an explicit contextual edit exists.
    for row in result:
        for section in ('hearings', 'coming_clean'):
            for field, speech in row[section].items():
                for ident, person in known.items():
                    if ident in selected:
                        continue
                    first_name = person['name'].split()[0]
                    if re.search(r'\b' + re.escape(first_name) + r'\b', speech):
                        raise ValueError(f'Unresolved absent guest {person["name"]}: {row["id"]}/{field}')
    return {
        'schema_version': 1,
        'status': 'partial_authoring_bank_not_canonical_source_or_complete_game',
        'active_character_ids': sorted(selected),
        'authored_route_count': len(result),
        'unwritten_active_ids': sorted(selected - seen),
        'characters': result,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--active', default='all')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    destination = args.output.resolve()
    if not destination.is_relative_to(LAB) and not destination.is_relative_to(ROOT / 'build'):
        raise ValueError('Authoring output must remain in this lab or build/.')
    result = compile_bank(args.active)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False, width=110), encoding='utf-8')
    print(f'Authored {result["authored_route_count"]} routes; {len(result["unwritten_active_ids"])} active routes remain unwritten.')
