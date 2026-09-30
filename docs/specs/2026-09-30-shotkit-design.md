# shotkit — portable cinematic prompt craft

**Date:** 2026-09-30
**Status:** design approved, ready for implementation planning

## Purpose

Take the prompt craft that today only works inside the Short Drama tool and ship it as a
standalone folder that works with any text-to-image / text-to-video generator — Midjourney,
Kling, Runway, Seedream, nano-banana, Veo, whatever comes next.

Two things have to survive the extraction:

1. **References stay references.** A role-labelled reference set (face / body / hair /
   outfit / object / whole) still reaches the model as a numbered manifest whose ordinals
   match the order the images are attached in.
2. **The prompt stays complete.** What shotkit emits is the same full string the tool sends
   to its generator — preamble, reference-layout clause, scene, setting, props, identity,
   safety tail — not a sketch the operator finishes by hand.

Nothing inside the `shortdrama` repo changes. shotkit reads from it once, during porting,
and then stands alone.

## Non-goals

- No generation. shotkit emits prompts and an ordered file list; the operator (or their own
  script) feeds them to whatever generator they use.
- No asset store, no cache, no cost accounting, no provider selection, no paid-tool gating.
- No story branching. Forks, `link_branch`, `mergeSceneId` and `references/branching.md`
  are player features with nothing to attach to outside the tool; they are not ported.
- No MCP server, no HTTP API, no database.

## Delivery: a Claude Code plugin that is also just a folder

```
shotkit/
  .claude-plugin/
    plugin.json                    # name, version, description
    marketplace.json               # makes `marketplace add ./shotkit` work
  skills/
    cinematic-scenes/
      SKILL.md
      references/
        scene-patterns.md
        failure-modes.md
        frame-guards.md            # NEW — lifted from director.system.md
    pov-scenes/SKILL.md
    short-drama-structure/
      SKILL.md
      references/
        genre-engines.md
        story-tests.md
    character-refs/
      SKILL.md
      references/
        ref-roles.md
        body-plans.md
    prompt-assembly/
      SKILL.md
      references/
        motion-dialogue.md
        engines.md
  shotkit/                         # pure Python, standard library only
    __init__.py
    mentions.py
    ref_kit.py
    guards.py
    scene.py
    turnaround.py
    style.py
    project.py
    cli.py
  shotkit.py                       # entrypoint
  template/                        # starter project
    bible.json
    scenes/s01.json
    refs/.gitkeep
  tests/
    golden/                        # byte-exact expected output, generated from the tool
    test_*.py                      # stdlib unittest
  README.md
```

### Three ways to install, none of which need hosting

1. **Copy the folder** into `~/.claude/skills/shotkit/` — Claude Code auto-loads it next
   session as `shotkit@skills-dir`. Zero commands. This is the "I sent you a folder" path.
2. **Local marketplace:** `claude plugin marketplace add ./shotkit` — the CLI accepts a
   path, not only a GitHub repo.
3. **Committed into a team repo:** `claude plugin marketplace add ./shotkit --scope project`,
   commit, and everyone on that repo gets it.

A GitHub repo can be added later without changing the layout — only the source changes.

The plugin form is what buys five separate skills instead of one large router skill: each
one loads only when its craft is needed. The skill bodies contain no plugin-specific
machinery, so a person on another agent can read `skills/cinematic-scenes/SKILL.md`
directly.

`${CLAUDE_PLUGIN_ROOT}` locates `shotkit.py` regardless of where the folder was placed.

## Zero-install constraint

Python 3.9+, standard library only. No `pip install`, no virtualenv, no lockfile.

The one dependency the ported code carries today is the `regex` package, used in
`mentions.py` for `\p{L}\p{N}` character classes. Python 3's built-in `re` makes `\w`
Unicode-aware by default, so `[\w-]+` covers `[\p{L}\p{N}_-]+`. The port swaps the module
and pins the equivalence with a test (see Testing).

## Data model

A shotkit project is a directory the operator owns:

```
my-film/
  bible.json
  scenes/s01.json  s02.json  …
  refs/*.png            # images live here; every path in JSON is relative to the project root
  out/                  # CLI writes here
```

### bible.json

