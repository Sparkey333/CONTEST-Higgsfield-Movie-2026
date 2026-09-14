# Higgsfield project — element and asset cleanup

Pulled 2026-08-31 · 604 generations · 37 elements · 1 trained Soul

The Higgsfield API can **create** elements but cannot rename or delete them, and
the same is true of Souls (`list` / `train` / `status` only). So everything under
CREATED below is already done in your account; everything under RENAME and DELETE
has to be actioned in the web UI.

---

## 1. Stop-everything finding: the Soul named "Caedom" holds Oriane

Your only trained Soul, `Caedom` (soul_id `48700a9f-61a0-4b20-8c57-5a7f8a9b0e02`),
carries thumbnail `b84cff52…`. That image's generation prompt begins:

> "Cinematic still, 2.39:1 anamorphic, photoreal. **A woman** stands at the edge
> of a courtyard built from solidified beams of light…"

That is Oriane's lane-B prompt. The element named `Caedom` (`586e5d33…`, media
`f9a6af77…`) and the element `oriane_v5` (`69196068…`) resolve to the **same
batch and the same prompt** — all three are Oriane.

**Consequence:** generating with the `Caedom` Soul returns Oriane's face. Caedom
opens and closes the film, so this fails at both ends of the picture.

**Fix, in order:**
1. In the UI, rename the Soul `Caedom` → `oriane-soul` (it is a usable Oriane
   identity — do not delete it).
2. Generate `REF-caedom-ascended-A` (top of the Phase 0 run order).
3. Train a new Soul named `caedom` from that sheet plus his mortal-form sheet.
4. Re-check before Gate A: open both Souls side by side and confirm the faces.

---

## 2. Naming convention, applied

`<character>` for identity · `<character>-<state>` for a variant ·
`<character>-<place>` for an in-world plate. Lowercase, hyphens, no version
numbers — the element IS the current version, and a `_v5` suffix is how you end
up with five of something and no rule about which one is real.

**Production names only.** The festival publishes prompts and generation history,
so anything named for the novel goes public with the entry. That is the whole
reason the crosswalk lives outside the repo.

---

## 3. CREATED — 14 clean elements, already live in your account

Identity sheets (lane A) — the continuity pass:

| element | covers |
| --- | --- |
| `oriane` | at rest, travelling |
| `oriane-damaged` | the three fixed marks |
| `oriane-ascended` | seam-lit robe, barefoot |
| `caedom-ascended` | ⚠ built from lane B — A does not exist yet |
| `caedom-mortal` | the man before, no light at all |
| `alder` | nineteen, blonde, watchful |
| `wren` | eighteen, brunette, mid-speech |
| `threadwright` | face never revealed |
| `keeper` | the order, adults only |
| `turned` | three ranks, every centre black |
| `lev-rider` | the fused wielder |

In-world plates (lane B) — for shot work, not identity:

| element | covers |
| --- | --- |
| `oriane-on-the-sun` | Movement I, key from beneath |
| `alder-beach` | the frame the film ends on |
| `keeper-kneel` | what Movement III is built toward |

Each carries its continuity rule in the description, so the rule travels with the
handle instead of living only in the bible.

---

## 4. RENAME in the UI — off-doctrine names that would publish

| current | rename to | why |
| --- | --- | --- |
| `Caedom` (element) | `oriane-on-the-sun-v0` | it is Oriane, not Caedom |
| `Caedom` (Soul) | `oriane-soul` | trained on Oriane images |
| `loc_kephas-island_v1` | `nacre-beach-v0` | off-doctrine name |
| `loc_kephas-island-town_v2` | `island-town-v0` | off-doctrine name |
| `loc_sector-guard-isle_v1` | `keepers-isle-v0` | off-doctrine name |
| `sector-guardians_v2` | `keeper-v0` | off-doctrine name |
| `prop_sector-guardians_v1` | `keeper-kneel-v0` | off-doctrine name |
| `loc_starsun_v1/v2/v3` | `courtyard-v0/v1/v2` | off-doctrine name |

Confirm each against the crosswalk before renaming — I mapped these from the
generation prompts, not from the novel, and the crosswalk is not in this repo.

## 5. DELETE in the UI — superseded, once the renames are done

`char_oriane_v1` · `char_oriane_v3` · `char_oriane_v4` · `oriane_v5` ·
`char_caedom_v1` · `caedom_v2` · `caedom_v3` · `char_oriane_damaged` ·
`prop_the-turned-ones_v1/v2/v3` · `prop_beast-leviathan_v1` ·
`prop_beast-dominion-skeleton_v1` · `prop_enemy-pirate-ships_v1`

All are pre-rename or pre-age-up work now superseded by the 14 above. The bible's
own lesson applies: *three sheets for one character is three chances to generate
from the wrong one.*

**Not part of this film — leave or delete as you like:**
`Reborn-Green-Forest` · `Siege-Battleground` · `Cosmic-Mind-Walk`

---

## 6. Still open

- **`REF-caedom-ascended-A`** — the only missing character sheet.
- **259 off-sheet generations** — real images whose prompts match no current
  sheet, from before the rename and the age-up. They will not match the film.
- **Coverage: 10 of 42 A lanes.** Gate A cannot close until every character sheet
  exists, and Phase 1's 39 anchors must not start until it does.
