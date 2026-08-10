# LITIGUH — Higgsfield Global Film Festival 2026

A 5:00 short film adapted from Chapters I–III of *Litiguh*, built for the
Higgsfield Global Film Festival ($1,000,000 pool, 14 winners).

## The deliverable

**[`litiguh-director-bible.html`](./litiguh-director-bible.html)** — a self-contained,
themed director's bible. Open it in any browser, or view the published page.

It contains:

| Section | What's in it |
| --- | --- |
| The Thesis | Shot-density ribbon: 23 generations at 13.0s mean vs. a typical AI short's 71 at 4.2s |
| The Brief | Verified festival constraints — 3:00 floor, Cinema Studio festival project, Sep 3 deadline |
| Doctrine | Seven rules for avoiding the ad-collage cut rhythm; three camera grammars, one per movement |
| Blend Options | Four ways to combine the three chapters, with a recommendation |
| Shot List | All 23 shots — timecode, duration, model, camera direction, seam, and a copyable prompt |
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

## Source

`source/` holds the original chapter document and its extracted text.

## Keys

The bible's vault covers Higgsfield, Claude, Google AI Studio, Ollama, Lovable,
ElevenLabs, and OpenAI. Keys live in browser local storage only; export a `.env`
for any local tooling. **Never commit `.env`.**