```json
{
  "style": {
    "globalPreamble": "one line per project, reproduced verbatim in every frame",
    "banned": "negative terms"
  },
  "characters": [
    {
      "id": "skye",
      "name": "Skye",
      "canonicalDescription": "IDENTITY ONLY: face, hair, build, age — never clothing",
      "bodyPlan": "humanoid | quadruped | wingedQuadruped | avian",
      "looks": [
        { "label": "primary", "description": "wardrobe / durable state",
          "refImage": "refs/skye-primary.png" }
      ],
      "identityRefs": ["refs/skye-photo1.jpg"],
      "refKit": [
        { "role": "face|body|hair|outfit|object|full",
          "uri": "refs/skye-face.png", "note": "" }
      ]
    }
  ],
  "locations": [
    {
      "id": "church", "name": "Church",
      "canonicalDescription": "…",
      "lightingProfile": "…",
      "views": [{ "label": "primary", "uri": "refs/church-01.png" }]
    }
  ],
  "props": [
    { "id": "key", "name": "Red Key", "canonicalDescription": "…", "uri": "refs/key.png" }
  ]
}
```

The `canonicalDescription` = identity / `looks` = wardrobe split is ported unchanged. It is
what keeps a face stable across shots in *any* generator, not a Short Drama implementation
detail.

`refKit` stays separate from `identityRefs`; they are never merged.

### scenes/&lt;id&gt;.json

```json
{
  "id": "s01",
  "locationId": "church",
  "scenePrompt": "@skye kneels before the altar in @church",
  "motionPrompt": "…",
  "dialogue": "Skye: [shot 2] I never asked for this",
  "voiceover": "",
  "durationSec": 8,
  "generateAudio": true,
  "aspect": "9:16",
  "loop": false,
  "banned": ""
}
```

## CLI

Invoked as `python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" <command>`; `shotkit` below is that,
abbreviated. Commands run from the project directory.

```
shotkit init my-film                   # copy template/
shotkit frame    s01                   # t2i keyframe
shotkit poster   s01                   # vertical key art
shotkit motion   s01 --mode i2v        # i2v | t2v | ref-anchored
shotkit sheet    skye --look primary   # turnaround / ref-kit sheet
shotkit location church --view night
shotkit prop     key
shotkit lint     s01                   # every lint at once
```

Every generating command writes two files and echoes the prompt to stdout:

```
out/s01.frame.txt        the finished prompt — paste into any UI
out/s01.frame.refs.txt   image paths, one per line, IN MANIFEST ORDER
```

The two files together are the portability contract: attach the images in the listed order
and the ordinals written into the prompt ("the third image is the GARMENT…") line up.

## Prompt assembly contract

Ported block-for-block. These orderings are not stylistic — each one encodes a generator
failure that was observed and fixed.

**frame** — `globalPreamble` → reference-layout clause (only when characters or props are
present) → `Single cinematic keyframe. <scenePrompt>.` → single-photograph clause → single
-frozen-instant clause → `Setting:` → `Props:` → `Maintain identity:` → frame-safety tail
(plus `Avoid:` when `banned` is set).

**poster** — same, with the theatrical-key-art clause and the crop-aware composition clause
in place of the keyframe clauses.

**motion** — identity clause → `motionPrompt` → loop hint → spoken-line clause + narration
clause → **exactly one** of \{keyframe anchor (`@Image1` is frame 0) | i2v safety clause |
nothing, for a pure t2v reference render\} → audio discipline (only when audio is baked) →
`strip_mentions`, so no `@token` / `#view` / `*` noise reaches the model.

Which of the three motion variants applies is the `--mode` flag. In the tool it is derived
from engine capabilities; outside it, the operator knows their generator and says so.
`references/engines.md` documents the distinction: i2v takes a seed frame and must be told
to animate only what it shows; reference-to-video takes the keyframe as a peer reference and
must be told that reference #1 *is* frame 0.

**sheet** — medium (`globalPreamble`) first, because opening tokens dominate an image
model's read → `9:16 character reference sheet…` → **the reference manifest immediately
behind the medium** → body-plan panels → identity anchor → style block → common tail.

When a manifest is present, the written subject line and look line are **dropped, not
reworded**. Two sources for one trait is a coin toss; per-image notes inside the manifest
carry any nuance the prose used to.

**Reference ordering is load-bearing.** The manifest numbers images from the slot list, so
nothing may reorder, filter or insert into that list between building the manifest and
writing `*.refs.txt`. Both come from the same list object in the same function.

## What changes in the port

