# shotkit

Portable cinematic prompt craft — the shot direction, reference discipline and motion/
dialogue safety rails that make a scene render as intended, in a folder that works with
any text-to-image / text-to-video generator, not one tool's API. It turns a small
project folder (a style, a cast, a set of scenes) into the finished prompt a generator's
web UI already accepts, plus an ordered list of which reference images to attach. shotkit
never talks to a generator itself — it writes text and lists files; you paste and attach.

## Install in a project — Codex and Claude Code

One command installs the same six skills for both agents, at project scope only:

```bash
python3 /absolute/path/to/shotkit/install.py "/absolute/path/to/your/project"
```

The target project must already exist. The installer copies the six folders into
`.agents/skills/` and creates relative links in `.claude/skills/`. The CLI and its
templates live inside `prompt-assembly/scripts/`; there is no separate runtime
folder, no duplicate skill files, and no dependency on the source checkout after
installation. On macOS/Linux, the relative links continue to work if you move the
project. Repeating the command skips identical files and refuses conflicting local
changes. See [INSTALL.md](INSTALL.md) for updates, migration and verification.

Start a session in the target project and invoke `$scene-from-scratch` in Codex or
`/scene-from-scratch` in Claude Code. Inspect each agent's skill menu to confirm all
six are discovered; a successful copy alone does not verify discovery.

The source retains its Claude plugin manifests for packaged plugin distribution.
The local installer does not register a plugin or copy those manifests.

## Requirements

Python 3.9 or newer. Nothing else — no `pip install`, no virtualenv, no third-party
package of any kind. The whole thing is the standard library, on purpose: a team member
should be able to clone this, run it, and never wonder what else needs installing.

## Five minutes to a first prompt

From the source repository, run `skills/prompt-assembly/scripts/shotkit.py` as below.
After installation, use `.agents/skills/prompt-assembly/scripts/shotkit.py` from the
target project root, or its absolute path when working from another directory.
The CLI, Python package and templates live together in
`skills/prompt-assembly/scripts/`.

```bash
python3 skills/prompt-assembly/scripts/shotkit.py init my-film
```

This scaffolds `my-film/` with a starter `bible.json` (style, a couple of characters, a
location, a prop) and one example scene, `scenes/s01.json`. The bible's reference image
paths point at files that don't exist yet on purpose — that's the next step, not a bug.

Open `my-film/bible.json` and `my-film/scenes/s01.json` and make them your own: your
project's visual style, your cast (with `@id`-addressable characters, locations and
props), your first scene's action. Then add the actual reference images the bible names,
under `my-film/refs/`.

If you have no images yet, create the first references with these handoffs:

```bash
python3 skills/prompt-assembly/scripts/shotkit.py --project my-film sheet hero --handoff
python3 skills/prompt-assembly/scripts/shotkit.py --project my-film sheet ally --handoff
python3 skills/prompt-assembly/scripts/shotkit.py --project my-film location warehouse --handoff
python3 skills/prompt-assembly/scripts/shotkit.py --project my-film prop case --handoff
```

Generate each image and save it at the destination shown. The starter characters
need no input photos. Add `identityRefs` or a role-labelled `refKit` only when you
actually have source images. Location and prop commands attach existing images for
consistency on later runs; ungenerated destinations are not attachment requirements.

```bash
python3 skills/prompt-assembly/scripts/shotkit.py --project my-film frame s01
```

This writes `my-film/out/scenes/s01/frame.txt` (the finished keyframe prompt — also
echoed to your terminal) and `my-film/out/scenes/s01/frame.refs.txt` (the reference
images to attach, one absolute path per line, in the order the prompt numbers them).
Paste the `.txt` into your generator's prompt box, attach every file `.refs.txt` lists
— **in that order** — and generate. Add `--handoff` to any generating command and
stdout carries one paste-ready block (the prompt, then a numbered image list in that
same order) instead of the plain echo — the two `out/` files are written either way.
The handoff also shows manual generator settings and reference save destinations.

## Rebuild after edits

From the installed project's root:

```bash
python3 .agents/skills/prompt-assembly/scripts/shotkit.py --project my-film build
```

This rebuilds all reference prompts and each scene's full motion prompt into the
existing `out/` structure. Scene JSON is authored input; `out/scenes/<id>/motion.txt`
is the assembled generator text. Frames are included when `scenePrompt` is present.
The batch uses `t2v`; use the individual motion command for other modes. Missing
reference images are reported in `out/build-report.json` and do not prevent text
assembly. A successful build is not a claim that media has been generated.

The authoring agent runs `build` after source changes. Keep character IDs stable
and use `@id` for dialogue speakers as well as shot prose, so display-name changes
resolve everywhere those tokens appear. Plot edits require the author to update
`STORY.md` and affected scene JSON first. Build does not interpret Markdown,
watch files, regenerate existing images, or remove obsolete output files.

## Scene fields and narration

All speech belongs in `dialogue`, with `generateAudio: true`:

```json
{
  "dialogue": "Alex: [shot 1] Keep the case.\nAlex: VO: [shot 2] That was the last time I saw him.",
  "generateAudio": true
}
```

Plain lines are on-camera speech; `VO:` segments are off-screen narration generated
in the same clip. The numbered anchors require matching `SHOT 1` and `SHOT 2` in
`motionPrompt`. Give narration a shot without on-camera speech. `lint` budgets all
spoken and narrated words together at roughly two words per second. Keep a named
narrator's `gender` and `voiceNote` consistent in the bible to guide their voice.
The old `voiceover` field is removed: a non-empty value raises an error explaining
how to move it to `dialogue`; empty legacy values remain readable.

