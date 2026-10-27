"""Build an OPTIONAL, isolated current22 ensemble prototype. Never promotes a release.

Usage: python scripts/build_ensemble_packets.py --source PATH --output PATH --version candidate06
The output directory must be new. Do not invoke until its semantic source is frozen.
"""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json
import re
import shutil

import fitz
import yaml
import build as b
from character_copy import load_characters
from american_copy import american
from ensemble_printable import packets, schedule_text, ensemble_enabled
from public_lock import verify_public_lock

RUN = b.ROOT/'docs/playtest/2026-10-26-ENSEMBLE-RESCUE-SPOILERS'
DEFAULT_BASE = Path(r'C:\Users\dalmo\Documents\Codex\2026-10-24\what\outputs\dramaturgical-candidate02')
PROTECTED = ('02_Hunt_Clues.pdf', '03_Staged_Evidence.pdf',
             '05_Name_Tents_Current_22.pdf', '06_Animal_Draw_Cards.pdf',
             'ACT_III_Evidence.pdf', 'ACT_III_Replacement_Artifacts.pdf')
KEYS = {'motive':'motive', 'opportunity':'where', 'method':'evidence'}
EXPECTED_IDS = ('01','02','04','05','06','07','08','09','11','12','13','14','15','18','19','20','23','24','25','27','28','29')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return ''.join(c.lower() for c in american(text) if c.isalnum())


def load_source(source):
    bank=yaml.safe_load((source/'confirmed.yaml').read_text(encoding='utf-8'))
    performance=yaml.safe_load((source/'performance.yaml').read_text(encoding='utf-8'))
    rows=bank['characters'];ids=[r['id'] for r in rows]
    assert tuple(ids)==EXPECTED_IDS, 'Only the exact current22 roster is supported'
    assert len(set(r['name'] for r in rows))==22
    assert set(bank['active_character_ids'])==set(ids)
    metadata=performance['metadata']
    schedules=metadata['schedules']
    assert isinstance(schedules,list) and len(schedules) in (0,3), 'Support either zero or three marked schedules'
    if schedules:
        assert metadata['group_index_base']==1 and metadata['numbering_is_spoken'] is False
        assert {s['round_key'] for s in schedules}==set(KEYS)
    by_id={r['id']:r for r in rows};by_name={r['name']:r['id'] for r in rows}
    fields=performance['fields'];used=set();part_total=0
    assert isinstance(fields,dict) and set(fields)<=set(ids)
    if not schedules:assert fields=={}, 'Single-turn mode cannot contain hidden numbered parts'
    assert len(bank['question_rounds'])==3 and {r['key'] for r in bank['question_rounds']}==set(KEYS)
    for row in rows:
        for base in KEYS.values():
            for branch in ('innocent','murderer'):
                assert isinstance(row['hearings'][base+'_'+branch],str) and row['hearings'][base+'_'+branch].strip()
        assert all(isinstance(row['coming_clean'][branch],str) and row['coming_clean'][branch].strip() for branch in ('innocent','murderer'))
    for rd in bank['question_rounds']:
        key=rd['key'];base=KEYS[key]
        targets=[name for group in rd['groups'] for name in group['targets']]
        assert len(targets)==22 and set(targets)==set(by_name), (key,'question coverage')
        if not schedules:continue
        schedule=next(s for s in schedules if s['round_key']==key)
        assert 1<=schedule['group_index']<=len(rd['groups'])
        members={by_name[n] for n in rd['groups'][schedule['group_index']-1]['targets']}
        turns=schedule['turns']
        assert {t['id'] for t in turns}==members
        assert len(turns)==len(members)+2, (key,'exactly two returns required')
        assert all(isinstance(t['id'],str) and t['id'] in by_id and isinstance(t['part'],int) for t in turns)
        assert len({(t['id'],t['part']) for t in turns})==len(turns)
        for ident in members:
            needed=[t['part'] for t in turns if t['id']==ident]
            assert needed==list(range(1,len(needed)+1))
            for branch in ('innocent','murderer'):
                field=base+'_'+branch;parts=fields[ident][field]
                assert [p['part'] for p in parts]==needed
                assert all(isinstance(p['speech'],str) and p['speech'].strip() for p in parts)
                assert norm(' '.join(p['speech'] for p in parts))==norm(by_id[ident]['hearings'][field]), (ident,field,'parts must exactly reconstruct canonical answer')
                used.add((ident,field))
        # 22 complete accounts: ordinary single turns plus all fixed group parts.
        assert (22-len(members))+len(turns)==24
        part_total+=len(turns)
    assert used=={(ident,field) for ident,values in fields.items() for field in values}, 'Unused or unexpected performance field'
    assert part_total==(17 if schedules else 0)
    return bank,performance


