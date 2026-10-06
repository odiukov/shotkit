---
name: scene-from-scratch
description: |
  Start or resume a Shotkit story, episode or scene project, including requests phrased
  as "make a story" within the filmmaking workflow. Fill the cast, locations and props,
  and automatically create the populated bible, draft scene files and reference-generation
  prompts as well as the story outline. Covers creating the named
  project folder, the cold-start question pass (what's missing, ask only what's needed),
  writing the bible, generating references before the scene, resuming a project in a new
  session, and the final copy-paste handoff. Load for story/episode/scene creation in a Shotkit project, missing character or
  reference prompts, or a named project to continue. Explicit prose-only brainstorming
  stays prose-only; do not turn unrelated fiction writing into a production project.
---

# Starting a scene from scratch

This is the front door. `cinematic-scenes` teaches the shot craft, `character-refs`
teaches reference roles and looks, `prompt-assembly` teaches what the CLI actually
emits — all three assume the project folder exists and the bible already names the
people, places and things in the scene. This skill covers everything before that point:
turning a story or scene request into a project folder, a filled-in bible, draft
scenes, and reference-generation prompts — and everything after the shot is authored: handing the user one prompt
and an ordered image list they can act on immediately.

Write project artifacts in English: entity names, descriptions, story prose,
prompts and dialogue. Do not author Cyrillic text. Follow `prompt-assembly`'s
English name and ID rules; the CLI rejects non-English letters in project JSON.

## Story requests still need a production handoff

In a Shotkit filmmaking workflow, "create a story" can describe the whole project,
not just its synopsis. Use `short-drama-structure` for episode beats when appropriate,
then continue this workflow through the bible, draft scene files and reference-prompt pass. `STORY.md`
and an empty `bible.json` are an outline, not a completed production starter.
Honor an explicit request for ideas, a synopsis only, or a pause before production.
Do not ask whether to create the skeleton after the user has requested the story
project. Do not add an approval gate merely because story or character designs are
first drafts. Unspecified visual details are draft design choices, not blockers.

For a production starter, finish the following before handing work back:

- Write the story and record the actual intended scope in `STORY.md`.
- Populate `bible.json` with the cast, locations and recurring props needed for that
  scope. Keep identity separate from wardrobe and give references save destinations.
- Write valid `scenes/<id>.json` drafts for the opening sequence or episode being
  developed. Use actual beats, entity IDs and location IDs from this story, with
  playable action and appropriately sized dialogue; do not leave `scenes/` empty
  or retain the unrelated `init` sample. Read `cinematic-scenes` for shot craft.
  Record the draft scope and provisional format in `STORY.md`; do not invent every
  future episode just to fill folders.
- Resolve the bundled CLI using `prompt-assembly`, then **execute**
  `python3 "$SHOTKIT_CLI" --project <dir> build`. It assembles character, location,
  prop and scene prompts in one pass. A list of commands to run later is not output.
  It writes full `out/scenes/<id>/motion.txt` and `motion.refs.txt` even when images
  are missing. The authored `motionPrompt` in JSON is only an input, not the final
  assembled generator prompt.
- Verify the resulting `out/characters/<id>/primary.sheet.txt`,
  `out/locations/<id>/<view>.view.txt` and `out/props/<id>/prop.txt` files and their
  paired reference lists. Also verify the full `out/scenes/<id>/motion.txt` and
  `motion.refs.txt` for every authored scene; scene JSON alone is insufficient.
  Read `out/build-report.json` and link to the actual files in the handoff.
- State what is still pending: generated reference images, video generation or
  later episodes outside the current scope. Do not label prompts as images.

Missing reference images do **not** block this text-prompt pass. With no supplied
photos, prepare the first reference prompts from descriptions. For unspecified
appearance, clothing, lighting and ordinary props, propose coherent draft choices
that fit the story and mark them as provisional in `STORY.md`; do not stop to ask
permission for each creative choice. Preserve any details the user already gave.
Ask only when a missing answer materially changes the requested story or the user
explicitly reserves a choice. If the user says they will supply designs or photos,
honor that dependency while completing independent parts of the skeleton.

Before finishing, check the filesystem, not just the prose: a production skeleton
needs populated entity arrays, actual story-specific scene JSON, and nonempty
reference prompt files for every character/location/prop included in its scope.
Do not claim completion while those are absent. Report any concrete generation
error instead of substituting empty folders or a command list.

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
  `<resolved-project-root>/mira-vale-bank-lobby`." This is the path they'll need to name to
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
  disk), or *prompts assembled* (`shotkit motion`/`frame` has run for it).
  Keep *images/video generated* separate: those require actual media files.
  Also record *reference prompts prepared* when the `sheet`/`location`/`prop` text
  files exist but their images have not been generated yet.
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