`locationId` supplies the default location and its reference. An explicit
`@location#view` selects a named view. `style.globalPreamble` prefixes frame, poster,
and motion prompts. Scene `aspect` overrides `style.aspect` in frame/motion handoffs;
`durationSec` supplies motion's manual duration setting. Posters and reference images
use their fixed 9:16 composition. Set these values in your generator UI yourself.

For `motion --mode i2v --keyframe refs/opening.png --handoff`, the keyframe appears
as a separate start-frame-slot instruction. In `ref-anchored`, it is reference #1.
Relative keyframe paths use the project root; `t2v` rejects `--keyframe`.
Unknown JSON fields, invalid types, duplicate entity IDs, and unknown requested
character looks produce errors instead of silently using defaults.

Author names, descriptions, prompts and dialogue in English. Non-English letters
(including Cyrillic) are rejected with the field's path; English typography such
as curly quotes and em dashes is allowed. Filesystem paths may contain Unicode.
Entity names are required and cannot be blank. Character names use one to three
capitalized English words, with apostrophes or hyphens allowed, so dialogue speakers
can be parsed reliably (for example, `Alex Rivera` or `Mary-Jane O'Neil`).
IDs and look/view labels use only `A-Z`, `a-z`, `0-9`, `_` and `-`; use `winter-coat`,
not `winter coat`. IDs and names share a case-insensitive namespace: duplicate IDs,
duplicate names and names matching another entity's ID are errors.

Location defaults select the view labelled `primary`, falling back to the first
view only when no such label exists. Explicit `--view` labels must exist, except
that `primary` also supports this default fallback. Unknown `#look`/`#view` selectors
in scene prose warn and fall back during assembly; they also make `lint` fail.

`python3 skills/prompt-assembly/scripts/shotkit.py --project my-film lint s01` checks a scene for broken or missing
references and dialogue that won't fit its clip length, before you spend anything on a
render. `python3 skills/prompt-assembly/scripts/shotkit.py --project my-film status` prints a read-only inventory of
the whole project — every character/location/prop with a mark for whether its
reference image exists on disk, every scene with a mark for whether it already has
rendered output — without opening any of the individual files by hand.
`python3 skills/prompt-assembly/scripts/shotkit.py styles` lists the six shipped style presets (id, name, preamble,
banned) to copy into a project's `style.globalPreamble` / `style.banned` — no
`--project` needed, nothing written to disk. Run `python3 skills/prompt-assembly/scripts/shotkit.py --help` for the
full command list — `frame`, `poster`, `motion`, `sheet`, `location`, `prop` each accept
`--handoff` and write their own prompt + refs pair nested under `out/` by kind and
entity id:

```
out/scenes/<scene-id>/frame.txt            out/scenes/<scene-id>/frame.refs.txt
out/scenes/<scene-id>/poster.txt           out/scenes/<scene-id>/poster.refs.txt
out/scenes/<scene-id>/motion.txt           out/scenes/<scene-id>/motion.refs.txt
out/characters/<character-id>/<look>.sheet.txt
out/characters/<character-id>/<look>.sheet.refs.txt
out/locations/<location-id>/<view>.view.txt
out/locations/<location-id>/<view>.view.refs.txt
out/props/<prop-id>/prop.txt               out/props/<prop-id>/prop.refs.txt
```

## The six skills

- **cinematic-scenes** — grounded, photorealistic shot direction: body weight,
  environmental force, motivated camera movement, and why a clip reads flat or gets
  refused before it starts.
- **pov-scenes** — first-person/subjective-camera craft: the camera as a character's
  eyes, one continuous take, embodiment cues.
- **short-drama-structure** — vertical short-form drama structure: the hook, reversal
  cadence, per-episode cliffhangers, mapped onto an ordered scene sequence.
- **character-refs** — keeping a face, body and wardrobe stable across renders with
  role-labelled reference images and named looks, including non-human body plans.
- **prompt-assembly** — what shotkit actually emits: the fixed clause order in a frame,
  poster or motion prompt, and the CLI's file contract.
- **scene-from-scratch** — the entry point: what to do when someone asks for a scene and
  the project may not have the cast, location or props yet — the cold-start question
  pass, writing the bible, generating references before the scene, and the final
  copy-paste handoff.

## The reference-order rule

> **Attach images in exactly the order `.refs.txt` lists them.** Two commands make that
> strictly load-bearing for identity: `sheet` (built from a `refKit`) numbers its
> references by position in the prompt itself ("the third image is the GARMENT..."),
> and `motion --mode ref-anchored` declares `@Image1 is the EXACT opening frame` — get
> either of those out of order and a role really does swap onto the wrong photo.
> Everything else — `frame`, `poster`, `motion` on `t2v`/`i2v`, `location`, `prop` — binds
> identity by DESCRIPTION, not position, so reordering those doesn't swap anyone. Keep the
> order anyway: many generators weight earlier references more heavily, and a reference
> set past an engine's cap silently drops the surplus, so which images come first can
> decide which ones make the trip at all.

## Development checks

Run `python3 -m unittest discover -v` from the repository root.
GitHub Actions runs the suite on Python 3.9 and 3.14 on Linux and macOS, including
the installer, CLI, prompt snapshots and input-validation regressions.

## Not included

shotkit does not generate anything, hold an API key, or spend any money. It never calls
a generator, never talks to a network, never sees a cost. It reads your project folder
and writes two things: a finished prompt and an ordered list of file paths. Everything
after that — pasting, attaching, clicking generate — is on you and whatever generator
you've pointed it at.
