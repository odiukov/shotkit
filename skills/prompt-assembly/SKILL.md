---
name: prompt-assembly
description: |
  Explains what `shotkit` actually emits when it assembles a frame, poster or motion
  prompt — the fixed order of clauses in each, why a project's visual style must live
  in one preamble instead of being rewritten per scene, why a reference manifest and
  written wardrobe/identity prose fight rather than add together, and the CLI commands
  plus the out/*.txt + out/*.refs.txt file contract every generating command writes.
  Load when authoring or debugging any scene prompt, wiring up a new project's style,
  or figuring out why an attached reference didn't behave the way the prompt implied.
---

# Prompt assembly

`shotkit` never sends a raw prose block to a generator. Each generating command
resolves your project's JSON into a **fixed sequence of clauses**, then writes the
result to two files under `out/`. Knowing that sequence — and why it's ordered the way
it is — is what lets you predict what a generator will actually receive before you spend
a render on it.

## The frame block (`shotkit frame`)

`scenePrompt` becomes a still keyframe in this order:

1. The project's style preamble (`style.globalPreamble`), verbatim.
2. A reference-layout guard, only when at least one character or prop is `@mentioned` —
   it tells the model that an attached reference is a multi-panel sheet for identity
   only, never a layout to reproduce (otherwise a still keyframe echoes the sheet's grid
   as a split-screen).
3. `"Single cinematic keyframe. <your scenePrompt>."`
4. A lock that this is one continuous photograph, one camera angle, filling the frame
   edge to edge.
5. A lock that this is a single frozen instant — no motion blur, no before-and-after.
6. The resolved `Setting:` clause, for every `@mentioned` location.
7. The resolved `Props:` clause, for every `@mentioned` prop.
8. `"Maintain identity: <name>: <canonicalDescription>. Wearing: <tagged look text>"` —
   built only from characters actually `@mentioned` in `scenePrompt`; wardrobe text
   appears only for an explicitly tagged look (see `character-refs`).
9. The frame-safety tail: keep the frame clean of on-screen text/captions/watermarks,
   plus `Avoid: <banned>` (the project's `style.banned` unioned with the scene's own
   `banned` — a per-scene banned list is a shotkit original the tool this craft came from
   doesn't have; shotkit unions the two rather than letting one override the other).

## The poster block (`shotkit poster`)

Same shape, with three swaps:

- The header line (step 3) reads `"Theatrical movie poster key art, vertical 9:16
  portrait composition. <scenePrompt>."` instead of "Single cinematic keyframe."
- The lock right after it (step 4) reads "A single polished poster image with a clear
  focal hierarchy and dramatic cinematic lighting" instead of the frame's
  one-continuous-image-edge-to-edge lock.
- Step 5 (the frozen-instant lock, in the frame block) is replaced by a composition
  clause naming the exact top/bottom percentage band a vertical poster's crop will keep
  on screen (from the scene's `posterFocusY`, or a sensible default) — a poster is
  composed for a crop, not a full frame, so the subject has to land inside the surviving
  band on purpose.

Carrying the frame's continuous-image lock into a poster prompt produces a sentence
`shotkit` never actually emits for a poster — the two headers lead into two different
follow-up locks, not the same one.

## The motion block (`shotkit motion`)

`motionPrompt` becomes a video prompt in this exact order — nothing here is
interchangeable:

1. `"Maintain identity: …"` — the same identity clause as the frame block, built from
   every character `@mentioned` in `motionPrompt`.
2. Your authored `motionPrompt` text.
3. A loop clause, only when the scene's `loop` flag is set (locks the camera and pins
   first/last frame for a seamless repeat).
4. The baked-speech clauses, built from `dialogue` — an on-camera line clause for plain
   `Name: words` segments, a narration clause for `VO:`-prefixed segments — only when
   `generateAudio` is true. See `references/motion-dialogue.md`.
5. **Exactly one** mode clause, chosen by `--mode`:
   - `t2v` — no clause added; there's no seed frame or reference-#1 anchor to declare.
   - `i2v` — "animate only what is already visible in this frame; introduce no new
     people, objects, vehicles or text."
   - `ref-anchored` — "reference #1 is the EXACT opening frame: reproduce it as frame 0
     … then animate onward from it."
6. An audio-discipline tail (no music/score/singing), again only when `generateAudio`
   is true.
7. Every `@mention` is stripped to its plain display name for the final text sent to
   the generator (the reference images resolved from those same mentions are what's
   listed in `out/<stem>.refs.txt`).

See `references/engines.md` for how to choose between the three modes for a given
generator.

## Never author a fresh style per scene

A project's look lives in exactly **one** place: `style.globalPreamble`. Every frame,
poster and motion prompt reproduces it verbatim, as the very first clause. Authoring a
fresh camera/film-stock line per scene, instead of reusing this one, is the single most
common way a project's visual identity drifts scene to scene.

Six style presets ship as starting points to copy into `style.globalPreamble` and
`style.banned` rather than write from scratch: **Romance drama (photoreal)**,
**Cinematic 35mm**, **Hand-painted 2D gouache storybook**, **Anime cel**, **Pixar-style
3D**, **Comic ink**.

The style preamble goes **first**, ahead of everything else in every prompt, because the
opening tokens of a prompt dominate an image model's read — state the medium before any
layout or scene instruction has a chance to bias it toward a different one.

## Two sources for one trait is a coin toss

When a character's reference manifest (a `refKit` — see `character-refs`) is attached
to a render, the written identity and wardrobe prose for that character is **dropped
entirely**, not reworded or merged with it. Two descriptions of the same trait — one in
pixels, one in words — do not add together; the model treats them as contradictory and
picks one, unpredictably. Recording a face's shape in prose while also attaching a face
reference photo is not "extra emphasis" — it is a coin toss between the reference and
the sentence, and the sentence can win. Once a manifest exists for a trait, that
manifest is the only source for it; put any nuance the prose used to carry into the
manifest's own per-image notes instead.

## The CLI commands

Every command is invoked as `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" <command>` from
inside a project directory (a directory holding `bible.json` and `scenes/`).

- `init <dir>` — scaffold a new project from the template.
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" init my-project`
- `frame <scene>` — render a scene's opening keyframe prompt.
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" frame s01`
- `poster <scene>` — render a scene's poster/key-art prompt.
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" poster s01`
- `motion <scene> --mode i2v|t2v|ref-anchored [--keyframe PATH]` — render a scene's
  motion prompt (`--mode` is required; `ref-anchored` also requires `--keyframe`).
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" motion s01 --mode t2v`
- `sheet <character> [--look LABEL]` — render a character reference-sheet prompt
  (`--look` defaults to `primary`).
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" sheet hero --look primary`
- `location <location> [--view LABEL]` — render a location-view prompt (no `--view`
  renders the primary view).
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" location warehouse --view night`
- `prop <prop>` — render a prop hero-shot prompt.
  `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" prop case`
- `lint <scene>` — check a scene for broken or missing references, music/singing words,
  dialogue/voiceover that won't fit the clip, and `[shot N]` anchors pointing at shots
  the motion prompt never declares. Writes nothing to `out/`; exits 1 if it found
  anything, 0 if clean.

## The `out/*.txt` + `out/*.refs.txt` contract

Every generating command writes exactly two files to `out/`, named from the command and
its target (`s01.frame.txt` / `s01.frame.refs.txt`, `hero.primary.sheet.txt` /
`hero.primary.sheet.refs.txt`, and so on):

- `out/<stem>.txt` — the finished prompt text, exactly as it will be sent to a
  generator, no trailing newline added.
- `out/<stem>.refs.txt` — the reference image paths this render resolved, one absolute
  path per line, in the exact order the prompt's own manifest or `@mention` resolution
  numbered them.

**Attach the images to your generator in that file's order.** Any ordinal language in
the prompt — "the third image is the GARMENT," a character's turnaround sheet, a
location's stored views — was computed from this list's order, not from the order the
images happen to sit in your folder or your upload dialog. Reorder the attachments and
every image after the change is mislabelled, with no error from anything: the generator
has no way to know your attachment order doesn't match the prompt it was given.
