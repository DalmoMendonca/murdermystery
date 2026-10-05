# Editing the character copy

Edit `source/character_copy.yaml`. It contains all 30 characters' public descriptions, roles, acting tips, costume suggestions, relationship bullets, and spoken introductions. It contains no private secrets, answers, or confessions.

The current `active_character_ids` list has the 19 assigned roles. Guest names and phone numbers stay in your Google Sheet and are not published in the repository. Update that list when attendance changes. A relationship prints only when everyone listed in its `with` field is active. Keep the target IDs and names in each bullet consistent. All 15 core roles must remain active.

Each character's `relationships` list is editable. `with: ['02']`, for example, means the bullet refers to Claire O’Scuro. The ID-to-name mapping appears in the character entries. Save at least one relationship to another active role for each active character. The present 19-player version has three bullets per active character.

Use the full character names in relationship bullets. If you change whom a bullet refers to, update its `with` IDs too. The build checks that the full names in the text match those IDs and stops with a correction message if they disagree.

Keep IDs and character names unchanged unless we also update the questions, evidence, and private packets. All other public copy fields can be edited. Costume suggestions do not need a repeated introductory label.

The build reads this YAML directly. `source/characters.json` preserves the original full-cast copy and private game logic; editing YAML does not change murderer selection, evidence, answers, or confessions. To restore relationships when a role rejoins, use the original relationship bullets from that JSON or ask me to revise the active cast.

After editing, ask me to rebuild and publish from the edited YAML. I will validate the roster, render the changed pages, check their layout, rebuild the downloads, commit the files, and update murder.dalmo.ai. The normal build remains `python scripts/build.py`.
