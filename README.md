# shotkit

Portable cinematic prompt craft — the shot direction, reference discipline and motion/
dialogue safety rails that make a scene render as intended, in a folder that works with
any text-to-image / text-to-video generator, not one tool's API. It turns a small
project folder (a style, a cast, a set of scenes) into the finished prompt a generator's
web UI already accepts, plus an ordered list of which reference images to attach. shotkit
never talks to a generator itself — it writes text and lists files; you paste and attach.

## Install — three ways

Pick whichever matches how you work. All three end up at the same place: five Claude
Code skills plus a `shotkit` CLI, available next session.

**1. Copy the folder.** Drop this whole directory at `~/.claude/skills/shotkit/`. Claude
Code auto-loads anything under `~/.claude/skills/` as a plugin — no install step, no
restart beyond starting a new session.

```bash
cp -R shotkit ~/.claude/skills/shotkit
```

**2. Install from a local marketplace.** Registers this folder as a plugin marketplace,
then installs the one plugin in it:

```bash
claude plugin marketplace add ./shotkit
claude plugin install shotkit@shotkit
```

**3. Ship it with a repo.** Same two commands, scoped to the project instead of your
user config — this writes both the marketplace and the install into `.claude/settings.json`
at the repo root. Commit that file and everyone who opens the repo in Claude Code gets the
plugin with no per-person install step:

```bash
claude plugin marketplace add ./shotkit --scope project
claude plugin install shotkit@shotkit --scope project
git add .claude/settings.json
git commit -m "chore: add shotkit plugin"
```

Verify any of the three with `claude plugin details shotkit` — it should list five
skills (`cinematic-scenes`, `pov-scenes`, `short-drama-structure`, `character-refs`,
`prompt-assembly`). Fewer than five means something didn't load; re-check the copy.

## Requirements

Python 3.9 or newer. Nothing else — no `pip install`, no virtualenv, no third-party
package of any kind. The whole thing is the standard library, on purpose: a team member
should be able to clone this, run it, and never wonder what else needs installing.

## Five minutes to a first prompt

From inside this folder (adjust the path to `shotkit.py` if you're running from
elsewhere):

```bash
python3 shotkit.py init my-film
```

This scaffolds `my-film/` with a starter `bible.json` (style, a couple of characters, a
location, a prop) and one example scene, `scenes/s01.json`. The bible's reference image
paths point at files that don't exist yet on purpose — that's the next step, not a bug.

Open `my-film/bible.json` and `my-film/scenes/s01.json` and make them your own: your
project's visual style, your cast (with `@id`-addressable characters, locations and
props), your first scene's action. Then add the actual reference images the bible names,
under `my-film/refs/`.

```bash
python3 shotkit.py --project my-film frame s01
```

This writes `my-film/out/s01.frame.txt` (the finished keyframe prompt — also echoed to
your terminal) and `my-film/out/s01.frame.refs.txt` (the reference images to attach, one
absolute path per line, in the order the prompt numbers them). Paste the `.txt` into your
generator's prompt box, attach every file `.refs.txt` lists — **in that order** — and
generate.

`python3 shotkit.py --project my-film lint s01` checks a scene for broken or missing
references and dialogue that won't fit its clip length, before you spend anything on a
render. Run `python3 shotkit.py --help` for the full command list — `frame`, `poster`,
`motion`, `sheet`, `location`, `prop`, `lint` each write their own `out/<stem>.txt` +
`out/<stem>.refs.txt` pair.

## The five skills

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

## The reference-order rule

> **Attach images in exactly the order `.refs.txt` lists them.** The prompt shotkit
> writes numbers its references ("the third image is the GARMENT...") based on that
> same order. Attach them out of order — or add, drop, or re-sort one along the way —
> and every image after the change is mislabelled. The generator will not complain;
> it will simply act on the wrong image for a given role, silently.

## Not included

shotkit does not generate anything, hold an API key, or spend any money. It never calls
a generator, never talks to a network, never sees a cost. It reads your project folder
and writes two things: a finished prompt and an ordered list of file paths. Everything
after that — pasting, attaching, clicking generate — is on you and whatever generator
you've pointed it at.
