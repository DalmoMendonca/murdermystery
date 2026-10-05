# Twenty-two-guest revision

Added Al Baster, Anne E. Dote and Justin Tyme to the active cast. Their three public relationship bullets use the host-approved text. Justin's Paige Turner relationship is retained verbatim. Justin is now an Independent Blogger & Local Truthstorian, with new public biography, acting tips, costume suggestions and introduction.

Reciprocal connections are editable under `packet_relationships` in the YAML. Five fit on the secret packet's introduction page: Claire, Dada, Vincent, Frank and Reed. Artie's extra is omitted because his introduction is too full. These extras never appear in the pre-party invitations. Body text remains 16 points; no extra pages are created.

Rebuilt 87 PDFs and 30 pre-party JPEGs. Rendered all 961 pages, with no boundary issues. Compared with the previous release: 922 unchanged page instances, 20 distinct changed pages, all visually inspected. Packet, question, hunt and culprit/attendance checks passed. Private game facts and branches are unchanged.

`scripts/prepare_texting.py` creates a private folder per assigned guest with two 1224×1584 JPEGs: the public invitation and their current pre-party character poster. It also creates a ZIP and optional message drafts. Pass a local JSON list with `character`, `first` and `last` fields via `--guests`, and a folder outside this repository via `--out`. Guest names are never included in published downloads or source control.
