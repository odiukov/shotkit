---
name: cinematic-scenes
description: |
  Author grounded, photorealistic cinematic scenes for any text-to-image / text-to-video
  generator — structured shot direction, body movement with real weight and momentum,
  environmental force interaction, motivated camera movement, motion and pacing that keep
  a clip from reading static, and reference-anchored continuity across shots. Load when
  the user asks for cinematic film scenes, realistic motion direction, action sequences,
  emotional close-ups, intimacy scenes, driving scenes, environmental/weather interaction,
  multi-shot continuity, photorealistic cinematic motion — or when clips come out flat,
  static, boring, or "nothing happens", or when a render is REFUSED before it starts
  ("content flagged as potentially sensitive", "job failed", a prompt rejected by
  moderation).
---

# Cinematic scene craft

## When to use

Trigger when the user wants **photorealistic cinematic motion** — not stylized animation, cartoon, motion design, or UGC. Specifically:

- "cinematic scene", "shot like a movie", "film-style sequence"
- "realistic body movement", "grounded motion", "natural human behavior"
- "emotional close-up", "restrained performance", "subtle expression"
- "driving scene", "intimacy scene", "action sequence", "foot chase", "fight choreography"
- "wind / rain / water / gravity / dust interaction", "weather as character"
- "multi-shot scene", "match cut", "scene-to-scene continuity"

If the request is stylized animation, cartoon, or UGC, this skill does not apply.

## Core principle

**Cinematic realism is built from WEIGHT, not stillness.** The AI-cinema tell is not *too much* motion — it is motion with **no mass**: no footing, no contact, no momentum, no consequence in the world. So the guardrail is on **how** a thing moves, never on **how much**. Give a beat full amplitude and full physics; a person standing still is not realism, it is the **absence of a scene**.

Five grounding pillars:

1. **Body weight & physics** — actors have mass; movement has friction, momentum, contact force. This pillar *licenses* strong action — it does not suppress it. A sprint, a shove, a thrown chair all have weight; write the weight, not a smaller action.
2. **Environmental force** — wind, water, gravity, fabric, surface push back on the actor.
3. **Restrained FACE, free BODY** — the ban is on *telegraphed expression* (the wailing face, the wide grin), never on *action*. A character can hurl a phone at a wall with a blank face; that reads truer than a trembling lip. Do not let "restraint" leak from the face into the body — that is what produces actors who stand and breathe.
4. **Camera with a motive** — the lens has weight, but it moves when there is a reason to move: it follows, pushes, whips, tracks, cranes. What is banned is **unmotivated floating** (drone sweeps, 360° orbits, "cinematic camera movement"), not movement itself. An unmotivated move is worse than a locked frame — a motivated move beats both.
5. **Continuity anchors** — same look across shots comes from **reference images**, not prose.

Drop any pillar → "AI cinema": technically a video, structurally a tell. But the far more common failure in practice is the opposite one — a technically clean clip in which **nothing happens**.

## The dynamism gate — something must be MOVING, and something must HAPPEN

The single most common defect in a finished clip is not a drift or a swap — it is that the clip is **boring**: the camera sits, the actors stand and breathe, a short line is spoken, and 15 seconds pass with nothing occurring. Every rule below exists to make that impossible to author by accident.

### 1. The three motion channels — the per-shot gate

Every shot line must carry **at least ONE** of these channels; a standard drama beat carries **TWO**:

- **BODY** — the actor **travels through space or applies force**. Crossing the room, sitting down hard, setting a box on a table, pulling a coat on, shoving a door. *A tightening jaw is not BODY.* Micro-expression is performance, not motion — it does not fill this channel. **Force fills it as well as travel, and a seated pair of hands fills it:** turning a glass on the table, pressing a thumb through an envelope, setting a key down. Do not read this channel as "make them walk somewhere" — locomotion is the *least* interesting way to pay it.
- **CAMERA** — the frame itself changes: push, follow, truck, arc, rack focus, whip. A "locked-off frame with slight handheld breathing" does **not** fill this channel — that is a static frame with texture.
- **WORLD** — the world changes state: someone enters or leaves, a glass tips, a door slams, a phone lights up, the lights cut out, rain starts.

**A shot on zero channels is a photograph.** If a shot line reads "static — she stands at the window, light rakes her shoulders, she swallows once", it has no channel and must be rewritten or cut.

**Every CLIP needs at least one WORLD event** — one thing that is different in the world at the end of the clip than at the start, and that the camera can see. Without it the clip is an atmosphere plate, not a scene.

**No shot may merely CONTINUE the previous one.** A shot that shows the same action still going — she is still walking, he is still watching her, the meal continues — spends its seconds on nothing and reads as a stall, even though a body is technically moving. Each shot must move the beat somewhere new: the action **starts**, **changes**, **is interrupted**, or **lands**. If shot 3's only content is "shot 2, later", cut it or give it a turn.

**The turn is what's missing, NOT the speed.** The fix for "she is still walking" is *not* "she walks faster" or "she breaks into a run" — it is that the walk **arrives, stops, or changes**: she reaches the door and doesn't open it, she turns back mid-corridor, someone steps into her path. Escalating the amplitude of an unchanging action is the same stall, louder.

**HARD RULE — no dead scene.** Every scene in the episode carries a dynamic: something happens, changes, or gets decided on camera. The one narrow exception is a deliberately authored **idle/loop scene** — a held ambient loop, never a default (see "Looping / idle scenes"). Everything else must clear the gate.

The tells that you have written a dead scene, in the prompt text itself. Any of these phrasings is the failure showing up in words — rewrite, don't soften:

- "in silence", "silently", "without a word", "neither speaking", "the stillness holds"
- "they stand and look at each other", "he watches her", "she waits", "they sit together"
- "the tension builds", "the moment stretches", "a long pause"

None of these name a happening. Replace each with an action, an event, or a turn — the character *does* the thing the phrase was gesturing at. (A quiet scene is fine; a **dead** one is not. Quiet = an activity with the emotion under it. See Pillar 2.)

**What is banned is the phrase as the scene's WHOLE content — not the posture.** Characters may sit, wait, stay silent and look at each other; people do that. The failure is when that is *all* the scene is. "They sit at the table" is a fine opening state — it just isn't a beat until something happens at that table, and they can stay seated for all of it.

**The fix ladder — always take the LOWEST rung that works.** A dead scene is repaired from the bottom, and you should almost never reach the top:

1. **The activity CHANGES** — she keeps folding, but stops pressing the shirts flat and starts dropping them in. Same posture, same place; the beat turned. *This is the right answer most of the time.*
2. **A small WORLD event** — the lamp goes out, a phone lights up face-down, a glass is set on the paper, someone's name is called from off-screen.
3. **The CAMERA turns** — a push that lands on what changed, a rack to the thing that just entered.
4. **A cross or an entrance** — somebody moves through the space, arrives, or leaves.
5. **An Act** — a slap, a shove, a chair going over. **Hook and reversals only** (see the tier table).

**Running, chasing, pacing and storming out live on rung 4–5 and are almost never the answer.** If the scene has characters moving at speed and the beat is not the hook, a reversal or a literal chase, you skipped four rungs — go back to rung 1. A dynamic is a **change**, not a **velocity**.

### 1a. Start on the ARRIVAL, not the approach

**Walking to the place is preamble, not the beat.** Crossing the drive, climbing the stairs, entering the room, getting out of the car — by default the scene opens with the character **already there**: standing at the door, not walking toward it. The viewer infers the journey from the state (gravel underfoot, coat still on, keys in hand); you do not have to show it.

This is the single most common source of "somebody is walking/running somewhere" in a finished clip — not a decision, but a scene that **started too early** and then had to fill the opening seconds with travel. It compounds badly: two shots of approach eat half a 12s clip, the real beat gets three seconds, and the engine adds pace of its own to a prompt that is mostly locomotion.

- ✗ SHOT 1 she strides up the drive → SHOT 2 she climbs fast toward the house → SHOT 3 she stops and looks up
- ✓ SHOT 1 she stands at the foot of the drive, folder flat to her chest, the one lit window above her

**Travel earns a shot only when the path itself is the event** — a chase, an escape, a walk that costs her something (a red carpet, a corridor of people who know), an entrance staged as a power move. If you cannot say what the walking *is*, cut to the arrival and give the seconds back to the beat.

The shot-level version of this rule is "enter LATE, leave EARLY" (§3). This is the scene-level version: it deletes the whole approach, not just the first second of it.

### 2. Play the emotion against an ACTIVITY — the anti-boredom default

The fix for a static beat is almost never "add a slap". It is to give the character **something to do** while the emotional beat plays underneath. This is the default register for most scenes and it is what keeps them watchable without turning the episode into a soap opera.

> "She realizes she has been betrayed" is a stage direction, not a scene.
> **"She realizes she has been betrayed while she packs his suitcase"** is a scene — the realization stays quiet, and the frame has hands, weight, objects, and direction.

Three escalating tiers of "what happens" — pick the *lowest* one that serves the beat:

| Tier | What it is | Use it |
|---|---|---|
| **Activity (business)** | An ordinary physical task carrying the scene: packing, pouring, buttoning a cuff, stacking chairs, walking somewhere with purpose | **The default for most scenes** — quiet drama, dialogue, deliberation |
| **Event** | Something in the world irreversibly changes: a person enters, paper tears, a cup goes over, a light dies | **At least once per clip** |
| **Act** | A strong physical act: a slap, a shove, a phone smashed, a table cleared with one sweep | **Only** the hook and the reversals |

Boring = not even the first tier. Overcooked = the third tier everywhere. **Default = an activity plus one event.** Do not stage an Act just to hit a quota — an unearned slap is as bad as a static stare.

**Subtext lives in HOW the activity is done.** The same packing reads as grief (slow, folding each shirt) or as rage (jamming things in, a zip yanked hard) — the activity carries the emotion, so you rarely need the face to do it.

### 3. The dead-air rule — kill the standing-around

`durationSec × ~2 words` is the clip's **spoken-word budget**. When the actual `dialogue` fills far less than that budget, the remaining seconds must be filled with **action, not with holding**.

- **A 15s clip with one short line is 12 seconds of something.** Decide what. If the answer is "she stands there", the clip is **too long** — cut `durationSec` down, or add an activity/event. Do not pad with breath.
- **Enter each shot LATE, leave it EARLY.** No shot may open with more than ~1s of settling before its action begins, and none should linger after its action completes. The action starts at or near the shot's first frame. (Scene-level: open on the arrival, not the approach — §1a.)
- **The OPENING shot of a t2v clip runs long — never spend it on a slow, low-event beat.** On t2v the first shot gets a disproportionate share of the generated frames, and the model settles into the opening bit: a 3s "he drifts toward her" is rendered as if it had twice the time, and the whole clip reads as slow before anything has happened. So shot 1 either **opens on an action already in motion** (the hand is already on the door, the folder is already sliding) or **on a fast reveal** (a hard reframe, an entrance, the thing that changed). A slow drift, a settling pose, or a wordless approach belongs anywhere but first — and usually nowhere.
- **Rough pacing target: a nameable happening every ~3 seconds.** A 15s clip should have ~5 of them (an activity beat, an event, a line landing, a look that turns, an arrival). Fewer than that and it will read as dead.

### 4. Energy registers — choose one per beat

Replaces "just default to 2–4 cuts". Pick the register from the beat's content, and write the whole clip in it:

| Register | Cuts / 15s | Camera | Body | Use for |
|---|---|---|---|---|
| **HELD** | 0 — one continuous take | locked-off, or breath/micro-drift | micro-motion only | Intimacy, a decision, the exhale after violence, a signature oner |
| **CHARGED** | 3–4 | slow push, handheld follow, rack focus, reframe on a move | activity, crosses, status moves, props handled | **The drama default** — confrontation, dialogue, deliberation |
| **KINETIC** | 5–6 | whip, hard tracking, snap push, speed ramp on impact | full-amplitude action | The hook, a reversal, a chase, a humiliation, violence |

**The HELD take is a PURCHASE, not a reflex.** You are spending the clip's entire budget on stillness, so the stillness must **be** the event (a decision landing, a body that cannot move yet). If you cannot name why the stillness is the point, you did not choose HELD — you defaulted into it, and the clip will read as flat. Everywhere else, cut.

**HELD is one uncut take, NOT a scene where nothing happens.** It still owes the dynamism gate a happening: the letter gets opened and folded, the radio gets killed, the camera pushes. A HELD clip whose content is "they hold the moment" is a dead scene under the hard rule above — only an **idle loop scene** may be that. Write the turn into the take.

### 5. Cut ON the action, never between actions

A cut placed **mid-movement** carries kinetic energy across the edit; a cut between two settled poses reads as two photographs shown in sequence. Author the shot lines so the action **straddles the timecode boundary**:

- ✗ `[0:03–0:06] … she reaches for the folder. Hard cut.` → `[0:06–0:09] … she is holding the folder.`
- ✓ `[0:03–0:06] … her hand leaves the table and starts toward the folder — cut ON the reach.` → `[0:06–0:09] … the reach completes: her fingers close on the folder and drag it across the desk.`

Name it explicitly in the line (`cut ON the reach`, `cut ON the turn`, `cut ON the impact`). The same idea drives the **match cut**: end one shot on a movement and open the next on a matching movement (a door swinging shut → a briefcase snapping shut).

**Caveat — a cause and its physical effect must NOT be split across a cut.** Cutting *on* a movement is right; cutting *between* a force and its consequence (a hand knocks a glass → next shot the glass is already down) renders as two unrelated states. Keep contact→result inside one continuous shot, and cut after it lands. (See the failure-modes row.)

### 6. Foreground parallax — the cheapest dynamism multiplier

Put something **between the camera and the subject** and let it move: a passing body crossing frame, a swinging door, traffic, steam, a hand entering. Parallax reads as depth *and* as motion even when the subject is still — it is the highest-yield-per-word tool in a vertical frame, where there is little horizontal room to stage travel. Use it especially on a shot that would otherwise be a static single.

## How a shotkit project renders — the model you must respect

