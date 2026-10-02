#!/usr/bin/env python3
"""Turn a screenplay PDF (or its extracted .txt) into one codex note: scene headings become
sections, character cues become bold, page markers go.   
    python3 codex/_build/screenplay-to-codex.py "codex/_source/<file>.pdf" codex
Text comes out of the PDF with pypdfium2 (pip install pypdfium2); a .txt is used as is.
"""
import re, sys, pathlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
if src.suffix.lower() == ".pdf":
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(str(src)); text = "\n".join(p.get_textpage().get_text_range() for p in doc)
else: text = src.read_text(encoding="utf-8")
lines, body, scenes = text.splitlines(), [], 0
for raw in lines:
    l = raw.rstrip()
    if re.match(r"^=+ PAGE \d+ =+$", l) or re.match(r"^\s*\d{1,3}\.?\s*$", l): continue
    s = l.strip()
    if re.match(r"^(EXT|INT)[:.]", s): scenes += 1; body.append(f"\n## {s}\n"); continue
    if re.match(r"^(FADE IN|FADE OUT|CUT TO|DISSOLVE TO)[:.]?$", s, re.I): body.append(f"*{s}*\n"); continue
    if re.match(r"^[A-Z][A-Z0-9 .'’()\-]{1,40}$", s) and len(s) > 1 and not s.endswith("."): body.append(f"\n**{s}**  "); continue
    if s.startswith("(") and s.endswith(")"): body.append(f"*{s}*  "); continue
    body.append(s if s else "")
title = re.sub(r"\s*—\s*screenplay.*$", "", src.stem)
md = "---\ntitle: \"" + title.replace('"', "'") + " (screenplay)\"\nkind: screenplay\nsource: \"" + src.name + "\"\nscenes: " + str(scenes) + "\ntags: [screenplay, ep-2]\n---\n\n# " + title + " — screenplay\n\nConverted from the PDF by `codex/_build/screenplay-to-codex.py`; the PDF in `codex/_source/` is the authority. " + str(scenes) + " scene headings. ← [[Series/Ep 2 — Darkness|Ep 2 — Darkness]] · [[Legend of Litiguh — MOC]]\n\n" + "\n".join(body).strip() + "\n"
md = re.sub(r"\n{3,}", "\n\n", md)
(out / "Screenplays").mkdir(parents=True, exist_ok=True)
dst = out / "Screenplays" / (title + " (screenplay).md"); dst.write_text(md, encoding="utf-8")
print(f"wrote {dst} · {scenes} scenes · {len(md.split())} words")
