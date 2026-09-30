---
name: scene-from-scratch
description: |
  The entry point for a scene request when the project may not exist yet, or exists but
  doesn't have the cast, location or props the request implies. Covers creating the named
  project folder, the cold-start question pass (what's missing, ask only what's needed),
  writing the bible, generating references before the scene, resuming a project in a new
  session, and the final copy-paste handoff. Load whenever the user asks for a scene and
  you haven't first confirmed the project folder exists with the entities it needs, or
  when they say "we're working on project X" / name an existing project to continue.
---

# Starting a scene from scratch

This is the front door. `cinematic-scenes` teaches the shot craft, `character-refs`
teaches reference roles and looks, `prompt-assembly` teaches what the CLI actually
emits — all three assume the project folder exists and the bible already names the
people, places and things in the scene. This skill covers everything before that point:
turning a scene request into a project folder, a filled-in bible, and a generated
reference set — and everything after the shot is authored: handing the user one prompt
and an ordered image list they can act on immediately.

## Step 0 — the project folder, named and placed

Every project is a folder: `bible.json` + `scenes/*.json` + `refs/*.png`, with `out/`
added as renders happen. `shotkit init <dir>` (verified against `shotkit/cli.py::cmd_init`)
scaffolds one from the template — it refuses only if `<dir>` already exists and is
non-empty, and creates it otherwise.

- **Derive a folder name from the story or scene the user asked for**, in kebab-case —
  not a generic placeholder. "Mira hands Vale a folder in a bank lobby" → something like
  `mira-vale-bank-lobby`, not `my-film` or `project1`.
- **If the user names a location for the project, use theirs** instead of picking one.
- Run `shotkit init <name>` to create it, then **say the folder's absolute path back to
  the user in the same message, explicitly** — e.g. "Project created at
  `/Users/alex/films/mira-vale-bank-lobby`." This is the path they'll need to name to
  resume later; a path only mentioned in passing is one nobody can recall a week on.
- Everything about this story lives under that one folder from here on —
  `bible.json`, `scenes/`, `refs/`, `out/` — never scattered elsewhere.
- Immediately after `init`, write `STORY.md` at the project root (see below) from the
  user's request — this is the first artifact in the folder, before the bible is filled
  in.

## Resuming a project

When the user says "we're working on project X" (or otherwise names an existing
project) in a fresh session, pick it back up — **do not start a new project for the
same story.** A second folder for one story splits the cast across two bibles, and
references stop matching the scenes that need them.

1. **Get the path.** The user gives it, or you ask for it. Do not guess at a location.
2. **Confirm it's a shotkit project** — a readable `bible.json` at that path — before
   writing anything into it. If it isn't, say so; don't silently start a fresh one at
   the same path.
3. **Read `STORY.md` first, before running `status`.** `STORY.md` says what this story
   is and where it was going — the premise, the cast's reasons for mattering, the scene
   order, and what was already decided or deliberately rejected (see below). Reading
   only the files on disk (the next step) gives you inventory with no direction, and a
   later session re-litigates choices the user already made; reading only `STORY.md`
   risks acting on a note that has drifted from what's actually on disk. Read both, in
   that order.
4. **Then run `shotkit status`** (verified against `shotkit/cli.py::cmd_status`) —
   no scene argument, honors `--project`. It prints a read-only inventory: every
   character/location/prop with a mark for whether its reference image exists on disk,
   and every scene with a mark for whether `out/` already holds its rendered artifacts.
   Report this inventory back to the user before doing anything else.
5. **If `STORY.md` and what's on disk disagree** — it claims a scene `scenes/` doesn't
   hold, or a character with no entry in `bible.json` — **say so to the user rather than
   silently trusting either one.** A stale note quietly believed is worse than no note.
6. **Continue in the same files.** New scenes go in the same `scenes/`, new cast and
   locations go into the same `bible.json`, new references go into the same `refs/`.
   Update `STORY.md` as you go (see below) — never leave the resumed project with a
   `STORY.md` that still describes the state from before this session.

## `STORY.md` — the intent a bible and scene files can't hold

`bible.json` and `scenes/*.json` record entities and prompts, not intent: what the story
is, what happens in what order, what was already decided and why. Without a record of
that, a fresh session re-invents direction instead of continuing it. So every project
also carries a `STORY.md` at its root, a plain Markdown file **you write and maintain**
— nothing in `shotkit` itself generates or reads it. It holds:

- **Premise** — a few lines on what the story is.
- **Cast** — one line per character on why they matter (their role in the story, their
  relationships, what they want). **Not their appearance** — that's `canonicalDescription`'s
  job in `bible.json`; duplicating it here means two copies that can drift, and then
  nothing tells you which one the renders actually used.
- **Scenes in order** — each scene's id, a one-line beat, and its state: *authored*
  (prompts written), *references ready* (cast/location/props for it have images on
  disk), or *rendered* (`shotkit motion`/`frame` has run for it).
- **Decisions** — what was settled and what was deliberately rejected, with the reason.
  This is what stops a later session from re-opening a question the user already
  closed.

Rules for keeping it:

- Write it **during the cold start**, from the user's own request — not a placeholder,
  the actual premise and cast as first described.