A project holds a **bible** (`bible.json`: style, characters, locations, props) and **scenes** (`scenes/<id>.json`). Each scene becomes a clip via `shotkit motion <scene-id> --mode …`, which has three modes:

- **`t2v` — THE DEFAULT for every scene, and the stronger path.** With **no** keyframe, `shotkit motion --mode t2v` composes the clip straight from the `@mentioned` character/location/prop reference images, with no seed frame. This frees the camera (reveals, tilts, push-ins) and tends to produce better motion than a seeded path. Needs at least one `@mention`. This is the path for **all** scenes — single-character AND multi-character — unless the user explicitly opts into a seeded mode.
- **`i2v` — OPT-IN ONLY, never the default.** First run `shotkit frame <scene-id>` from `scenePrompt` to get the still-keyframe prompt, generate it in an image model, review/approve the result, then run `shotkit motion <scene-id> --mode i2v` and hand that approved frame directly to your video model's own image-to-video / start-frame input. Use **only when the user explicitly asks** to lock an exact composition before motion (a hard identity/blocking lock). If the user has not asked for a seeded mode, do not go down this path and do not author a `scenePrompt`.
- **`ref-anchored --keyframe PATH` — the hybrid, for a video model with no dedicated start-frame slot.** Some engines take only a flat list of reference images, with no separate seed-frame input. For those, generate the keyframe the same way as `i2v`, then run `shotkit motion <scene-id> --mode ref-anchored --keyframe PATH` — shotkit puts that frame first in `out/scenes/<scene-id>/motion.refs.txt` and writes an explicit instruction into the prompt that reference #1 IS frame 0, to reproduce and animate onward from. Reach for this only when the target engine's API genuinely has no seed-frame input — check `prompt-assembly/references/engines.md` for which shape a given engine expects.

**DEFAULT AUTHORING RULE — write ONLY `motionPrompt`.** On the default no-keyframe path the `scenePrompt` prose is **never sent to the model** (it only resolves `@mention` refs — and `@mentions` in `motionPrompt` already do that). So **do not author a `scenePrompt` at all by default** — put the *entire* shot (style/lens + every `@mention` + framing + settled body/weight + environmental force + camera + ambient) into a self-contained `motionPrompt`. Author a `scenePrompt` **only** when the user has opted into a seeded mode for that scene. The field-mapping table and `scenePrompt` recipe below describe the seeded path only.

In every mode the `motionPrompt` drives the motion; the scene optionally bakes on-camera `dialogue` (lip-synced) plus a post `voiceover` track — see the field table below for what each of these actually asks of your generator.

**CRITICAL for the default path — only `motionPrompt` text reaches the model (refs are sent separately).** On the no-keyframe path there is no seed frame; the model receives exactly two things — the **prompt text** and the **reference images** (`out/scenes/<scene-id>/motion.refs.txt`). Concretely:

