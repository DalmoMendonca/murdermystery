"""Apply separate editable public copy and organizer-only investigation branches."""
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_characters(root=ROOT):
    characters = json.loads((root/'source/characters.json').read_text(encoding='utf-8'))
    path = root/'source/character_copy.yaml'
    if not path.exists():
        return characters
    copy = yaml.safe_load(path.read_text(encoding='utf-8'))
    assert copy['schema_version'] == 1, 'Unsupported character-copy schema'
    by_id = {c['id']: c for c in characters}
    entries = copy['characters']
    assert len(entries) == len(by_id) and {c['id'] for c in entries} == set(by_id), 'List every character exactly once'
    active = set(copy['active_character_ids'])
    assert len(active) == len(copy['active_character_ids']), 'Duplicate active character ID'
    assert active <= set(by_id), 'Unknown active character ID'
    assert {c['id'] for c in characters if c['tier']=='CORE'} <= active, 'Keep all 15 core roles active'
    for entry in entries:
        c = by_id[entry['id']]
        assert entry['name'] == c['name'], 'Name changes need a coordinated game update; edit the public copy fields freely'
        assert isinstance(entry['role'],str) and entry['role'].strip(), f'Empty role for {c["name"]}'
        c['role'] = entry['role']
        for source, destination in [('description','description'),('acting_tips','acting'),('costume_suggestions','costume')]:
            assert isinstance(entry[source], str) and entry[source].strip(), f'Empty {source} for {c["name"]}'
            c['preparty'][destination] = entry[source].removeprefix('Optional inspiration: ').strip()
        assert isinstance(entry['introduction'], str) and entry['introduction'].strip(), f'Empty introduction for {c["name"]}'
        c['introduction'] = entry['introduction']
        for field in ['relationships', 'packet_relationships']:
            relationships = []
            for relation in entry.get(field, []):
                targets = set(relation['with'])
                assert targets and targets <= set(by_id) and c['id'] not in targets, f'Invalid relationship targets for {c["name"]}'
                assert isinstance(relation['text'], str) and relation['text'].strip()
                mentioned={p['id'] for p in characters if p['id']!=c['id'] and p['name'] in relation['text']}
                assert targets==mentioned, f'Relationship IDs do not match the names in {c["name"]}: use {sorted(mentioned)}'
                if targets <= active:
                    absent = [p['name'] for p in characters if p['id'] not in active and p['name'] in relation['text']]
                    assert not absent, f'Relationship text still names absent characters: {absent}'
                    relationships.append(relation['text'])
            if field=='relationships' and c['id'] in active:
                assert relationships, f'Add an active relationship for {c["name"]}'
            c['preparty'][field] = relationships
    from investigation_copy import apply_investigation
    return apply_investigation(characters, root)

if __name__ == '__main__':
    print(json.dumps(load_characters(), ensure_ascii=False))
