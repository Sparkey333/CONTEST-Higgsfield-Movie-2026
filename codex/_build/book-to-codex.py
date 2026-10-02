#!/usr/bin/env python3
"""Split the paperback .docx into one Obsidian note per chapter, with front matter and links.
   python3 codex/_build/book-to-codex.py codex/_source/<the .docx> codex
Idempotent: regenerates every note under "Book I — Stone of Matter/". Hand-written notes live elsewhere."""
import sys, zipfile, re, html, pathlib, json
src = pathlib.Path(sys.argv[1]); root = pathlib.Path(sys.argv[2])
xml = zipfile.ZipFile(src).read("word/document.xml").decode("utf8")
paras = []
for m in re.finditer(r"<w:p[ >].*?</w:p>", xml, re.S):
    p = m.group(0)
    st = re.search(r'<w:pStyle w:val="([^"]+)"', p); st = st.group(1) if st else ""
    runs = re.findall(r"<w:r[ >].*?</w:r>", p, re.S)
    txt = ""
    for r in runs:
        t = "".join(html.unescape(x) for x in re.findall(r"<w:t[^>]*>(.*?)</w:t>", r, re.S))
        if not t: continue
        if "<w:i/>" in r or "<w:i " in r: t = "*" + t + "*"
        txt += t
    txt = txt.replace("**", "").strip()
    if txt and not txt.startswith("<w:"): paras.append((st, txt))
ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,"XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15,"XVI":16,"XVII":17,"XVIII":18,"XIX":19,"XX":20,"XXI":21,"XXII":22,"XXIII":23,"XXIV":24,"XXV":25,"XXVI":26,"XXVII":27,"XXVIII":28,"XXIX":29,"XXX":30,"XXXI":31,"XXXII":32,"XXXIII":33,"XXXIV":34,"XXXV":35,"XXXVI":36,"XXXVII":37}
def slug(t): return re.sub(r"[^\w\s\-–—']", "", t).strip()
# walk: parts and chapters
chapters = []; part = 0; cur = None
start = next(i for i, (st, t) in enumerate(paras) if t == "PROLOGUE")
for st, t in paras[start:]:
    if t in ("PART I", "PART II", "PART III", "PART IV"): part = ROMAN[t.split()[1]]; continue
    if t in ("END OF PART I", "END OF PART II", "END OF PART III"): continue
    if t in ("END OF BOOK I", "REVIEW", "Acknowledgements", "About the Author"): cur = None; 
    if t == "Acknowledgements" or t == "About the Author": cur = dict(kind="back", n=None, part=part, head=t, title="", body=[]); chapters.append(cur); continue
    if t in ("END OF BOOK I", "REVIEW"): continue
    if st == "Heading1" or t in ("PROLOGUE", "EPILOGUE"):
        if t.startswith("CHAPTER "):
            n = ROMAN[t.split()[1]]; cur = dict(kind="chapter", n=n, part=part, head=t, title="", body=[])
        else:
            cur = dict(kind=t.lower(), n=None, part=part, head=t, title="", body=[])
        chapters.append(cur); continue
    if cur is None: continue
    if st == "CSP-ChapterTitle" and not cur["title"]: cur["title"] = t.title().replace("’S", "’s").replace("Of ", "of ").replace("The ", "the ").replace("– The", "– The"); continue
    if not cur["title"] and cur["kind"] == "chapter" and len(cur["body"]) == 0 and t.isupper() and len(t) < 40: cur["title"] = t.title(); continue
    cur["body"].append((st, t))
# titles that live only in the TOC (e.g. chapter XIV): best effort from the first body line
for c in chapters:
    if c["kind"] == "chapter" and not c["title"]: c["title"] = "Untitled"
PARTS = {0: "Front matter", 1: "Part I", 2: "Part II", 3: "Part III", 4: "Part IV"}
book = root / "Book I — Stone of Matter"
for d in list(book.glob("**/*.md")): d.unlink()
index = []
for c in chapters:
    if c["kind"] == "chapter":
        name = f"Ch {c['n']:02d} — {slug(c['title'])}"; folder = book / PARTS[c["part"]]
    elif c["kind"] == "prologue": name = "Ch 00 — Prologue"; folder = book / "Part I"
    elif c["kind"] == "epilogue": name = "Ch 38 — Epilogue"; folder = book / "Part IV"
    else: name = c["head"]; folder = book / "Back matter"
    folder.mkdir(parents=True, exist_ok=True)
    words = sum(len(t.split()) for _, t in c["body"])
    body = []; pend = ""
    for st, t in c["body"]:
        if re.fullmatch(r"[IVX]+", t): body.append(f"\n## {t}\n"); continue
        if re.fullmatch(r"[A-Z]", t): pend = t; continue
        if pend: t = pend + t; pend = ""
        body.append(t + "\n")
    tag = "chapter" if c["kind"] == "chapter" else c["kind"]
    fm = ["---", f'title: "{c["title"] or c["head"].title()}"', f"book: Stone of Matter", f"part: {c['part']}", f"chapter: {c['n'] if c['n'] is not None else 'null'}", f"words: {words}", f"tags: [book-i, {tag}]", "---"]
    head = "# " + (c["head"] if c["head"].startswith("CHAPTER") else c["head"].title()).replace("CHAPTER", "Chapter") + (f" — {c['title']}" if c["title"] else "")
    nav = "← [[Book I — Stone of Matter/_Book I — Stone of Matter|Book I]] · [[Legend of Litiguh — MOC]]"
    (folder / f"{name}.md").write_text("\n".join(fm) + "\n\n" + head + "\n\n" + nav + "\n\n" + "\n".join(body))
    index.append((c["part"], name, c["title"], words, folder.name))
# the book's own index note
lines = ["---", "title: Book I — Stone of Matter", "tags: [book-i, moc]", "---", "", "# Book I — Stone of Matter", "", "B. L. Barkey · Wolf Den Publishing · 2019 · ISBN 9781093422160. Thirty-seven chapters, a prologue and an epilogue in four parts; regenerated from the paperback by `codex/_build/book-to-codex.py`. The source file is in `_source/`.", "", "← [[Legend of Litiguh — MOC]]", ""]
lastp = None
for p, name, title, words, folder in index:
    if folder != lastp: lines.append(f"\n## {folder}\n"); lastp = folder
    lines.append(f"- [[{folder}/{name}|{name}]] · {words:,} words")
(book / "_Book I — Stone of Matter.md").write_text("\n".join(lines) + "\n")
json.dump([dict(part=p, name=n, title=t, words=w, folder=f) for p, n, t, w, f in index], open(root / "_build" / "chapters.json", "w"), indent=1)
print(len(index), "notes ·", sum(w for _, _, _, w, _ in index), "words")