| In the tool | In shotkit |
|---|---|
| `uri` into the asset store | relative path to a file on disk |
| engine selection (Seedance / Kling), per-engine reference caps | `--mode` flag + `references/engines.md` |
| cache, billing, providers, paid-tool gates, MCP | removed |
| `regex` package | stdlib `re` (`\w` is Unicode-aware in Python 3) |
| MCP tool names in skill prose (`update_character`, `generate_character_look`) | "edit `bible.json`" + shotkit CLI commands |
| story branching / forks | not ported |

## Source map

| Source in shortdrama | Destination in shotkit |
|---|---|
| `shortdrama-skills/skills/cinematic-scenes/**` | `skills/cinematic-scenes/**`, tool references rewritten |
| `shortdrama-skills/skills/pov-scenes/SKILL.md` | `skills/pov-scenes/SKILL.md` |
| `shortdrama-skills/skills/short-drama-structure/**` minus `branching.md` | `skills/short-drama-structure/**` |
| `director.system.md` — frame & motion directing constraints (insert/macro, eyeline, screen direction, no duplication, per-angle locations) | `skills/cinematic-scenes/references/frame-guards.md` — **currently written down nowhere but the tool's system prompt** |
| `director.system.md` — identity is sacred, look-not-a-second-character, `bodyPlan`, "consistency is a reference image, not prose" | `skills/character-refs/**` |
| `director.system.md` — keyframe = SHOT 1, multishot in the motion prompt, dialogue vs voiceover, `[shot N]` anchors, ~2 words/sec | `skills/prompt-assembly/references/motion-dialogue.md` |
| `director.system.md` — never author a fresh style in a scene prompt; style presets | `skills/prompt-assembly/SKILL.md` + `shotkit/style.py` |
| `app/domain/ref_kit.py` | `shotkit/ref_kit.py` |
| `app/domain/turnaround.py` | `shotkit/turnaround.py` |
| `app/domain/prompt_guards.py` | `shotkit/guards.py` |
| `app/domain/mentions.py` | `shotkit/mentions.py` |
| `app/domain/ref_budget.py` | folded into `shotkit/project.py` |
| `app/domain/style_presets.py` | `shotkit/style.py` |
| `app/application/storyboard.py` prompt builders | `shotkit/scene.py` |
| `app/web/handlers/scene_request.py` motion assembly | `shotkit/scene.py`, minus engine/cost logic |

`app/domain/**` is already pure — no infrastructure imports — which is why the port is a
copy plus a rename rather than a rewrite.

## Testing

Standard-library `unittest`. No test dependencies.

**Golden fixtures, generated from the tool itself.** A one-off script (run from a scratch
directory, importing shortdrama read-only, changing nothing) calls the tool's own
`build_scene_frame_prompt`, `build_poster_prompt`, `build_character_sheet`,
`build_ref_manifest`, `build_location_view`, `build_prop_view`, `with_i2v_safety`,
`with_keyframe_anchor`, `with_audio_discipline`, `with_spoken_line` and `parse_dialogue`
over a fixed input set and writes the results to `tests/golden/`. shotkit's tests assert
byte-exact equality.

This turns "the prompt is the same one the tool sends" into a verified fact with a
regression net, rather than a claim.

**`regex` → `re` equivalence.** A Unicode mention corpus — Cyrillic names, `@Cleo's auto
door` (a location name that reaches across an apostrophe), `@anna_new` against a character
named `@Anna` — runs through both implementations during the port, and the outputs must
match. Both cases are real bugs recorded in `mentions.py`'s own comments; the port must not
resurrect them.

**Reference-order test.** Building a manifest and the reference list from a slot set must
produce ordinals and file order that agree, including when roles repeat and when the slot
count exceeds the ordinal word list.

**End-to-end.** From `template/`, one character + one location + one scene must produce a
`frame.txt`, a `refs.txt` and a `motion.txt` whose reference count matches the file list.

## Work order

1. Repo skeleton: `.claude-plugin/*`, `template/`, `README.md`
2. Generate golden fixtures from the tool (read-only, outside the shortdrama tree)
3. Port `shotkit/` module by module against those fixtures, TDD:
   `mentions` → `guards` → `ref_kit` → `turnaround` → `scene` → `style` → `project` → `cli`
4. Write the five skills; strip tool-specific prose; lift `frame-guards.md` and
   `motion-dialogue.md` out of `director.system.md`
5. End-to-end run from `template/`
6. Verify all three install paths: copy into `~/.claude/skills/`,
   `marketplace add ./shotkit`, `--scope project`

## Open questions

None outstanding. Naming, scope, reference transport, bible format, style handling and the
branching cut are all settled.
