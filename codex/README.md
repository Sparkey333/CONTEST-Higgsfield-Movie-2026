# The Litiguh codex

A plain-folder Obsidian vault for the *Legend of Litiguh* world: the full text of *Stone of Matter* (Book I) one note per chapter, the world broken out by character, place, stone and era, the series ladder from book to episode to short film to shot, and the screenplays. It is the story's persistent memory for every branch of this repository — the Episode 1 film, the Episode 2 board, and whatever comes next.

## Open it
Obsidian → *Open folder as vault* → this `codex/` folder. Nothing else is needed; links are double-bracket wikilinks, every note has YAML frontmatter, and `Legend of Litiguh — MOC` is the front door. Any Markdown editor works too.

## What is where
| | |
| --- | --- |
| `Legend of Litiguh — MOC.md` | the map of content: zoom out to the world, zoom in to a shot |
| `World/` | characters, places, the Seven Stones, orders and factions, the timeline, the glossary — hand-written, grounded in the text, with mention counts |
| `Book I — Stone of Matter/` | the novel, generated: Prologue, 37 chapters and the Epilogue in four parts, one note each, with word counts |
| `Series/` | the ladder: which chapters each episode adapts, the Episode 1 film record, the Episode 2 board, a proposed map for the rest |
| `Screenplays/` | the screenplays, converted: scene headings as sections |
| `_source/` | the authorities: the paperback `.docx` and the Episode 2 screenplay PDF |
| `_build/` | the converters: `book-to-codex.py`, `screenplay-to-codex.py`, and `chapters.json` (the chapter index they share) |

## Regenerate
The book and screenplay notes are functions of the sources. Do not hand-edit them; edit the source or the converter and rebuild.
```
python3 codex/_build/book-to-codex.py "codex/_source/Stone of Matter — Paperback (B. L. Barkey, 2019).docx" codex
python3 codex/_build/screenplay-to-codex.py "codex/_source/Stone of Matter — Ep. 2 Darkness — screenplay (LoL Movie Night).pdf" codex
```
`World/` and `Series/` are hand-written and are the notes to grow: one note per chapter read, one line per fact, a chapter link on every claim.

## The ladder
World → Book → Part → Chapter → Episode → Short film → Movement → Shot. The first five live here; the last three live in a project folder on an Anchorframe branch (`anchorframe/projects/<slug>/project.json`), and the `Series/` note for each episode is the bridge between the two.

## Names, and what is public
This repository is public. The novel here is the published 2019 text, and the series notes name its characters. The Episode 1 film was released under *production names* so that its public prompts did not tie it to the book; the mapping between the two name sets is deliberately **not** in this folder. Keep it in `Crosswalk.local.md` beside this file — `.gitignore` here excludes `*.local.*` — or in the `crosswalk.local.js` the Episode 1 branch already ignores. If the whole codex should be private, move it to a private repository and leave a pointer; nothing on the film branches depends on its path.