- The prompt text is **only `motionPrompt`** — the `scenePrompt` prose is **never sent**; it is used merely to resolve which `@mention` refs to attach.
- The `@mentioned` reference images ARE attached and sent (`@mentions` are scanned across `scenePrompt` + `motionPrompt` combined, so a mention in either attaches the ref). What's lost on the default path is the *textual* direction in `scenePrompt`, not the refs.
- Therefore the `motionPrompt` must be **self-contained**: lead with style/lens, `@mention` every character + location + prop, and write the framing, the settled body + weight, the environmental force, the camera, and the ambient — everything, not just "how it moves". A bare `motionPrompt` like "she pulls the tie…" loses all style, identity, and place at render.
- **Each clip is a SEALED single document — no memory of any other clip.** The engine sees only this one prompt; it has no idea what scene number this is or what happened in the previous shot. So carry **nothing** cross-clip into the text: no scene numbers or `SCENE N` labels, no "as above / continues from…" phrasing, no summary of the prior beat. (A descriptive cue for THIS clip like `INT. @church, afternoon` is fine — what's banned is a *reference to other clips*, not an in-prompt slug/time line.) Self-contained cuts **both** ways — write in every entity present, and write in **nothing that is not physically in this clip**: an `@mention` for a character or prop that isn't in the frame **drags that entity into the shot** (most reference-driven engines try to honor the tag). Anything that must persist across clips (a stain, a screen-side, wardrobe state) is carried by refs + inline STATE prose, never by referring back.
- (On a seeded mode the `scenePrompt` IS rendered as the seed frame, so there you split craft across both fields as the table shows.)

**When the user's plan has no keyframe, write the full cinematic content into `motionPrompt`.**

**HARD RULE — `@mention` in EVERY prompt, ALWAYS, in every mode.** A reference image attaches to a render ONLY through its `@mention` (locations have one extra path: the scene's `locationId`, but a bare `locationId` alone does not put the location's name into the `motionPrompt` TEXT — see the trap below). This is true for **every mode, every scene image and every clip** — it is not a no-keyframe-only concern. Forget to `@mention` a character/location/prop and its ref is simply **not attached**, in any mode, and the entity is re-invented. So: write every `scenePrompt` and every `motionPrompt` with `@mention`s for **every** character + location + prop present, from the start, before any image exists. Never author a prompt with a bare "she"/"the room"/"the bag" — name it `@lana` / `@classroom` / `@uniform`.

**The location-ref TRAP on the default path — a ref attached is NOT a ref anchored.** `shotkit lint` scans `@mentions` across `scenePrompt` + `motionPrompt` **combined**, so a location `@mentioned` only in the (seeded-only) `scenePrompt` **still lints clean**. But on the default path **only `motionPrompt` text reaches the model**: if `@great_hall` isn't in the `motionPrompt` itself, the model gets the image with no location word to bind it to and the place drifts anyway. **A clean lint does NOT mean the `motionPrompt` is anchored.** Put every location/character/prop `@mention` in the `motionPrompt` TEXT, not just in `scenePrompt`.

**REWRITE/EDIT RULE — re-verify every `@mention` survived the rewrite.** When you rewrite or trim an existing `motionPrompt`, the most common regression is silently dropping a location/character/prop `@mention` that was in the old text. After any rewrite, diff against the old prompt and confirm **every** entity present in the scene is still `@mentioned` in the new `motionPrompt` text (location included, in every shot of a multi-shot clip). Don't trust a clean `shotkit lint` alone — it can stay clean off the `scenePrompt`.

**Consistency is a reference image, not prose.** A character, location, or prop keeps its look across scenes ONLY if it has a reference image AND is `@mentioned` by id in the prompt (e.g. `@skye inside @church wheeling @suitcase`). Generate a character's turnaround with `shotkit sheet <id>`; **locations and props do NOT auto-generate one — you anchor them**: run `shotkit location <id> --view <label>` / `shotkit prop <id>`, generate the resulting prompt in your image model, save the approved frame under `refs/`, and point the entry's `uri` at it in `bible.json`. Without a reference the place/object is re-invented every frame.

### Reference images must be SINGLE clean frames — never a board/collage

A reference image is fed to the video model as one picture. If you anchor a **multi-panel board, collage, contact-sheet or turnaround grid** as a location/prop reference, the model reproduces the **grid** — you get a split-screen "several frames in one shot". Always anchor a **single, clean, full-frame** photo. (Characters are the one exception: their turnaround sheet, from `shotkit sheet`, is handled by the pipeline; you don't hand-anchor a grid for a location.)

**Character sheets DO leak into a still keyframe.** The character turnaround sheet is fine for the **video** path (the default and seeded modes are built to read it), but when it conditions a **still `shotkit frame` / `shotkit poster` keyframe**, the image model copies the sheet's layout — a portrait panel on top, a full-figure panel below = a **diptych / split-screen**. `shotkit frame` / `shotkit poster` **auto-inject a guard clause** (gated on characters being present, keyframe-only) telling the model the reference is identity/wardrobe only and to render one figure in one unbroken frame. If a keyframe still splits, add the same lock to the front of the `scenePrompt`: *"one single continuous photograph edge to edge, NOT a character sheet / split-screen / inset; use the reference only for face, hair and wardrobe."* The durable fix is to feed the generator a single-pose crop instead of the whole sheet.

### Location views & the reference budget

A location can hold **several named views of the SAME place** — one establishing wide, a window angle, the dais — each a separate single-frame reference with a `label` (an entry in the location's `views` list in `bible.json`). Index 0 is the **primary** view. Address them per shot:

- `@hall` — the **primary** view (bare mention; the safe default).
- `@hall#window` — a **specific** stored view, for a shot that needs that angle.
- `@hall*` — **all** stored views (use sparingly — it eats budget).

**The reference budget is real.** A typical reference-driven video engine honors only a bounded number of reference images per clip — a common cap is **9**, counting characters + location views + props **combined**; the exact number varies by engine (see `prompt-assembly/references/engines.md`). Past it the model blends refs and identities/composition drift. 9 is roomy for most scenes, but a dense one (a full cast + several location angles + props) still blows it, so **curate per shot, don't dump**:

- Pick the **one** location view that fits the shot; reach for `@hall#label` only when a specific angle matters; avoid `@hall*` unless the budget is free.
- `shotkit lint <scene-id>` checks that every `@mention` resolves to an entity with an image on disk, and `out/scenes/<scene-id>/motion.refs.txt` (or `frame.refs.txt` / `poster.refs.txt`, whichever you rendered) is the actual resolved list — **author to that list**: if a scene is over budget, drop a `@mention` or a `#view`.
- **Don't assume the engine trims gracefully for you.** shotkit writes exactly what your prompt resolves to, in mention order — it does not reorder or drop anything by priority. A scene with a 4-character cast + 3 location views + 3 props is 10 refs; if the target engine's cap is 9, the engine's own trim/blend behavior decides what's lost, and that is not yours to rely on — cut a `@mention` or a `#view` yourself instead.

**A clean lint does NOT tell you WHICH view attached — and ONE location gets ONE view per clip.** `shotkit lint` confirms a mention resolves and its file exists, not which labelled view a mixed set of mentions will select. The mechanism: mentions resolve to **one view selector per entity**, and **an explicit `#label` beats a bare mention wherever it appears in the text** — mention `@foyer` in shot 1 and `@foyer#stairs` in shot 3, and the whole clip gets the **stairs** ref only. The primary view (with the side table and the lamp the beat is built on) is never attached, and a clean lint says nothing about it.

- **Never mix a bare `@loc` and a `@loc#view` for the same location in one clip.** It does not attach two views; the labelled one silently wins the whole clip.
- **Several views of one place in a clip is fine — but `@loc*` is the ONLY way to get them.** Listing labels one by one does not accumulate: two different labels resolve to one view too (the first wins). A bare mention and a `#label` resolve to one view each by construction, so `*` is the single selector that attaches more than one image for a location.
- **When two SPECIFIC views must both attach, promote one to its own location entity.** Mentions resolve per entity id, so two different ids never collapse: render the angle as a view of the original (`shotkit location <id> --view stairs`, so it stays canon to the primary), then add a second location entry `foyer_stairs` in `bible.json` and point its first `views` entry at that same frame. Now `@foyer` and `@foyer_stairs` are two mentions of two entities — both survive, and you get exactly the two angles you named rather than every stored view. Cost: one more roster entry to keep consistent. (Mind the name matching — mentions match longest-first, so `@foyer_stairs` is safe beside `@foyer`.)
- **`@loc*` puts every stored view on the budget at once.** On a dense scene that can blow the cap faster than you expect — reserve `*` for a clip that is otherwise light on refs; on a full-cast scene pick the one view the shot needs, and if two angles are genuinely both load-bearing, split the beat into two scenes.
- **Read the resolved ref list, not just the mention count.** `out/scenes/<scene-id>/motion.refs.txt` (or `frame.refs.txt` / `poster.refs.txt`) lists which images will actually attach, in order — confirm the view named is the one the shots are built on, before spending a render.

**Building a location's view set:** add named views under the location's `views` array in `bible.json` (`{label, uri}`), `label:"primary"` for the canonical establishing frame. Generate each with `shotkit location <id> --view <label>`: the **`primary` view first** (it defines the canon); every other view's prompt asks the model to match it — "the SAME place from a different camera angle" — so the whole set stays one place, never a redesign. Each view is a **single clean frame**. Regenerate any single view by re-running `shotkit location` for that label — the others are untouched and stay consistent.

So craft and consistency are two separate jobs: this skill writes the **craft** (the five pillars) into the prompt fields; the `@mention` + reference-image rules carry the **identity**.

## Mapping the five pillars onto shotkit's scene fields

shotkit does not take one prose block: a scene JSON's fields map onto separate slots that `shotkit frame` / `shotkit poster` / `shotkit motion` read differently. Map craft onto them like this. **On the default no-keyframe path you fill only `motionPrompt` (and `dialogue`/`voiceover`/`generateAudio`) — `scenePrompt` is seeded-mode-only.**

| Field | What goes in it | Pillars it carries |
|---|---|---|
| `scenePrompt` | **Seeded-mode-ONLY (opt-in) — leave empty by default.** When the user has chosen `i2v` or `ref-anchored --keyframe`: the **keyframe = SHOT 1** still: style/lens, framing, the actor's settled body, environmental force visible in frame, who/where/what (`@mention` every character + location + prop). | 1, 2, 3 (held pose), 4 (start framing), 5 |
| `motionPrompt` | How the clip **moves** from that still: the actor's motion, the camera's behavior over the duration, environmental force in motion. Shot 1 must match the keyframe when one exists. **On the default path this is the only PROMPT TEXT sent (refs are attached separately) — make it self-contained (style/lens + `@mentions` + framing + body + environment + camera + ambient), not just motion.** | 1, 2, 4 (and all of 1–5 without a keyframe) |
| `dialogue` | **Everything meant to be baked into the clip's own audio**, speaker-labeled, IF the target video model bakes audio from the prompt text (see `prompt-assembly/references/engines.md` for which ones do). Plain lines (`Skye: ...`) = on-camera lip-synced speech. A `VO:`-prefixed segment (`VO: ...` or `Skye: VO: ...`) = **narration meant to render as off-screen speech in the same clip** — but its baked voice is NOT guaranteed consistent across clips. On a multishot clip, **pin WHEN a segment lands with a `[shot N]` anchor** at its head — `Skye: [shot 2] ...`, `VO: [shot 3] ...` — pointing at a `SHOT N` the motionPrompt actually declares (`shotkit lint` warns otherwise); unanchored segments are placed at the model's discretion, so also write the speaking cue into the target shot's own text. **A spoken line and a `VO:` segment must never share a shot** — same shot = the narration renders as that character's lip-synced speech; see "One voice per shot". Size ALL baked words (spoken + VO:) ~2 words/sec of duration. | 3 |
| `voiceover` | The narration track for a **separate TTS step**, synthesized after the clip, never lip-synced. shotkit has no voice catalog and does not track which TTS voice you use — if a narrator must sound the same across every scene of a story, holding that voice constant is on you (or whatever TTS tool renders it), not on shotkit. **Narration lives in exactly ONE place per scene**: `VO:` in `dialogue` for a one-off baked aside, this field when the narrator must sound the same across scenes — never both (double narration). **Fit it to the clip:** a TTS pass typically only compresses speech up to ~1.15× before it gets choppy or cut off, so budget ≈ `durationSec × 2.3` words (~2.3 words/sec at natural pace) — a rich `motionPrompt` doesn't buy the VO more room than a short scene allows. | — |
| `generateAudio` | `true` tells shotkit to append an audio-discipline clause (ambient/dialogue only, no music) to the assembled `motionPrompt`, for a video model that bakes native audio — write the ambient cue into `motionPrompt` itself. Music is a separate post layer, not here. | — |

**Pin the baked narrator's voice as best you can.** A `VO:` segment asks the video model itself to voice the narration, and left unpinned that voice can drift — even flip gender — clip to clip. Two levers, stack both: name the speaker inline (`Skye: VO: ...`) AND set that character's `gender` (and optionally `voiceNote`) in `bible.json` — a named `VO:` speaker with a `gender` set gets it spelled out in the baked clause itself ("an off-screen female narrator voice-over says…", or "female (warm, low register) …" with a `voiceNote`), a stronger nudge than `canonicalDescription` consistency alone. It is still a nudge, not a guarantee — shotkit's own reasoning for it is "so the engine stops flipping the narrator's voice," not a lock on an exact voice. When a narrator must sound identical in every scene, use the `voiceover` field (a separate TTS pass) instead of `VO:`, and hold that TTS voice choice constant yourself across every scene of the story.

#### One voice per shot — never a spoken line and a `VO:` in the same shot

An on-camera `dialogue` line and a `VO:` segment are **both** appended to the `motionPrompt` as speech clauses by shotkit's motion-prompt builder — `In SHOT 2, Skye speaks this line aloud, naturally and in sync: "…"` next to `In SHOT 2, an off-screen narrator voice-over says, no narrator appears on camera: "…"`. Land them on the **same** shot and the engine reads one speech event over a face that is already in frame: **the narration comes out as that character's direct speech, lip-synced.** The baked narrator stops being off-screen. Nothing catches this automatically — `shotkit lint`'s `lint_shot_anchors` only checks that an anchor points at a declared shot, not who else is speaking there. It is an authoring rule.

**The rule: any one shot carries EITHER an on-camera line OR narration — never both.**

- **A scene that carries both kinds must anchor EVERY segment** — `Skye: [shot 2] …` *and* `VO: [shot 4] …`. Leaving both unanchored is the same collision: the engine places them itself, and it places them together.
- **No two segments of different kinds may name the same `SHOT N`.**
- **Fix by moving the NARRATION, not the spoken line.** Give the `VO:` its **own shot inside the same scene** — a shot with nobody speaking on camera: an insert, a reaction, a listening beat, a wide on the room. Add that shot to the `motionPrompt`'s timecoded shot list (so the anchor validates and the timecodes still cover `durationSec`), then re-anchor the `VO:` to its number.
- **A single held take cannot separate them** — one take is one `SHOT 1`. Either split it into two shots and give the narration the second, or move the narration out of the scene.
- **The TTS `voiceover` field is NOT affected** — it never reaches the motion prompt, so it can't be lip-synced onto anyone. It still plays *over* the clip, so don't lay it across a scene whose spoken line is carrying the beat.

### scenePrompt recipe (the keyframe / shot 1) — seeded modes only

**Skip this entirely on the default no-keyframe path.** Use it only when the user has opted into `i2v` or `ref-anchored --keyframe` for the scene. One tight paragraph, in this internal order — the prompt builder weights the front most:

1. **Style & lens** (one clause). Cinematographer lexicon, not adjective stacks.
   - ✓ "35mm anamorphic, naturalistic skin tones, soft window light, muted teal-and-amber."
   - ✗ "Cinematic, beautiful, dramatic, epic." → flattens output.
2. **Framing + subject** with `@mentions`. "Medium close-up of `@skye` at `@kitchen` window holding `@letter`."
3. **The settled body** — a weight cue + a held pose. This is the grounding anchor.
   - weight cue: "weight on her right hip", "shoulders dropped", "hand braced on the counter".
4. **Environmental force visible in frame** — what pushes back (see Pillar 2 categories below). Without it the still reads as a soundstage.

### motionPrompt recipe (how the clip moves)

1. **Actor motion** — what the body **does**, with momentum and contact. Lead with the *activity or action* (the BODY channel); micro-actions are seasoning on top of it, never the whole performance.
   - activity (the default): "she works down the row of chairs, stacking them two at a time"; "he shoulders the door open and drops the crate on the counter".
   - action (a reversal): "she sweeps the files off the desk in one pass — paper still settling as he steps back".
   - micro-action, **on top of an activity, never instead of one**: "her thumb traces the paper's edge *as she keeps folding*".
   - a held beat is a **punctuation mark**, not a performance: use it to land something that just happened ("she stops mid-fold, the shirt still in her hands"), never as the shot's only content.
2. **Camera behavior** — grounded and **motivated** (see Pillar 4). Default to a camera that does something: follow the activity, push on the turn, rack to the thing that changed. A locked frame is a deliberate choice you can justify, not the resting state.
3. **Environmental force in motion** — wind lifting hair, curtain breathing, rain in bursts.
4. **Ambient sound cue + its ARC** — name the soundscape, and where it matters, give it a *shape over the clip*, not a flat bed. With `generateAudio:true`, shotkit appends an audio-discipline clause telling a native-audio video model to bake diegetic sound **from the prompt text**, so the ambient you describe here is what such a model renders (see `prompt-assembly/references/engines.md` for which engines support native audio). Specify ambient first, then any non-spoken sound; put on-camera speech in `dialogue` (plain lines), a one-off baked narrator as `VO:` in `dialogue`, and the consistent story-voice narration in `voiceover`.
   - ✓ "Ambient: tire roar on asphalt, faint heater fan, occasional passing vehicle; no score, diegetic ambient only."
   - For silence: "Ambient: room tone only, no score."
   - **Never type the word "music" in a prompt field — not even to negate it.** `shotkit lint`'s `lint_music_words` check matches the bare word and warns on `no music` exactly as it warns on `music`, because many native-audio video models read it as a cue toward a musical/lip-sync register regardless of the "no". Write `no score` / `diegetic ambient only` instead. The same lint fires on **`song`, `sing`, `melody`, `tune`, `chant`, `hum` and `lip-sync`** — so an innocent ambient noun like "refrigerator hum" or "a radio mid-song" trips it too; use `whirr`, `roar`, `rumble`, `a radio talk-voice`.
   - **Sound as a dramatic beat.** A diegetic sound *transition* can carry the turn better than the picture — write the arc with an arrow: "kitchen roar of a lawnmower from the first frame → it drops hard into a muffled hush as the door shuts"; "the room tone falls to dead silence the instant she reads the line"; "a rising ring builds under the argument until the cut". A native-audio model renders this within the one clip — use it for the emotional pivot.
   - **Music and cross-scene sound-bridges are POST, not the prompt.** `generateAudio` only makes *in-clip diegetic* sound, and each scene is a separate generation with **no audio continuity to the next** — so a music track and any **sound-bridge** (the next scene's sound arriving on the tail of this one) are laid in by hand at edit time, not authored here. Any post-production music-direction note you keep is for that step, not a model instruction. You *can* prep a bridge in the prompt by writing the **tail of one clip and the head of the next to share an ambient** (both carry the same low rumble / rain / room tone) so they overlap cleanly when cut together.

5. **Inline VFX (only when a stylized effect is intended).** Some video models read a bracketed effect tag dropped into the action text at the moment it happens — `[VFX: branching electric circuits pulsing with white-blue current]`, `[VFX: embers lifting off the blade]`. Keep it inline beside the action, one effect per tag. This is for deliberate stylized/genre beats; for grounded realism leave it out (a realism shot wants none).

Shot 1 of `motionPrompt` must match the keyframe (on a seeded mode). Write the shots inline inside ONE `motionPrompt` — there is no separate `shots` field on the scene; the timecoded shot list in the `motionPrompt` text IS the shot structure.

#### Shot-list format (preferred) — timecoded lines

Write the multi-shot `motionPrompt` as one **timecoded shot list**, one line per shot, lead with a style/lens line, then:

```
<structure line — shot count + total duration + aspect, e.g. "6 shots, 15s total, 9:16">
<style/lens line — set it once at the top>
SHOTS:
SHOT 1 [0:00–0:02] WIDE SHOT — Static low-angle. @a right, @b left, 2m apart. White suit lit hard, black suit in shadow. Smash cut.
SHOT 2 [0:02–0:03] EXTREME CLOSE-UP — Both visors in frame. Lamp glint on both. Smash cut.
SHOT 3 [0:03–0:05] MEDIUM SHOT — Handheld. @a throws a punch, @b dodges; suit fabric pulls at contact. Smash cut.
...
SHOT 6 [0:13–0:15] WIDE SHOT — Static. @b at the shelving wall, @a at distance; debris settling in the lamp beam. Fade to black.
```

Each line, in order: **`SHOT N` label → `[start–end]` timecode → SHOT TYPE/angle (caps) → camera behavior → `@mention`ed action (every character/location/prop tagged; the who-is-who is auto-injected from `canonicalDescription`, so no inline identity trait needed) → one light/environment detail → the transition (`Smash cut.` / `Hard cut.` / `Fade to black.` on the last).** Rules:

- **Declare the structure UPFRONT — first line of the `motionPrompt`.** Many video models read a header that states the **shot count + total duration + aspect** ("6 shots, 15s total, 9:16") as the plan for the whole clip. Lead with it, then the style/lens line, then the timecoded shots. For a single held take, say so instead ("ONE continuous shot, no cuts, 8s, 9:16").
- **Lead every shot line with a literal `SHOT N` ordinal, then the timecode.** `SHOT 3 [0:06–0:09] 29° CLOSE …`. This is not cosmetic: a `[shot N]` anchor in `dialogue` is validated against a literal `SHOT <number>` token in the `motionPrompt` (`lint_shot_anchors`, part of `shotkit lint`), and a timecode alone does not satisfy it — anchor your lines any other way and `shotkit lint` warns that the motionPrompt "has no `SHOT N — …` structure". Number them from 1, sequentially, matching the anchors you write in `dialogue`.
- **Label the UNIT as `SHOT` (by its type), name the TRANSITION as the cut — don't label units `CUT N`.** In film grammar a *shot* is the continuous unit, a *cut* is the transition between two shots. So name each line by its shot TYPE (`WIDE SHOT`, `CLOSE-UP`) and put the edit as an explicit transition word at the line's end (`Smash cut.` / `Hard cut.`). A bare ordinal `CUT 1 / CUT 2` carries less — it names the join, not the framing, and conflates unit with transition. The timecode (sequential, non-overlapping) plus the transition word already encode "these run in time, separated by an edit" more strongly than a `CUT N` label would.
- **Name the TRANSITION from the cut vocabulary — don't just write "cut".** The transition word at each line's end is one of: `Hard cut.` (the default, neutral), `Smash cut.` (jarring, on a loud/sudden beat), `Match cut.` (end on a shape or motion the next shot echoes — a door swinging shut → a case snapping shut), `Whip cut.` (a whip-pan blur — needs ≥0.8s, see transition timing), `Fade to black.` (endings only). Pick the one that fits the beat; the transition word carries intent the timecode alone can't, and fades/crossfades appear only when actually wanted. **An INSERT or a REVERSE is a shot TYPE, not a transition** — name it at the START of the next line (`INSERT — a hand on the phone`, `REVERSE single on @b`) and reach it with a plain `Hard cut.`, keeping unit and transition separate exactly as the shot-label rule above requires.
- **Timecodes must cover the whole `durationSec` with no gaps/overlaps**, and the last shot ends exactly at `durationSec`. Pace ~2–4s per shot (a beat can be shorter).
- **Style/lens once at the top**, not repeated every line. Ambient cue stays as its own clause at the end of the `motionPrompt` (it feeds `generateAudio`).
- Keep the camera grounded (Pillar 4) — `Static`, `Handheld`, `Slow push`, `Lateral tracking`, `Dutch tilt 20°` are fine; no drone/sweep.
- This is the same "hard cuts in TIME, one continuous clip" idea — the timecodes just make the cut points and pacing explicit. The older `SHOT 1 — … HARD CUT. SHOT 2 — …` prose still works; the timecoded form is preferred for any multi-shot clip.

#### The canonical t2v motionPrompt skeleton

Every default-path (t2v) `motionPrompt` assembles the same way — fill this skeleton, then run the enhancement pass and the pre-submit checklist:

```
<header — "N shots, Xs total, 9:16" | or "ONE continuous shot, NO cuts, no zoom, Xs, 9:16" for a held take/loop/POV>
<style/lens line — concrete film vocab + "WB locked NNNNK">
SHOTS:
SHOT 1 [t0–t1] FOV° SHOT TYPE, HEIGHT/ANGLE — camera behavior (a MOVE unless stillness is the point) — @mentioned action: what the body DOES, with contact and consequence (every character/location/prop tagged; STATE prose inline, identity traits NEVER) — one light/environment detail. Transition, cut ON the action.
SHOT 2 [t1–t2] …
LOCKS: 2–4 positive invariants (frame-sides, prop state, skin tone even) — "X stays …", never "don't".
Ambient: <soundscape, with an arc — "A → B" — where the beat turns>; no score, diegetic ambient only.
```

For a held single take, the SHOTS block collapses into one flowing paragraph after the header + style line — same ingredients, no timecodes.

### The enhancement pass — submit an already-enhanced prompt (no paid enhancer)

Some hosted pipelines beat the same underlying engine on its own home turf because they run your prose through an LLM **prompt-enhancer** that expands it into a dense, concrete caption *before* the model sees it. shotkit has **no such pass** — what you author is **verbatim** what your video model gets (it sends `motionPrompt`, assembled with the identity/loop/audio clauses, unchanged). **So YOU are the enhancer.** You are an LLM authoring this prompt directly — doing this rewrite yourself costs nothing per render and replaces a paid API enhancer entirely. **Never submit a first-draft `motionPrompt`.** After drafting, do **one rewrite** that raises every beat to enhanced grade.

A first draft and an enhanced caption differ on five axes — rewrite each (draft → enhanced):

1. **Concrete set detail.** Name **3–5 specific, textured objects** that fix the place. "a church interior" → "worn wooden pews, a dust-flecked centre aisle, high narrow windows, plain white walls, a simple wooden cross at the altar." A generic place name renders generic.
2. **Light, specified.** Give **direction + quality + what it touches**. "afternoon light" → "strong afternoon backlight raking through the high windows, dust motes suspended in the beam, faces rim-lit." **Tie colour to material + light + role, never a flat list** — "the woman wears red, the man blue" reads flat; "crimson silk scarf catching the cold tungsten spill from the corridor" gives the render a surface, a light source, and a reason the colour is there.
3. **Performance subtext, not just blocking.** Each beat carries an **intention/attitude**, not only a movement. "she walks in and stops" → "she walks in like she owns the room — chin up, shoulders back, a walk built for cameras — then stops dead mid-aisle." "she smiles" → "the smile switches on, full voltage, honey-warm — a weapon she's used a thousand times."
4. **Specific nouns + verbs, never adjective stacks.** Cut "beautiful, dramatic, cinematic, epic" — they flatten output. Let the concrete noun and the exact verb carry the image ("heels strike the stone", not "she walks dramatically"). **But specific film-emulation terms are NOT empty adjectives — most engines honor them, keep them.** There's a real difference between mood-padding ("cinematic, beautiful, epic" → banned) and concrete optical/film-stock vocabulary the engine renders: **`ARRI ALEXA aesthetic`, `35mm film grain`, `anamorphic`, `shallow depth of field`, `halation on highlights`, `focus breathing`, `soft highlight rolloff`, `slightly desaturated`, `motion blur on fast actions` (name the shutter — `180° shutter motion blur` — for handheld/moving beats), `professional color grade`.** A short stack of *these* in the style/lens header is good craft; the banlist is only for the empty mood words.
5. **Clean, flowing prose.** It should read like a screenplay a human wrote, not a tag-salad. Keep the required `@mentions` and shot structure, but smooth the sentences around them.

**`@mentions` reach the model literally on most modes** — shotkit's `strip_mentions` pass turns a resolved `@id`/`@name` into the entity's plain display name before the final prompt goes out (an unresolved/unknown `@token` is left untouched, so a typo'd id still shows up as a stray `@token`). Keep them **inline beside a natural noun phrase** so the line still reads as prose (`@sky strides in, heels striking the stone, and stops mid-aisle…` — the noun phrase carries ACTION and STATE only, **never an identity trait or a garment**: face, hair and costume come from the ref, see the wardrobe rule below), and **prefer bare `@id`**; avoid leaving raw `@hall*` / `@hall#window` selector syntax sitting in the final prose where a plain place-name reads cleaner (use the selector only when a specific stored view is genuinely needed — shotkit drops the selector suffix when it renders the name anyway).

#### Before / after (the church beat)

**Draft (thin — do NOT submit):**
> `@sky` walks into `@church` and stops when she sees `@eli` fixing a pew. He stands and turns. She smiles and speaks. WIDE SHOT then CLOSE-UP.

**Enhanced (submit this — the canonical t2v form: header, timecoded shots, locks, ambient arc):**
> 5 shots, 15s total, 9:16.
> 35mm anamorphic, naturalistic skin, muted teal-and-amber, WB locked 5600K, shallow depth of field, halation on highlights.
> SHOTS:
> SHOT 1 [0:00–0:03] 84° WIDE, eye-level — static — INT. `@church`, afternoon: worn wooden pews, a dust-flecked centre aisle, high narrow windows throwing strong backlight, dust motes suspended in the beam, a simple wooden cross at the altar. `@sky` strides in like she owns the room — chin up, shoulders back, heels striking the stone with even, unhurried weight. Hard cut.
> SHOT 2 [0:03–0:06] 47° MEDIUM, LOW ANGLE — slow push at walking pace — `@sky` stops dead mid-aisle of `@church`, the window backlight raking her shoulders; her chin lifts one degree. Hard cut.
> SHOT 3 [0:06–0:09] 63° MEDIUM-WIDE, HIGH ANGLE 30° down — static — far down the `@church` aisle `@eli` crouches over a loose pew, back to her, near-silhouetted against the window light; he stills, then pushes up to standing in one weighted move. Hard cut.
> SHOT 4 [0:09–0:12] 29° CLOSE, eye-level — locked-off — `@eli` turns, the `@church` window light raking his jaw; his eyes find her and hold. Hard cut.
> SHOT 5 [0:12–0:15] 18° CLOSE-UP, LOW ANGLE — slow push — `@sky`'s smile switches on: full voltage, honey-warm, a weapon she's used a thousand times; behind her the `@church` aisle falls out of focus. Hold on her eyes.
> LOCKS: @sky stays frame-left facing screen-right and @eli frame-right facing screen-left in every shot; the aisle runs toward the altar in the background of every shot; skin tone even and constant across all cuts.
> Ambient: cavernous church reverb, the click of heels on stone → the heels stop dead, a single wood creak under his hands, room tone swelling in the silence; no score, diegetic ambient only.

Note what the enhanced version does **not** do: no identity traits inline (`@sky (strawberry-blonde…)` is the who-is-who duplication anti-pattern — shotkit injects each character's `canonicalDescription` automatically); no bare "she/the church" (every entity `@mentioned` in every shot); no single continuous push standing in for an edit.

#### Enhancement red flags — if any are true, it's still a draft

- **A shot in which nothing moves** — no BODY travel/force, no CAMERA move, no WORLD change. The most expensive miss on the list.
- **A quiet beat with no activity** — the character is "feeling something" with nothing in their hands and nowhere to go.
- The place is a **generic name** ("a room", "a church", "an office") with **no specific objects** in frame.
- **No light direction/quality** stated.
- Blocking is **mechanical** ("walks in", "turns", "smiles") with **no intention** behind any beat.
- **Adjective stacks** ("cinematic, beautiful, dramatic") are doing the work concrete nouns should.
- It reads as a **tag salad** of `@mentions` and SHOT labels rather than flowing prose.
- **No structure header** (shot count + duration + aspect, or the ONE-continuous-shot clause) as the first line.
- **Identity traits typed inline** next to an `@mention` (`@sky (strawberry-blonde…)`) — the who-is-who clause already injects them; inline traits are duplication, only STATE prose belongs inline.

**Enhance density, not length.** The rewrite makes every clause more concrete; it must not balloon the prompt. Target **~150–300 words total** for a `motionPrompt` (header + style ≈2 lines, 1–2 lines per shot, LOCKS 2–4 clauses, ambient 1–2 lines) — the who-is-who clause is prepended on top of your text, and past this budget most engines start diluting per-shot instructions instead of following them. If an enhanced draft runs long, cut a shot or a detail — don't keep both.

### Pre-submit checklist — run before every render

The final gate. Walk every item against the finished `motionPrompt`; any miss = fix before submitting.

**Items 1–4 are the DYNAMISM GATE — run them first. A prompt that fails these is boring, and a boring clip is a wasted paid render no amount of craft below can save.**

1. **Every shot carries a motion channel** — BODY (travel/force), CAMERA (frame changes), or WORLD (something changes). A drama beat carries two. No shot line reads as a person standing while the camera watches.
2. **The clip has ≥1 WORLD event** — one thing the camera can see that is different at the end than at the start.
3. **The quiet beats have an ACTIVITY** — the emotion plays against a physical task, not in a vacuum. And the Acts (slap, shove, smash) appear only on a hook or a reversal, not as filler.
4. **No dead air** — the action starts within ~1s of each shot's open; there is a nameable happening about every 3s; if the beat runs shorter than `durationSec`, `durationSec` was cut down, not padded with holding.
5. **Energy register chosen and stated** — HELD (one take, and the stillness *is* the event — you can say why), CHARGED (3–4 cuts, the drama default), or KINETIC (5–6 cuts).
6. **Header** — first line states shot count + total duration + aspect, or "ONE continuous shot, NO cuts, no zoom, Xs, 9:16" for a held take / loop / POV.
7. **Style/lens line** — concrete film vocab (no empty mood adjectives) + `WB locked NNNNK`.
8. **Every entity `@mentioned` in the `motionPrompt` TEXT** — characters, location, props; the location in **every** shot line of a multi-shot; no bare "she / the room / the bag". (A green ref budget does NOT count — it can be fed by the unsent `scenePrompt`.)
9. **No identity traits OR garments inline** — who-is-who injects `canonicalDescription`; only STATE/action prose sits next to an `@mention`. **Name no specific garment** (`tee`, `shirt`, `hoodie`, `jacket`, `dress`) for a character whose wardrobe is fixed by a ref — a garment word OVERRIDES the ref and re-clothes them; the costume is the ref's job (see "Wardrobe is the reference's job").
10. **FOV from the ladder** (8/12/18/29/47/63/84/107/180 — never an in-between), restated at start AND end of the shot line for extreme values (8–12°, 107°+).
11. **Cuts land ON the action**, every cut motivated, adjacent shots differ in size AND height/angle; no cause split from its effect across a cut.
12. **Strong actions pay the force triad** — force → point of contact → consequence in the world. No amplitude without physics.
13. **Timecodes** cover 0 → `durationSec` exactly, no gaps or overlaps, and every shot line leads with a literal `SHOT N` before its timecode — that token is what a `[shot N]` dialogue anchor is validated against.
14. **LOCKS block** — 2–4 positive invariants (frame-sides, prop state, posture, skin tone even); no negatives, no identity re-assertion.
15. **Ambient cue with an arc** where the beat turns; music and cross-scene bridges left to post.
16. **No trap words** — "stacked / split / panel / side-by-side"; vignette/eyehole words in POV; a removal-implying verb ("wipes off") on a state that must persist.
17. **Length ≤ ~300 words**; `dialogue` sized ≤ ~2 words/sec of `durationSec`.
18. **One voice per shot** — no shot carries both an on-camera `dialogue` line and a `VO:` segment. If the scene has both kinds, **every** segment is `[shot N]`-anchored and the two kinds name different shots; the narration sits in a shot where nobody speaks on camera.
19. **Idle loop** (only for a deliberate idle hold, not a default) — `loop: true`, one held take with reversible motion returning to the start pose, `dialogue` empty.
20. **Continuity** — entry state matches the previous scene's exit (positions, frame-sides, prop state, wardrobe state, time-of-day); after any edit, dependents re-checked.
21. **Nothing that trips the moderation gate** — no negated constraint anywhere (`NO fire`, `no clothing`, `no restyling`, `fully covered`), no age in years or diminutive on a character in a romance beat, no "mounted behind her"-class blocking, no role or franchise in a roster **name** — and every `@mentioned` character's `canonicalDescription` re-read, since it is injected into this prompt and you cannot see it here. A refused job is the one failure that costs the render before a frame exists. See "The moderation gate".

**`shotkit lint <scene-id>` checks before you render.** It flags unknown or missing-image
`@mention`s in `scenePrompt` and `motionPrompt`, music/singing words in `motionPrompt`,
`dialogue` or `voiceover` that doesn't fit `durationSec`, a `[shot N]` anchor pointing at a
shot the motionPrompt never declares, and any resolved reference file missing on disk. It
exits 1 when it found anything, 0 when clean.
Treat every reported line as a defect: fix it and re-run `lint` before rendering — a warning
you ignore is a render you have to redo. Write every prompt field in English regardless of
the conversation's language — many video models silently mis-render other scripts.

### Quantify what the engine measures — numbers beat adjectives

Most video models obey a **number** far more reliably than a mood word (the FOV-in-degrees rule generalises). Where a beat has a measurable quantity, state it — and where it should *change* across a multi-shot clip, ramp the number shot to shot:

- **Atmosphere in % / metres, ramped across shots.** "light fog" → "fog density 40%", "haze visible at 15 m depth". A thin/vague density renders as clean air. For a build, step it: shot 1 fog 20% → shot 2 40% → shot 3 60% — the growing number is what reads as the atmosphere thickening.
- **Speed in km/h — subject AND camera, stated separately.** "fast car" / "slow pan" → "the car powers through the wet curve at 90 km/h", "camera pans at 5 km/h". Especially load-bearing for driving/action, where "fast" alone floats.
- **A HUMAN's gait is a number too — and it is the one that bites most.** An adjective for walking speed (`strides`, `brisk`, `climbs fast`, `hurries`, `moves with purpose`) is read at its **fastest** plausible value, so a character who was supposed to walk comes out running. Quantify it and put it in LOCKS: "`@sky` walks at an even 4 km/h, an unhurried walking pace — walking throughout, never running, never jogging". A tight follow ("breathing with her stride") **amplifies** whatever pace the engine picked, so a follow shot needs the number even more than a static one.
  - The other half of the same failure is **distance, not wording**: if the route you describe (the gate → the house) can't be covered in `durationSec` at the pace you asked for, the engine speeds the body up to make it fit. **Shorten the route to the clock, never the clock to the route** — start the character already most of the way along it (or, better, already arrived — see §1a).
- **White balance in Kelvin, LOCKED per scene.** Don't just name a grade — pin the WB and hold it across every cut of a continuity block: `WB locked 3200K` (warm tungsten interior), `4000K`, `5600K` (neutral daylight), `8500K` (cold shade/moonlight). A stated Kelvin holds colour temperature even across hard cuts where "warm light" drifts. (Put it in the style/lens header and repeat it in the continuity block — see Multi-shot continuity §1.)
- **Giant / abnormal scale via human-height comparison, not metres.** "huge", "three metres tall" render inconsistently; "stands as tall as four humans stacked head to toe" gives the model a scale reference it can actually build. Use for creatures, monuments, genre beats.
- **Left / right is always from the CAMERA.** State the convention once when it could be ambiguous — "she moves left" means left from the camera's view. (This is the same axis as the frame-left/frame-right blocking discipline below.)

### Multi-shot by default — don't render one flat continuous take

A `motionPrompt` that asks for a single continuous move ("slow push from medium to close-up") renders as **one static-feeling shot with no edit** — the #1 cause of "this looks flat / no cinematography / no shot changes". Unless the beat is a deliberately held single take (an emotional close-up, an intimacy/environmental hold), **default to a multi-shot sequence with hard cuts inside the one clip** — that's where the cinematic dynamism and the change of angle come from.

- **Structure most clips as 2–4 shots**, hard cuts, with **varied shot sizes**: e.g. SHOT 1 wide/establishing → HARD CUT SHOT 2 medium (the action) → HARD CUT SHOT 3 close-up (the beat). Inserts (a hand, an object), over-the-shoulders, and reverse singles add energy and read as edited coverage.
- **Keep `@mentions` in every shot** so each cut still resolves its refs and identity holds across the cuts.
- **Pace to duration — the clip is a CUT BUDGET, ~1 cut per 2–3s.** 2 shots in a 6s clip, 3 in 7–9s, 4 in ~10s, **5–6 in a full 12–15s clip**. More cuts = more energy (short drama); fewer = a slower, heavier beat. **Soft ceiling ~6 cuts in a 15s clip** for a typical engine's per-generation cap (see `prompt-assembly/references/engines.md`): below ~1.5–2s a cut has too few frames to read as its own shot and the sequence smears into one blurry move — past ~6 distinct cuts the model stops separating them. When a beat needs more coverage than ~6 cuts, split it into a second scene, don't cram. The opposite extreme is also a deliberate choice: **spend the whole budget on ONE held take** for a signature/climax beat (the held-single-take exception below) — a long unbroken shot reads as confidence, a rushed 6-cut montage reads as panic. Pick the cut count from the beat's energy, not by habit.
- **Take the cut count from the ENERGY REGISTER, not from a habit.** CHARGED (the drama default) = 3–4 cuts in 10–15s; KINETIC (hook, reversal, chase, violence) = 5–6; HELD = one take, and only when the stillness IS the event. `~6 cuts / 15s` is the engine's practical ceiling, not a target: below ~1.5–2s a shot has too few frames to read as its own shot and the sequence smears. **But a long shot only "breathes" if something is happening in it** — a 6-second shot of a person standing is not a breath, it is dead air. Hold a shot long only when it is holding an *activity*, an *event*, or a camera move (the three channels). Otherwise cut.
- **Cut on MOTIVATION — but "nothing is happening" is itself a motivation to cut.** A cut is justified by content: new information, a reaction worth seeing, a shift of who-we-watch, an action completing. An unmotivated cut reads as nervous coverage — but so does an unmotivated *hold*, and the hold is the far more common failure here. When you cut, cut to a **meaningfully different** size/angle (the 30° guideline — never between two near-identical framings, that's a jump cut) and **cut ON the action** (see "Cut ON the action"). Holding a charged face for 8s is right only when that face is *doing* something the shot needs; holding it because you had nothing else to shoot is exactly the flat clip you are trying to avoid.
- **Two speakers → put each in their own SHOT** (e.g. SHOT 2 his line, SHOT 3 her reply) so each is lip-synced cleanly on its own cut.
- **Vary the shot SIZE on every cut — film breathes by changing the plan.** The flat, AI-made look comes from holding ONE size across a clip or a whole conversation (all close-ups, or all wides). When you cut, cut to a *different* size, and pick it by intent: **WIDE** = geography / power / isolation; **MEDIUM** = action & blocking; **CLOSE-UP** = emotion / a decision; **EXTREME-CU or insert** = a tell or a detail (a hand, an object, an eye); **OTS / two-shot** = the connection between two people. Avoid two adjacent shots at the same size, and don't open several scenes running on the same framing. **Dialogue especially:** a clean close-up is the right home base for the speaker's emotional line. Don't sit a whole exchange in one *identical* CU with no coverage — but the fix is to cut **on the beats** (a reaction worth seeing, a power shift, a new line that turns), not on every line. When you do cut, cut to a meaningfully different plan (his line in a CU, then her reaction in an OTS, the turn on a two-shot) — vary the *what*, but let each shot hold for its beat. Holding one good framing through several lines is fine when nothing motivates a cut; the failure is the *unchanging restless monotone*, in either direction — neither a jittery cut-every-line nor a flat single locked for the whole scene.
- **Vary the ANGLE/HEIGHT too, not only the size — and pin the lens by FOV.** Size is the horizontal axis (how close); camera *height/angle* is the second, vertical axis, and it carries **status**: a **low angle / worm's-eye** makes the subject dominant (power, threat, the hero as titan); a **high angle / overhead** makes them small (pressure, defeat, being looked-down-on); **eye-level** is neutral. In a confrontation or dialogue, assign the angle by who holds the upper hand this beat (boss high over the cowed lead; flip it when the lead seizes control), and change the height between cuts, not just the size. Name the setup explicitly — `LOW ANGLE`, `HIGH ANGLE 45° down`, `EYE-LEVEL`, `OVERHEAD`, `GROUND-LEVEL`, `WORM'S-EYE`. **Pin the lens by FOV in degrees, not "close-up" alone** — t2v obeys a number far more reliably: a long lens (~10–15° FOV) compresses and isolates (a tight detail/face); a normal lens (~45–50° FOV) reads natural; a wide lens (~90–110° FOV) immerses and bends space. "29° FOV, framed chest-to-top-of-head" pins both the size and the optics where "medium close-up" leaves the model guessing. (`mm` works too, but degrees give a more predictable spread across the cuts of one clip.) **Pick from a discrete FOV ladder — don't invent in-between values** (use `18°`, not `23°`); the model spreads the named steps cleanly and blurs arbitrary ones together: **`8°`** extreme tele — observation/compression, watching from far · **`12°`** tele-detail — hands, an object, a face on a wide · **`18°`** natural portrait — identity-preserving close · **`29°`** portrait compression — dialogue bust, medium-isolate · **`47°`** neutral human perspective — the universal medium/establish · **`63°`** observational wide — reportage feel · **`84°`** wide — group blocking, establish · **`107°`** architectural ultra-wide — huge interiors, immersion · **`180°`** fisheye — POV/dream distortion.
- **Grounded ≠ static.** The bans (Pillar 3/4) are on a *telegraphed face* and an *unmotivated camera* — NOT on cutting, NOT on strong action, and NOT on the camera moving with a reason. You still cut between grounded shots, the actors still cross the room and handle things, and the camera still follows them. "Grounded" describes the physics of the motion, not its quantity. Write "camera grounded, no drone, no sweeping moves" to keep each move *motivated* — never to keep the frame *still*.
- **The held single-take exception must be EARNED:** for a pure emotional/intimacy/environmental beat, ONE shot is right — there the stillness *is* the event. State why, or you have not chosen it. Everywhere else, cut. **But most engines DEFAULT TO CUTTING** — left alone they insert angle changes even when you wanted one continuous take. So a held take (and any oner, driving lock, or POV) must say it **explicitly**: "ONE continuous shot, NO cuts, no zoom" in the `motionPrompt`. Without that clause the engine splits your held beat into angles on its own.
- **Cut with intent, never by template.** Every cut must be motivated — a new piece of information, a reaction worth seeing, a change of who-we-watch — not a rote "wide→medium→CU" stamped on every scene. The best edit is the fewest cuts that serve the beat: a decision beat or an emotional exhale is stronger held; a reversal lands on the cut to the loser's reaction; a search/scan IS the character's eyeline. Decide the shot count per scene from what the beat needs, then justify each cut to yourself. If you can't say why a cut is there, cut the cut.

### Cross-cut locks — a positive-invariant block in the motionPrompt tail

A t2v multi-shot has **no per-cut keyframe**, so anything that must stay identical across the hard cuts has nothing pinning it — and the cheap stuff drifts shot to shot: which shoulder the bag-strap is on, a chair pushed back vs tucked in, a second character who must stay beside the desk, skin tone re-rolling warmer/cooler on each new angle. The reference images hold **identity** (face, garment, the prop's look), but they do **not** hold this per-clip *state and blocking*. Close the gap with a short **locks block** at the end of the `motionPrompt`:

- **Write 2–4 invariants as POSITIVE assertions, never as negatives.** "The bag strap stays on his camera-left shoulder in every shot. The boss stays beside the desk, chair pushed back, in every cut. Skin tone stays even and constant across all cuts." Positive "X stays / X is" obeys far better than "don't change X" — a negation often drags the banned thing into frame. (This is distinct from `style.banned`, which is for things that must *never* appear at all; a lock is for a present thing that must stay *the same*.)
- **Lock the things refs can't:** which hand / which shoulder, on/off and open/closed prop state, where a second character stands, posture (hunched/upright), and **skin-tone constancy** (a known t2v failure — faces re-tint per angle).
- **Don't lock identity** — face, hair, the garment's look are the reference image's job; re-asserting them here only bloats the prompt (the same duplication the who-is-who rule warns about). Lock *state and position*, not *appearance*.
- **Extreme-FOV multishots need a LENS LOCK per beat** (an `8°` tele or `107°` ultra-wide clip loses its optics after 2–3 cuts and drifts back toward a neutral ~47°). Restate the FOV **twice** — as the first word of each shot line (LENS LOCK opener) and again at its end (LENS CHECK closer): `[0:02–0:04] 8° tele — @lana isolated at the far bench … held on the 8° long lens.` Naming the number at both ends of the beat pins the compression the whole clip through; a single mention at the top decays.
- **If the default path still won't hold a lock that's load-bearing** (a precise composition a beat depends on — "exactly two empty seats visible"), that's the signal to give that beat its **own seeded scene with a keyframe**, not more lock prose. Same logic throughout this skill: what the default path can't guarantee, promote to a seeded frame.

### Looping / idle scenes (seamless loop)

**Author this only when the scene genuinely calls for a held, endlessly-repeating shot** — an ambient establishing loop, a background loop behind some other UI. It is never a default state for an ordinary scene (see the dynamism-gate hard rule above).

**This scene is a HOLD, not a beat.** Anything the viewer might sit on for an unpredictable stretch — the same few seconds replaying over and over — needs to look identical at its start and its end, or every repeat announces itself. Author it as a **near-still held frame that starts and ends identically**, and the loop disappears; author it as a normal beat and every repeat is visible.

- **Prefer a seeded mode (`i2v` or `ref-anchored --keyframe`) for anything that must loop cleanly.** `loop:true` makes shotkit append a text instruction asking the model to begin and end the clip on the same frame, in every mode — but only a seeded mode actually **hands the model a real start frame** to return to; on the default no-keyframe path nothing pins "the first frame" at all, so the loop clause has less to hold onto and a ref-composed loop is more likely to seam.
- **Bake identity into the KEYFRAME when you go seeded.** Some image-to-video endpoints take no reference images at all once a seed frame is set, so `@mentions` in the `motionPrompt` of a looping scene may buy nothing once your video model has the keyframe. `@mention` the characters and the location in the **`scenePrompt`** instead (the image model *does* read refs), get the faces right in the frame, and let the video merely breathe it. This is the one scene type where "add more refs" to the motion prompt is not the fix.
- **SHORT — 3–4s (`durationSec`).** It repeats forever; length buys nothing and only adds drift and cost.
- **ALMOST NO MOTION, and all of it reversible.** A slow breath in and out, hair settling, a faint chandelier sway, a weight shift that eases back — landing exactly on the opening pose and expression. **Nothing enters or changes:** no new people, objects or text, no wardrobe or lighting change, no one-way move (a walk, a turn, a push-in that doesn't pull back). The frame must still be the same frame when it loops.
- **ONE held continuous take — NO hard cuts.** A multi-shot hard-cut sequence cannot seamless-loop (the cut back to shot 1 is a jump). This is the held-single-take exception. **State "ONE continuous take, NO cuts, no zoom" explicitly** — most engines default to inserting cuts, and a single auto-cut breaks the loop.
- **Camera: locked-off, or a tiny drift that returns.** No one-way push/truck. `loop:true`'s own clause locks the camera itself (no zoom, no pan, no tilt, no dolly) — write the `motionPrompt` to agree with it rather than fight it.
- **Set `loop: true`** in the scene JSON — shotkit appends the seamless-loop clause to the assembled `motionPrompt` automatically.
- **Keep `dialogue` empty.** A spoken line that re-fires every loop sounds broken; let the held expression and ambient carry it.

### Verbs — two lists, and don't confuse them (Pillar 3)

**Emotion-as-verb is BANNED.** Most video models over-render raw feeling words into a telegraphed, mugging face. Replace with the body:

- "tears stream down her face" → "her eyes glass over; she does not blink."
- "smiles widely" → "the corner of her mouth lifts, then settles."
- "he rages" → "he sets both hands flat on the desk and does not look up."

**Action-as-verb is LICENSED — write it at full strength.** `slams`, `rips`, `hurls`, `shoves`, `kicks`, `sweeps`, `yanks`, `drags`, `sprints` are *not* on the banlist and never were the problem. Weakening them is what makes a clip limp. Write the strong verb — and **pay for it with the force triad**:

> **force applied → point of contact → consequence in the world**

That triad is the entire guardrail. It is what makes a big action land with mass instead of rubber, and it replaces any limit on amplitude:

- ✗ (weak) "he pushes the door open."
- ✗ (rubbery — force with no contact or consequence) "he violently smashes the door open."
- ✓ "he puts his **shoulder** into the door — the hinges **bang against the frame**, dust **jumping off the lintel**."
- ✗ "he runs furiously." ✓ "he breaks into a run — the first three strides explosive off the back foot, **gravel kicking out behind each push-off**, shoulder leading."
- ✓ "she **sweeps** the files off the desk in one pass — the **edge of her forearm** takes them, paper **still settling on the floor** two seconds later."

No consequence in the world = no weight = the floaty AI look. The fix for a rubbery action is **more physics, never less action**.

### Environmental force categories (Pillar 2)

- **Air**: wind direction + strength on hair, fabric, dust.
- **Water**: rain weight on shoulders, sheeting off surfaces, droplet trails.
- **Gravity**: weight transfer — hip-shift, knee-bend, contact with chair/wall/ground.
- **Surface**: floor compliance (carpet absorbs step, hardwood transmits), wall texture catching light.
- **Light source**: where it is, is it moving (passing headlights, candle flicker, blinds).

The force must shape **multiple** elements (hair + coat + grass + gulls) — single-element wind reads as a fan on set.

### Camera lexicon most reference-driven video models handle well (Pillar 4)

**Reach for a MOVE first — the locked frame is the last item on this list, not the first.** Every move must be *motivated* (it follows an action, reveals something, or lands a beat), but "motivated" is easy to satisfy: if the actor is doing anything, the camera has a reason to move with them.

Motivated moves — the default:

- "Handheld follow, two paces behind her shoulder, breathing with her stride."
- "Dolly-in at walking pace, ending in medium close-up."
- "Slow push from medium to close-up, arriving as the line lands."
- "Slow truck right, following the actor's shoulder."
- "Reframe on the move — the camera resettles as he drops into the chair."
- "Rack focus from the foreground hand to the background eyes."
- "Whip-pan to the door as it opens" (give it ≥0.8s — see transition timing).
- "Arc / orbital move — a slow deliberate lateral arc around the subject."
- "Crane up as she walks out of frame."
- "Anamorphic dolly, slight lens flare from an off-screen window."

Static frames — a deliberate choice, used when the stillness is the point:

- "Slow handheld breathing, micro-drift." (A textured static frame — it does **not** fill the CAMERA motion channel.)
- "Locked-off static frame, no movement." (Correct for a HELD beat, a driving lock, an idle loop — say *why*.)

**Named shot-list moves many current video engines execute directly** — use the exact term, the more specific the more reliable: `dolly in`, `push in`, `pull back wide`, `truck left` / `truck right`, `arc shot` / `orbital move` (a slow lateral arc around the subject), `handheld follow`, `crane up`. Keep them grounded and motivated — `arc`/`orbital` is a slow deliberate move around the actor, NOT a fast 360 sweep (that's still forbidden below).

**Speed ramps (action/impact beats).** Many engines control in-clip slow-motion with **caps, present-tense cue verbs** placed at the moment in the shot text: "RAMPS TO SLOW MOTION" on the impact, then "SNAPS BACK TO FULL SPEED" on the recovery. Use them to hit a punch, a fall, a reveal — not as a constant; one ramp per beat reads as intent, ramping everything reads as a music video.

**Mixing speeds across a clip — switch between CONSTANT speeds only on a cut.** A *ramp* (above) is a smooth, one-way glide of speed across a single continuous action — that belongs **inside** one shot and is fine. What smears is **hard-toggling between two constant speed modes within one continuous shot** (full-speed, then abruptly slow-mo, then back). So a shot is either **one constant speed** or **one smooth ramp**; when a whole beat wants a different constant speed, give it its **own shot and change speed on the cut** — real-time beat in one shot, slow-mo beat in the next. (This is exactly the humiliation-hook pattern in scene-patterns: shot 2 *ramps* to slow-mo on the impact, then a hard cut, and shot 3 snaps back to full speed — the mode switch lands on the cut, not mid-shot.) Short-drama use: reserve a slow-mo shot for the reversal/impact beat — a slap landing, a head turning on the line — not a whole scene; on 720p a music-video slow-mo everywhere just looks soft.

**Forbidden** (produces floaty/video-game camera): "epic sweeping drone shot", "cinematic camera movement", "360-degree rotation".

### Optical recipes (named looks) & transition timing

A few looks come from stacking specific optical ingredients — name all of them or the look half-forms:

- **Observation / hidden-camera (someone is being watched).** Three ingredients at once: (1) **foreground occlusion** — an out-of-focus obstruction over 20–30% of frame (a pillar, a branch, a doorframe edge); (2) **atmospheric haze** between camera and subject (fog/dust/shimmer — quantify it, e.g. "haze 30%"); (3) a **distant vantage** on a super-tele `8°–12°` FOV, operator anchored far away. Change the occlusion type between beats but keep the single far vantage — that's what sells "observed, not filmed".
- **Tele compressed air column (isolate a face/detail across depth).** On a long lens (`8°–12°`) name the air itself: "dust suspended in the long compressed air column between camera and subject", "heat shimmer compressed into a wall of haze in front of the figure". The compression + visible air column reads as watching from distance, and isolates the subject without shallow-DoF blur.
- **Whip-pan transition — give it ≥0.8s.** A whip-pan needs enough frames to render as motion blur; **under ~0.8s it collapses into a plain hard cut with no blur.** Author it as three timecoded beats — subject A settled → the whip (motion-blur smear) → subject B settled — with the whip spanning at least 0.8s. (For an intended instant edit, just write a HARD CUT — don't ask for a whip you're not giving time to.)
- **Intimate wide (a face WITH its world, in focus).** A wide FOV (`63–84°`) held on a *close* face — the face fills the frame but the surroundings stay **readable and in focus**, not thrown to bokeh. This is the counter to the shallow-DoF isolate: use it when the place matters as much as the emotion (a face against the room she's about to leave, the kitchen still alive behind her). It reads especially well in vertical 9:16, where the environment fills the strip above and below the head instead of dead blur — a high-yield way to keep a dialogue close-up from looking like a soundstage.

## Vertical framing (9:16 — the default)

The project default is `9:16` (vertical). Vertical is not landscape cropped narrow — it changes how you stage the shot:

- **Keep the subject and key info in the upper two-thirds.** The bottom strip is routinely covered by UI, captions, and subtitles — never put a reversal beat, a key prop, or a face down there.
- **Favor close-ups and mediums.** Vertical reads faces and emotion; wide shots waste the frame on dead horizontal space and lose information density. Reach for a wide only when the geography is the point.
- **Stage vertically, not horizontally.** Two actors face-to-face fill a landscape frame but fight for room in 9:16 — place one nearer/lower and one further/higher *within one continuous frame*, use over-the-shoulder, or cut between singles instead of a wide two-shot.
  - **NEVER call this a "stacked two-shot" / "stacked composition" — the model reads "stacked" (and "split", "panel", "side-by-side", "top and bottom") LITERALLY and renders two separate images split top/bottom in one frame.** Describe the vertical staging as a position *inside one frame*: "@a higher in frame, @b lower in the same frame", and add "ONE continuous full frame, not split, not a stacked panel". See the split-screen failure-mode row.
- **Dialogue and on-screen text carry the story.** In short vertical drama the spoken line is the payload — write the key reversal line so it lands hard, size it to `durationSec` (~2 words/sec), and keep it in `dialogue` (on-camera, or `VO:`-prefixed for an engine-baked aside) or `voiceover` (the consistent TTS narrator).

When the user asks for widescreen (`16:9` / `21:9`), drop these constraints and stage horizontally as normal.

## Scene patterns

Battle-tested starting templates (driving / emotional close-up / foot chase / intimacy / weather) live in **[references/scene-patterns.md](references/scene-patterns.md)** — read it when you need a starting point for one of those beats. Each is written **t2v-native** (a full self-contained `motionPrompt` per the canonical skeleton); the file's header note covers deriving an i2v `scenePrompt` when the user opts in.

## Multi-shot continuity

For a multi-shot scene (a beat, an exchange), continuity is enforced two ways:

**Identity (faces, places, objects) → reference images.** Generate/approve one clean keyframe, save it under `refs/` and point the entity's `bible.json` entry at it, then `@mention` that id in every later scene's `scenePrompt`. Do not re-describe a face in prose hoping it matches — it will drift. A prop that crosses a cut must be in the **same state** (which hand, open/closed, on/off) at the end of one clip and the start of the next — write that matching state into both the prior `motionPrompt` and the next `scenePrompt`.

**Look (light, wardrobe, time, ambient) → repeated text anchors.** Copy these verbatim into every shot's prompt:

1. **Lighting**: same source + direction, and a **locked Kelvin WB**. "Late-afternoon window light from screen-left, WB locked 5600K." Repeating the same Kelvin number in every shot holds colour temperature across the cuts (see "Quantify what the engine measures").
2. **Wardrobe**: full, same wording. "Navy wool coat, gray scarf, no jewelry."
3. **Time-of-day**: explicit. "Overcast late afternoon, ~4pm light."
4. **Geography**: where the actor ended the previous shot. "She has just stepped back from the counter; now she stands at the window."
5. **Ambient**: same signature, so `generateAudio` keeps the bed consistent.

## Spatial continuity & screen direction — the THIRD axis

Identity (refs) and look (text anchors) are not enough: a clip can have the right faces, right light, and still feel broken because the actors **jump around the frame** between shots and scenes — A is screen-left in one shot and screen-right in the next, two people swap sides, someone who walked to the window is suddenly back at the door. This is the **180° rule / screen-direction** problem, and it must be authored deliberately because the model has no memory of where anyone stood in the previous prompt. **You are the continuity department.** Three disciplines:

### 1. Author scenes in SEQUENCE, each continuing the last — never in isolation

When you generate or rewrite the prompts for a whole episode, **work scene by scene in story order**, and before writing each scene read the previous scene **in the same location** and answer:

- **Who is where** — each character's position in the space (left/right of frame, foreground/background, standing/sitting, at the door / at the window).
- **Which side of frame** each character occupies, and **who faces whom** (eyelines).
- **What each character holds** and in **which hand** (prop state — see the prop rule above).
- **Where anyone moved** during that scene — the **exit state** is the next scene's **entry state**.

The new scene opens consistent with that exit state unless a deliberate time-jump/relocation cut intervenes (and then say so). Don't author each scene as a fresh island — that's what produces actors teleporting across the cut.

### 2. Keep a blocking ledger per location

Hold a small **ledger** (in notes / your working memory) for each recurring location, updated as you write each scene:

```
@great_hall — line of action: camera on the south side.
  @lana:     frame-RIGHT, facing screen-left, stained blazer, empty hands.
  @caroline: frame-LEFT, facing screen-right (toward Lana), couture uniform.
  @theo:     deep background, frame-RIGHT bench, seated.
@classroom — line of action: camera at the front of the room.
  @lana:     side desk, frame-LEFT, facing screen-right toward the rows.
  @priya:    margin, frame-RIGHT, hunched.  @theo: mid-row, frame-RIGHT.
```

Write these positions **explicitly into the prompt** — "@lana on frame-right facing screen-left, @caroline on frame-left facing screen-right" — in **every** shot and **every** scene in that location. State the **spatial relation** as a hard lock when it matters ("@lana, @caroline and @theo in one straight line, in that order") — a stated geometric relation holds placement better than three separate side-tags. For a **hard 3+-body blocking** that keeps drifting, you can anchor a **top-down schematic of the staging** (a clean single frame marking where each figure stands) as a location view (add it to the location's `views` list with `label:"blocking"`) and `@mention` it — the geometry then conditions the render like any location ref. (A real photo gives texture, a schematic gives geometry — use the schematic only when placement, not look, is the problem.) Stating the side is what holds it; the model won't infer it. If a character **crosses the frame** in a scene ("she moves to the window, now frame-left"), update the ledger and reflect the **new** position in every subsequent shot/scene. The ledger is also how you keep the same **camera angles/coverage** on a returning location — reuse the established shot vocabulary (the OTS favouring Lana, the wide from the dais) rather than re-inventing the geography.

### 3. Screen-direction / 180° rules to bake into the prompt text

- **Pick ONE line of action per location and keep the camera on one side of it.** Crossing the line flips everyone left↔right and reads as a swap. State the camera's side once at the top of the location's scenes.
- **A character keeps their side of frame across shots AND scenes** in the same geography. Lana frame-right in the hall stays frame-right every hall shot, this scene and the next.
- **Eyelines match the blocking.** If A (frame-right) looks screen-left at B, then B (frame-left) looks screen-right at A. Write both directions.
- **Movement is one-way and tracked.** "Crosses from the door (frame-right) to the window (frame-left)" — after it, she is frame-left until she moves again. Never silently reset her.
- **Entrances/exits keep their vector.** Someone who exited screen-left should re-enter screen-right (continuing the same travel), not pop back where they left.

### 4. Edit propagation — change one prompt, fix the whole dependent chain

Blocking, screen-side, wardrobe state, prop state, and time-of-day **propagate forward**. So when you change one scene, you are not done until the **dependents** are consistent:

- Rewrite a character's **exit position / screen-side / what-they-hold** in scene N → immediately rewrite scene N+1 (and onward, while they're in the same location/continuity) so its entry state matches.
- Change a **prop's state** (suitcase now open, jacket now off) → carry the new state into every later scene until something changes it again.
- Change **wardrobe / lighting / time-of-day** → update every scene that shares that continuity block.
- After any single-prompt edit, **re-scan the neighbours** (the scene before and after, plus other scenes in the same location) and reconcile. A change that leaves scene N contradicting scene N+1 is a half-done edit. State to the user which dependents you touched.

This is a separate job from identity and look: refs hold **who**, text anchors hold **how it looks**, and this axis holds **where everyone is in the space and which way they face** — across the whole episode, not just within one clip.

## Authoring order & division of labor (default)

**Write scene JSON complete up front; render and generate afterward, in whatever order suits the work.** shotkit never calls an image or video model itself — it only turns `bible.json` + `scenes/*.json` into a prompt and a reference list. Unless the user is generating right now, your job is to author the bible + every scene's prompt fields **fully and immediately**, and leave running `shotkit frame` / `poster` / `motion` / `sheet` / `location` / `prop` — and feeding the output into an actual generator — for whenever they're ready.

This works because **shotkit resolves `@mention`s fresh, every time you run a render command** — reading whatever `bible.json` says at that moment. So the order is decoupled:

1. Author every prompt **now**, with `@mention`s for every character + location + prop already in place (and, on the default path, the full self-contained `motionPrompt` — see the CRITICAL note above), even though no reference images exist yet.
2. Later, generate + save the reference images and point `bible.json` at the saved files.
3. Every render command re-reads `bible.json` at the moment you run it, so a `@mention` written before the image existed still attaches it once it's there — nothing needs to be re-authored.

So: **always write prompts with all `@mention`s and full default-path content from the start** — don't defer mentions "until the images exist". The only hard requirement is that a `@mentioned` entity has at least one reference image on disk **by the time you actually render** — `shotkit lint` flags a missing one.

## Workflow

**Starting from an empty or partially-cast project?** This workflow assumes the project
already exists and the bible is at least partly filled in. When the user asks for a
scene and the cast, location or props it needs aren't in `bible.json` yet — or the
project folder doesn't exist at all — start from `scene-from-scratch` instead: it covers
creating the project, the cold-start question pass, writing the bible, and generating
references before any scene is authored. Come back here once that's done.

1. **Bible.** The project is seeded photoreal already (`style.globalPreamble` + `style.banned` in `bible.json`) — **don't overwrite the look unless the user wants a different one** (see Defaults); if you hand-write a new `globalPreamble` it must name the medium and `banned` must negate the opposite one. Set `style.aspect` for the project default (`"9:16"` unless the user asks for widescreen) — frame the keyframes for a vertical 9:16 crop (subject centered, headroom managed, less horizontal staging). Add characters/locations/props as entries in `bible.json`, giving each a `canonicalDescription`.
2. **Anchor identity.** For each recurring location and prop, generate a reference image (`shotkit location <id> --view <label>` / `shotkit prop <id>`, then your image model), save it under `refs/`, and point the entry's `uri` at it. Characters get a turnaround via `shotkit sheet <id>`, but you can point `looks[].refImage` at a chosen reference too. Without this, identity drifts.
3. **Scenes.** Add a `scenes/<id>.json` per scene (`locationId` + the prompt fields). Each scene's `locationId` is injected as text — still `@mention` a location reference for visual consistency.
4. **Author the shot (default = no keyframe → only `motionPrompt`).** Write a self-contained `motionPrompt` plus `dialogue` / `voiceover` / `generateAudio` / `durationSec`. **Leave `scenePrompt` empty** unless the user opted into a seeded mode. `@mention` every character + location + prop by id, in the `motionPrompt`.
5. **Narration sweep — once over the WHOLE episode, after the prompts are written.** Walk **every scene** and list its `dialogue` segments **by shot number**. Any shot holding both an on-camera line and a `VO:` segment is a defect: move the `VO:` into its own shot **inside that same scene** (a shot with nobody speaking on camera — insert, reaction, listening beat), add that shot to the `motionPrompt`'s shot list, and re-anchor it. Run this as its own pass across the episode, not scene-by-scene while authoring — a narrator line reads fine in isolation, and the collision only shows up when you read the shot's speech clauses together. See "One voice per shot".
6. **Clip (default = no keyframe).** `shotkit motion <scene-id> --mode t2v`, straight off the `@mentioned` references. This is the default and the stronger path for every scene. On this path the **`motionPrompt` is the only text sent** (a `scenePrompt`, if present, only resolves refs) — so the self-contained `motionPrompt` defines the look and composition, and the camera is free to move from there.
7. **Seeded mode (opt-in ONLY).** Only when the user explicitly asks to lock an exact frame first: NOW author the `scenePrompt`, run `shotkit frame <scene-id>` → generate it in an image model → review the result (regenerate if it came out wrong) → approve → run `shotkit motion <scene-id> --mode i2v` (or `--mode ref-anchored --keyframe PATH`) and hand that frame to your video model.
8. **Audio polish.** The post `voiceover` track and any music are separate post layers, laid in after the clip — not baked by `generateAudio` (unlike `VO:` segments in `dialogue`, which a native-audio engine bakes into the clip itself). If a story needs one consistent narrator voice, pick your TTS tool's voice **before** generating any VO and hold it constant across every scene yourself — shotkit has no voice catalog to do this for you.

### Multi-character same-frame shots — still no-keyframe by default

When 2+ characters share the frame and interact (a standoff, a conversation, a fight), **stay on the default no-keyframe path** — author only a self-contained `motionPrompt` and just `@mention` each character (shotkit auto-injects the who-is-who clause from their `canonicalDescription` — see "Who-is-who" below; don't hand-tag the trait inline). Do **not** switch to a seeded mode on your own; multi-character is not a reason to leave the default.

**A seeded mode here is a user-opt-in hard lock only.** If the user explicitly asks to lock blocking/identity for a tricky multi-character interaction, then build the static keyframe deliberately **before** animating: author the `scenePrompt`, run `shotkit frame` with every character + location `@mentioned` in one composition with one consistent light, generate it, review, approve — then run `shotkit motion --mode i2v` (or `ref-anchored --keyframe`) from that approved frame. A composed keyframe holds positions/identities harder than loose refs — but only reach for it on request.

### Who-is-who on the default path — identity binding (multi-character)

**On the default path the model receives N unlabeled reference images + the `motionPrompt` text.** With **2+ characters** it has no inherent binding of *which image is which name*, so left alone it assigns identities by guess and **swaps them** — even when the characters look clearly different, and multi-shot prompts ("3-shot sequence, hard cuts") make it worse because identity re-assigns across each cut.

**shotkit closes this automatically — but only once there are 2+ faces to disambiguate.** With **two or more** `@mentioned` characters that each carry a non-empty `canonicalDescription`, `shotkit motion` prepends a who-is-who clause built from them:

```
Character identities — match each face to its reference image: Caroline: <canonicalDescription> Lana: <canonicalDescription>
```

Below that count — a single `@mentioned` character — shotkit injects **nothing**: with only one face in the shot there is no other identity to swap it with, so there's nothing to disambiguate. **This is NOT the same string `shotkit frame`/`shotkit poster` inject** (their identity clause reads `"Maintain identity: Caroline: <text>. Lana: <text>."` and fires at any count, including one — see below); the two clauses live in different code, have different thresholds, and must not be confused for each other.

So `canonicalDescription` **IS** sent on the default path once 2+ characters share the shot (via this clause), and it is the binding that stops the swap.

So for any 2+ character shot:
1. **Just `@mention` each character — do NOT re-type their identity trait inline.** shotkit already injects the who-is-who from `canonicalDescription`, so repeating `@caroline (platinum-blonde, couture)` inline only **duplicates** that text and bloats the prompt. Plain `@caroline tips the tray onto @lana` is enough for identity.
2. **Each character MUST have a `canonicalDescription` set** — a short, clean identity tag. That is what powers the auto-binding; an **empty** `canonicalDescription` = no who-is-who clause for that character = the swap risk returns. Fill it.
3. **Keep shots fewer on dense beats** (3–4 faces): each cut still re-rolls identity; the auto clause lowers the rate but doesn't fully eliminate it. For a hard lock, opt into a seeded mode (keyframe first, per above). Default stays no-keyframe.

**`canonicalDescription` must be a SHORT, clean identity tag — NOT a full turnaround-sheet prompt.** shotkit already adds the sheet boilerplate under the hood; `canonicalDescription` is the *identity*, never the layout. It is consumed in two places, both of which want it short and clean:
- **Character-sheet generation** (`shotkit sheet`, built by `shotkit/turnaround.py`) wraps it: it emits the 9:16 reference-sheet layout — head-rotation grid, full-body panels, the style block and the banned tail — **itself**, and drops your text in as one `Subject identity` line. So the turnaround/grid/panel layout is **automatically appended** — you write only `Caroline — 18, platinum-blonde blowout, pale-blue eyes, couture navy uniform…`.
- **Scene keyframe generation** (`shotkit frame`, built by `shotkit/scene.py` — the seeded-mode start frame) injects it **verbatim** as `Maintain identity: Caroline: <text>. Lana: <text>.` So a bloated `canonicalDescription` containing "turnaround board / head-rotation grid / full-body panels" **leaks those words into a single-frame render** and induces the exact split-screen/multi-panel the `style.banned` list fights. Keep it a plain person description.

So **never paste sheet-layout text into `canonicalDescription`** (some auto-generators wrongly do — fix the data to a tight identity paragraph). The `board/grid/panels` words belong only inside `shotkit sheet`'s own template, which shotkit owns.

**And never paste an authoring DIRECTIVE into it either** — `Identity only — no clothing here.`, `Identity/species only — no rider, no saddle here.` Those sentences address whoever fills the field; injected into a clip prompt they are just words about clothing sitting beside a described body, which is how a whole render comes back refused as sensitive. Same class of leak as the sheet-layout text, different blast radius: this one is scored on **every** scene the character appears in. shotkit strips a known set of these directive phrasings before prompting (`clean_identity_description`), but the field should never carry them in the first place — the stripper knows only the phrasings it's seen, not the one you invent next. See "The moderation gate".

**`canonicalDescription` IS what disambiguates identity swaps now** — shotkit's auto who-is-who clause is built from it (above), so on the clip identity rides the **reference image PLUS that injected clause**. One job, one source: keep `canonicalDescription` a short clean identity tag and let shotkit inject it; don't hand-write the trait inline (that just duplicates).

#### Identity vs. STATE — `canonicalDescription` is the CLEAN base look, never a scene state

`canonicalDescription` (and the auto who-is-who clause it feeds) carries **stable identity only** — face, hair, **base/clean wardrobe** — and it is injected into **every** scene that character appears in. So **never bake a scene-specific STATE into it**: a food spill, a stain, blood, a wound, wet hair, a torn sleeve, a removed jacket. Bake it in and that state wrongly shows up in scenes *before* the event and in unrelated scenes.

A scene-specific look that must **carry forward** — e.g. food gets dumped on Lana and the **stained blazer continues** for the rest of the episode — is a **continuity entity, handled exactly like a prop. Option A does NOT touch it:**

- Make it a **Prop** with its own reference (`@stained_blazer`): pull a clean frame of the stain from a rendered clip (or generate one), save it under `refs/`, and add a prop entry pointing its `uri` at that file.
- **`@mention` the prop in every scene from the spill onward, AND write the state prose inline in every shot** — "wears `@stained_blazer` with the SAME pale sauce spill and crumbs down the front; the stain is IDENTICAL in every shot, never fades, washes off or cleans up."
- This inline **state prose is NOT the identity trait** shotkit injects (that's the clean look), so it is **not** the duplication option A removes. **State prose always stays inline.** Option A only stops you re-typing "platinum-blonde, couture"; it never stops you describing the stain.
- The clean `canonicalDescription` ("plain navy uniform") still gets injected, but the `@stained_blazer` ref + the explicit "SAME stain, never disappears" prose **override the look for that scene**. (See the stain/continuity rows under Failure modes.)

**Rule of thumb:** if it's true of the character in *every* scene → `canonicalDescription` (clean identity, injected automatically). If it's true only *from some event onward* → a Prop ref + inline state prose, in every affected shot.

**When the state change is BIG, give the character a new LOOK — not a second character, not a prop, not inline prose.** Small/local state (a stain, one rolled sleeve, hair mussed) is held fine by a prop ref + inline prose. But a *large, silhouette-changing* transformation that persists — soaked-through after rain, bloodied and beaten, a full costume change, aged 20 years, caked in mud — is more than inline prose can hold across cuts: the model under-applies it and it flickers shot to shot. Then give that look its own **look tag on the same character**: add a `looks: [{label: 'wet', description: '...', refImage: 'refs/hero-wet.png'}]` entry in `bible.json`, render it with `shotkit sheet <id> --look wet`, generate it in your image model, save the result, and `@mention` it as `@hero#wet` in the affected scenes. It conditions **both** the keyframe and the clip and rides the who-is-who binding, so the big state stays consistent without re-describing it inline every shot. **Never create a second character (`@hero_wet` beside `@hero`) for this** — the face does not survive a prose re-description, and the identity splits in two. Reserve looks for *large, durable* changes; a passing or minor state isn't worth a tag.

#### Wardrobe is the reference's job — never name a garment that fights it

A character's costume is **identity, exactly like their face** — the primary look / `canonicalDescription` and the reference sheet carry it, and on the default (refs-only) path **naming a specific garment in the prompt OVERRIDES the ref and re-clothes them.** This is a different, worse failure than the who-is-who *duplication* (which only bloats): a concrete garment word reads as an *instruction*, and the instruction beats the picture. If `@jace`'s ref is a black hoodie and the shot says "`@jace` in a fitted team tee", the render puts him in a grey tee. This bites a **single** character on their own line, not just multi-character shots.

- **Describe only the ACTION and the STATE; let the primary ref/look dictate the costume.** "the shove landing on his shirt" → "the shove landing square on his chest". "`@jace` in a grey hoodie crosses the room" → "`@jace` crosses the room". Cut every concrete garment noun (`tee`, `shirt`, `hoodie`, `jacket`, `dress`, `jeans`, `joggers`, `coat`, `suit`) for any character whose wardrobe is already fixed by a ref.
- **Positive-lock the costume instead of naming it, when a lock helps** — `@charlie` and `@jace` each in exactly their reference-sheet wardrobe — no restyling, no changed clothing. This pins the ref without ever naming a garment, so nothing can override it.
- **Name a garment ONLY when you genuinely want a wardrobe CHANGE** — and then do it the durable way, never as a bare adjective in the prose: a **look tag** on the character (`looks: [{label:'gym', …}]`, addressed `@jace#gym`) or a **prop ref** for a carried/added piece (`@varsity_jacket`). A one-off garment word is the failure; a ref-backed look/prop is the fix.
- **Stripping a garment from an existing prompt is a FIX, not lost detail** — the costume was never yours to specify; it belongs to the ref. On any rewrite, sweep the whole scene (and the rest of the episode) for garment nouns on ref-fixed characters — one leftover "team tee" or "grey hoodie" re-clothes that shot.

### Defaults

- **globalPreamble + banned**: a new project is already seeded photoreal (`template/bible.json`'s `style` block: "photoreal cinematic, 35mm film look, natural light, shallow depth of field", banned "text, watermark, logo, extra limbs, blurry, low quality"). **Leave it alone unless the user asks for a different look** — a preamble that only names cinematography ("cinematic, 35mm, warm grade") states no medium at all, which is how a photoreal cast renders as cartoons. If you edit `globalPreamble` by hand, it **must name the medium** ("hyper-realistic photography, full photorealism" / "hand-painted 2D animation"), and `banned` **must negate the opposite medium** ("illustration, anime, cartoon, 3D render" for photoreal). The two are one style — never change one without the other.
- **aspect**: default **`9:16`** (vertical / portrait) — set `style.aspect` in `bible.json` (a scene's own `aspect` overrides it). Use `21:9` or `16:9` only when the user explicitly asks for widescreen/landscape.
- **durationSec**: **10–15s for a standard multi-shot drama beat** (CHARGED — 3–4 motivated cuts inside the clip); **6–10s for a single held take**; **3–4s for an idle loop**. A full 12–15s spent on ONE unbroken take is the signature-beat exception (intimacy, environmental hold, climax oner). **Set the duration from the CONTENT, not the other way round** — count the happenings in the beat (~one per 3s) and pick the length that fits them. A 15s slot with 8s of beat in it is a boring clip; make it a 10s clip. Duration is a container to fill, never a quota to pad.
- **generateAudio**: `true` unless the user wants silence.
- **Language**: every prompt field (`motionPrompt`, `scenePrompt`, `dialogue`, `voiceover`, `canonicalDescription`, view prompts) is **English only**, regardless of the conversation's language — most video/image models and shotkit's own assembly templates are English; talk to the user in their language, author the fields in English.

## The moderation gate — the prompt that never renders

Many image/video providers run a **text classifier over the whole assembled prompt** before generating a single frame, and it can return one opaque refusal, in the shape of something like:

> `Content flagged as potentially sensitive. Please try different prompts or images.`

It names nothing — not the word, not the field, not the character. The whole render is refused. Three properties of that kind of classifier decide how you have to write:

- **It scores what is PRESENT, not what you meant. Negation is not reliably parsed.** `NO fire`, `no clothing`, `fully covered and modest`, `no restyling` put `fire` / `clothing` / `modest` / `restyling` into the text. A negated word is still that word — and beside a described body it is *worse* than silence, because it is your prompt raising the topic.
- **It reads the FINAL text, not the field you edited.** shotkit prepends the who-is-who clause (every `@mentioned` character's `canonicalDescription`) and appends the audio-discipline tail before the prompt ever leaves your machine. A phrase parked in a character's bible entry is therefore scored on **every scene that character appears in** — and it is invisible in the field you are staring at.
- **It is ONE score over the whole passage.** Individually harmless clauses add up: an age in years, a body description, the word `delicate`, and a line about falling in love are each fine and jointly a refusal.

### The rules that keep a prompt renderable

1. **Write every lock and constraint POSITIVELY.** Same rule as the LOCKS block (positive invariants only); the moderation gate is its second, harder reason. `NO fire, NO smoke` → `clear untouched air`. `no restyling` → `costume unchanged across shots`. `she stays fully covered` → `she wears full flight-leathers, high collar, gloves, buckled harness`. State what IS.
2. **Never write about clothing in the negative — in any direction.** `no clothing`, `not naked`, `fully covered`, `modest`, `undressed` all raise the sexual-content score of a passage that also describes a body. Wardrobe belongs to the reference anyway (see "Wardrobe is the reference's job"), so for a ref-fixed character the correct amount of clothing prose is **none**.
3. **`canonicalDescription` is prompt text, never a note to yourself.** It ships verbatim into every clip and every sheet. Directives written for the bible's *author* — `Identity only — no clothing here.`, `Identity/species only — no rider, no saddle here.` — are pure content to a classifier: a phrase about clothing sitting next to a described body. Write description only; shotkit supplies its own framing. (shotkit strips a known set of directive forms on the way out (`clean_identity_description`), but the field should never carry them — the stripper knows only the phrasings it's seen, not the one you invent next.)
4. **Roster NAMES are injected verbatim too.** Every `@mention` resolves to the name and the who-is-who clause repeats it, so a name is prompt text like any other.
   - **No parenthetical roles.** `Wren (heroine)`, `Lord Cassian (Dragon Queen's husband)` render nothing and get scored like any other words — and `heroine` contains `heroin`, which keyword-level drug filters do match. Call her `Wren`; keep the role in your notes.
   - **No franchise or house names.** `Royal Dragon (House of Dragons)` drops a near-miss of a real title into every prompt — an IP flag stacked on top of a safety one.
   - Plain, human, one or two words. The model does not render the parentheses.
5. **Age + body + romance is the highest-risk combination in the whole system.** Any one alone is fine; together they read as sexualisation of a minor, the axis with the lowest threshold and no appeal. For any character in a romance beat:
   - **State no age in years.** `a delicate young woman of nineteen` → `a young adult woman`. The number buys nothing — the reference sheet carries the face.
   - **Cut the diminutives**: `delicate`, `slight, light build`, `youthful features`, `the youngest of the cast`, `little`, `girl`.
   - Keep what actually pins identity — hair, eyes, bone structure, skin tone — and drop the rest.
6. **Watch blocking language that doubles as a sex position.** `mounted directly behind her`, `on top of him`, `beneath him`, `straddling` are read on their own terms even when the subject is a saddle, a horse or a dragon. `@wren seated forward and @cassian mounted directly behind her` → `@wren in the forward saddle, @cassian in the rear saddle`.
7. **Violence tokens are the same trade.** `dagger teeth`, `scarred hands`, `draws breath to burn`, and any `no fire / no smoke` said in the negative each add a little. None will refuse a job alone — drop the ones not earning their place in the frame.

### When the refusal fires

The message names nothing, so **bisect — never rewrite blind**:

1. **Re-submit once, unchanged.** These classifiers are not deterministic and a borderline score sometimes passes. If it does, the prompt is still over the line — fix it anyway; do not ship on a coin-flip.
2. **Suspect the INJECTED text first, because you can't see it.** Read every `@mentioned` character's `canonicalDescription` and apply rules 3–5. In practice this is where the trigger lives, precisely because it is the text nobody was looking at.
3. **Then bisect your own field.** Submit the shot lines with no LOCKS block; then the LOCKS with one shot. The half that refuses holds the phrase.
4. **Check the images too.** Many providers moderate a seeded keyframe and every reference image separately from the text, and no amount of text editing clears an image-level flag. If the text is clean and it still refuses, cut back to a bare `@mention` set and add refs one at a time.
5. **Fix the SOURCE, not the scene.** A `canonicalDescription` fix clears every scene that character is in; a scene-level workaround leaves the next render to fail identically.

## Failure modes

The **full symptom → cause → fix catalog (45+ rows) lives in [references/failure-modes.md](references/failure-modes.md)** — read it whenever a render came out wrong. The failures worth preventing at authoring time, as one-line reminders:

- **Actors stand and breathe; the clip is boring** → no motion channel and no activity; give the beat something to *do* (see "The dynamism gate").
- **15 seconds, one short line, nothing else** → dead air; shorten `durationSec` or fill it with action — never with holding.
- **The cut lands but nothing changed** → cut between two settled poses; cut ON the action instead, and make each shot differ in size AND height.
- **The camera never moved** → the locked frame was the reflex, not a choice; default to a motivated move (follow, push, rack).
- **Flat, no cinematography** → the `motionPrompt` was a single continuous take; structure the cuts by energy register (CHARGED 3–4, KINETIC 5–6).
- **A held take cut itself into angles** → most engines default to cutting; say "ONE continuous shot, NO cuts, no zoom" explicitly.
- **Cuts smear together** → too many cuts for the duration; ~1 per 2–3s, ≤~6 in 15s.
- **Identities swapped (2+ characters)** → an empty `canonicalDescription` broke the auto who-is-who clause; fill it, never re-type traits inline.
- **A character rendered in the WRONG clothes** (not what their ref shows) → a garment word (`tee`, `shirt`, `hoodie`, `jacket`) in the prompt overrode the ref and re-clothed them; name no garment for a ref-fixed character — describe only the action and let the look dictate the costume (see "Wardrobe is the reference's job").
- **Location drifted despite a clean lint** → the `@mention` sat only in the unsent `scenePrompt`; it must be in the `motionPrompt` TEXT, every shot.
- **State/blocking drifted across cuts** (strap, chair, skin tone) → no LOCKS block; add 2–4 positive invariants at the tail.
- **Crowd of clones** (extras wearing the lead's face) → describe extras as distinct strangers, out of focus, faces averted.
- **Frame split into stacked panels** → the words "stacked/split/panel/side-by-side" were in the prompt; remove them, state "ONE continuous full frame".
- **The narrator's line came out of a character's mouth, lip-synced** → a `VO:` segment shared a shot with an on-camera `dialogue` line (or both were left unanchored); move the narration to its own shot in the same scene and anchor both kinds to different shots.
- **Idle loop jumps on repeat** → it wasn't authored as a seamless loop; one held take, reversible motion, `loop:true`, preferably a seeded mode.
- **`Content flagged as potentially sensitive` — the job never rendered** → a negated constraint (`no clothing`, `NO fire`), an authoring directive or an age-plus-body description sitting in an injected `canonicalDescription`, or a role/franchise baked into a roster name; bisect from the injected text outward (see "The moderation gate").

## Output discipline

Return only what the user needs:

- A brief plain-language description of what was made ("Held close-up at the kitchen window, 21:9, 8s, ambient room tone").
- Do not paste the full `scenePrompt`/`motionPrompt` unless asked.
- Do not paste tool internals, media ids, scene ids, or the framework itself ("I applied the five pillars…").

## Pitfalls

1. **Don't ship a clip where nothing happens.** The #1 defect. Every shot needs a motion channel (BODY / CAMERA / WORLD), every clip needs one WORLD event, and every quiet beat needs an **activity** to play against. Actors who stand and breathe for 15 seconds are not "restrained" — they are a failed scene.
2. **Don't stack adjectives** in the style clause. One specific film-stock reference beats "cinematic, beautiful, dramatic, epic".
3. **Don't write emotion as a verb** — but don't weaken an *action* verb either. The face stays restrained; the body is free. `slams` / `rips` / `hurls` are correct, as long as you write the contact and the consequence.
4. **Don't skip environmental force.** Without it every shot reads as a soundstage.
5. **Don't let the camera float without a motive** — no drone sweeps, no 360° orbits. But a camera that never moves is the more common failure: a motivated move beats a locked frame, and an unmotivated hold is as lazy as an unmotivated swoop.
6. **Don't pad to `durationSec`.** If the beat runs out before the clock does, shorten the clip — never fill the gap with holding.
7. **Don't trust prose for identity.** Same face/place/prop across shots = reference image + `@mention`, never description.
8. **Narration lives in ONE place per scene — and in its OWN shot.** Plain `dialogue` lines are on-camera speech only. Narration goes either into `dialogue` as a `VO:`-prefixed segment (baked by the video model itself, a one-off voice) or into `voiceover` (a separate TTS pass, the same story-wide voice every scene) — never both on one scene: both are audible and you get double narration. And a `VO:` segment never shares a **shot** with a spoken line — same shot and the engine lip-syncs the narration onto the on-camera face, turning the off-screen narrator into direct speech. Sweep the whole episode for this before rendering (see "One voice per shot" and Workflow step 5).
9. **Don't state a constraint by negating it.** "NO fire", "no clothing", "fully covered", "no restyling" — the render engine under-weights the negation and the moderation classifier ignores it entirely, so you get both the thing you banned and a refused job. Every lock is a positive invariant, in the LOCKS block and everywhere else.
10. **Cold-viewer test.** Before finalizing a shot, read it as a first-time viewer with no context: can you tell WHO this is, WHERE they are, and WHY this beat matters from what's on screen alone? If not, the framing/`@mention`/blocking isn't doing its job yet. **The hardest version of this is a silent CLUE:** an insert meant to plant information ("someone was just here") fails if the inference rests on invisible state — temperature, freshness, or "this wasn't here before". Render the change as a visible *process* (condensation running down the glass, a wet ring spreading, steam still lifting) or give it a line — a wordless frame cannot carry an inference. See short-drama-structure → "A PLANT must be readable from the frame alone".

## When a shot fails

If the user reports a failure mode, consult the full catalog in [references/failure-modes.md](references/failure-modes.md) and **rewrite the offending field** (`scenePrompt` or `motionPrompt`), then re-run `shotkit frame` / `shotkit poster` / `shotkit motion` and generate again. Do not switch engines or chase a different model — quality lives in the prompt structure and the reference images, not the engine. For an identity drift specifically, the fix is almost always a missing reference image or a missing `@mention`, not a prompt rewrite.

## Related

- **[scene-from-scratch](../scene-from-scratch/SKILL.md)** — the entry point when the
  project is empty or the cast/location/props a request implies aren't in the bible yet:
  the cold-start question pass, writing the bible, and the reference pass that has to
  happen before this skill's craft has anything to anchor onto.
- **[character-refs](../character-refs/SKILL.md)** — who the people (and creatures, and objects) in a scene are: building the reference kit each `@mention` resolves to, so this skill's craft has faces, places and props to anchor onto.
- **[prompt-assembly](../prompt-assembly/SKILL.md)** — how the fields this skill teaches you to write (`scenePrompt`, `motionPrompt`, `dialogue`, `voiceover`) become the one finished string a generator actually receives, and which engine-specific numbers (ref caps, duration bounds) currently apply.
