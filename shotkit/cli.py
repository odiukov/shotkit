"""shotkit/cli.py — the operator-facing surface.

Each generating command loads the project, resolves one render via
`shotkit.project`, and writes exactly two files under `out/`:

    out/<stem>.txt        the finished prompt (no trailing newline added)
    out/<stem>.refs.txt   `Render.refs`, one absolute path per line, untouched

The prompt is also echoed to stdout; warnings go to stderr. Every refusal
(unknown scene/character/location/prop id, a missing --mode, ref-anchored
with no --keyframe, `init` into a non-empty directory) prints a message
naming the offending thing to stderr and returns 1. `lint` returns 1 when it
found anything, 0 when clean, and never writes to `out/`.
"""

from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

from shotkit import project as project_mod

TEMPLATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "template"

_MOTION_MODES = ("i2v", "t2v", "ref-anchored")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def _write_render(root: pathlib.Path, stem: str, render: project_mod.Render) -> int:
    out_dir = root / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{stem}.txt").write_text(render.prompt, encoding="utf-8")
    refs_text = "\n".join(render.refs)
    if refs_text:
        refs_text += "\n"
    (out_dir / f"{stem}.refs.txt").write_text(refs_text, encoding="utf-8")
    print(render.prompt)
    for w in render.warnings:
        print(w, file=sys.stderr)
    return 0


def _refuse(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


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


def cmd_frame(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    render = project_mod.render_frame(project, scene)
    return _write_render(root, f"{args.scene_id}.frame", render)


def cmd_poster(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    render = project_mod.render_poster(project, scene)
    return _write_render(root, f"{args.scene_id}.poster", render)


def cmd_motion(root: pathlib.Path, args: argparse.Namespace) -> int:
    if not args.mode:
        return _refuse("motion requires --mode (i2v|t2v|ref-anchored)")
    if args.mode not in _MOTION_MODES:
        return _refuse(
            f"unknown --mode {args.mode!r}: must be one of {', '.join(_MOTION_MODES)}"
        )
    try:
        project = project_mod.load_project(root)
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    try:
        render = project_mod.render_motion(
            project, scene, mode=args.mode, keyframe=args.keyframe
        )
    except ValueError as exc:
        return _refuse(str(exc))
    return _write_render(root, f"{args.scene_id}.motion", render)


def cmd_sheet(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        render = project_mod.render_sheet(project, args.character_id, look=args.look)
    except KeyError as exc:
        return _refuse(f"unknown character id: {args.character_id!r} ({exc})")
    return _write_render(root, f"{args.character_id}.{args.look}.sheet", render)


def cmd_location(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        render = project_mod.render_location(project, args.location_id, args.view)
    except KeyError as exc:
        return _refuse(f"unknown location id: {args.location_id!r} ({exc})")
    stem = f"{args.location_id}.{args.view or 'primary'}.view"
    return _write_render(root, stem, render)


def cmd_prop(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        render = project_mod.render_prop(project, args.prop_id)
    except KeyError as exc:
        return _refuse(f"unknown prop id: {args.prop_id!r} ({exc})")
    return _write_render(root, f"{args.prop_id}.prop", render)


def cmd_lint(root: pathlib.Path, args: argparse.Namespace) -> int:
    try:
        project = project_mod.load_project(root)
        scene = project_mod.load_scene(project, args.scene_id)
    except FileNotFoundError as exc:
        return _refuse(f"unknown scene id: {args.scene_id!r} ({exc})")
    issues = project_mod.lint_scene(project, scene)
    for issue in issues:
        print(issue, file=sys.stderr)
    return 1 if issues else 0


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

    p_frame = sub.add_parser("frame", help="render a scene's opening keyframe prompt")
    p_frame.add_argument("scene_id")

    p_poster = sub.add_parser("poster", help="render a scene's poster-frame prompt")
    p_poster.add_argument("scene_id")

    p_motion = sub.add_parser("motion", help="render a scene's motion/video prompt")
    p_motion.add_argument("scene_id")
    p_motion.add_argument("--mode", default=None, help="i2v | t2v | ref-anchored")
    p_motion.add_argument("--keyframe", default=None, help="path to the anchor frame")

    p_sheet = sub.add_parser("sheet", help="render a character reference sheet prompt")
    p_sheet.add_argument("character_id")
    p_sheet.add_argument("--look", default="primary")

    p_location = sub.add_parser("location", help="render a location view prompt")
    p_location.add_argument("location_id")
    p_location.add_argument("--view", default=None)

    p_prop = sub.add_parser("prop", help="render a prop hero-shot prompt")
    p_prop.add_argument("prop_id")

    p_lint = sub.add_parser("lint", help="check a scene for broken/missing references")
    p_lint.add_argument("scene_id")

    return parser


_ROOT_HANDLERS = {
    "frame": cmd_frame,
    "poster": cmd_poster,
    "motion": cmd_motion,
    "sheet": cmd_sheet,
    "location": cmd_location,
    "prop": cmd_prop,
    "lint": cmd_lint,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:]) if argv is None else list(argv)
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1

    if args.command == "init":
        return cmd_init(args)

    root = pathlib.Path(args.project).resolve()
    return _ROOT_HANDLERS[args.command](root, args)


if __name__ == "__main__":
    raise SystemExit(main())
