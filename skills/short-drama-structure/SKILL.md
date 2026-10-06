---
name: short-drama-structure
description: |
  Structure vertical short-form drama (micro-drama / 短剧 / paid web drama) for retention —
  the 3-second hook, reversal cadence across a clip, and per-episode cliffhangers — and map
  that structure onto an ordered sequence of scenes. Load when the user asks for a micro-drama,
  vertical paid drama, reversal/twist drama, a hook-driven opening, a binge-able series, a
  cliffhanger ending, episode pacing, or genres like revenge / rebirth / secret-identity /
  CEO-romance short drama. This skill handles STRUCTURE (beats, order, twists) and the
  dramaturgy under it (spine, escalating conflict, chemistry, causality, setup-before-payoff,
  and beats that are physically playable rather than internal states); for the shot craft
  inside each scene use the cinematic-scenes skill.
---

# Short-drama structure

## When to use

Trigger when the user wants the **structure of vertical short-form drama** — the thing that makes people keep watching — not just a single beautiful shot:

- "micro-drama", "短剧", "vertical paid drama", "web drama", "reels drama"
- "hook", "강한 오프닝", "grab them in 3 seconds", "강한 시작"
- "reversal", "twist", "plot turn", "爽点", "逆袭 / 重生 / 追妻 / 霸总"
- "cliffhanger", "binge", "next-episode hook", "multi-episode series"

This skill decides **what happens and in what order**. For the craft inside each scene (body weight, environmental force, camera, vertical framing, dialogue sizing), use the **cinematic-scenes** skill. The two compose: this one lays out the episode's beats, cinematic-scenes renders each beat.

## Continue into production when that is the requested scope

For a Shotkit story or episode project, the outline is the structure stage. Use
`scene-from-scratch` to automatically populate the bible, write draft scene JSON
and execute the character, location and prop reference-prompt pass before calling
the production starter complete. Run `build` after source edits so every scene also has its full
`out/scenes/<id>/motion.txt`, even while images are pending. Propose unspecified visual details as provisional
designs; do not wait for a separate request to create the skeleton. A
`STORY.md` plus empty entity arrays does not provide the generation assets. Keep an
explicit request for a synopsis or concept only within that narrower scope.

## Core principle

**Vertical short drama is retention engineering.** Viewers swipe away in seconds. Every choice serves one goal: get them to the next beat, and every episode to the next episode. Three levers do almost all the work:

1. **The hook** — the first ~3 seconds decide whether anyone watches the rest.
2. **Reversal cadence** — a steady drumbeat of turns; flat stretches lose the audience.
3. **The cliffhanger** — every episode ends on an unresolved beat that forces the next tap.

## Story foundation — the dramaturgy under the beats

The hook / cadence / cliffhanger below are retention *mechanics*; they only land if the story underneath holds. Six load-bearing rules (they fix "flat / choppy / static / no chemistry / nothing grabs"):

