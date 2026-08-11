# LITIGUH — Higgsfield Global Film Festival 2026

A 5:00 short film adapted from Chapters I–III of *Litiguh*, built for the
Higgsfield Global Film Festival ($1,000,000 pool, 14 winners).

## The deliverable

**[`litiguh-director-bible.html`](./litiguh-director-bible.html)** — a self-contained,
themed director's bible. Open it in any browser, or view the published page.

It contains:

| Section | What's in it |
| --- | --- |
| **Control Room** | **A 22-step run sheet that remembers where you stopped. One step is highlighted at a time; press Done and the next lights up. Two lanes — let Claude drive generation over MCP, or click it yourself with the exact screen, prompt and filename named per step.** |
| Asset Prompts | 14 copyable Phase 0 prompts — 5 character sheets, 3 lighting plates, 6 prop and background plates |
| Tweaks & Export | Symptom → the one dial that fixes it, plus the seven-step delivery order |
| The Thesis | Shot-density ribbon: 23 generations at 13.0s mean vs. a typical AI short's 71 at 4.2s |
| The Brief | Verified festival constraints — 3:00 floor, Cinema Studio festival project, Sep 3 deadline |
| Doctrine | Seven rules for avoiding the ad-collage cut rhythm; three camera grammars, one per movement |
| Blend Options | Four ways to combine the three chapters, with a recommendation |
| Shot List | All 23 shots — timecode, duration, model, camera direction, seam, and a copyable prompt |
| Pipeline & Gates | Eight production phases with five hard locks; image-first, video-last |
| Frame String | Interactive ledger of all 39 anchor frames, shared joins, and bridge frames |
| Revision Rules | Four-rung escalation ladder — when to re-roll, when to change the anchors, when to stop |
| Model Matrix | Every Higgsfield video model compared on max length, resolution, frame roles, refs, pros/cons |
| Techniques | Seven mechanisms that buy continuous screen time, ranked |
| Layered Truths | Eight themes from the source text, each mapped to the shot that carries it |
| Key Vault | BYOK storage + `.env` / `config.json` export for the local runner |
| Build Order | 24-day production schedule, Aug 10 → Sep 3 |

## Design constraints driving the film

The brief was to avoid *"a collection of small clips as a long collection of ads."*
The structural answer is a **shot budget of 23 generations** and three distinct camera
grammars — a sustained oner on the Sun, continuous travelling motion over the ocean,
and locked-off static frames on the island — so cuts are motivated by point of view,
time, or revelation, never by a clip running out.

## The pipeline is image-first

In a chained film the keyframes *are* the movie — video generations only interpolate
between anchors that were already approved. So the film is built as a **string of 39
still anchor frames** (23 shots × 2 slots = 46, minus 7 shared joins where one image
serves as both shot N's end and shot N+1's start), locked as a contact sheet and cut
as a stills reel before a single video credit is spent.

Roughly **200 images to 76 video generations**. Rearranging is then an editing problem,
not a regeneration problem: reordering two shots costs 2 images, inserting one costs 3,
cutting one costs 1.

## Source

`source/` holds the original chapter document and its extracted text.

## Keys

The bible's vault covers Higgsfield, Claude, Google AI Studio, Ollama, Lovable,
ElevenLabs, and OpenAI. Keys live in browser local storage only; export a `.env`
for any local tooling. **Never commit `.env`.**
