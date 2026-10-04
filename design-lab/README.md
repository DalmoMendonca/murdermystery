# Landing page choices

Three standalone concepts for Dalmo to select before changing the production homepage.

- **After Hours:** a dark marble lion scene, burgundy velvet, cream lettering, and a red download button.
- **The Private View:** an ivory gallery wall with three framed character paintings.
- **Going, Going, Gone:** a teal auction poster with a tilted portrait and a red auction stamp.

Public comparison: https://gala-designs--murdermysteryparty.netlify.app/

Each directory under `published/` contains directly editable HTML and CSS. Shared artwork lives in `published/art/`. Download buttons use the current production ZIP URLs. There are no font downloads, analytics, or client dependencies.

Publish the alternatives as a Netlify draft with `npx netlify deploy --dir design-lab/published --alias gala-designs --site 1c6399c1-a5f5-4f10-95dd-ffa9459e553d --no-build`. Do not use `--prod` for this comparison. Once Dalmo chooses, move the chosen composition into `site/`, change relative art paths to match that directory, run desktop/mobile visual checks, and publish production.

The local `index.html` is an Impeccable live comparison workspace and is intentionally excluded from this branch's release. Its helper injection never appears in the published files. The generation script is local scratch work; the public HTML/CSS files are the editable source of each option.

Validation before selection: the comparison page, all three option URLs, and generated hero artwork returned HTTP 200; each option references both existing download URLs. Visual revisions and full browser QA follow the user's selection in the live workflow.
