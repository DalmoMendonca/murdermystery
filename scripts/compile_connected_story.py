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
    rules = yaml.safe_load((LAB / 'attendance-edits.yaml').read_text(encoding='utf-8'))['rules']
    rows = first['characters']
    for filename in ('production-family-scenes.yaml', 'collection-scenes.yaml', 'market-scenes.yaml', 'remaining-scenes.yaml'):
        group = yaml.safe_load((LAB / filename).read_text(encoding='utf-8'))
        rows.extend({k: row[k] for k in ('id', 'name', 'hearings', 'coming_clean')}
                    for row in group['characters'])
    by_id = {str(row['id']).zfill(2): row for row in rows}
    for filename, fields in (
        ('motive-dialogue.yaml', {'motive_innocent', 'motive_murderer'}),
        ('stage-dialogue.yaml', {'evidence_innocent', 'evidence_murderer'}),
    ):
        revision = yaml.safe_load((LAB / filename).read_text(encoding='utf-8'))
        revision_ids = [str(row['id']).zfill(2) for row in revision['characters']]
        if len(set(revision_ids)) != len(revision_ids) or set(revision_ids) != set(by_id):
            raise ValueError(f'Incomplete or duplicate dialogue revision: {filename}')
        for row in revision['characters']:
            ident = str(row['id']).zfill(2)
            if set(row['hearings']) != fields:
                raise ValueError(f'Unexpected dialogue fields: {filename}/{ident}')
            by_id[ident]['hearings'].update(row['hearings'])
    # The narrative pass replaces spoken text only. Frozen full04 is the
    # comparison baseline; public copy and staged evidence remain untouched.
    dramatic = []
    for filename in ('dramatic-dialogue-01.yaml', 'dramatic-dialogue-02.yaml', 'dramatic-dialogue-03.yaml'):
        dramatic.extend(yaml.safe_load((LAB / filename).read_text(encoding='utf-8'))['characters'])
    dramatic_ids = [str(row['id']).zfill(2) for row in dramatic]
    if len(set(dramatic_ids)) != len(dramatic_ids) or set(dramatic_ids) != set(by_id):
        raise ValueError('Incomplete or duplicate dramatic dialogue revision')
    expected_hearings = {act+'_'+branch for act in ('motive','where','evidence')
                         for branch in ('innocent','murderer')}
    for revision in dramatic:
        ident = str(revision['id']).zfill(2)
        if set(revision['hearings']) != expected_hearings:
            raise ValueError(f'Incomplete dramatic hearings: {ident}')
        row = by_id[ident]
        row['hearings'] = dict(revision['hearings'])
        row['coming_clean']['innocent'] = revision['innocent_ending']
        confession = row['coming_clean']['murderer']
        # Keep the crime admission and clue explanation for the AFTER-vote
        # confession; replace its moral-summary last sentence with a consequence.
        row['coming_clean']['murderer'] = confession.rsplit('. ', 1)[0] + '. ' + revision['guilty_consequence']
        absent_roles = {
            '01':'the director', '02':'the curator', '03':'the dealer', '04':'accounts',
            '05':'the conservator', '06':'the artist', '07':'the painter', '08':'counsel',
            '09':'the professor', '10':'the family representative', '11':'security',
            '12':'the reporter', '13':'the architect', '14':'the advocate',
            '15':'the technology supplier', '16':'the founder', '17':'the auctioneer',
            '18':'the textile artist', '19':'the researcher', '20':'the sculptor',
            '21':'the collector', '22':'the critic', '23':'catering', '24':'the handler',
            '25':'the educator', '26':'the photographer', '27':'the campaigner',
            '28':'the buyer', '29':'the local historian', '30':'production',
        }
        for section in ('hearings','coming_clean'):
            for field, speech in row[section].items():
                for other, role in absent_roles.items():
                    if other in selected:
                        continue
                    first = known[other]['name'].split()[0]
                    if first == 'Dr.':
                        continue  # no new dramatic speech directly addresses the professor
                    # A direct appeal to an absent guest is private feeling,
                    # not an instruction to summon that character at the party.
                    speech = re.sub(r'\b'+re.escape(first)+r'\b', role, speech)
                row[section][field] = speech
    seen = set()
    for row in rows:
        ident = str(row['id']).zfill(2)
        if ident in seen or known[ident]['name'] != row['name']:
            raise ValueError(f'Duplicate or changed public identity: {ident}')
        seen.add(ident)
        expected = {act+'_'+branch for act in ('motive','where','evidence') for branch in ('innocent','murderer')}
        if set(row['hearings']) != expected or set(row['coming_clean']) != {'innocent', 'murderer'}:
            raise ValueError(f'Incomplete paired route: {ident}')
        for act in ('motive', 'where', 'evidence'):
            if row['hearings'][act + '_innocent'] == row['hearings'][act + '_murderer']:
                raise ValueError(f'Identical branches: {ident}/{act}')
        for section in ('hearings', 'coming_clean'):
            for field, speech in row[section].items():
                for rule in rules:
                    if str(rule['absent']).zfill(2) not in selected:
                        speech = speech.replace(rule['find'], rule['replace'])
                speech = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m[1]+m[2].upper(), speech)
                row[section][field] = speech
    result = [r for r in rows if str(r['id']).zfill(2) in selected]
    result.sort(key=lambda r: int(r['id']))
    contracts = yaml.safe_load((LAB / 'evidence-contracts.yaml').read_text(encoding='utf-8'))
    opening = []
    if selected & {'12', '27'}:
        opening = list(contracts['editor_opening'])
        if '12' not in selected:
            opening = [line.replace('PAIGE:', 'PRESS CORRESPONDENT:')
                       .replace('Thank you. Paige, I', 'Thank you. I') for line in opening]
        if '27' in selected:
            opening += contracts['robin_interruption']
    question_spec = yaml.safe_load((LAB / 'question-rounds.yaml').read_text(encoding='utf-8'))
    question_rounds = []
    for phase in ('motive','opportunity','method'):
        groups = []
        covered = []
        for group in question_spec['groups']:
            targets = [str(i).zfill(2) for i in group['character_ids'] if str(i).zfill(2) in selected]
            if targets:
                covered.extend(targets)
                groups.append({'targets':[known[i]['name'] for i in targets], 'question':group['questions'][phase]})
        if set(covered) != selected or len(covered) != len(selected):
            raise ValueError(f'Missing or duplicated question targets in {phase}')
        question_rounds.append({'key':phase,'groups':groups})
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
        'status': 'complete_authoring_bank_not_accepted_or_integrated' if selected <= seen else 'partial_authoring_bank_not_canonical_source_or_complete_game',
        'active_character_ids': sorted(selected),
        'authored_route_count': len(result),
        'unwritten_active_ids': sorted(selected - seen),
        'pre_method_press_interview_opening': opening,
        'question_rounds': question_rounds,
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
