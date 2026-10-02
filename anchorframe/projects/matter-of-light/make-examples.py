#!/usr/bin/env python3
"""Build examples.json for this project: the frames, takes, sheets and voice lines that show
each workflow stage, with what to look for. Curation lives here; every URL comes from the data
files, so nothing is retyped.   python3 anchorframe/projects/matter-of-light/make-examples.py <element-thumbs.json>
"""
import json, sys, pathlib
P = pathlib.Path(__file__).resolve().parent; ROOT = P.parents[2]
G = {g["id"][:8]: g for g in json.load(open(P / "generations.json"))}
F = {f["f"]: f for f in json.load(open(ROOT / "design" / "anchor-plan.json"))["frames"]}
E = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
V = json.load(open(ROOT / "design" / "dialogue.json"))["takes"]["lines"]
SOUL = {"oriane": "https://d2ol7oe51mr4n9.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/3eb248ba-0858-4f4c-971a-930e7a577fec.png",
        "caedom-ascended": "https://d2ol7oe51mr4n9.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/212bcdc1-b55e-48c0-93ea-4a89a2e66bd5.png",
        "alder": "https://d2ol7oe51mr4n9.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/68fc0492-219e-4c18-99fa-b7d22de8398c.png",
        "wren": "https://d2ol7oe51mr4n9.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/1a4944fa-82d6-4e7e-9d51-26d1a00c1065.png"}
