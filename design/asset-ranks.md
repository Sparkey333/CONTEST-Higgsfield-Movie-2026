# Asset ranks — what is measured, what is judged, and what gets promoted

Two different kinds of claim live in this file and they are not interchangeable.

**Videos are measured.** Higgsfield's Virality Predictor returns numbers; those numbers are in
`virality-results.json` with the job ids that produced them, and the ranking below is just that file
sorted. Anyone can re-run it and get the same order.

**Stills are judged, structurally.** The predictor has no still-image mode — there is no way to score
an image with it — and the sandbox this analysis ran in cannot load the account's CDN, so **no image
in this project was looked at.** The still ranking below is built from things that *are* checkable
without seeing a picture: which lane it belongs to, how many generations back it, whether one model
or several rendered it, and whether it has already been promoted to a clean element handle. That is
a real signal about pipeline health. It is not a claim about whether the picture is good, and it
should not be read as one.

---

## Videos — measured

Nine clips, three video models, two weeks of generation dates.

| # | Clip | Ground | Model | Hook | Overall | Engage | DMN ↓ |
|---|------|--------|-------|-----:|--------:|-------:|------:|
| 1 | Starless void, colossal form | dark | kling3_0_turbo | **40** | **56** | **55** | **0.453** |
| 2 | Water sphere, macro | dark | kling3_0_turbo | 39 | 55 | 50 | 0.553 |
| 3 | Coral reef, low and fast | dark | kling3_0_turbo | 36 | 53 | 48 | 0.501 |
| 4 | Figure on mirror water | dark | kling3_0_turbo | 33 | 51 | 44 | 0.565 |
| 5 | Two figures on the Sun | bright | seedance_2_5 | 34 | 49 | 41 | 0.573 |
| 6 | Courtyard on the Sun | bright | kling3_0_turbo | 31 | 48 | 40 | 0.605 |
| 7 | Light-wielder, glow in void | bright | seedance_2_5 | 30 | 48 | 39 | 0.649 |
| 8 | The Sun, vertical 10 s | bright | minimax_h3 | 32 | 47 | 41 | 0.592 |
| 9 | The Sun, wide | bright | seedance_2_5 | 31 | 47 | 39 | 0.607 |

DMN is the mind-wandering proxy: lower is better. Sustain scored **100 on every clip**, zero variance
— retention is not the problem and needs no work. Every point available is in the first three seconds.

### What actually separates them

Look at the *Ground* column. **Every high-contrast image on a dark ground scores 51–56. Every diffuse
bright field scores 47–49. Nothing crosses the line** — the worst dark clip beats the best bright clip
by two points.

That separation survives three video models, four subjects (void, water, reef, figures), three aspect
ratios, and two weeks of dates. The mind-wandering proxy orders the whole table almost by itself:
0.453, 0.501, 0.553, 0.565, 0.573, 0.592, 0.605, 0.607, 0.649. A diffuse bright field gives the eye
nowhere to fix, and attention drifts.

**Two hypotheses were tested and killed on the way to that, recorded so they aren't re-run:**

- *Close and singular beats spectacle at distance.* Refuted by the coral reef flyover, which has no
  single subject anywhere in frame and outscored the lone walking figure.
- *kling3_0_turbo beats seedance and minimax by ~6 points.* This looked airtight — four kling clips
  at 51–56 against four others at 47–49, zero overlap. Then the kling courtyard-on-the-Sun control
  came back at **48**, inside the seedance range and eight points below every other kling clip. The
  apparent model effect was an artefact of every early kling clip happening to be shot on dark ground.
  **Do not choose a video model on this evidence.**

### The warning this produces about the film itself

**Movement I is the Sun, and the Sun scored worst four separate ways with no exception:** wide 16:9
seedance (47), vertical minimax (47), two figures seedance (49), kling courtyard (48). Three models,
three aspect ratios, four compositions, one answer.

This is *not* an argument to change Movement I. A sustained bright oner on the Sun is the film's
opening argument and the festival cut keeps it. It is an argument that **Movement I must never be the
material the social posts are cut from.** Post the ocean and the island. Hold the Sun for the film.

Caveat worth keeping: nine clips is a small sample, subject was not randomised against luminance, and
these are the platform's proxy metrics, not audience data.

### Promoted for main asset consideration — video

1. **Starless void, colossal form** — best on hook, overall, engagement and mind-wandering
   simultaneously. Opens the release stream.
2. **Water sphere macro** — highest attention mean in the set, and the only clip whose *first* frame
   sits near its own attention peak.
3. **Coral reef flyover** — second-best mind-wandering figure. Movement II establishing.
4. **Figure on mirror water** — the best-scoring clip containing a person.

All four are landscape, water or void with no identifiable character design in them, so they carry
none of the publication risk the character clips do — nothing in them can be contradicted by the
finished film. The best-scoring material is also the safest to post, which does not usually happen.

