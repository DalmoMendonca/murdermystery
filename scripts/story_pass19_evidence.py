"""Author the isolated Round 19 release timing; refuse to edit a frozen trial."""
from pathlib import Path
import copy
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-19-SPOILERS'

def main():
    assert not (ROOT / 'build/story-pass19/private-manifest.json').exists(), 'Frozen trial cannot be rewritten'
    data = copy.deepcopy(yaml.safe_load((ROOT / 'docs/story-pass-18-SPOILERS/evidence_design.yaml').read_text(encoding='utf-8')))
    reports = {r['id']: r for r in data['reports']}
    reports['F3'] = {
        'id': 'F3', 'department': 'INVESTIGATION / SCENE RECORD',
        'title': 'The missing bottle at reception',
        'text': "Jordan West, collections assistant: During the search after Grant's death, the original Velvet Widow bottle was recovered behind the long reception sideboard beside the entry. Its receiving description identifies the object. The clear, open-bottom display replica remained separate. Casey Hart, service manager: I placed Grant's new museum-star glass on that sideboard at 6:32. I left reception to settle the kitchen's extra-course authorization, and collected the glass at 6:44. Gift packets, programs and guest correspondence also used that station. The cabinet lock and secondary case had been forced at 6:12; the original was missing then.",
        'rows': [['Historical original', 'Recovered behind reception sideboard after the death'],
                 ['Donor glass', 'On reception sideboard 6:32–6:44'],
                 ['Service manager', 'In kitchen to settle extra-course authorization'],
                 ['Storage', 'Cabinet lock and secondary case forced at 6:12']],
        'layout': 'recovery_scene', 'photo': 'original_recovery19_REQUIRED',
    }
    f4 = reports['F4']
    f4['title'] = 'The glass and the broken bottle'
    f4['text'] = "The original recovered behind reception is dark-blue glass with a fresh piece missing from its neck. The fragment in folded favor paper joins the irregular curved neck edge. The receiving record described the original neck as intact. The recovered miniature fragrance bottle has an intact neck and body; the display replica is clear with an open bottom. Casey Hart's service photographs also identify the new museum-star glass: empty when placed on reception at 6:32, and empty when collected onto the tray at 6:44. Casey states: I filled it with shared punch on the tray at 6:46, and kept it there until Grant's 6:49 toast. The photographs record these moments, not continuous surveillance of the sideboard."
    f4['photo'] = 'fracture_comparison_v18'
    f4['service_photo'] = 'sideboard_service_v18'
    f4['service_timeline'] = [
        {'time': '6:30', 'caption': 'New donor glass, wrapped'},
        {'time': '6:32', 'caption': 'Empty glass placed on reception sideboard'},
        {'time': '6:44', 'caption': 'Empty glass collected onto service tray'},
        {'time': '6:46', 'caption': 'Shared punch poured on service tray'},
    ]
    reports['F5'].pop('photo', None)
    data['reports'] = [reports[f'F{i}'] for i in range(1, 6)]
    for clue in data['discoveries']:
        if clue['number'] == 16:
            clue['paragraphs'] = [p.replace('museum star etched into base', 'museum star on the bowl') for p in clue['paragraphs']]
    # No clock claim in Hunt supplies the actual empty-at-collection image.
    # Hunt's existing service order remains a plan, not proof of compliance.
    (OUT / 'evidence_design.yaml').write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')
    print('Round19 evidence timing authored; actual service-state proof withheld until Method. Production unchanged.')

if __name__ == '__main__':
    main()