- **Update it whenever a scene or cast member is added, or a decision is made** — in the
  same turn, not batched for later. A note written at the end of a session is a note
  that was never actually written during the work it was supposed to track.
- On resume, it is the **first** thing you read (see above) — before `shotkit status`.

## The cold-start check

Read the user's scene request and list every character, location and prop it implies.
Check each name against `bible.json` (or, for a brand-new project, against nothing —
everything is missing). **Name what's missing before asking anything** — tell the user
plainly which of the implied cast/location/props already exist and which don't, so the
questions that follow are visibly about filling a specific, named gap, not a generic
intake form.

## The question protocol — few, specific, answerable

Ask everything you need in **one message**, not one question at a time:

- **Character** — two pieces of information, kept separate:
  1. **Identity**: age, face, build, hair. This becomes `canonicalDescription` — the person themselves, unchanged across scenes.
  2. **Default look** (wardrobe/state): what they're wearing when we first meet them. This becomes the `primary` entry in the character's `looks[]` array.
  
  **Why split them?** Folding a garment into identity is the single most common way a project loses face consistency across renders. A `canonicalDescription` is read at every render regardless of what the character is wearing that scene — if wardrobe is baked there, you've locked the character's face to one outfit and lost the ability for costume changes or scene variations. `character-refs` explains why a reference image, not prose, is what holds a face steady; the wardrobe lives in a separate `look` so a character can be recast in different costumes and still hold the same face.
- **Location** — what kind of place, and the light.
- **Prop** — what the object is.

**If the user already described someone/someplace/something in their request, use
that** — don't re-ask for a detail they already gave you.

## Writing the bible

Write `bible.json` and `scenes/<id>.json` yourself — `shotkit` has no authoring command
for either file; they're plain JSON you create directly (field shapes verified against
`shotkit/project.py`'s wire-format loaders — `_character_from_json`, `_location_from_json`,
`_prop_from_json`, `_scene_from_json`):

- Character: `id`, `name`, `canonicalDescription` (identity only, from the answers
  above), a `looks` entry labelled `"primary"` with a `description` (wardrobe/state) and
  a `refImage` path under `refs/` **that does not exist yet** — that's what the
  reference pass below fills in.
- Location: `id`, `name`, `canonicalDescription`, `lightingProfile`, a `views` entry
  labelled `"primary"` with a `uri` under `refs/` that doesn't exist yet.
- Prop: `id`, `name`, `canonicalDescription`, a `uri` under `refs/` that doesn't exist
  yet.
- Scene: `id`, `locationId`, plus the prompt fields `cinematic-scenes` teaches you to
  fill (`motionPrompt` primarily, `dialogue`/`voiceover`/`generateAudio`/`durationSec`).

Update `STORY.md`'s Cast / Scenes-in-order sections as you add each entry.

## The reference pass — before the scene

The scene cannot be assembled until every entity it `@mentions` has a reference image on
disk — `shotkit lint` will report each one missing, and a `.refs.txt` that lists a path
resolving to nothing is silently useless to a generator. So before authoring the scene:

For each **new** character:
```
shotkit --project <dir> sheet <character-id> --handoff
```
For the **location**:
```
shotkit --project <dir> location <location-id> --handoff
```
For each **prop**:
```
shotkit --project <dir> prop <prop-id> --handoff
```
(all three flags and commands verified against `shotkit/cli.py`'s subparsers and
`_render_paths`/`_write_render`/`_handoff_block`). Each `--handoff` prints one block: the
prompt to paste into an image model, and — for `sheet` specifically — a numbered
reference list if the character already has other reference images configured (a new
character's first sheet typically has none yet, so the list may say so plainly rather
than show an empty heading).

**Hand the user every block, tell them where to save each result** (the look's/view's/
prop's `refImage`/`uri` path under `refs/`, exactly as written into `bible.json` above),
**and stop.** Do not attempt to author or render the scene yet — update `STORY.md` to
note these entities are now "references ready" once the user confirms the images are
saved, then continue.

## The scene pass

Once every `@mentioned` entity has its reference image in place:

1. Author `motionPrompt` and `dialogue` following `cinematic-scenes`'s recipe — the
   upfront structure header (shot count + duration + aspect), the timecoded
   `SHOT N [start–end]` lines, `@mention` for every character/location/prop present,
   `[shot N]` anchors on any `dialogue`/`VO:` segment, and the narration sweep so no
   single shot carries both a spoken line and a `VO:` segment.
2. Run `shotkit --project <dir> lint <scene-id>` and fix anything it reports — it
   checks for unresolved/missing references, music/singing words, dialogue or
   voiceover that won't fit the clip, and `[shot N]` anchors pointing at shots the
   motion prompt never declares.
3. Run `shotkit --project <dir> motion <scene-id> --mode t2v --handoff` — `t2v` is the
   default mode for every scene per `cinematic-scenes` (frees the camera, needs no seed
   frame); add `--handoff` for the paste-ready block.
4. Update `STORY.md`'s scene state to *authored* once the prompt is written, and to
   *rendered* once the user confirms they generated it.

## What the user gets at the end

Exactly what `cinematic-scenes`'s workflow was missing a clean handoff for: **one prompt
to paste into their generator, and a numbered list of images to attach, in that exact
order.** That is the `--handoff` block from the `motion` command above — nothing further
to open, reconcile or re-order by hand.