- **Spine — ONE dramatic question per episode.** Name it in a line, driven by the protagonist's concrete want ("Will she expose the groom before the wedding?" — not "a story about trust"). Every scene must raise, complicate, or push toward its answer; a scene that doesn't touch the spine is cut or rewritten.
- **Conflict & escalating stakes.** Every scene = intention + obstacle (someone wants something NOW, something/someone blocks it). Stakes rise beat to beat; the price of losing is visible on screen. Two scenes at equal pressure → one is redundant.
- **Chemistry = opposed wants + shifting status.** Two people want different things from the same moment; the upper hand flips. Show it in behaviour and subtext, not narrated feelings. Indifference kills the scene.
- **Causality — "therefore / but," never "and then."** Each scene is *caused by* the last and *causes* the next. If you can reorder two scenes with no damage, the chain is broken — add the connective beat. This is what makes an episode feel whole, not choppy ("рвано").
- **Setup before payoff (the #1 hidden failure).** A character who knows / fears / can do / reacts to something the viewer never saw planted on-screen reads as a cheat. Trace every reaction, stake, and twist back to an earlier **on-screen** plant — written into that beat's actual action/dialogue; a "(plan: …)" note is intent, NOT a plant. No plant → add one.
- **A PLANT must be readable from the frame alone — a silent clue that rests on invisible state is not a plant.** The commonest way a planted clue dies: it encodes information the camera physically cannot show. *A sweating glass on the table, meant to say "someone was here minutes ago"* asks the viewer to infer **temperature** (it's cold, so it's fresh) and **absence** (it wasn't there before) — neither is on screen, so the beat plays as an unmotivated shot of a glass and the viewer asks what the scene was for. The same trap: a cup that is "still warm", a chair "she never sits in", a door "that was locked this morning". **The test:** state what the shot proves using only what a first-time viewer can see in that frame. If the sentence needs a word like *fresh, still warm, recently, again, no longer, unlike before*, the clue is invisible. Two fixes, and you need one of them:
  - **Make the change VISIBLE as a process, not a state** — not a sweating glass but condensation *running down it in a visible trickle*, a wet ring *spreading* on the paper, steam *still lifting* off the cup, ice *shifting and clinking* as it melts. Motion and change are on screen; temperature and history are not.
  - **Or give it a LINE** — one clause in `dialogue` or `VO:` ("That's not mine.", "He was here.") does the work the silent frame cannot. A wordless insert cannot carry an inference; a three-word line can.
  
  Formally this is the cold-viewer test (cinematic-scenes → Pitfalls) applied to a *plant*: the shot may be gorgeous and still prove nothing. When in doubt, plant it twice — once visibly, once in a line.
- **The silent-film test — every beat must be PLAYABLE.** Turn the sound off: could a viewer watch this scene and see what happened? *"She realizes she has been betrayed"* fails — it is a stage direction, not a scene, and it renders as a person standing still. Rewrite every beat until it names something the **camera can see a body do**. This is the single biggest cause of flat, static clips, and it is decided here, at the beat level — no amount of shot craft downstream can rescue a synopsis that contains no action.
- **Every scene carries a dynamic.** A scene where nothing happens (characters stand and look at each other, a mood interlude, "the tension builds") is not a scene. Every scene in the episode moves.

Run these as a hostile critic pass before you build the episode — see **[Story self-check](#story-self-check-the-critic-gate)** below.

### Writing a beat that can actually be filmed

The fix for a static beat is almost never "add a slap" — an episode of slaps is a soap opera. It is to give the scene an **activity** and let the emotion play against it:

> ✗ "Mara realizes he has been lying to her."
> ✓ "Mara packs his suitcase — folding each shirt flat, precisely — and somewhere in the folding she stops pressing them down and starts just dropping them in."

Same beat, same subtext, now it is a scene. Three tiers — **use the lowest one that serves the beat**:

| Tier | What it is | Where it belongs |
|---|---|---|
| **Activity** | An ordinary physical task the scene is played over: packing, clearing a table, buttoning a cuff, walking somewhere with purpose | **The default for most scenes** |
| **Event** | Something in the world irreversibly changes: someone enters, paper tears, a glass goes over, a light dies | **At least once per scene** |
| **Act** | A strong physical act: a slap, a shove, a phone smashed, a tray tipped | **The hook and the reversals only** |

**The twist needs a BODY.** A reversal carried by a spoken line alone renders as a talking head. Land the line **together with a physical act or a change of possession** — she drops the file on the table as she says it; he takes the ring back; the photo goes face-down. The line is the payload, but the body is what makes it play. (Shot craft for all of this — motion channels, energy registers, the force triad — lives in cinematic-scenes.)

## 1 — The golden 3-second hook (the first scene)

Scene 1 of any episode must land a hook inside the first beat — no slow build, no establishing throat-clear. Open on the strongest unresolved tension you have. Pick one:

- **Suspense-first** — open on the unexplained strong-conflict image. "She tears up the wedding invitation in front of every guest."
- **Status humiliation** — the lead is humiliated or wronged at the extreme. "The assistant gets a coffee thrown in her face in front of the whole office."
- **Reverse-persona tease** — the apparent underdog flashes the first hint of a hidden identity/power.
- **Lethal countdown** — a timer or threat. "Ten seconds before the door blows."

The hook is a *situation*, not exposition. Show the worst/strangest moment, then let the rest of the episode explain how we got here.

## 2 — Reversal cadence (distribute the turns)

Lay the twists across the episode by length. Treat each beat below as **one scene = one rendered clip**. A clip is either a single held take (≈6–10s) or a small 2–4-shot mini-edit (≈10–15s) — cinematic-scenes owns the cutting *inside* the clip; this skill only orders the beats:

- **~60s episode (≈6–8 scenes):** hook (scene 1) → small reversal (~scene 3) → main reversal (~scene 5) → hook-style button / open loop (final scene).
- **~90s episode (≈9–11 scenes):** hook → setup → reversal 1 → escalation → reversal 2 → payoff / release → cliffhanger into next episode.

Rules:
- **No flat stretch longer than ~2 scenes** without a turn, reveal, or escalation.
- **Escalate** — each reversal should raise the stakes over the last, not just sidestep.
- **One payoff per episode** — let the audience feel a release (the "爽点") before you re-tighten with the cliffhanger.

## 3 — The cliffhanger (the last scene)

Every episode's final scene throws a *new* unresolved beat — a reveal, a threat, an arrival, a question — so the only way to resolve the tension is the next episode. Never end on a settled state. The cliffhanger is mandatory for any multi-episode series and strongly recommended even for single episodes that might continue.

**The last scene IS the cliffhanger — one per episode.** Write its own short/punchy "title" line and a 1–2 sentence tease of what's coming, exactly as you would a hook, and keep it to **one** unresolved beat, not several competing ones — whatever surrounds shotkit (a player, a publishing tool, your own notes) is what actually wires "next episode" and displays the CTA; shotkit itself only renders the scene's clip. A title with no genuine unresolved question is just an ending, not a cliffhanger — don't let the last scene settle just because you wrote a tagline for it.

## 4 — Linear by default

**An episode is a single ordered run of scenes: hook → reversal cadence → cliffhanger. No viewer
forks, no choice buttons, no merge scenes.** One spine, one path through it — that is the only
shape this skill (and shotkit) authors. Viewer-choice branching is out of scope entirely: if a
user wants forks, that is a different tool and a different pipeline, not this one.

## Story self-check (the critic gate)

Before you turn the episode into scene files, **switch roles — stop being the author, become a hostile script editor who did NOT write this outline** (you wrote it, so it *feels* fine — that's the blind spot). Run the seven story tests against the beat list: **spine, escalation, chemistry, hook, causality, setup-plant ledger, and the silent-film test.** Evidence rules: only what's literally written in a beat is admissible — your intent and any "(plan: …)" note don't count; a bare "PASS" with no ledger is a FAIL; find at least one real problem before allowing any pass. Fix every problem, *then* build the episode — cheap now, expensive once the scenes and prompts exist.

**The silent-film test, run as a critic pass:** go beat by beat with the sound off. For each, name the **physical action the camera sees**. A beat whose only answer is an internal state ("she realizes", "he decides", "tension builds") FAILS — rewrite it around an activity. Then check the tiers across the episode: is there an **Act** anywhere other than the hook and the reversals (soap opera), and is there any scene with **no activity at all** (a static clip waiting to happen)? Every scene must name an action; a beat that names none is a FAIL, not a soft note.

The full test procedure with the plant ledger lives in **[references/story-tests.md](references/story-tests.md)** — read it when running the gate. (If your runtime can dispatch a subagent, give the critic pass to a fresh agent whose only input is the outline text.)

## Mapping structure onto shotkit scenes

shotkit has no built-in "episode" object — a project is just `bible.json` + a folder of `scenes/*.json`. An **episode** is a convention you keep yourself: an ordered group of scene ids (e.g. `s01`…`s08`, or `ep02_s01`…`ep02_s06` once there's more than one episode in the project). The ordering *is* the pacing. Build it like this:

1. **Lay the beats as a scene list.** Create one `scenes/<id>.json` per beat, in order, each with a `locationId` and a synopsis you keep in your own notes — scene 1 = the hook, the middle scenes = the reversal cadence, and the last = the cliffhanger. Insert a scene by giving it an id that sorts where you want it (or renumber neighbors); there's no separate insert/reorder operation, the file list *is* the order.
2. **Write the reversal lines as `dialogue` — but give the twist a BODY.** Land the line on a physical act: she slides the contract across the table, he sets the ring down, the photo goes face-down. Put on-camera speech in plain `dialogue` lines and narration in `VO:` segments in that same field, with `generateAudio: true`. Budget all words together at roughly two per second of `durationSec`. On a multishot clip, anchor the reversal to its action with `[shot N]`, such as `Skye: [shot 3] You signed it yourself.` Give narration its own shot without on-camera speech so the model does not lip-sync it onto the visible face.
3. **Keep it vertical and tight — and set duration from CONTENT.** Default `aspect: "9:16"` (in `bible.json`'s `style`, or per-scene), short `durationSec` per scene (6–10s held beats, 10–15s multi-shot beats), rapid cadence. **Count the happenings in the beat (~one per 3s) and size the clip to fit them** — a 15s slot holding 8s of beat is a boring clip; make it 10s. Never stretch a beat to fill a slot; the padding renders as actors standing around. Vertical framing rules (key info in the upper two-thirds, close-ups over wides) live in cinematic-scenes.
4. **Keep the run linear.** Scenes chain in order, hook to cliffhanger — no forks, no merge scenes. Viewer-choice branching is out of scope for this skill and for shotkit.
5. **Write the cliffhanger — one per episode.** The last scene's `dialogue`/`motionPrompt` throws the new unresolved beat itself (see "3 — The cliffhanger"); if your surrounding pipeline needs a separate title/teaser for a "next episode" prompt, that's data your own tooling keeps, not a shotkit field.
6. **Sweep the episode for narration/speech collisions — after every prompt is written, before generating anything.** Go scene by scene across the **whole episode** and list each scene's `dialogue` segments by shot number. A shot carrying both an on-camera line and a `VO:` segment is a defect: move the `VO:` into its own shot within that same scene. This is an episode-level pass on purpose — each scene reads fine alone, and the collision is only visible when you check the shots one by one. See cinematic-scenes → "One voice per shot" and Workflow step 5.

### Multi-episode series

A shotkit project's **bible** (`bible.json`: style, characters, locations, props with reference images) is shared across every scene file in the project, so cross-episode consistency is structural — you do not re-invent identities each episode. So for episode N>1:

- Reuse the existing bible characters/locations/props by `@mention` — same reference images, same faces (see cinematic-scenes for the reference-image rule).
- Reuse the same `style` block (don't edit `globalPreamble`/`banned` per episode) so episodes don't shift color or look.
- Start episode N's premise from episode N−1's cliffhanger, so the arc stays continuous.
- Keep episode N's scene ids distinct from episode N−1's (a naming convention, e.g. `ep02_s01`) so nothing collides in the `scenes/` folder.

## Genre engines

Vertical drama runs on a handful of engines, each with a native reversal shape and a payoff the audience is explicitly buying:

- **Revenge glow-up / 逆袭** — humiliation hook → hidden capability revealed → a named target taken down every episode.
- **Reborn / rewind / 重生** — death or ruin cold open → she wakes before it → foreknowledge weaponised against a disaster we watched happen.
- **Secret identity / billionaire / 霸总** — the disrespected nobody is the most powerful person in the room; the wait for the reveal *is* the product.
- **Contract marriage** — marry for a deal, fall in love after; the cold one falls first.
- **Substitute bride** — the overlooked stand-in out-plays the entitled original.
- **Werewolf / fated mate** — the rejected heroine is the Alpha's fated mate; the grovel is the payoff.
- **Win-back / 追妻** — the breach hook → escalating pursuit → reversal of who needs whom.

**Engines stack** — real hits braid two (reborn + revenge, billionaire + revenge). Take one as primary and graft the second's signature beats.

The full engines — hook, beat rhythm, native cliffhanger and what to avoid — live in **[references/genre-engines.md](references/genre-engines.md)**. Read it when you pick an engine.

## Pitfalls

1. **Don't write a beat that can't be filmed.** "She realizes he lied" is a stage direction; it renders as a person standing still. Every beat names an action the camera can see — usually an ordinary **activity** the emotion plays against. Run the silent-film test.
2. **Don't open with setup.** No "establishing" first scene — the hook is scene 1, beat 1.
3. **Don't let the middle go flat.** A pretty but turn-less stretch is where viewers swipe away — and "flat" is physical as well as dramatic: a turn-*ful* scene in which nobody moves is still a dead clip.
4. **Don't resolve the episode.** End on a new open loop, always.
5. **Don't answer a static beat with a slap.** Over-correcting into an Act every scene is a soap opera. Acts belong on the hook and the reversals; everywhere else, an ordinary activity carries the scene.
6. **Don't bury the twist in the bottom of the frame.** The reversal line/image sits in the upper two-thirds (vertical) — see cinematic-scenes.
7. **Don't re-create characters each episode.** Reuse the bible's reference-anchored entities so faces hold across the series.
8. **Don't do shot craft here.** Body weight, camera, environmental force, ambient — that's cinematic-scenes. This skill decides *what happens*; that one decides *how it's shot*. But "what happens" must be something physical — that part is this skill's job.
9. **Don't add a fork.** The episode is linear, full stop — viewer-choice branching is out of scope for this skill and for shotkit.
10. **Don't let the narrator turn into a character.** A `VO:` segment sharing a shot with an on-camera line renders as that character speaking the narration, lip-synced — the off-screen voice becomes direct speech. Give narration its own shot in the scene, and sweep the whole episode for it once the prompts exist.
