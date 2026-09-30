# scene-from-scratch — implementation report

Branch `feat/scene-from-scratch`, starting commit `3d64367`.

## What was built

The task grew through four coordinator messages while in flight (the `--handoff` flag +
`scene-from-scratch` skill; then project-folder naming/resume + `shotkit status`; then
the nested `out/` layout; then `STORY.md`). All four landed in this one pass — nothing
was silently dropped, but this is materially more than the original brief and the
report says so plainly where a corner was cut.

### 1. `--handoff` on all six generating commands

`shotkit/cli.py`:
- `_handoff_block(render)` — one shared helper building the paste-ready block from a
  `Render`. Numbers `render.refs` **in the order they arrive, untouched** — no sort, no
  dedup — with a docstring calling out that a `refKit` manifest's in-prompt ordinals
  ("the third image is the GARMENT...") are computed from that exact same list, so
  reordering here would silently mislabel every image after the change.
- When `render.refs` is empty, the heading still prints, followed by
  `(none needed — this render has no reference images to attach)` — never a bare empty
  heading.
- `_write_render` takes a `handoff: bool` and prints the block instead of the plain
  prompt when true; the two `out/` files are written identically either way; warnings
  always go to stderr regardless.
- `--handoff` (`action="store_true"`) added to `frame`, `poster`, `motion`, `sheet`,
  `location`, `prop`'s subparsers — one shared help string, one shared code path.

### 2. `shotkit status`

