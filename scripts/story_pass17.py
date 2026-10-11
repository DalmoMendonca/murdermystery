"""Compile an isolated character-first fracture-evidence experiment."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/story-pass-17-SPOILERS'

def load(name):
    return yaml.safe_load((OUT / name).read_text(encoding='utf-8'))

def save(name, value):
    (OUT / name).write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100), encoding='utf-8')

def main():
    rounds = load('rounds.yaml')
    observations = {r['id']: r['text'].replace('binned', 'threw away') for r in load('glass-observations.yaml')['characters']}
    motives = {r['id']: r['text'] for r in load('motives.yaml')['characters']}
    investigation = load('investigation_copy.yaml')
    old = {r['id']: r for r in investigation['characters']}
    dialogue = []
    for r in rounds['characters']:
        ident = r['id']
        # Distribute document disputes among their actual participants; they do not
        # all take place in the donor assistant's twelve-minute confrontation.
        changes = {
            '03': [('Grant\'s assistant then produced', 'At yesterday\'s settlement call, Sue produced'), ('before the trustees saw it', 'before the trustees received the file')],
            '04': [('Then his assistant showed me a message', 'The bank compliance officer had already forwarded a message'), ('while she watched', 'before tonight\'s board meeting')],
            '05': [('Grant\'s assistant demanded', 'the insurer had demanded'), ('She knew which copy to ask for.', 'The claim number was on both copies.')],
            '07': [('Grant\'s assistant heard that and asked', 'Claire heard that and asked')],
            '08': [('His assistant now wanted to know', 'Penny wanted to know')],
            '09': [('Grant\'s assistant found', 'The exhibition committee circulated'), ('I refused to withdraw it.', 'I refused to withdraw it at Thursday\'s review.')],
            '12': [('His assistant saved it.', 'My editor has the message.')],
            '14': [('His assistant called that blackmail.', 'Sue called that blackmail.')],
            '16': [('Grant\'s assistant had demanded that file too.', 'The trustees had demanded that file at the archive review.')],
            '17': [('Grant\'s assistant then asked', 'Sue had asked at yesterday\'s accounts meeting')],
            '19': [('Grant\'s assistant wanted', 'The exhibition committee wanted')],
            '24': [('Grant\'s assistant demanded', 'the courier demanded')],
            '29': [('Then Grant\'s assistant played', 'At the press table, Paige played'), ('before she reached that part', 'before she reached that part')],
        }
        op = r['opportunity']
        for before, after in changes.get(ident, []):
            op = op.replace(before, after)
        innocent = r['innocent'].replace('The camera disconnection covered the office', 'The camera disconnection covered the Donor Salon')
        guilty = r['guilty'].replace('A small bottle', 'My favor bottle')
        if ident == '20':
            innocent = "I lifted the glass with my plaster-covered hand. Brie was right to shout at me. My favor spilled on the rejected carving invoice; Casey collected that bottle with the invoice case. The carving was already delivered. Grant was keeping the credit and refusing the balance. I threatened to take the head back because I couldn't take back the hours. The lab has my bottle. The money is still missing."
        if ident == '25':
            innocent = "The sign-up desk was open from six-thirty until the toast. I was taking parents' bookings, with the volunteers, after leaving that petition. They have the carbon copies. I withdrew Artie's endorsement and sent the petition with my own name. One class surviving while its teachers lose their jobs isn't a rescue. Monet, I still want you to release that offer."
        row = dict(id=ident, motive=motives[ident], opportunity_innocent=op,
                   opportunity_murderer=op + ' ' + observations[ident],
                   method_innocent=innocent, method_murderer=guilty)
        dialogue.append(row)
        target = old[ident]
        target['hearings'] = {
            'motive_innocent': motives[ident], 'motive_murderer': motives[ident],
            'where_innocent': row['opportunity_innocent'], 'where_murderer': row['opportunity_murderer'],
            'evidence_innocent': innocent, 'evidence_murderer': guilty,
        }
        target['coming_clean'] = {
            'innocent': innocent + ' I did not kill Grant.',
            'murderer': 'I killed Grant. The blue fragment was from the stolen original, not my gift. I wrapped it in the favor paper and discarded it. I used the miniature favor to carry poison to his glass, then hid the original behind the sideboard. ' + motives[ident],
        }
    investigation['status'] = 'Pass17: delayed fracture comparison; distributed disputes; isolated test only'
    save('investigation_copy.yaml', investigation)
    save('dialogue.yaml', dict(schema_version=1, characters=dialogue))
    save('endings.yaml', dict(schema_version=1, characters=[dict(id=r['id'], **r['coming_clean']) for r in investigation['characters']]))
    e = load('evidence_design.yaml')
    reports = {r['id']: r for r in e['reports']}
    reports['F2']['photo'] = 'sealed_receiving_case_pass17_REQUIRED'
    reports['F2']['text'] = "Grant Larceny became ill after drinking his toast and died at the gala. The examination identifies cyanide poisoning. The museum had received a historical poison bottle for The Art of Murder. The auction file said its contents were retained; Grant told security it had been emptied. Collections placed it in a locked preparation cabinet inside a secondary case and withheld display approval. Only an empty replica went to the galleries. At 6:12 the cabinet alarm registered a forced opening. The original was missing. Food, drinks, props and recovered bottles are being examined."
    reports['F3']['text'] = "Jordan West, collections assistant: The secondary case was photographed closed at 5:45. At 6:12 the cabinet alarm sounded. The lock and case were broken; the original was gone. The display replica remained on its trolley. Casey Hart, service manager: The reception desk is the long sideboard beside the entry. I unwrapped Grant's new museum-star glass there at 6:32. I went to settle the kitchen's extra-course authorization. I collected the glass at 6:44 and filled it with punch at 6:46. The photographs show it on the service tray until Grant's 6:49 toast. Guests' favors, programs and correspondence were also on the sideboard. Police found a small blue glass fragment folded in favor paper in its waste basket. Comparison is pending."
    reports['F3']['rows'] = [['Preparation cabinet', 'Lock and secondary case forced; original missing'], ['Reception waste', 'Blue glass fragment folded in favor paper; comparison pending'], ['Service', 'Glass unwrapped 6:32; collected 6:44; filled 6:46; toast 6:49']]
    reports['F3']['photo'] = 'sideboard_and_wrapped_fragment_pass17_REQUIRED'
    reports['F4']['title'] = 'Two pieces of one bottle'
    reports['F4']['text'] = "The original Velvet Widow bottle was found behind the reception sideboard. It is dark-blue glass, with a fresh piece missing from the neck. The fragment recovered in folded favor paper fits that gap: the two irregular edges join across the stamped inventory mark. The original's receiving record describes an intact neck inside a sealed case. The recovered miniature fragrance bottle has an intact neck and body. The open-bottom display replica is clear glass."
    reports['F4']['rows'] = [['Original bottle', 'Dark-blue glass; fresh missing neck fragment'], ['Fragment in favor paper', 'Fits missing edge and divided inventory stamp'], ['Recovered favor bottle', 'Neck and body intact'], ['Display replica', 'Clear glass; open bottom']]
    reports['F4']['photo'] = 'fracture_comparison_pass17_REQUIRED'
    reports['F4']['layout'] = 'fracture_comparison'
    reports['F5']['text'] = "Cyanide was found inside Grant's museum-star glass, in the recovered original, on the blue neck fragment, and in a miniature LARCENY No.1 bottle from reception waste. The shared punch, meal, sauce, PROP glass, brush-water bottle and studio FIXER tested clear. Al's favor bottle collected with the invoice case contained fragrance and tested clear. Unopened favor stock also tested clear. The contaminated miniature has the common manufacturer label and no recipient name. Plaster and cloth fibers were found on the outside of Grant's glass."
    reports['F5']['rows'] = [['Grant\'s glass / original / blue fragment', 'Cyanide detected'], ['Miniature from reception waste', 'Cyanide; common favor label; no recipient name'], ['Punch / meal / sauce / PROP / brush-water / FIXER', 'Clear for cyanide'], ['Al\'s miniature collected with invoice case', 'Fragrance; clear for cyanide'], ['Unopened favor stock', 'Fragrance; clear for cyanide']]
    d = {r['number']: r for r in e['discoveries']}
    d[4]['paragraphs'][2] = 'Guest gift: LARCENY No.1 miniature fragrance. Art-glass bottles in assorted colors; one sealed bottle in every gala packet. Include in donor photographs.'
    d[13]['paragraphs'] = ['Auction condition: sealed historical bottle; original contents retained. Specialist hazard assessment required. Display status: withheld. Empty replica supplied for gallery installation.', 'Buyer requests The Art of Murder display tonight. Collections has declined approval of the original.']
    d[14]['paragraphs'] = ['5:45: Original secured in locked preparation cabinet and secondary case. Receiving photograph shows the closed case. Condition entry: neck intact. Empty clear-glass, open-bottom replica to display trolley.', '6:12: Forced-opening alarm. Cabinet lock and secondary case damaged. Original missing.', '6:15, security radio: Grant says the original was emptied. Search preparation corridor; close storage access. Collections disputes his claim. 6:22: Auction condition received confirming contents retained. Security requests emergency assistance.']
    d[14]['annotation'] = 'Display approval withheld. Cabinet key retained by collections.'
    d[15]['stamp'] = 'LIGHTING JOB LOG'
    d[16]['paragraphs'][-1] = 'Reception sideboard also used for guest gift packets, correspondence and printed programs.'
    save('evidence_design.yaml', e)
    case = load('case_design.yaml')
    case['revision'] = 17
    case['crime']['trace'] = 'Blue source-neck fragment discarded in common favor paper; physical fracture and divided inventory stamp matched in Method'
    save('case_design.yaml', case)
    print('Compiled private round17 only; sent public assets unchanged.')

if __name__ == '__main__':
    main()