def cast(bank,source):
    canonical={c['id']:c for c in load_characters()}
    public={r['id']:r for r in yaml.safe_load((b.ROOT/'source/character_copy.yaml').read_text(encoding='utf-8'))['characters']}
    voices={r['id']:r for r in yaml.safe_load((source/'voice-story-bible.yaml').read_text(encoding='utf-8'))['characters']}
    attending={r['id'] for r in bank['characters']};result=[]
    for row in bank['characters']:
        c=copy.deepcopy(canonical[row['id']]);assert c['name']==row['name']
        for field in ('relationships','packet_relationships'):
            c['preparty'][field]=[r['text'] for r in public[c['id']].get(field,[]) if set(r['with'])<=attending]
        c['hearing']=row['hearings']
        c['private'].update(history=voices[c['id']]['private_stake'], final_innocent=row['coming_clean']['innocent'],final_murderer=row['coming_clean']['murderer'])
        result.append(c)
    return result


def baseline_host_sections():
    """Reuse the five original sections verbatim, then replace only conflicting cues.

    Evaluate the local AST's literal host assignment with its one locations value;
    this does not execute build_release or any promotion/public mutation function.
    """
    from hunt_copy import load_hunt
    tree=ast.parse((b.ROOT/'scripts/connected_release.py').read_text(encoding='utf-8'))
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_release')
    assignment=next(n for n in function.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='host' for t in n.targets))
    return eval(compile(ast.Expression(assignment.value),'<baseline-host-sections>','eval'),{'__builtins__':{},'str':str,'locations':load_hunt(b.ROOT)['locations']})


def host_sections(version):
    sections=baseline_host_sections()
    sections[0]['paragraphs'][0]='Use ONLY the confirmed 22-guest packet file in this optional prototype. Print single-sided at 100%. Each guest has twelve pages, including a cover and detachable ballot. Put the covered packet at the assigned seat. Keep private pages facing their player.'
    sections[3]['paragraphs'][-1]='In each act, invite a guest to choose an unheard attending character by name. Outside the marked exchange, ask their printed question; they read their own branch and choose next. Selecting ANY marked member starts the WHOLE fixed exchange from its first speaker. The HOST reads the shared question and cues every scheduled part. Read only the chosen branch; part labels are silent. No one chooses a new guest until the final part finishes. The final speaker chooses an unheard guest outside the completed group. If everyone is heard, close the act. See the next cue page and use the fresh per-act roster.'
    sections[4]['paragraphs'][1]='Tally every attending character, including zero votes. Rank the original top three by total; break ties alphabetically by full character name. Announce ALL THREE names together. Only named INNOCENT guests read Coming Clean now, one at a time in any order. The murderer waits even if named. Do not replace a waiting murderer with the fourth-ranked innocent.'
    sections[4]['paragraphs'][2]='When the named innocents finish, ALWAYS call the selected animal: its guest stands and reads IF MURDERER LAST, whether or not named in the top three. This gives three speeches if the murderer is named, four otherwise. Escaped Justice depends on the ORIGINAL locked top-three tally. Award the accusation, acting, costume and scavenger prizes.'
    if not ensemble_enabled(b):
        sections[3]['paragraphs'][-1]='In each act, invite a guest to choose an unheard attending character by name and ask their printed question from the question page. The named guest reads their own branch and chooses the next unheard guest. Tick that name on the fresh per-act checklist. Every attending guest answers once. If the chain stalls or a completed name is chosen, nominate an unheard guest. When all 22 have answered, close the act. Let discussion happen between rounds while keeping later pages private.'
        return sections
    # Schedules go on a separate sixth page, keeping all original hunt locations.
    sections.append({'title':'Marked exchange cues / '+version,'paragraphs':[
        'Use a fresh name checklist each act. Reserve the entire marked group as in progress when ANY member is chosen. Host reads the shared question once and cues speakers by name in this order. Part numbers are silent navigation labels, never read aloud.',
        *[key.upper()+': '+schedule_text(b,key) for key in KEYS],
        'Between parts, cue only the next listed speaker. Each reader stops at the end of the numbered part in their own branch. Addresses inside speeches are not invitations to interrupt. The last listed speaker finishes the exchange and chooses next; the host then marks ALL its members heard together. Earlier parts do not complete a returning guest\'s answer.',
        'Redirect a repeated/completed name to an unheard guest; never replay a block. If the chain stalls, host nominates an unheard guest. A marked block may occur first, mid-act or last. If no unheard guest remains after either a normal answer or the final group part, the host closes the act. Allow discussion between acts, keeping later pages private.'
    ]})
    return sections