New subcommand (no scene argument, honors `--project`), `cmd_status` in `cli.py`:
- Reuses `project_mod.load_project` (via the existing `_load_project_or_refuse`, so the
  refusal message/exit-code is identical to every other command's bad-`--project` case)
  and a new `project_mod.missing_ref_files`-based presence check — **no second way of
  deciding "is a reference present"**: `project.py::status_ref_paths` only gathers which
  path to ask about (reusing `_select_character_look`/`_select_location_views`, the same
  selectors `render_frame`/`render_motion` already use); `missing_ref_files` alone
  decides presence.
- Prints characters/locations/props each with `[x]`/`[ ]` + the resolved path or a
  `missing: <path>` / `no reference image configured` note, then scenes with `[x]`/`[ ]`
  + whether `out/scenes/<id>/` holds anything.
- Exit 0 always once the project loads; exit 1 only the same way every other command
  refuses a bad `--project` (no `bible.json`) — it is a report, not a gate.

### 3. The nested `out/` layout (breaking change, done completely)

```
out/scenes/<scene-id>/{frame,poster,motion}.txt(.refs.txt)
out/characters/<character-id>/<look>.sheet.txt(.refs.txt)
out/locations/<location-id>/<view>.view.txt(.refs.txt)
out/props/<prop-id>/prop.txt(.refs.txt)
```
`_render_paths(root, category, entity_id, leaf)` is the one place that builds these; all
six `cmd_*` functions were switched to it. `shotkit status`'s scene-output check looks in
`out/scenes/<scene-id>/`, matching this layout.

**Every old flat-stem assertion was updated, none left dangling:**
- `tests/test_cli.py` — all `out/<stem>.*` assertions rewritten to the nested paths.
- `tests/test_end_to_end.py` — `out/s01.frame.txt`/`out/s01.motion.txt` → nested.
- Skills swept for path claims and corrected against `shotkit/cli.py` (see verification
  table below): `skills/character-refs/SKILL.md`,
  `skills/character-refs/references/ref-roles.md`, `skills/cinematic-scenes/SKILL.md`
  (4 spots), `skills/cinematic-scenes/references/failure-modes.md`,
  `skills/prompt-assembly/SKILL.md` (CLI command list + a new "out/ file contract" +
  "--handoff" section replacing the old flat one), `skills/prompt-assembly/references/
  engines.md` (2 spots). `docs/plans/` and `docs/specs/` (historical design docs, not
  load-bearing) were left untouched — noted, not fixed.
- `README.md` rewritten: six skills, `--handoff` on the command list, `status`,
  the nested `out/` tree, "Five minutes to a first prompt" walkthrough updated.
- `.claude-plugin/marketplace.json` description updated to list `scene-from-scratch`
  (not under a test, done for consistency with the README's six-skill claim).

### 4. The `scene-from-scratch` skill

`skills/scene-from-scratch/SKILL.md` — frontmatter `name: scene-from-scratch`,
description states what it does and when it loads, names no tool. Covers, in order:
project-folder creation (`shotkit init <dir>`, kebab-case name derived from the
request, absolute path stated back to the user explicitly, user's own location wins if
given), `STORY.md` (premise/cast-by-role-not-appearance/scenes-in-order-with-state/
decisions; written at cold start, updated same-turn on every scene/cast/decision change,
read first on resume, disagreement with disk state flagged rather than trusted),
resuming (get the path → confirm `bible.json` → read `STORY.md` → run `shotkit status` →
reconcile → continue in the same files), the cold-start cast/location/prop check named
before asking, the one-message question protocol (age/face/build/hair, never clothing —
with the `character-refs` cross-reference for why), writing the bible directly (no CLI
authoring command exists for `bible.json`/`scenes/*.json` — verified), the reference
pass (`sheet`/`location`/`prop --handoff` per new entity, then stop), the scene pass
(`cinematic-scenes` recipe → `lint` → `motion --mode t2v --handoff`), and the final
handoff shape.

`cinematic-scenes/SKILL.md`'s Workflow section gained a pointer at its top ("Starting
from an empty or partially-cast project?") to `scene-from-scratch`, plus a "Related"
entry; `tests/test_skills.py`'s `EXPECTED` set now has six skills (test renamed
`test_all_six_skills_exist`).

## Every command claim in the new skill, verified against source

| Claim in `scene-from-scratch/SKILL.md` | Verified against |
|---|---|
| `shotkit init <dir>` scaffolds from template, refuses only on a non-empty existing dir | `shotkit/cli.py::cmd_init` |
| `shotkit status` — no scene arg, honors `--project`, read-only, exit 0 unless no `bible.json` | `shotkit/cli.py::cmd_status`, `_build_parser`'s `status` subparser (no extra args) |
| `shotkit sheet <id> --handoff` / `shotkit location <id> --handoff` / `shotkit prop <id> --handoff` | `_build_parser`'s `p_sheet`/`p_location`/`p_prop`, each with `--handoff` added |
| `--handoff` prints prompt + numbered image list; empty list says so plainly | `cli.py::_handoff_block` |
| `shotkit lint <scene-id>` checks refs/music-words/dialogue-fit/VO-fit/shot-anchors | `cli.py::cmd_lint` → `project.py::lint_scene` |
| `shotkit motion <scene-id> --mode t2v --handoff` | `_build_parser`'s `p_motion` (`--mode` required, `--handoff` added) |
| No CLI command authors `bible.json`/`scenes/*.json` — Claude writes them directly | `_ROOT_HANDLERS` in `cli.py` has no such command; `project.py`'s `_character_from_json`/`_location_from_json`/`_prop_from_json`/`_scene_from_json` are the wire-format field maps the skill's field lists were read from |
| `bible.json`/scene field names (`canonicalDescription`, `looks[].refImage`, `views[].uri`, prop `uri`, `locationId`, `motionPrompt` etc.) | `shotkit/project.py`'s `_*_from_json` functions |
| Output paths in the reference pass (`out/characters/.../<look>.sheet.*`, etc.) | `cli.py::_render_paths` call sites in `cmd_sheet`/`cmd_location`/`cmd_prop` |

## RED evidence (TDD)

Before implementing `--handoff`/`status`, the 7 new tests (in `TestHandoff` and
`TestStatusCommand`, `tests/test_cli.py`) were run against the unmodified CLI:

```
FAILED tests/test_cli.py::TestHandoff::test_handoff_block_exact_shape_with_references
FAILED tests/test_cli.py::TestHandoff::test_handoff_still_writes_both_out_files
FAILED tests/test_cli.py::TestHandoff::test_handoff_still_writes_warnings_to_stderr
FAILED tests/test_cli.py::TestHandoff::test_handoff_with_no_references_says_so_plainly_not_an_empty_heading
FAILED tests/test_cli.py::TestStatusCommand::test_status_marks_a_missing_reference_file_and_a_rendered_scene
FAILED tests/test_cli.py::TestStatusCommand::test_status_marks_present_reference_scene_without_output_and_writes_nothing
FAILED tests/test_cli.py::TestStatusCommand::test_status_refuses_a_bad_project_naming_bible_json
======================= 7 failed, 25 deselected in 0.11s =======================
```
(all failed with argparse exit code 2 — `--handoff`/`status` were unrecognized — the
expected RED for "doesn't exist yet"). Implemented, then green: full suite
`162 passed`. (The original 155 plus these 7.) Two of the seven initially still failed
after the CLI was implemented — both were test bugs I found and fixed, not product bugs:
a `tempfile.TemporaryDirectory()` `with`-block whose file assertions ran after cleanup,
and an `assertIn("bible.json", err)` checking the `StringIO` object instead of
`err.getvalue()`.

## Isolation evidence

`/Users/oleksandr/orca/projects/shortdrama` git status, before and after this task —
identical (confirmed via `git status --porcelain` at both points):
```
 M CLAUDE.md
 M docs/superpowers/specs/2026-09-17-video-analysis-design.md
 M graphify-out/GRAPH_REPORT.md
 M shortdrama-skills
?? .claude/skills/skills-doc-sync/
?? .claude/worktrees/
?? app.zip
?? docs/superpowers/plans/
```
Nothing in shortdrama was touched. All work is in `/Users/oleksandr/orca/projects/shotkit`
on `feat/scene-from-scratch`; nothing from a scratch directory was committed (nothing was
committed at all — the task didn't ask for a commit).

## Test summary

`python3 -m pytest` from `/Users/oleksandr/orca/projects/shotkit`: **162 passed** (155
original + 7 new), 0 failed.

## Noticed but not touched

- `docs/plans/2026-09-30-shotkit.md` and `docs/specs/2026-09-30-shotkit-design.md`
  contain historical `out/`-path snippets from before this change; left as-is since
  they're dated design records, not living documentation, and nothing tests them.
- No `ruff`/formatter config exists in this repo (unlike the sibling `shortdrama`
  project) — confirmed via `py_compile` instead; nothing to run.
- `STORY.md` is Claude-maintained prose with no CLI support and no automated test — by
  design (the coordinator said "not something the CLI generates"), but it means its
  correctness rests entirely on the skill text being followed, with nothing in this repo
  that checks a real `STORY.md` against a real `bible.json`/`scenes/` for drift. If that
  matters later, a `shotkit status`-adjacent check could compare scene ids mentioned in
  `STORY.md` against `scenes/*.json`, but that was out of scope here (no CLI command was
  asked for).
- `git status` in shotkit itself is *not* clean (expected — this is the deliverable):
  modified `cli.py`, `project.py`, six skill/reference files, `README.md`,
  `marketplace.json`, three test files, plus the new `skills/scene-from-scratch/`
  directory. No commit was made (not requested).