---

## Stills — judged structurally

Sixteen of the forty-two asset sheets have generations attributed to them by prompt match. **All
sixteen are characters.** The twenty-six with nothing against them are every location, every lighting
plate, every prop and creature, every effect, and five Turned domain variants.

That is the shape of the project right now: **the cast is cast and the world is not built.**

### Ranking signals

- **A lane present** — the continuity lane everything downstream inherits. Its absence is disqualifying.
- **One model or several** — an A lane rendered by two different engines is drift built into the
  foundation. This is the signal that separates tier 1 from tier 2 below.
- **Generation count** — how much selection pressure was applied before something was chosen.
- **Clean element handle** — already promoted, already named in production vocabulary.

### Tier 1 — promote now

A lane rendered by a single model, backed by eight or more generations, already carrying a clean
element handle.

| Asset | A lane | Model | Handle |
|---|---:|---|---|
| The Keepers | 12 | nano_banana_2 | `@keeper` |
| The fused Dominion wielder | 12 | nano_banana_2 | `@lev-rider` |
| Oriane | 14 | text2image_soul_v2 | `@oriane` |
| The Turned — sixteen pursuers | 8 | nano_banana_2 | `@turned` |
| Oriane — the ascended state | 8 | nano_banana_2 | `@oriane-ascended` |
| Oriane — battle damage | 8 | text2image_soul_v2 | `@oriane-damaged` |
| The Turned — attunement ladder | 8 | nano_banana_2 | — |
| Aura grammar — core vs hollow | 8 | nano_banana_2 | — |

### Tier 2 — one re-render away

These have an A lane, but it was rendered by **two different models**, which is precisely the drift
the A lane exists to prevent. Re-render each A lane on one engine before locking identity at Gate A.

| Asset | A lane split | Handle |
|---|---|---|
| Alder | 8 × nano_banana_2 + 4 × text2image_soul_v2 | `@alder` |
| Wren | 8 × nano_banana_2 + 4 × text2image_soul_v2 | `@wren` |
| Caedom — the mortal form | 4 × nano_banana_2 + 4 × text2image_soul_v2 | `@caedom-mortal` |
| The Threadwright | 4 × nano_banana_2 + 2 × text2image_soul_v2 | `@threadwright` |
| Turned — Water and its Phases | 4 × text2image_soul_v2 + 2 × soul_cinematic + 1 × seedream_v5_pro | — |

**The brothers are the urgent case.** Alder and Wren have to read as the same age, the same height,
and unmistakably related, and their identity sheets are currently two-thirds one engine and one-third
another. Pick nano_banana_2 — it is the majority on both — and re-render the four odd ones.

*A worry that turned out to be unfounded, recorded so it is not re-investigated:* several A lanes use
`text2image_soul_v2`, and the account's only trained Soul is mislabelled — named for Caedom, resolving
to Oriane's images. If those generations had been Soul-conditioned, Wren and Caedom would be wearing
Oriane's face. They were not: **no `soul_id` is attached to any generation in any A lane.** The model
was used text-to-image. The sheets are clean.

### Tier 3 — blocked

**Caedom — the ascended form** has B, C and D lanes and **no A lane at all**. It is the form Scene 1
is played in, and it is the one character with no identity sheet. Its element handle
`@caedom-ascended` was sourced from lane B as a stopgap and is labelled as such. This is the single
highest-priority character generation left.

### Tier 4 — the twenty-six with nothing

Not ranked, because there is nothing to rank. Ordered for generation in the canvas build queue
instead — three lighting plates, then six locations, then seven props and creatures, then four
effects and the five Turned variants. That order is in the director's bible under **Higgsfield → the
canvas**, and it is an order rather than a list: every location inherits its key from a plate, so a
plate made late invalidates the locations made before it.

One thing the video results change about how these get made. The three lighting plates are the assets
that set luminance structure for everything downstream, and the measurements above say luminance
structure is the single strongest predictor in the whole dataset. So when generating **l2 (the Ocean)**
and **l3 (the Island)**, push for a dark ground with high local contrast — that is the regime every
clip in the top four sits in, and those two movements are where the social cuts have to come from.
**l1 (the Sun)** stays a diffuse bright field because the film requires it; just know while making it
that it is the plate whose descendants will not travel, and do not spend extra passes trying to make
it perform on a metric it structurally cannot win.

---

## What could not be done, and why

- **No still was scored.** The predictor is video-only. There is no workaround that does not involve
  animating each image into a clip first, and generation through the API bills credits the account
  does not have.
- **No image was looked at.** The CDN holding every asset is unreachable from the analysis sandbox.
  Everything above is inference from prompt text, lane structure, model, count and date.
- **Clips over 16 seconds cannot be tested at all.** That rules out both 30 s 21:9 clips and every
  20 s seedance clip in the account.
