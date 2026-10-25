"""One shared attendance filter for player releases and printed evidence."""
import copy

def exhibits(evidence,release,confirmed=False):
    policy=evidence.get('confirmed_filters',{}) if confirmed else {}
    out=[]
    for original in release['exhibits']:
        if original['id'] in policy.get('omit_exhibits',[]):continue
        item=copy.deepcopy(original);ident=item['id']
        if 'rows' in item:item['rows']=[r for r in item['rows'] if r[0] not in policy.get('omit_rows',{}).get(ident,[])]
        if 'paragraphs' in item:item['paragraphs']=[p for p in item['paragraphs'] if not any(p.startswith(prefix) for prefix in policy.get('omit_paragraph_prefixes',{}).get(ident,[]))]
        out.append(item)
    return out