def host_guide(output,version):
    from connected_release import document
    document(b,output/'01_Host_Guide.pdf','Optional ensemble host guide',host_sections(version))
    with fitz.open(output/'01_Host_Guide.pdf') as doc:assert len(doc)==len(host_sections(version)), 'Host section overflow'


def roster(output,chars):
    s=b.Sheet(output/'07_Ensemble_Hearing_Roster.pdf','Optional ensemble host checklist')
    for key in KEYS:
        s.header('HOST CHECKLIST / '+key.upper())
        schedule=next((v for v in b.ENSEMBLE['metadata']['schedules'] if v['round_key']==key),None)
        members={t['id'] for t in schedule['turns']} if schedule else set()
        y=s.block('Fresh act: track complete accounts',42,105,528,24,'BookBold',b.TEAL)+12
        instruction=('EX = marked exchange. Reserve all EX names while in progress; tick ALL only after the final part. Ordinary guests: tick after their answer. Redirect a completed name. When all 22 are heard, close the act.' if schedule else 'Use a fresh checklist each act. Tick each name after that guest reads their own branch. They choose the next unheard guest. Redirect a completed name. When all 22 are heard, close the act.')
        y=s.block(instruction,42,y,528,14)+15
        if schedule:y=s.block(schedule_text(b,key),42,y,528,12,'BookBold',b.TEAL)+20
        for n,c in enumerate(chars):
            col=n//11;row=n%11;x=42+col*276;top=y+row*31
            s.rect(x,top+2,12,12)
            s.block(('EX  ' if c['id'] in members else '')+c['name'],x+20,top,232,13)
        if schedule:s.block('Exchange: [ ] not started    [ ] in progress    [ ] complete',42,661,528,13,'BookBold',b.TEAL)
        s.footer('Everyone supplies a complete account; only final group part hands over.' if schedule else 'Each guest answers once, then chooses the next unheard guest.');s.next()
    s.header('HOST / LOCKED BALLOT TALLY')
    s.block('Attending: ____   Ballots collected: ____   Counts match: ____',42,110,528,14,'BookBold')
    s.block('Lock every ballot before Coming Clean. Tally all 22 names including zero; ties alphabetical by full name. Announce the top THREE together. Named innocents in any order, then selected-animal murderer LAST. No replacement fourth innocent.',42,152,528,14)
    for n,c in enumerate(chars):
        col=n//11;row=n%11;x=42+col*276;y=245+row*29
        s.block(c['name'],x,y,192,13);s.rect(x+196,y,55,21)
    for n in range(3):s.block(f'Top {n+1}: ______________________________  Votes: ____',42,591+n*29,528,14)
    s.block('Escaped Justice: murderer outside the ORIGINAL locked top three.',42,700,528,13,'BookBold',b.TEAL)
    s.footer('Keep ballots locked / Guests retain their Coming Clean pages');s.save()


def ensure_isolated(source,output,version):
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',version), 'Use a simple version label'
    assert source.is_dir()
    assert output!=source and not output.is_relative_to(source)
    assert not output.exists(), 'Refusing to overwrite any existing output or frozen suite'
    assert not output.is_relative_to(b.ROOT/'site') and not output.is_relative_to(b.ROOT/'source')
    # Frozen trials are immutable even if a caller selects a new output folder.
    candidates=[source.parent/(version+'-blind-suite'),source.parent/(version+'-blind'),
                b.ROOT/'docs/playtest'/('2026-10-26-ENSEMBLE-'+version.upper()+'-BLIND-SPOILERS')]
    candidates.extend(p for p in source.parent.glob('*') if p.is_dir() and 'blind' in p.name.lower() and version.lower() in p.name.lower())
    candidates.extend(p for p in (b.ROOT/'docs/playtest').glob('*ENSEMBLE*BLIND*') if p.is_dir())
    assert not any(p.exists() for p in candidates), 'Frozen blind suite exists for this version; refusing rebuild'