The automatic skeleton above is the default for a Shotkit story request. Use the
questions below only for choices the user wants to supply or ambiguities that
materially change the story. They are not a mandatory intake form or a prerequisite
for drafting. If a question is needed, ask the missing details in **one message**:

- **Character** — three pieces of information, kept separate:
  1. **Identity**: age, face, build, hair. This becomes `canonicalDescription` — the person themselves, unchanged across scenes.
  2. **Default look** (wardrobe/state): what they're wearing when we first meet them. This becomes the `primary` entry in the character's `looks[]` array.
  3. **Reference photos**: do they already have any images of this person's face? This is the fork in how the sheet gets generated, so use any supplied photos here; if none were supplied, start with a text-only draft. If supplied, the photos go under `refs/` and their paths into the character's `identityRefs` list in `bible.json` — the sheet is then generated to MATCH that face, not invented from prose. If no, `identityRefs` stays empty and the sheet is generated from the description alone (see "The reference pass" below for what each route produces). Neither route blocks creating the initial prompt files.

  If what they have is several separate photos — one for the face, one for a garment, a separate body reference — that's a stronger mechanism than one flat photo (`refKit`, role-labelled references); don't set that up here, just note it and point them at `character-refs`, which owns it.

  **Why split identity and look?** Folding a garment into identity is the single most common way a project loses face consistency across renders. A `canonicalDescription` is read at every render regardless of what the character is wearing that scene — if wardrobe is baked there, you've locked the character's face to one outfit and lost the ability for costume changes or scene variations. `character-refs` explains why a reference image, not prose, is what holds a face steady; the wardrobe lives in a separate `look` so a character can be recast in different costumes and still hold the same face.
- **Location** — what kind of place, and the light.
- **Prop** — what the object is.

**If the user already described someone/someplace/something in their request, use
that** — don't re-ask for a detail they already gave you.

**And split what they gave you along the same line.** A request almost always arrives with
the wardrobe attached — *"a woman in a charcoal coat hands him a folder"*. Take the coat as
the `primary` look and keep `canonicalDescription` to the person, exactly as if you had
asked the two questions separately. Copying their sentence whole into `canonicalDescription`
is the easy mistake here, because it is the sentence you were handed: it reads as obedience
and silently locks that coat onto the character in every scene they ever appear in. If what
they gave you is all wardrobe and no face, propose a separate draft identity unless
the user has reserved that choice.

## Writing the bible

Write `bible.json` and `scenes/<id>.json` yourself — `shotkit` has no authoring command
for either file; they're plain JSON you create directly (field shapes verified against
`shotkit/project.py`'s wire-format loaders — `_character_from_json`, `_location_from_json`,
`_prop_from_json`, `_scene_from_json`):

- Character: `id`, `name`, `canonicalDescription` (identity only, from the answers
  above), a `looks` entry labelled `"primary"` with a `description` (wardrobe/state) and
  a `refImage` path under `refs/` **that does not exist yet** — that's what the
  reference pass below fills in. If the user has existing photos of this person, save
  them under `refs/` too and list their paths in `identityRefs`; otherwise leave
  `identityRefs` empty (or omit it) — see "The reference pass" below for what each
  choice produces.
- Location: `id`, `name`, `canonicalDescription`, `lightingProfile`, a `views` entry
  labelled `"primary"` with a `uri` under `refs/` that doesn't exist yet.
- Prop: `id`, `name`, `canonicalDescription`, a `uri` under `refs/` that doesn't exist
  yet.
- Scene: `id`, `locationId`, plus the prompt fields `cinematic-scenes` teaches you to
  fill (`motionPrompt` primarily, `dialogue`/`generateAudio`/`durationSec`). All
  narration belongs in `dialogue` as `VO:` or `Name: VO:` with `generateAudio: true`.

Update `STORY.md`'s Cast / Scenes-in-order sections as you add each entry.

## The reference pass — before the scene

A character's sheet runs one of two routes, and both end at the same place: a saved
image file that the look's `refImage` points at, which every scene from then on attaches.

