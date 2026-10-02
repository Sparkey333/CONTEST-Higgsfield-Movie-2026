# Working tips — what one production learned, written so the next one starts there

Each of these cost a day, a shot, or a scare on *Matter of Light*. They are in the order you meet them.

## Before the first frame
1. **One project, one cast, ids not names.** Every character, location, prop and effect is an element with a uuid, referenced as `@[name](uuid)`. A rename cannot break an id. A prompt that describes a face instead of attaching one is a prompt that will drift.
2. **Build the cast on plain backgrounds first.** Damage, costume and power state are generated *from* the identity, never re-described. Re-describing a face is how faces drift.
3. **Retire elements deliberately.** When you replace one (`prop_enemy_ships` → `twelve-ships`), record old id → new id in `project.json → retired` and sweep every prompt. Two swaps went unrecorded on this film and would have shipped four prompts pointing at dead elements.
4. **One lighting plate per act, one board per plate.** Every frame on a board inherits that board's key. A board that mixes plates is a board where the light drifts.

## Generating
5. **Image first.** Nothing goes to video until the film exists as stills. A shot is a move between two frames that are already right.
6. **Chain from the rendered last frame, never from the anchor still.** The still is the target; the render is the truth. Only 2 of 16 renders on this film used start/end frames — both were the longest shots, which is exactly right. Chain anything over 12s.
7. **Two takes, then rewrite.** A third take on the same prompt is almost always a different prompt, not a better one.
8. **Read what you are actually using.** The desk's own notes said v2, 12s, 720p. The account said v4.0, 16s. Pull the history before you spec a run; `ingest.py` exists for this.
9. **Hold the long shots whole.** Awe needs duration. The Predictor curves say the same thing the bible did: attention is still climbing at the last frame of every held wide.

## Scoring and choosing
10. **Score every take, then read the curves, not the number.** 17 of 18 renders peaked on their final second. That is the film working — and it is why the hook column is weak: the tool scores seconds 0–3 and this kind of film does not front-load.
11. **Use the hook score for one thing: the public post.** Cut the post peak-first from the three highest-rated final seconds. The film's opening can be quiet by design; the post's cannot.
12. **Cut on the tail, never the head.** If a take is longer than its slot, the time comes off the front.
13. **Selection is the grade.** Same shot, five takes: the two chroma takes scored 59 and 58; the flat ones 49. One look decision, ten points — and a colour pass across two lighting worlds in an hour produces drift, which a cinematographer punishes. Pick the graded take; ship the renders as rendered.
14. **Watch for the identity break the model can't see.** The Predictor scored S5 fine. S5 had the wrong Caedom sheet in all four takes. Scores rank takes; only the continuity audit catches the wrong face.

## Sound
15. **Route dialogue through a model that takes audio references** (`minimax_h3` was the one here that also chained frames at 21:9). Generate the voice first, attach it, and turn the model's own audio *off* on that shot.
16. **Silence is a choice you make once.** Decide which shots are silent in the shot list, and set `audio: false` there, so nobody turns ambience on by habit.
17. **The auditory channel was the weakest region in 13 of 18 clips.** Generated ambience is doing less than you think. Where speech arrives, attention jumps with it — put the film's first line under its first three seconds.

## Delivering
18. **Deliver at the render's native size ×2 at most.** 1344×576 to UHD is 8× the pixels and produces a soft image with 4K in the filename. *Up to* 4K is a ceiling, not a floor.
19. **Timeline resolution before export.** A 16:9 timeline with 21:9 clips bakes the bars in. Set the timeline to the film's aspect first, then export.
20. **End card plate and end card type are two things.** Generate the plate (no text, no letters, no numerals in the prompt — say so three ways). Lay the type in the NLE. Every model garbles letterforms, and a misspelled author credit is the worst possible last frame.
21. **Watermark, packshot, public post, public account.** Whatever the rules name as the minimal submission, do it in the platform's own flow and check every link in a private window. A private account is the most common way a strong entry becomes an ineligible one.

## The desk itself
22. **Every submission goes on the ledger before you wait for it.** `generate.py` writes the request id to `project.json` on acceptance. If the wait dies, the id survives.
23. **Keys in `keys.env`, never in a prompt, never in a commit.** The keys page exports to a gitignored filename on purpose.
24. **Regenerate, don't hand-edit.** `board.html` is a function of three JSON files. If it is wrong, the JSON is wrong.

## After the cut
25. **The board is the plan; the cut is the truth; the difference is the course.** Put the delivered film back through the desk. Upload the master into the project root, run the scene analysis, diff the scenes against the board as it stood at picture lock, and write each delta as a lesson, a reminder on the stage that could have caught it, and an example. Stage 8 exists for this.
26. **Favourites are the cut's own record.** Read them against the picks before any analyser returns: a favourite on a take that is not the pick is the editor telling you where the board was wrong. On this film seven of the favourited takes were the board's *alternates*, and every one was a look decision, not a score decision.
27. **A 16-second render is 16.1 seconds.** The Predictor refuses it. Score the 15s and 8s takes; for the 16s ones trim a quarter-second off the tail before you upload, or accept that the longest shots go unscored.
28. **Regenerate silent shots with audio off, and solo the tail of every audio-on take.** Two of four 'regenerate this clip' takes made on deadline night came back with the model's own voice — "Thank you" at 14–15s in one, "I'm sorry." at 12–13s in the other — in flank runs with no dialogue. Phantom speech is inaudible in a browser tile and very audible in a cinema.
29. **The analyser queues, and it is slow on a six-minute film** — 59 minutes to leave the queue on this one, and it labels a film's scenes with a marketing vocabulary ('Opening Hook', 'Usage Scenarios') you ignore. Its scene splits, palettes and audio transcriptions are the useful part. Start it the moment the master exists, and do the favourites diff by hand while it runs.
30. **Keep the master and the low proxy as two uploads in the project root.** The proxy is what you analyse and share; the master is what the jury saw. Name both in `project.json → final` so the next reader knows which is which.
31. **Plan coverage or plan montage, but decide.** The board planned 23 shots at 13 seconds; the cut ran 100 at 3.7, because one generation per shot gave the editor one angle and the film wanted three. If the film is to hold, generate the B lane and the multi-shot lane for every dialogue and set-piece shot before Gate D. If it is to be cut to music, write the board for it.
32. **Lock the song before the stills reel.** Three songs scored this film and the cuts land on their lyrics; the silent climax did not survive 'In the sky!' over the eye of the storm. The bible's own music-video rule applied and nobody noticed it applying.
33. **Audit the timeline, not the board.** Five costume states of the lead and two different beasts for one creature reached the jury. The continuity audit ran on the board, where every pick was clean; the seams only exist on the timeline. Run it at Gate E, before sound.
34. **Read every wide back through the analyser before delivery.** It described the reef swimmers as toddlers and the beach runners as young boys. The sheets say nineteen and eighteen; a wide does not carry the age, and a juror reads the wide.