def verify_packets(path,bank):
    checked=0
    with fitz.open(path) as doc:
        assert len(doc)==264
        for index,c in enumerate(bank['characters']):
            for field,page in [('motive',5),('where',7),('evidence',9)]:
                text=norm(doc[index*12+page].get_text())
                for branch in ('innocent','murderer'):
                    parts=b.ENSEMBLE['fields'].get(c['id'],{}).get(field+'_'+branch,[])
                    assert norm(c['hearings'][field+'_'+branch]) in text or (parts and all(norm(p['speech']) in text for p in parts)),(c['id'],field,branch)
                    checked+=1
            for branch in ('innocent','murderer'):
                assert norm(c['coming_clean'][branch]) in norm(doc[index*12+11].get_text())
                checked+=1
            for page in (4,6,8):
                text=doc[index*12+page].get_text()
                if ensemble_enabled(b):
                    assert 'WHOLE exchange' in text and 'HOST READS' in text
                else:
                    assert 'next unheard guest' in text
                    for forbidden in ('MARKED EXCHANGE','WHOLE exchange','PART 1','GROUP DONE','HOST READS'):
                        assert forbidden not in text, (c['id'],page,forbidden)
            if not ensemble_enabled(b):
                for page in (5,7,9):
                    text=doc[index*12+page].get_text()
                    for forbidden in ('MARKED EXCHANGE','PART 1','PART 2','GROUP DONE','host cues'):
                        assert forbidden not in text,(c['id'],page,forbidden)
            assert 'ALL THREE' in doc[index*12+11].get_text()
    assert checked==176
    return checked


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=RUN/'candidate06-source')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--version',required=True)
    parser.add_argument('--protected-base',type=Path,default=DEFAULT_BASE)
    args=parser.parse_args(argv)
    source=args.source.resolve();output=args.output.resolve();base=args.protected_base.resolve()
    ensure_isolated(source,output,args.version)
    source_hashes={p.name:digest(p) for p in source.iterdir() if p.is_file()}
    bank,performance=load_source(source)
    verify_public_lock(b.ROOT)
    protected={name:digest(base/name) for name in PROTECTED}
    with fitz.open(base/'03_Staged_Evidence.pdf') as doc:
        assert len(doc)==9
        assert sum(p.get_text().startswith('ACT III: METHOD') for p in doc)==6
    with fitz.open(base/'ACT_III_Evidence.pdf') as doc:assert len(doc)==6
    # Keep all state inside the explicit new isolated output, never release KIT.
    output.mkdir(parents=True)
    b.KIT=output;b.WORK=output/'_layout';b.WORK.mkdir();b.AUDIT=[]
    b.ENSEMBLE=performance;b.ENSEMBLE_NAMES={c['id']:c['name'] for c in bank['characters']}
    b.fonts();chars=cast(bank,source)
    packets(chars,b,bank['question_rounds'])
    merged=output/'PRINT_WITHOUT_READING/03_Secret_Player_Packets_PRINT_DO_NOT_READ.pdf'
    merged.replace(output/'04_Guest_Packets_PRINT_WITHOUT_READING.pdf')
    checked=verify_packets(output/'04_Guest_Packets_PRINT_WITHOUT_READING.pdf',bank)
    host_guide(output,args.version);roster(output,chars)
    for name,sha in protected.items():
        shutil.copy2(base/name,output/name)
        assert digest(output/name)==sha
    verify_public_lock(b.ROOT)
    assert source_hashes=={p.name:digest(p) for p in source.iterdir() if p.is_file()}, 'Source changed during build'
    receipt={'version':args.version,'status':'OPTIONAL ISOLATED PROTOTYPE; no promotion or performance claim',
             'source':str(source),'source_sha256':source_hashes,
             'roster':'current22 only; all30 not built or verified','packet_pages':264,'branches_verified':checked,
             'mode':'marked_exchanges' if ensemble_enabled(b) else 'single_turn',
             'speaker_entries_per_act':24 if ensemble_enabled(b) else 22,
             'schedule_entries':sum(len(row['turns']) for row in performance['metadata']['schedules']),
             'host_pages':len(host_sections(args.version)),
             'spoken_branch_words':sum(len(row['hearings'][base+'_'+branch].split()) for row in bank['characters'] for base in KEYS.values() for branch in ('innocent','murderer'))+sum(len(row['coming_clean'][branch].split()) for row in bank['characters'] for branch in ('innocent','murderer')),
             'evidence_pages':9,'act_iii_pages':6,'protected_copied_sha256':protected,
             'minimum_speech_pt':15,'layout_assertions':'all drawn blocks fit their measured boundaries',
             'visual_review':'REQUIRED; automated geometry is not visual acceptance'}
    (output/'ensemble-build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    (output/'_layout/layout-audit.json').write_text(json.dumps(b.AUDIT,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
