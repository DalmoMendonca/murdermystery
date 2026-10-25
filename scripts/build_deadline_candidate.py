"""Build in isolation; do not replace production source or published ZIPs."""
from pathlib import Path
import json,shutil,sys
import build as b
from connected_release import build_release
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-24-DEADLINE-FINISH-SPOILERS')
ready=RUN/'candidate-kit-path.txt'
if ready.exists():ready.unlink()
b.WORK=ROOT/'build'/RUN.name.lower()
b.WORK.mkdir(parents=True,exist_ok=True)
b.SITE=b.WORK/'site'
if not b.SITE.exists():shutil.copytree(ROOT/'site',b.SITE,ignore=shutil.ignore_patterns('downloads'))
(b.SITE/'downloads').mkdir(exist_ok=True)
if not (b.WORK/'fonts').exists():shutil.copytree(ROOT/'build/fonts',b.WORK/'fonts')
# old KIT points to locked exports solely for byte-for-byte copying.
build_release(b,RUN/'candidate-source')
ready.write_text(str(b.KIT)+'\n',encoding='utf-8')
print('Isolated candidate kit and deployment tree ready. Nothing deployed.')
