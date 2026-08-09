# Score & Sound — The DarkHearts Sonic Signature

*Metal and EDM roots, deployed as structure rather than as decoration.*

---

## 0. Rules Check First

Per `01-contest-brief.md` §6, one question governs this entire document:

> **Can the score be composed off-platform in your DAW and married in the edit, or must all audio be generated in Higgsfield?**

The official email says the film must be "made entirely in Higgsfield." Trade coverage says the rules don't spell out tool exclusivity beyond the subscription, and separately notes that **licensed music is prohibited — original or royalty-free compositions only**, with at least one documented entry using ElevenLabs for sound design.

Both paths are written below. **Answer this before Aug 12.**

- **Path A — DAW-composed.** You write and perform it. Best result, and the "original composition" clause clearly permits original music; the only question is the tool-exclusivity clause.
- **Path B — on-platform generated.** Build the score with Higgsfield's audio generation against the same spec. Fully compliant under the strictest reading. The spec below is written to survive either path — it's a *design*, not a session file.

Either way: **do not use anything licensed.** Not a needle-drop, not a stem, not a sample pack you didn't clear. Every entrant's project files go public after the deadline, which means every entrant's audio sources become inspectable. Do not be the disqualification story.

---

## 1. The Governing Idea

The DarkHearts thesis from `02-creative-dna.md`:

> **Stone remembers. Water carries. Sound is how the memory gets out.**

In SILT that isn't subtext — it's the plot. Which means **the score cannot be applied to the film. The score is a character in it.** The rule for the whole mix:

> **Every sound in SILT is either the dam, the bell, or the weather. There is no fourth category, and there is no music that isn't one of those three.**

No orchestral swell. No trailer braams. No emotional cue telling the audience to feel something. If a sound cannot be pointed at inside the frame, it does not exist — the audio equivalent of the "one light source you can point at" rule in the Look Bible. Papamichael's discipline, applied to the mix.

---

## 2. The Frequency Spine

This is the technical conceit and it is *actually correct*, which is the point.

| Element | Freq | Note | Role |
|---|---|---|---|
| Reservoir drone | **41.2 Hz** | **E1** | The weight of forty feet of water. Sub-only. Felt, not heard. |
| **The bell fundamental** | **82.4 Hz** | **E2** | The film's root. Every strike. |
| Turbine harmonic | **82.4 Hz** | **E2** | *Identical.* This is the whole story. |
| Bell partials | 165 / 247 / 330 Hz | E3, B3, E4 | The bronze's natural overtone series |
| The riff | root **E1/E2** | drop E | Enters at 3:56 and never before |

**82.4 Hz is E2 — the root of drop-E tuning.** The bell in a 19th-century Colorado mining town and the fundamental of modern down-tuned metal are the same note. That is not a metaphor you have to sell; it's a coincidence you get to *use*. The entire score is one note and its overtones, which is also why it will hold together across four minutes with no melodic material at all.

**Everything in the film is tuned to E.** Wind, cicadas, the truck, the klaxon, the boots in silt — pitch-shift every effect until it sits in the E harmonic series. The audience will never consciously notice. They will feel that the world is one object.

---

## 3. Cue Sheet