- **Text-only** (no `identityRefs` on this character) — the sheet is generated from
  `canonicalDescription` and the look's `description` alone, because prose is all there
  is to generate it from. Its output is not a reference for something else — it IS the
  reference: save the result to the `refImage` path already named in `bible.json`, and
  every later scene that `@mentions` this character attaches that file. An empty
  "ATTACH THESE IMAGES" list on this route is the expected outcome, not a sign
  something is missing — `shotkit sheet --handoff` says so directly and names the exact
  path to save the result to (or says plainly that no path is configured yet, if the
  bible entry doesn't have one, rather than invent one).
- **Reference-led** (the character carries `identityRefs` — photos the user already gave
  you) — the sheet prompt reads differently: it instructs the image model to match the
  attached photo's face, skin, hair and build exactly rather than inventing one from
  prose, and those photos appear in the handoff's numbered attach list. Role-labelled
  references (`refKit`: separate face/body/hair/garment photos) are a stronger version
  of the same idea — see `character-refs` for how those are built and attached.

Locations and props start from text when their configured images do not yet exist.
`location`/`prop --handoff` names the destination to save the generated reference to.
On later runs, existing location views or the existing prop image are attached for
consistency. Configured but not yet generated images are destinations, not inputs.

A generation-ready scene handoff needs the mentioned reference images on disk.
Missing images do not block full text assembly: `build` writes the same complete
motion prompt and ordered reference list now, with missing files in its report.
Mark the output "prompt assembled; images pending" until those paths exist. The
commands below are useful for individual references; `build` runs the whole pass.

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
prompt to paste into an image model, and a numbered reference list in attach order
whenever references exist — for the text-only route described above, it names the save
path instead (see above).

**Hand the user every block, tell them where to save each result** (the look's/view's/
prop's `refImage`/`uri` path under `refs/`, exactly as written into `bible.json` above —
the same path the handoff block itself now names when the list comes back empty),
**and record "reference prompts prepared; images pending" in `STORY.md`.**
Never stop earlier with only the story outline and an empty bible. If the requested
scope includes scene drafts, write those too and label missing image dependencies;
do not present an incomplete reference list as a ready-to-generate scene handoff.
Mark entities "references ready" only after verifying the actual image files, then
verify the image-dependent handoff is ready. Full text must already be assembled;
do not create placeholder images to pass lint.

## The scene pass

Write scene drafts during skeleton creation; generated images are not a dependency
for authoring text. Once the references exist, revise those same drafts as needed
and reassemble the scene handoff. Assemble full text now with `build`; do not wait
for images to create `out/scenes`. Do not create a second set of scenes.

1. Author `motionPrompt` and `dialogue` following `cinematic-scenes`'s recipe — the
   upfront structure header (shot count + duration + aspect), the timecoded
   `SHOT N [start–end]` lines, `@mention` for every character/location/prop present,
   `[shot N]` anchors on any `dialogue`/`VO:` segment, and the narration sweep so no
   single shot carries both a spoken line and a `VO:` segment.
2. Run `shotkit --project <dir> lint <scene-id>` and fix authoring errors. During
   skeleton creation, report genuinely missing image files as pending dependencies;
   do not fake them or wait to save the draft. Before the final handoff, resolve
   those missing references too. The command checks for unresolved/missing references, music/singing words, dialogue or
   `VO:` narration that won't fit the clip together with spoken lines, and `[shot N]` anchors pointing at shots the
   motion prompt never declares.
3. Run `shotkit --project <dir> build` after authoring or editing the scenes.
   For one scene's paste-ready stdout, run
   `shotkit --project <dir> motion <scene-id> --mode t2v --handoff` — `t2v` is the
   default mode for every scene per `cinematic-scenes` (frees the camera, needs no seed
   frame); add `--handoff` for the paste-ready block.
4. Update `STORY.md`'s scene state to *authored* once the prompt is written, and to
   *rendered* once the user confirms they generated it.

## Revising a story or character

Treat `STORY.md`, `bible.json` and `scenes/*.json` as authored sources, and `out/` as
compiled text. After a requested change, complete the affected source edits and
run `build` in the same turn, without waiting for a separate rebuild request.

- Keep entity IDs stable. Change display names and appearance in the bible; use
  `@id` in scene prose and dialogue speaker labels (`@mark: [shot 2] ...`) so the
  compiler resolves the current display name. Existing plain-name dialogue is
  supported, but the author must update those labels when renaming a character.
- A change of motivation, relationship or plot requires authoring: read the story
  and affected scenes, rewrite their action/dialogue and downstream consequences,
  and update the bible where relevant. `build` assembles text; it cannot infer new
  scenes from a change made only in `STORY.md`.
- Avoid duplicating canonical appearance in scene prose. If a scene contains an old
  name or appearance as plain text, update it deliberately; do not blindly replace
  text inside spoken dialogue or unrelated entities.
- Run `build`, read its report, and link the rebuilt motion files. It rebuilds all
  current scenes, so dependent prompts are not skipped. This is a workflow step
  performed by the agent, not a background file watcher.
- Changing text does not repaint reference images or videos. After a visual design
  change, identify the existing images needing regeneration and affected scenes;
  never imply the existing media has automatically adopted the new appearance.

## What the user gets at the end

For the initial story skeleton: link to `STORY.md`, `bible.json`, the draft scene
files, assembled `out/scenes/<id>/motion.txt` files, and character/location/prop prompts. State that reference
images and final video generation are still pending. An initial skeleton does not
require the user to generate images during the same turn.

For a final scene handoff with references ready: exactly what `cinematic-scenes`'s workflow was missing a clean handoff for: **one prompt
to paste into their generator, and a numbered list of images to attach, in that exact
order.** That is the `--handoff` block from the `motion` command above — nothing further
to open, reconcile or re-order by hand.
