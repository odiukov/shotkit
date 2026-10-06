"""shotkit/cli.py — the operator-facing surface.

Each generating command loads the project, resolves one render via
`shotkit.project`, and writes exactly two files nested under `out/`, grouped by
entity so a project with many scenes/characters doesn't dump hundreds of files
into one flat directory:

    out/scenes/<scene_id>/frame.txt            out/scenes/<scene_id>/frame.refs.txt
    out/scenes/<scene_id>/poster.txt           out/scenes/<scene_id>/poster.refs.txt
    out/scenes/<scene_id>/motion.txt           out/scenes/<scene_id>/motion.refs.txt
    out/characters/<character_id>/<look>.sheet.txt
    out/characters/<character_id>/<look>.sheet.refs.txt
    out/locations/<location_id>/<view>.view.txt
    out/locations/<location_id>/<view>.view.refs.txt
    out/props/<prop_id>/prop.txt               out/props/<prop_id>/prop.refs.txt

The `.txt` file is the finished prompt (no trailing newline added); the
`.refs.txt` file is `Render.refs`, one absolute path per line, untouched.

The prompt is also echoed to stdout, unless `--handoff` is given — see
`_handoff_block` for the paste-ready form that replaces it in that case.
Warnings always go to stderr, `--handoff` or not.

Every refusal (a --project with no bible.json, an unknown scene/character/
location/prop id, a missing --mode, ref-anchored with no --keyframe, a
non-primary `sheet --look` with no primary look reference to anchor on, `init`
into a non-empty directory) prints a message naming the offending thing to
stderr and returns 1 — never an uncaught traceback, and never a message
blaming the wrong one of those when more than one could be at fault (a bad
--project is never reported as an unknown scene id, and vice versa). `lint`
returns 1 when it found anything, 0 when clean, and never writes to `out/`.
`status` prints a read-only inventory and always returns 0 once the project
loads (it is a report, not a gate) — it only returns 1 the same way every
other command does, when `--project` has no `bible.json`. `styles` needs no
project at all and always returns 0.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

from shotkit import project as project_mod
from shotkit import style as style_mod

TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "template"

_MOTION_MODES = ("i2v", "t2v", "ref-anchored")

# Output directory category names — shared with _render_paths and cmd_status.
SCENES_CATEGORY = "scenes"
CHARACTERS_CATEGORY = "characters"
LOCATIONS_CATEGORY = "locations"
PROPS_CATEGORY = "props"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _render_paths(
    root: pathlib.Path, category: str, entity_id: str, leaf: str
) -> tuple[pathlib.Path, pathlib.Path]:
    """Where a render's two output files live: `out/<category>/<entity_id>/<leaf>.*`.

    The entity's own id is the directory, so everything about one scene/
    character/location/prop lands in one place instead of hundreds of
    compound-stem files in a single flat `out/`; the leaf names the KIND of
    artifact (`frame`, `motion`, `<look>.sheet`, `<view>.view`, `prop`).
    """
    out_dir = root / "out" / category / entity_id
    return out_dir / f"{leaf}.txt", out_dir / f"{leaf}.refs.txt"


def _handoff_block(render: project_mod.Render) -> str:
    """The copy-paste handoff: one prompt to paste, images to attach in order.

    `render.refs` is `Render.refs` **in order, untouched** — no sorting, no
    de-duplication. For a character sheet, the ordinals a `refKit` manifest
    writes into the prompt text itself ("the third image is the GARMENT...")
    are computed from that exact same list (see
    `project.render_sheet`'s ordering invariant) — reordering, filtering or
    inserting into this list here would silently mislabel every image after
    the change, with nothing to catch it.

    An empty `refs` means two different things depending on the command, and the
    message must not conflate them:

    - `sheet` / `location` / `prop` (`render.creates_reference`): this render's OWN
      output IS the reference — there is nothing to attach because nothing has been
      generated yet. `render.save_to` names the exact path bible.json already gives
      it, when one is configured; when the look/view/prop genuinely has no path
      configured yet, say that plainly instead of inventing one from the stem.
    - `frame` / `poster` / `motion`: an empty list means the prompt's `@mentions`
      resolved to nothing with an image attached — either it mentions no one, or
      what it mentions has no reference image configured. Never a save instruction
      here; this render doesn't produce a reference at all.
    """
    lines = [
        "=== PROMPT — paste this into your generator ===",
        render.prompt,
        "",
        "=== ATTACH THESE IMAGES, IN THIS ORDER ===",
    ]
    if render.refs:
        lines.extend(f"{i}. {p}" for i, p in enumerate(render.refs, start=1))
    elif render.creates_reference:
        if render.save_to:
            lines.append(
                "(nothing to attach — this render creates that reference: save "
                f"the output to {render.save_to}, then every scene onward attaches it)"
            )
        else:
            lines.append(
                "(nothing to attach — and no destination is configured in "
                "bible.json for this reference yet; add one, then rerun)"
            )
    else:
        lines.append(
            "(none attached — nothing in this prompt @mentions a reference image, "
            "or what's mentioned has none configured)"
        )
    if render.creates_reference and render.refs:
        lines.extend([
            "", "=== SAVE GENERATED REFERENCE ===",
            render.save_to or "No destination configured; add one in bible.json.",
        ])
    settings = []
    if render.mode:
        settings.append(f"Mode: {render.mode}")
    if render.aspect:
        settings.append(f"Aspect ratio: {render.aspect}")
    if render.duration_sec:
        settings.append(f"Duration: {render.duration_sec:g} seconds")
    if render.mode == "i2v":
        settings.append(
            "Start-frame slot (separate from reference images): "
            + (render.start_frame or "choose the generated opening frame")
        )
    if settings:
        lines.extend(["", "=== GENERATOR SETTINGS — set these manually ===", *settings])
    return "\n".join(lines)


def _save_render(
    prompt_path: pathlib.Path,
    refs_path: pathlib.Path,
    render: project_mod.Render,
) -> None:
    """Persist the shared prompt/refs contract without terminal output."""
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(render.prompt, encoding="utf-8")
    refs_text = "\n".join(render.refs)
    if refs_text:
        refs_text += "\n"
    refs_path.write_text(refs_text, encoding="utf-8")


def _write_render(
    prompt_path: pathlib.Path,
    refs_path: pathlib.Path,
    render: project_mod.Render,
    handoff: bool = False,
) -> int:
    _save_render(prompt_path, refs_path, render)
    if handoff:
        print(_handoff_block(render))
    else:
        print(render.prompt)
    for w in render.warnings:
        print(w, file=sys.stderr)
    return 0


def _refuse(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def _key_error_message(exc: KeyError) -> str:
    """The plain message a `_find`-raised KeyError carries, without repr-doubling.

    `_find` raises `KeyError(f"unknown {kind} id: {entity_id!r}")` — a single string
    argument. `KeyError.__str__` renders that as `repr(args[0])`, so printing `exc`
    (or interpolating it into an f-string) doubles the already-complete message:
    `unknown character id: 'nosuch' ("unknown character id: 'nosuch'")`. The message
    IS `exc.args[0]`; nothing further needs wrapping it.
    """
    return exc.args[0] if exc.args else str(exc)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> int:
    target = pathlib.Path(args.dir)
    if target.exists():
        if any(target.iterdir()):
            return _refuse(f"refusing to init: {target} is not empty")
    else:
        target.mkdir(parents=True)
    shutil.copytree(TEMPLATE_DIR, target, dirs_exist_ok=True)
    print(f"initialized shotkit project at {target}")
    return 0


def cmd_styles(args: argparse.Namespace) -> int:
    """List the shipped style presets — no project required, nothing written to disk."""
    for p in style_mod.STYLE_PRESETS:
        print(f"{p.id}  —  {p.name}")
        print(f"  preamble: {p.global_preamble}")
        print(f"  banned:   {p.banned}")
    return 0


def _load_project_or_refuse(root: pathlib.Path):
    """`project_mod.load_project(root)`, or None with the refusal already printed.

    Isolated from scene/character/location/prop loading so a bad --project (no
    bible.json) is never misreported as "unknown scene id" — the two failures name
    different things and must never share a message.
    """
    try:
        return project_mod.load_project(root)
    except FileNotFoundError as exc:
        _refuse(str(exc))
        return None


def cmd_frame(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    render = project_mod.render_frame(project, scene)
    prompt_path, refs_path = _render_paths(
        root, SCENES_CATEGORY, args.scene_id, "frame"
    )
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_poster(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    render = project_mod.render_poster(project, scene)
    prompt_path, refs_path = _render_paths(
        root, SCENES_CATEGORY, args.scene_id, "poster"
    )
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_motion(root: pathlib.Path, args: argparse.Namespace) -> int:
    if not args.mode:
        return _refuse("motion requires --mode (i2v|t2v|ref-anchored)")
    if args.mode not in _MOTION_MODES:
        return _refuse(
            f"unknown --mode {args.mode!r}: must be one of {', '.join(_MOTION_MODES)}"
        )
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    try:
        render = project_mod.render_motion(
            project, scene, mode=args.mode, keyframe=args.keyframe
        )
    except ValueError as exc:
        return _refuse(str(exc))
    prompt_path, refs_path = _render_paths(
        root, SCENES_CATEGORY, args.scene_id, "motion"
    )
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_sheet(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        render = project_mod.render_sheet(project, args.character_id, look=args.look)
    except KeyError as exc:
        return _refuse(_key_error_message(exc))
    except ValueError as exc:
        return _refuse(str(exc))
    prompt_path, refs_path = _render_paths(
        root, CHARACTERS_CATEGORY, args.character_id, f"{args.look}.sheet"
    )
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_location(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        render = project_mod.render_location(project, args.location_id, args.view)
    except KeyError as exc:
        return _refuse(_key_error_message(exc))
    leaf = f"{args.view or 'primary'}.view"
    prompt_path, refs_path = _render_paths(
        root, LOCATIONS_CATEGORY, args.location_id, leaf
    )
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_prop(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        render = project_mod.render_prop(project, args.prop_id)
    except KeyError as exc:
        return _refuse(_key_error_message(exc))
    prompt_path, refs_path = _render_paths(root, PROPS_CATEGORY, args.prop_id, "prop")
    return _write_render(prompt_path, refs_path, render, args.handoff)


def cmd_lint(root: pathlib.Path, args: argparse.Namespace) -> int:
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    try:
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    issues = project_mod.lint_scene(project, scene)
    for issue in issues:
        print(issue, file=sys.stderr)
    return 1 if issues else 0


def cmd_build(root: pathlib.Path, args: argparse.Namespace) -> int:
    """Reassemble all text artifacts, including drafts whose images are pending."""
    project = _load_project_or_refuse(root)
    if project is None:
        return 1
    # Validate scene JSON before replacing any outputs.
    scenes = [project_mod.load_scene(project, p.stem)
              for p in sorted((root / "scenes").glob("*.json"))]
    jobs = []
    for character in project.characters:
        labels = [look.label for look in character.looks] or ["primary"]
        labels.sort(key=lambda label: label.strip().lower() != "primary")
        for label in labels:
            jobs.append(("characters", character.id, f"{label}.sheet", project_mod.render_sheet,
                         dict(character_id=character.id, look=label)))
    for location in project.locations:
        labels = [view.label for view in location.views] or ["primary"]
        for label in labels:
            jobs.append(("locations", location.id, f"{label}.view", project_mod.render_location,
                         dict(location_id=location.id, view=label)))
    for prop in project.props:
        jobs.append(("props", prop.id, "prop", project_mod.render_prop, dict(prop_id=prop.id)))
    issues = {}
    for scene in scenes:
        issues[scene.id] = project_mod.lint_scene(project, scene)
        if scene.scene_prompt.strip():
            jobs.append(("scenes", scene.id, "frame", project_mod.render_frame, dict(scene=scene)))
        if scene.motion_prompt.strip():
            jobs.append(("scenes", scene.id, "motion", project_mod.render_motion,
                         dict(scene=scene, mode="t2v", keyframe=None)))
        else:
            issues[scene.id].append("motionPrompt is empty: no motion prompt assembled")

    # Assemble against one loaded snapshot, then persist structured results.
    compiled = []
    for category, entity_id, leaf, builder, options in jobs:
        try:
            render = builder(project, **options)
            messages = list(render.warnings)
        except (OSError, ValueError, KeyError) as exc:
            render = None
            messages = [_key_error_message(exc) if isinstance(exc, KeyError) else str(exc)]
        compiled.append((category, entity_id, leaf, render, messages))

    results = []
    for category, entity_id, leaf, render, messages in compiled:
        prompt, refs = _render_paths(root, category, entity_id, leaf)
        assembled = render is not None
        if assembled:
            try:
                _save_render(prompt, refs, render)
            except OSError as exc:
                assembled = False
                messages.append(str(exc))
        results.append({
            "prompt": str(prompt.relative_to(root)),
            "refs": str(refs.relative_to(root)),
            "assembled": assembled,
            "messages": messages,
        })
    failed = sum(not item["assembled"] for item in results)
    warnings = sum(len(item["messages"]) for item in results)
    report = {
        "motionMode": "t2v", "artifacts": results, "sceneIssues": issues,
        "note": "Text prompts only. Review missing references and authoring issues before generation. "
                "Existing images are not regenerated or verified against changed character designs. "
                "STORY.md and scene prose must be reconciled by the author before build.",
    }
    report_path = root / "out" / "build-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Assembled {len(results) - failed}/{len(results)} prompts; {len(scenes)} scenes; "
          f"{warnings} warnings; {failed} errors.")
    if not scenes:
        print("No scene JSON found: write scenes/*.json to build motion prompts.")
    print(f"Report: {report_path}")
    return 1 if failed else 0


def _presence_mark(paths: list) -> tuple[str, str]:
    """(" " | "x", note) for one entity's status line.

    The ONLY question "is this reference present on disk" answers to is
    `project_mod.missing_ref_files` — the same function `render_frame` et al.
    already use to warn. This does not re-decide presence; it only decides
    WHICH path(s) to ask that function about (`project_mod.status_ref_paths`).
    """
    if not paths:
        return " ", "no reference image configured"
    if project_mod.missing_ref_files(paths):
        return " ", f"missing: {paths[0]}"
    return "x", paths[0]


def cmd_status(root: pathlib.Path, args: argparse.Namespace) -> int:
    """A read-only inventory — never a gate. Exit 0 once the project loads."""
    project = _load_project_or_refuse(root)
    if project is None:
        return 1

    ref_paths = project_mod.status_ref_paths(project)

    print("characters:")
    for c in project.characters:
        mark, note = _presence_mark(ref_paths.get(c.id, []))
        print(f"  [{mark}] {c.id}  {note}")

    print("locations:")
    for loc in project.locations:
        mark, note = _presence_mark(ref_paths.get(loc.id, []))
        print(f"  [{mark}] {loc.id}  {note}")

    print("props:")
    for p in project.props:
        mark, note = _presence_mark(ref_paths.get(p.id, []))
        print(f"  [{mark}] {p.id}  {note}")

    print("scenes:")
    scenes_dir = root / "scenes"
    if scenes_dir.is_dir():
        for scene_path in sorted(scenes_dir.glob("*.json")):
            scene_id = scene_path.stem
            scene_out_dir = root / "out" / SCENES_CATEGORY / scene_id
            has_output = scene_out_dir.is_dir() and any(scene_out_dir.iterdir())
            mark = "x" if has_output else " "
            note = "out/ has rendered artifacts" if has_output else "no output yet"
            print(f"  [{mark}] {scene_id}  {note}")

    return 0


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shotkit")
    parser.add_argument(
        "--project", default=".", help="project root directory (default: cwd)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="scaffold a new project from the template")
    p_init.add_argument("dir")

    _HANDOFF_HELP = (
        "print one paste-ready block (prompt + numbered image list) to stdout "
        "instead of echoing the prompt; the two out/ files are written either way"
    )

    p_frame = sub.add_parser("frame", help="render a scene's opening keyframe prompt")
    p_frame.add_argument("scene_id")
    p_frame.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_poster = sub.add_parser("poster", help="render a scene's poster-frame prompt")
    p_poster.add_argument("scene_id")
    p_poster.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_motion = sub.add_parser("motion", help="render a scene's motion/video prompt")
    p_motion.add_argument("scene_id")
    p_motion.add_argument("--mode", default=None, help="i2v | t2v | ref-anchored")
    p_motion.add_argument("--keyframe", default=None, help="start/anchor frame; relative paths use the project root (i2v or ref-anchored)")
    p_motion.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_sheet = sub.add_parser("sheet", help="render a character reference sheet prompt")
    p_sheet.add_argument("character_id")
    p_sheet.add_argument("--look", default="primary")
    p_sheet.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_location = sub.add_parser("location", help="render a location view prompt")
    p_location.add_argument("location_id")
    p_location.add_argument("--view", default=None)
    p_location.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_prop = sub.add_parser("prop", help="render a prop hero-shot prompt")
    p_prop.add_argument("prop_id")
    p_prop.add_argument("--handoff", action="store_true", help=_HANDOFF_HELP)

    p_lint = sub.add_parser("lint", help="check a scene for broken/missing references")
    p_lint.add_argument("scene_id")

    sub.add_parser(
        "status",
        help="print a read-only project inventory (cast/locations/props refs, scene output)",
    )

    sub.add_parser("build", help="rebuild all reference and scene prompts (t2v), including drafts with missing images")
    sub.add_parser("styles", help="list the shipped style presets")

    return parser


_ROOT_HANDLERS = {
    "build": cmd_build,
    "frame": cmd_frame,
    "poster": cmd_poster,
    "motion": cmd_motion,
    "sheet": cmd_sheet,
    "location": cmd_location,
    "prop": cmd_prop,
    "lint": cmd_lint,
    "status": cmd_status,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:]) if argv is None else list(argv)
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1

    try:
        if args.command == "init":
            return cmd_init(args)
        if args.command == "styles":
            return cmd_styles(args)
        root = pathlib.Path(args.project).resolve()
        return _ROOT_HANDLERS[args.command](root, args)
    except (ValueError, OSError) as exc:
        return _refuse(str(exc))
    except KeyError as exc:
        return _refuse(_key_error_message(exc))


if __name__ == "__main__":
    raise SystemExit(main())
