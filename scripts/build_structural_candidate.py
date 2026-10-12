"""Actual production render in an isolated workspace, with no publishing/package step."""
from pathlib import Path
import shutil,sys
import build as b
from connected_release import build_release
run=b.ROOT/'docs/playtest'/(sys.argv[1] if len(sys.argv)>1 else '2026-10-11-STRUCTURAL-FOLLOWUP-SPOILERS')
b.WORK=run/'build';b.WORK.mkdir(exist_ok=True)
font_dest=b.WORK/'fonts'
if not font_dest.exists():shutil.copytree(b.ROOT/'build/fonts',font_dest)
# The public-asset copy uses the canonical old kit path; retain it until build_release
# switches to the isolated output. The public source and live downloads never change.
b.SITE=b.WORK/'preview-site';b.SITE.mkdir(exist_ok=True)
b.package=lambda:None
build_release(b,run/'candidate-source')
(run/'candidate-kit-path.txt').write_text(str(b.KIT)+'\n',encoding='utf-8')
