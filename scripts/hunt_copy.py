"""Editable location-first hunt source. JSON is a generated compatibility snapshot."""
import json,yaml
from pathlib import Path

def load_hunt(root):
    root=Path(root);data=yaml.safe_load((root/'source/hunt_copy.yaml').read_text(encoding='utf-8'))
    roles=json.loads((root/'source/characters.json').read_text(encoding='utf-8'))
    by_id={c['id']:c for c in roles}
    result={'locations':[],'characters':{c['slug']:[] for c in roles}}
    assert data['schema_version']==1
    assert len(data['locations'])==16 and len({l['location'] for l in data['locations']})==16
    for loc in data['locations']:
        assert isinstance(loc['location'],str) and loc['location'].strip()
        result['locations'].append({'envelope':loc['envelope'],'location':loc['location']})
        for item in loc['hints']:
            assert isinstance(item['hint'],str) and item['hint'].strip()
            role=by_id[item['character_id']]
            assert item['character']==role['name'],('Update character label',item)
            result['characters'][role['slug']].append({'envelope':loc['envelope'],'text':item['hint']})
    assert {l['envelope'] for l in result['locations']}==set(range(1,17))
    assert all(len(h)==3 and len({x['envelope'] for x in h})==3 for h in result['characters'].values())
    assert len({h['text'] for hs in result['characters'].values() for h in hs})==90
    return result

def sync_hunt(root):
    root=Path(root);data=load_hunt(root)
    (root/'source/hunt.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data