def frame(f, label, why): x = F[f]; return {"kind": "image", "ar": "21/9", "url": x["url"], "label": label or f, "why": why, "from": f"frame {f} · {x['job'][:8]}"}
def clip(id8, label, why): g = G[id8]; return {"kind": "video", "ar": "21/9", "url": g["mp4"], "poster": g["thumb"], "label": label, "why": why, "from": f"take {id8} · {g['duration']}s"}
def sheet(name, label, why, ar="16/9"): e = E.get(name) or sys.exit(f"no thumbnail for element {name}"); return {"kind": "image", "ar": ar, "url": e["thumb"], "label": label, "why": why, "from": f"element @{name}"}
def soul(name, label, why): return {"kind": "image", "ar": "1/1", "url": SOUL[name], "label": label, "why": why, "from": f"soul {name}"}
def voice(key, n, label, why): t = V[key]["takes"][n - 1]; return {"kind": "audio", "url": t["file"], "label": label, "why": why, "from": f"{key} · take {n} · rate {t.get('speech_rate')}"}
def pair(a, b, label, why): return {"kind": "pair", "a": a, "b": b, "label": label, "why": why, "from": a.get("from", "") + "  ·  " + b.get("from", "")}
X = {"project": "matter-of-light", "title": "Matter of Light", "note": "Every asset here was generated inside the festival project and is public under the festival's rules. They are examples, not templates: look for the thing named under each one, then make your own.",
 "stages": {
  "story": [
   clip("4896c8e3", "S22 · the turn", "The last held close-up belongs to whoever changes. The ending was rewritten on Sep 14 to make it Alder's, and this take carries it."),
   frame("F35", "F35 · the most important single image", "Alder at the end of the push, one dark cloud out of focus behind him. Written and anchored before a second of video existed."),
   frame("F01", "F01 · almost nothing", "The first frame of the film. Everything the opening does, it does by revealing.")],
  "cast": [
   pair(soul("oriane", "oriane", ""), soul("caedom-ascended", "caedom-ascended", ""), "Two of the four Souls", "One identity, trained once. Every state sheet — damaged, ascended, mortal — is generated from it, never re-described."),
   pair(soul("alder", "alder", ""), soul("wren", "wren", ""), "The brothers", "Same height, age only in the face. Two-person shots cannot use a Soul at all — they run on the elements."),
   sheet("white-temple", "A location, three ways on one sheet", "Intact in daylight, under cannon fire, and from behind looking out to sea. One id, three uses, no drift between them."),
   pair(sheet("plate-sun", "plate-sun", ""), sheet("plate-ocean-dark", "plate-ocean-dark", ""), "Two of the four lighting plates", "Every frame on a board inherits its plate's key. One board per plate is what stops the light drifting."),
   pair(sheet("caedom-ascended", "caedom-ascended (the film)", ""), sheet("char_caedom_v2_human", "char_caedom_v2_human (S5's mistake)", ""), "The identity break the model can't see", "All four takes of S5 attached the mortal sheet while every other shot used the ascended one. Scores rank takes; only a continuity read catches the wrong face."),
   sheet("twelve-ships", "Replaced by hand — and the repo didn't know", "This element replaced prop_enemy_ships in the web app. Four prompts pointed at the dead id for days. Record old → new the moment you swap.")],
  "anchors": [
   pair(frame("F01", "F01", ""), frame("F02", "F02 · shared", ""), "A shared frame", "F02 ends S1 and starts S2. One image doing two jobs, generated once; the seam lives inside the glare."),
   pair(frame("F09", "F09 · the facet", ""), frame("F10", "F10 · the ocean", ""), "The match pair", "The tear's blue facet becomes open water. Designed as a pair, not found in the edit — made independently, the 108-year jump costs the audience a beat."),
   frame("B01", "B01 · a bridge", "The leviathan's flank filling frame to near-black. It has to go genuinely black — 70% obscured reads as a hidden cut that failed."),
   frame("F17", "F17 · scale in one frame", "Oriane tiny between the opening jaws. This frame has to carry the shot's whole point alone, because the shot will not cut.")],
  "timing": [
   pair(frame("F22", "F22 · the streak in orbit", ""), frame("F23", "F23 · its residue on the beach", ""), "One object carries the cut across a day and three thousand miles", "The structural hinge between movements. Deciding where this lands is a Gate C decision — after it, moving it costs video."),
   clip("aa65cc3d", "S15 · the zero-generation fix", "The first five seconds of this take were moved before the vortex so the audience meets the brothers before Oriane dies. The rest stayed. One blade cut, no render.")],
  "motion": [
   clip("d484a959", "S21 · chained, 16s", "Chained on F32→F33. Only 2 of 16 renders in the account used start/end frames — both the longest shots, which is exactly right. Chain anything over 12s."),
   pair(clip("1971bd66", "S10 · @leviathan", ""), clip("4abb698e", "S10 · @prop_dragon_v1_dead", ""), "Same shot, two creature sheets", "The left take attaches the film's leviathan; the right attached a different creature entirely. Both scored fine. Read the references, not just the numbers."),
   clip("f84a308f", "S1 · one 30s crane", "It carries S1 and S2 in a single move, exactly as the bible asked. If it has to lose time, it comes off the front — every take here paid on its last second.")],
  "sound": [
   voice("S1-CAEDOM", 1, "The opening narration", "Measured, vast, already grieving. Lay it under the black so the first three seconds are not silent; the crane rises under the voice."),
   voice("S22-ALDER-b", 1, "“There's something more.”", "The smile arriving — hope, relief, something braver than either. Four words carry the ending."),
   voice("S5-CAEDOM", 1, "“Tomorrow.”", "One word, and it ends the scene. Generate the voice first; attach it as an audio reference; turn the model's own audio off on that shot.")],
  "cut": [
   pair(clip("4896c8e3", "S22 · chroma · scored 59", ""), clip("6b0d0fac", "S22 · flat · scored 49", ""), "Selection is the grade", "Same shot, same boys, one look decision, ten points. A colour pass across two lighting worlds in an hour drifts; picking the graded take does not."),
   clip("f8035ad4", "S6 · already opens on the match cut", "It carries the tear-to-ocean cut and the card — which made a planned transition shot redundant. Check what you have before you generate what you planned."),
   frame("F37", "F37 · the last frame", "The frozen tear as one point of light on a vast floor. It rhymes with F01; the end-card plate continues it to black, and the credits go on after, in the NLE.")],
  "deliver": []
 }}
(P / "examples.json").write_text(json.dumps(X, indent=1, ensure_ascii=False))
n = sum(len(v) for v in X["stages"].values()); print(f"examples.json: {n} examples across {sum(1 for v in X['stages'].values() if v)} stages")
