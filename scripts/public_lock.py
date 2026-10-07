"""Refuse mutation of the invite and already-sent character sheets."""
import hashlib,json

def verify_public_lock(root):
    manifest=root/'source/public_assets_lock.json'
    if not manifest.exists():return False
    data=json.loads(manifest.read_text(encoding='utf-8'))
    for relative,expected in data['files'].items():
        path=root/relative.replace('\\','/')
        assert path.is_file(),('Locked public asset missing',relative)
        payload=path.read_bytes()
        if relative in data.get('canonical_text_hashes',{}):
            payload=payload.replace(b'\r\n',b'\n');expected=data['canonical_text_hashes'][relative]
        assert hashlib.sha256(payload).hexdigest()==expected,('Already-sent public asset changed',relative)
    return True

def restore_missing_public(root,complete_kit_path=None,phone_zip_path=None):
    """Source-only archives restore frozen exports, never regenerate sent copy.

    Existing files are never overwritten. Every restored byte is checked against
    the lock. A local complete-kit ZIP can avoid downloading the public archive.
    """
    import io,zipfile,urllib.request
    data=json.loads((root/'source/public_assets_lock.json').read_text(encoding='utf-8'))
    missing=[name for name in data['files'] if not (root/name.replace('\\','/')).is_file()]
    if not missing:return
    kit_prefix='site/downloads/current/'
    phone_name='site/downloads/All_30_Characters_and_Invite.zip'
    assert all(name.replace('\\','/').startswith(kit_prefix) or name.replace('\\','/')==phone_name for name in missing),'Missing editable source or portrait; refusing to replace it with a download.'
    def archive_bytes(local,filename):
        if local:return local.read_bytes()
        errors=[]
        for base in ['https://raw.githubusercontent.com/DalmoMendonca/murdermystery/1bf7bf4/site/downloads/',
                     'https://murder.dalmo.ai/downloads/']:
            try:
                with urllib.request.urlopen(base+filename,timeout=60) as response:return response.read()
            except Exception as exc:errors.append(str(exc))
        raise RuntimeError('Could not restore frozen exports. Download the complete kit alongside the source archive. '+str(errors))
    def save(name,payload):
        expected=data['files'][name]
        assert hashlib.sha256(payload).hexdigest()==expected,('Frozen export download hash mismatch',name)
        target=(root/name.replace('\\','/')).resolve()
        assert target.is_relative_to(root.resolve()) and not target.exists()
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(payload)
    kit_names=[name for name in missing if name.replace('\\','/').startswith(kit_prefix)]
    if kit_names:
        local=complete_kit_path or root/'site/downloads/The_Last_Acquisition_Complete_Kit.zip'
        with zipfile.ZipFile(io.BytesIO(archive_bytes(local if local.exists() else None,'The_Last_Acquisition_Complete_Kit.zip'))) as archive:
            for name in kit_names:save(name,archive.read(name.replace('\\','/')[len(kit_prefix):]))
    if phone_name in [name.replace('\\','/') for name in missing]:
        original=next(name for name in missing if name.replace('\\','/')==phone_name)
        local=phone_zip_path or root/phone_name
        save(original,archive_bytes(local if local.exists() else None,'All_30_Characters_and_Invite.zip'))
    verify_public_lock(root)