| Cue | Time | Shots | Content |
|---|---|---|---|
| **M1 · "Forty Feet"** | 0:00–0:22 | 1–3 | E1 sub-drone rising from nothing. One bell strike at 0:08, full 8-second decay. Then silence under the title. **Nothing else.** |
| **— silence —** | 0:22–1:18 | 4–16 | **No score at all for 56 seconds.** Only wind, cicadas, boots, paper, radio. This is the single most important decision in the mix: the film earns the right to have music by not having any. |
| **M2 · "The Grid"** | 1:18–2:00 | 17–26 | E1 drone creeps back in at −40dB and rises 6dB over 40 seconds. Sub only. Nobody consciously hears it start. |
| **M3 · "Tone"** | 2:00–2:56 | 27–40 | The 82.4 Hz tone enters as **diegetic sound**, faint, then clarifies as he approaches. Drone underneath. As he climbs, the reverb tail lengthens with the architecture. |
| **M4 · "82.4"** | 2:56–3:31 | 40–50 | Bell hum and turbine hum **braid into one another** and become indistinguishable. This is the reveal, done in the mix rather than in dialogue. At the Turn (3:31), the radio goes down and **everything cuts to near-silence** — just his breath and the hum in the stone. |
| **M5 · "Ahead of the Machine"** | 3:40–4:14 | 52–60 | Klaxon. Rope strain. Then at 3:56 **THE STRIKE**, and on its decay the drop-E riff enters for the first time in the film — 30 seconds, low, mid-tempo, no double-kick, no blast. **A funeral riff, not a battle riff.** Under it, an EDM sidechain pump keyed to the gate cycle, so the whole low end breathes at the rate of the machinery. Man and machine locked in one groove, his beat leading by an eighth. |
| **M6 · "Under"** | 4:14–4:22 | 60–61 | Everything low-passes as the water climbs — the riff drowning in real time, filter closing to ~200 Hz, then ~80 Hz, then one bell strike underwater, then nothing. |

**Total music: about 90 seconds in a 4:22 film.** Three of the four minutes are wind, breath and machinery. That restraint is what makes the last 40 seconds hit like a truck — and it is what separates this from every other entry, which will be wall-to-wall scored from frame one.

---

## 4. Instrumentation

**Metal side.** One 8-string in drop E, no gain stacking — a single amp, mic'd, room in the signal. Palm-muted root motion, no lead. The riff is four bars and it repeats. Drums enter only at 4:04 (Shot 58), kick and floor tom, no cymbals until the last hit.

**EDM side.** Not the melodic side. The *architectural* side: sidechain compression, filter automation, and sub-bass design. The gate-cycle pump is the EDM contribution and it is doing structural work — it is how the audience feels the machine breathing.

**Bell.** If you can strike a real bell, do. If not, physical-model it: bronze has an inharmonic partial series (that slightly "wrong" hum-note a minor third below the strike tone) and a synthesized sine will sound like a synthesized sine.

**The forbidden list.** No strings. No choir. No piano. No trailer hits. No riser into the water. **No riser into the water** — the water arriving with no build is the whole gag.

---

## 5. Sound Design Notes

- **Reverb is a location, not an effect.** Exterior: no tail, dry, dead — the desert eats sound. Interior tower: a real 2.4s stone tail that lengthens as he climbs. That contrast at the cut into Shot 37 is one of the best moments in the film and it costs nothing.
- **The radio is always thin.** Band-limited 300 Hz–3 kHz, always slightly too loud, always the wrong texture for the space. It is the institution's voice: procedural, competent, deaf.
- **Silt has a sound.** Dry cracked plates under boots = a brittle ceramic crunch, not mud. Get this right; it's in 20 shots.
- **The strike (3:56) must clip the room.** Not the master — *the room*. It should sound like the microphone was too close to something that was too loud.
- **Cut audio one frame early on the hard cut at 0:22.** One frame of true digital silence before the sun. Nobody will know why it works.

---

## 6. Reusable Across the Slate

The spine transfers, which is what makes DarkHearts a studio and not a series of one-offs:

- **THE DOG AT THE DOOR** — the inverse. Near-total silence, no score until 3:12, then one sustained E2 drone under the last minute and nothing else. Same root note, opposite deployment. *(Full cue sheet in `docs/12-dog-full-build.md`. The refinement worth knowing: the house hums at ~120 Hz until the power is cut at 1:43, and the E2 arrives at 3:12 to fill the hole the refrigerator left. **The house's own hum is replaced by the studio's root note.**)*
- **ROLL** — same drop-E root, but the loop structure means the score is *literally* a loop that degrades: each restart, the same four bars with one more element wrong. By loop six it's barely holding together. The score tells you something's broken before the character notices.
- **CEPHAS** — the Creation Stones each get a pitch. The Stone of Matter is E2. Of course it is.

**One studio, one root note.** People will start to hear it.
