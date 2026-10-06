"""shotkit/project.py — load a project from disk, resolve references in order.

This is the module that turns a directory into the two things a generator needs:
a finished prompt, and an ordered list of image files. The ordinals a prompt writes
("the third image is the GARMENT...") only mean anything if the caller attaches
images in exactly that order — see `render_sheet` below, which is the single place
that invariant has to hold.

JSON on disk is camelCase; the dataclasses in shotkit.types are snake_case. The
translation happens here, and only here, through an explicit field map per entity —
never a generic camel-to-snake converter, which would silently accept a misspelled
key and hand back a dataclass with a quiet default where the author wrote a value.

Reference paths in bible.json / scene JSON are relative to the project root.
Every `Render.refs` entry is an absolute path (as a string), so the list can be
pasted anywhere.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field

from shotkit.guards import (
    lint_dialogue_fit,
    lint_music_words,
    lint_shot_anchors,
    narrator_voice_map,
)
from shotkit.mentions import (
    mentioned_ref_ids,
    parse_ref_mentions,
    prompt_ref_issues,
    strip_mentions,
)
from shotkit.ref_kit import build_ref_manifest
from shotkit.scene import (
    build_motion_prompt,
    build_poster_prompt,
    build_scene_frame_prompt,
)
from shotkit.turnaround import (
    build_character_sheet,
    build_location_view,
    build_prop_view,
)
from shotkit.types import (
    Character,
    Location,
    LocationView,
    Look,
    Prop,
    RefSlot,
    Style,
    norm_label,
)
from shotkit.validation import SCENE, path_component, validate, validate_bible


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Scene:
    id: str
    location_id: str
    scene_prompt: str
    motion_prompt: str
    dialogue: str
    duration_sec: float
    generate_audio: bool
    aspect: str | None
    loop: bool
    banned: str
    poster_focus_y: float | None = None


@dataclass
class Project:
    root: pathlib.Path
    style: Style
    characters: list[Character] = field(default_factory=list)
    locations: list[Location] = field(default_factory=list)
    props: list[Prop] = field(default_factory=list)


@dataclass
class Render:
    prompt: str
    refs: list[str]
    warnings: list[str]
    # Set only by render_sheet/render_location/render_prop — the three renders whose
    # OWN output becomes a reference image. The handoff shows its destination
    # independently of whether any existing images are used as inputs.
    creates_reference: bool = False
    save_to: str | None = None
    aspect: str | None = None
    duration_sec: float | None = None
    mode: str | None = None
    start_frame: str | None = None


# ---------------------------------------------------------------------------
# Wire-format field maps (explicit, one function per entity)
# ---------------------------------------------------------------------------


def _style_from_json(d: dict) -> Style:
    return Style(
        global_preamble=d.get("globalPreamble", ""),
        banned=d.get("banned", ""),
        aspect=d.get("aspect"),
    )


def _look_from_json(d: dict) -> Look:
    return Look(
        label=d.get("label", ""),
        description=d.get("description", ""),
        ref_image=d.get("refImage"),
    )


def _ref_slot_from_json(d: dict) -> RefSlot:
    return RefSlot(
        uri=d["uri"],
        role=d.get("role", "full"),
        note=d.get("note", ""),
    )


def _character_from_json(d: dict) -> Character:
    return Character(
        id=d["id"],
        name=d.get("name", ""),
        canonical_description=d.get("canonicalDescription", ""),
        body_plan=d.get("bodyPlan", "humanoid"),
        looks=[_look_from_json(x) for x in d.get("looks", [])],
        identity_refs=list(d.get("identityRefs", [])),
        ref_kit=[_ref_slot_from_json(x) for x in d.get("refKit", [])],
        reference_images=list(d.get("referenceImages", [])),
        gender=d.get("gender", ""),
        voice_note=d.get("voiceNote", ""),
    )


def _location_view_from_json(d: dict) -> LocationView:
    return LocationView(label=d.get("label", ""), uri=d["uri"])


def _location_from_json(d: dict) -> Location:
    return Location(
        id=d["id"],
        name=d.get("name", ""),
        canonical_description=d.get("canonicalDescription", ""),
        lighting_profile=d.get("lightingProfile", ""),
        views=[_location_view_from_json(x) for x in d.get("views", [])],
    )


def _prop_from_json(d: dict) -> Prop:
    return Prop(
        id=d["id"],
        name=d.get("name", ""),
        canonical_description=d.get("canonicalDescription", ""),
        uri=d.get("uri"),
    )


def _scene_from_json(d: dict) -> Scene:
    # Empty legacy fields remain readable; authored narration must use dialogue VO:.
    if d.get("voiceover", "").strip():
        raise ValueError("voiceover is removed; move narration to dialogue as 'VO: ...' and set generateAudio to true")
    return Scene(
        id=d["id"],
        location_id=d.get("locationId", ""),
        scene_prompt=d.get("scenePrompt", ""),
        motion_prompt=d.get("motionPrompt", ""),
        dialogue=d.get("dialogue", ""),
        duration_sec=d.get("durationSec", 0),
        generate_audio=d.get("generateAudio", True),
        aspect=d.get("aspect"),
        loop=d.get("loop", False),
        banned=d.get("banned", ""),
        poster_focus_y=d.get("posterFocusY"),
    )


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def load_project(root) -> Project:
    """Load bible.json under *root* into a Project. Raises FileNotFoundError if absent."""
    root = pathlib.Path(root).absolute()
    bible_path = root / "bible.json"
    if not bible_path.exists():
        raise FileNotFoundError(f"bible.json not found: {bible_path}")
    data = json.loads(bible_path.read_text(encoding="utf-8"))
    validate_bible(data, str(bible_path))
    return Project(
        root=root,
        style=_style_from_json(data.get("style", {})),
        characters=[_character_from_json(c) for c in data.get("characters", [])],
        locations=[_location_from_json(x) for x in data.get("locations", [])],
        props=[_prop_from_json(p) for p in data.get("props", [])],
    )


def load_scene(project: Project, scene_id: str) -> Scene:
    """Load scenes/<scene_id>.json. Raises FileNotFoundError if absent."""
    path_component(scene_id, "scene id")
    scene_path = project.root / "scenes" / f"{scene_id}.json"
    if not scene_path.exists():
        raise FileNotFoundError(f"scene file not found: {scene_path}")
    data = json.loads(scene_path.read_text(encoding="utf-8"))
    validate(data, SCENE, str(scene_path))
    if data["id"] != scene_id:
        raise ValueError(f"{scene_path}: id must match filename ({scene_id!r})")
    if data.get("locationId"):
        _find(project.locations, data["locationId"], "location")
    return _scene_from_json(data)


def _find(entities, entity_id: str, kind: str):
    for e in entities:
        if e.id == entity_id:
            return e
    raise KeyError(f"unknown {kind} id: {entity_id!r}")


# ---------------------------------------------------------------------------
# ref_dicts — the {id, name, has_image} view mentions.py needs
# ---------------------------------------------------------------------------


def _select_character_look(char: Character, view):
    """Port of app/domain/ref_budget.py::select_character_look, adapted to Character.

    Returns (uri: str | None, warnings: list[str]).
    """
    warnings: list = []
    primary_uri = next(
        (
            lk.ref_image
            for lk in char.looks
            if norm_label(lk.label) == "primary" and lk.ref_image
        ),
        None,
    )
    if primary_uri is None and char.reference_images:
        primary_uri = char.reference_images[0]

    if not isinstance(view, dict):  # 'primary' | 'all'
        return primary_uri, warnings

    want = (view.get("label") or "").strip().lower()
    hit = next((lk for lk in char.looks if norm_label(lk.label) == want), None)
    if not hit or not hit.ref_image:
        warnings.append(
            f'@{char.id}#{want}: no look labelled "{want}" with a reference image '
            "— using the primary look"
        )
        return primary_uri, warnings
    return hit.ref_image, warnings


def _primary_location_view(loc: Location):
    return next((v for v in loc.views if norm_label(v.label) == "primary"),
                next(iter(loc.views), None))


def _select_location_views(loc: Location, view):
    """Port of app/domain/ref_budget.py::select_location_views, adapted to Location.

    Returns (uris: list[str], warnings: list[str]).
    """
    warnings: list = []
    uris = [v.uri for v in loc.views]
    if not uris:
        if isinstance(view, dict):
            warnings.append(f'@{loc.id}#{view["label"]}: no view labelled "{view["label"]}"')
        return [], warnings
    if view == "all":
        return list(uris), warnings
    if view == "primary":
        return [_primary_location_view(loc).uri], warnings
    want = (view.get("label") or "").strip().lower()
    labels = [v.label for v in loc.views]
    idx = next((i for i, lbl in enumerate(labels) if norm_label(lbl) == want), -1)
    if idx < 0:
        warnings.append(
            f'@{loc.id}#{want}: no view labelled "{want}" — using the primary view'
        )
        return [_primary_location_view(loc).uri], warnings
    return [uris[idx]], warnings


def _selected_look_description(char: Character, view) -> str:
    """Port of app/domain/ref_budget.py::selected_look_description, adapted to Character."""
    if not isinstance(view, dict):
        return ""
    want = (view.get("label") or "").strip().lower()
    hit = next(
        (lk for lk in char.looks if norm_label(lk.label) == want and lk.ref_image),
        None,
    )
    return (hit.description or "").strip() if hit else ""


def _character_has_image(c: Character) -> bool:
    """Whether a bare @mention of this character attaches an identity reference.

    Only what _select_character_look resolves counts. identity_refs and ref_kit feed
    the character SHEET path (render_sheet) and never reach a scene frame, so counting
    them here reports a scene clean while render_frame attaches nothing — a paid render
    of an unanchored face.
    """
    uri, _ = _select_character_look(c, "primary")
    return bool(uri)


def status_ref_paths(project: Project) -> dict:
    """One resolved, absolute reference-image path per entity id, keyed by id.

    An id maps to `[]` when nothing is configured for it. Used only by `shotkit
    status`'s inventory to know WHICH path to check; whether that path exists on
    disk is decided exclusively by `missing_ref_files` — this function never makes
    that call itself, so there is exactly one place "is this reference present"
    is answered (the same one `render_frame`/`render_motion`/etc. already use).
    """
    out: dict = {}
    for c in project.characters:
        uri, _warns = _select_character_look(c, "primary")
        out[c.id] = [str(project.root / uri)] if uri else []
    for loc in project.locations:
        uris, _warns = _select_location_views(loc, "primary")
        out[loc.id] = [str(project.root / u) for u in uris]
    for p in project.props:
        out[p.id] = [str(project.root / p.uri)] if p.uri else []
    return out


def ref_dicts(project: Project) -> list[dict]:
    """{"id", "name", "has_image"} for every entity in the project, for mentions.py."""
    out = []
    for c in project.characters:
        out.append({"id": c.id, "name": c.name, "has_image": _character_has_image(c)})
    for loc in project.locations:
        out.append({"id": loc.id, "name": loc.name, "has_image": bool(loc.views)})
    for p in project.props:
        out.append({"id": p.id, "name": p.name, "has_image": bool(p.uri)})
    return out


# ---------------------------------------------------------------------------
# Mention resolution shared by render_frame / render_poster / render_motion
# ---------------------------------------------------------------------------


def _resolve_mentions(project: Project, text: str):
    """Resolve every @mention in *text* to entities, view-selected refs and warnings.

    Returns (chars, locations, props, look_desc_by_char, refs, warnings). The three
    entity lists are ordered: characters in the order first mentioned, then
    locations, then props — matching the order their refs are appended to *refs*.
    """
    refs_meta = ref_dicts(project)
    parsed = parse_ref_mentions(
        text, refs_meta
    )  # one entry per id, in first-mention order
    view_by_id = {e["id"]: e["view"] for e in parsed}

    char_by_id = {c.id: c for c in project.characters}
    loc_by_id = {l.id: l for l in project.locations}
    prop_by_id = {p.id: p for p in project.props}

    char_ids, loc_ids, prop_ids = [], [], []
    for e in parsed:
        eid = e["id"]
        if eid in char_by_id:
            char_ids.append(eid)
        elif eid in loc_by_id:
            loc_ids.append(eid)
        elif eid in prop_by_id:
            prop_ids.append(eid)

    warnings: list = []
    refs: list = []
    look_desc_by_char: dict = {}

    for cid in char_ids:
        c = char_by_id[cid]
        view = view_by_id[cid]
        uri, warns = _select_character_look(c, view)
        warnings.extend(warns)
        if uri:
            refs.append(str(project.root / uri))
        desc = _selected_look_description(c, view)
        if desc:
            look_desc_by_char[cid] = desc

    for lid in loc_ids:
        loc = loc_by_id[lid]
        view = view_by_id[lid]
        uris, warns = _select_location_views(loc, view)
        warnings.extend(warns)
        refs.extend(str(project.root / u) for u in uris)

    for pid in prop_ids:
        p = prop_by_id[pid]
        if p.uri:
            refs.append(str(project.root / p.uri))

    chars = [char_by_id[i] for i in char_ids]
    locations = [loc_by_id[i] for i in loc_ids]
    props = [prop_by_id[i] for i in prop_ids]
    return chars, locations, props, look_desc_by_char, refs, warnings


def _combined_banned(project: Project, scene: Scene) -> str:
    # The tool itself has no per-scene banned list — app/web/handlers/scene_request.py:272
    # sources `banned` from the style alone. A per-scene banned field is a shotkit
    # original; unioning it with the style's negatives (rather than one overriding the
    # other) means an author can add scene-specific negatives without having to repeat
    # or drop the project-wide baseline.
    return ", ".join(x for x in (project.style.banned, scene.banned) if x)


# ---------------------------------------------------------------------------
# On-disk reference checks
# ---------------------------------------------------------------------------


def missing_ref_files(paths: list) -> list:
    """Warn for every resolved reference path that does not exist on disk.

    `prompt_ref_issues` (mentions.py) checks the FIELD: whether bible.json names a
    reference image at all. This checks the FILE: whether the path that field names
    actually exists. In the tool this was ported from, references live in an asset
    store, so a populated field always resolves — the two checks were the same
    question. In shotkit a reference is a path on a filesystem, so a populated field
    can point at nothing (deleted, renamed, never added), and the two checks fail
    independently. Callers pass already-resolved, absolute paths — a Render's own
    `refs`, or a scene's resolved mentions; nothing here reads bible.json.
    """
    return [
        f"missing reference file: {p}" for p in paths if not pathlib.Path(p).is_file()
    ]


# ---------------------------------------------------------------------------
# Render builders
# ---------------------------------------------------------------------------


def _scene_mentions(project: Project, scene: Scene, text: str) -> str:
    """Use locationId as the default location; an explicit view selector wins."""
    if scene.location_id:
        _find(project.locations, scene.location_id, "location")
        if scene.location_id not in mentioned_ref_ids(text, ref_dicts(project)):
            return f"{text} @{scene.location_id}"
    return text


def render_frame(project: Project, scene: Scene) -> Render:
    chars, locations, props, look_desc_by_char, refs, warnings = _resolve_mentions(
        project, _scene_mentions(project, scene, scene.scene_prompt)
    )
    clean_prompt = strip_mentions(scene.scene_prompt, ref_dicts(project))
    prompt = build_scene_frame_prompt(
        clean_prompt,
        chars,
        locations,
        props,
        project.style.global_preamble,
        _combined_banned(project, scene),
        look_desc_by_char,
    )
    warnings = warnings + missing_ref_files(refs)
    return Render(prompt=prompt, refs=refs, warnings=warnings,
                  aspect=scene.aspect or project.style.aspect)


def render_poster(project: Project, scene: Scene) -> Render:
    chars, locations, props, look_desc_by_char, refs, warnings = _resolve_mentions(
        project, _scene_mentions(project, scene, scene.scene_prompt)
    )
    clean_prompt = strip_mentions(scene.scene_prompt, ref_dicts(project))
    # None (no posterFocusY on the scene) means "this project has no story-card crop
    # to compose for" — build_poster_prompt drops the composition clause entirely
    # rather than defaulting to the Short Drama card geometry. Do NOT substitute
    # poster.DEFAULT_FOCUS_Y here; that default exists for crop_band()/compose_clause()
    # callers who already know a crop band is wanted, not as a synthesized "yes".
    prompt = build_poster_prompt(
        clean_prompt,
        chars,
        locations,
        props,
        project.style.global_preamble,
        _combined_banned(project, scene),
        look_desc_by_char,
        scene.poster_focus_y,
    )
    warnings = warnings + missing_ref_files(refs)
    return Render(prompt=prompt, refs=refs, warnings=warnings, aspect="9:16")


def _project_narrator_voices(project: Project) -> dict:
    """The speaker -> {gender, voiceNote} map for `with_spoken_line`'s narration clause.

    Built from the WHOLE project roster (`project.characters`), not just the
    characters `@mentioned` in this scene's motionPrompt — exactly like the tool
    (`narrator_voices = narrator_voice_map(chars_raw)` in scene_request.py, computed
    once from `list_characters()` before any @mention resolution). A `VO:` speaker
    naming a character doesn't require that character to also be `@mentioned` as an
    on-screen reference, so narrowing this map to `chars` would silently lose a
    gender lookup for a narrator who never appears in frame.
    """
    return narrator_voice_map(
        [
            {"name": c.name, "gender": c.gender, "voiceNote": c.voice_note}
            for c in project.characters
        ]
    )


def render_motion(
    project: Project, scene: Scene, mode: str, keyframe: str | None = None
) -> Render:
    if mode == "ref-anchored" and not keyframe:
        raise ValueError("ref-anchored mode requires a keyframe")
    if mode == "t2v" and keyframe:
        raise ValueError("t2v has no start frame; use i2v or ref-anchored with --keyframe")
    if keyframe:
        keyframe = str((project.root / keyframe).absolute())

    # Resolve motion mentions first, then still-only mentions and the default location.
    # scenePrompt contributes references, not shot prose. The project style is shared.
    mention_text = " ".join(filter(None, [scene.motion_prompt, scene.scene_prompt]))
    chars, _locations, _props, _look_desc_by_char, refs, warnings = _resolve_mentions(
        project, _scene_mentions(project, scene, mention_text)
    )
    prompt = build_motion_prompt(
        scene.motion_prompt,
        mode=mode,
        chars=chars,
        dialogue=strip_mentions(scene.dialogue, ref_dicts(project)),
        generate_audio=scene.generate_audio,
        loop=scene.loop,
        refs_for_strip=ref_dicts(project),
        voices=_project_narrator_voices(project),
    )
    if project.style.global_preamble:
        prompt = project.style.global_preamble + "\n" + prompt
    if mode == "ref-anchored":
        refs = [keyframe] + refs
    warnings = warnings + missing_ref_files(refs)
    if mode == "i2v":
        if keyframe:
            warnings += missing_ref_files([keyframe])
        else:
            warnings.append("i2v needs a start-frame image in the generator; pass --keyframe to include its path in the handoff")
    return Render(prompt=prompt, refs=refs, warnings=warnings,
                  aspect=scene.aspect or project.style.aspect,
                  duration_sec=scene.duration_sec or None, mode=mode,
                  start_frame=keyframe if mode == "i2v" else None)


def _character_bases(project: Project, character: Character) -> list:
    ids = mentioned_ref_ids(character.canonical_description, ref_dicts(project))
    return [c for c in project.characters if c.id in ids and c.id != character.id]


def render_sheet(project: Project, character_id: str, look: str = "primary") -> Render:
    character = _find(project.characters, character_id, "character")

    # THE ORDERING INVARIANT: one list, bound once, feeding both the manifest text
    # and the ref paths below it — nothing may filter, sort or insert between them.
    slots = list(character.ref_kit)
    manifest = build_ref_manifest(slots)

    bases = _character_bases(project, character)
    look_label = norm_label(look)
    path_component(look, "look")
    look_obj = next(
        (lk for lk in character.looks if norm_label(lk.label) == look_label), None
    )
    if look_obj is None and look_label != "primary":
        raise ValueError(f"character {character_id!r}: unknown look {look!r}; add it to looks in bible.json first")
    # Mirrors the tool's generate_character_look (app/application/
    # ensure_references.py:240-259): once the requested look resolves to an
    # EXISTING, non-primary Look, both `bases` and `identity_refs` are dropped
    # unconditionally (`bases = []`, `identity = ... if label == "primary" else
    # []`) — a non-primary render conditions on the primary-look anchor ALONE,
    # never on identity-variant bases or the user's uploaded identity photos.
    is_non_primary_look = look_obj is not None and look_label != "primary"
    sheet_bases = [] if is_non_primary_look else bases
    has_identity_photos = bool(character.identity_refs) and not is_non_primary_look
    prompt = build_character_sheet(
        project.style,
        character,
        sheet_bases,
        look_obj,
        has_identity_photos=has_identity_photos,
        ref_manifest=manifest,
    )

    if manifest:
        # A refKit manifest REPLACES the reference clause (build_character_sheet drops
        # subject_line/look_line/_reference_clause entirely) — the kit's own slots are
        # the only images the prompt talks about.
        refs = [str(project.root / slot.uri) for slot in slots]
    elif is_non_primary_look:
        # A non-primary look conditions on the primary-look anchor ALONE — the
        # unconditional counterpart of `sheet_bases`/`has_identity_photos` above.
        # Mirrors the tool's generate_character_look (app/application/
        # ensure_references.py): for a non-primary label the anchor is unconditional
        # — `primary_look(c)` or `reference_images[0]`, `references = [ImageRef(uri=
        # anchor_uri)]`, and NOTHING ELSE (`bases = []`, `identity = []`) — and it
        # RAISES when neither exists rather than emit a sheet with no anchored face.
        anchor_uri, _warns = _select_character_look(character, "primary")
        if not anchor_uri:
            raise ValueError(
                f'character "{character.id}" has no primary look yet — generate '
                "the primary look first, the other looks condition on it to keep "
                "the same face"
            )
        refs = [str(project.root / anchor_uri)]
    else:
        # Primary look (first-ever sheet or a regeneration): the prompt's identity
        # clause (has_identity_photos) and its IDENTITY ANCHOR clause (bases) each
        # assert that specific images are attached — identity_refs and each base's
        # own primary reference, in that order, matching the tool's
        # ensure_references.py (`identity + references` in both
        # ensure_character_references and generate_character_look's primary branch).
        # Shipping those clauses beside an empty refs list is exactly the C2 bug: a
        # prompt that asserts references are attached next to a reference list that
        # does not contain them.
        identity_paths = [str(project.root / u) for u in character.identity_refs]
        base_paths: list[str] = []
        for b in bases:
            uri, _warns = _select_character_look(b, "primary")
            if uri:
                base_paths.append(str(project.root / uri))

        refs = identity_paths + base_paths

    # The destination is separate from input refs, and comes directly from the bible.
    save_to = (
        str(project.root / look_obj.ref_image)
        if look_obj and look_obj.ref_image
        else None
    )
    return Render(
        prompt=prompt,
        refs=refs,
        warnings=missing_ref_files(refs),
        creates_reference=True,
        save_to=save_to,
        aspect="9:16",
    )


def render_location(
    project: Project, location_id: str, view: str | None = None
) -> Render:
    loc = _find(project.locations, location_id, "location")
    if view:
        path_component(view, "view")
    prompt = build_location_view(project.style, loc, view)
    # Existing angles condition the new view; ungenerated paths are destinations.
    refs = [
        str(project.root / v.uri) for v in loc.views
        if (project.root / v.uri).is_file()
    ]
    selected = (
        next((v for v in loc.views if norm_label(v.label) == norm_label(view)), None)
        if view and norm_label(view) != "primary"
        else _primary_location_view(loc)
    )
    if view and selected is None and norm_label(view) != "primary":
        raise ValueError(f"location {location_id!r}: unknown view {view!r}; add it to views in bible.json first")
    return Render(
        prompt=prompt,
        refs=refs,
        warnings=missing_ref_files(refs),
        creates_reference=True,
        save_to=str(project.root / selected.uri) if selected else None,
        aspect="9:16",
    )


def render_prop(project: Project, prop_id: str) -> Render:
    p = _find(project.props, prop_id, "prop")
    prompt = build_prop_view(project.style, p)
    refs = [str(project.root / p.uri)] if p.uri and (project.root / p.uri).is_file() else []
    save_to = str(project.root / p.uri) if p.uri else None
    return Render(
        prompt=prompt,
        refs=refs,
        warnings=missing_ref_files(refs),
        creates_reference=True,
        save_to=save_to,
        aspect="9:16",
    )


# ---------------------------------------------------------------------------
# Lints
# ---------------------------------------------------------------------------


def lint_scene(project: Project, scene: Scene) -> list:
    refs = ref_dicts(project)
    out: list = []

    scene_text = _scene_mentions(project, scene, scene.scene_prompt)
    scene_issues = prompt_ref_issues(scene_text, refs)
    for tok in scene_issues["unknown"]:
        out.append(f"scenePrompt: unknown reference {tok}")
    for name in scene_issues["missing"]:
        out.append(f"scenePrompt: missing reference image for {name}")

    motion_issues = prompt_ref_issues(scene.motion_prompt, refs)
    for tok in motion_issues["unknown"]:
        out.append(f"motionPrompt: unknown reference {tok}")
    for name in motion_issues["missing"]:
        out.append(f"motionPrompt: missing reference image for {name}")

    words = lint_music_words(scene.motion_prompt)
    if words:
        out.append(f"motionPrompt contains music/singing words: {', '.join(words)}")

    dialogue = strip_mentions(scene.dialogue, refs)
    for token in prompt_ref_issues(scene.dialogue, refs)["unknown"]:
        out.append(f"dialogue: unknown reference {token}")
    msg = lint_dialogue_fit(dialogue, scene.duration_sec)
    if msg:
        out.append(msg)

    if scene.dialogue.strip() and not scene.generate_audio:
        out.append("dialogue (including VO:) is ignored when generateAudio is false")

    msg = lint_shot_anchors(dialogue, scene.motion_prompt)
    if msg:
        out.append(msg)

    # A field can be populated and still point at nothing (see missing_ref_files).
    # Resolve both prompts' mentions the same way render_frame/render_motion do, and
    # check the union of what they attach — deduped, order preserved, since the same
    # file can be mentioned in both prompts.
    scene_resolution = _resolve_mentions(project, scene_text)
    motion_text = " ".join(filter(None, [scene.motion_prompt, scene.scene_prompt]))
    motion_resolution = _resolve_mentions(project, _scene_mentions(project, scene, motion_text))
    scene_refs, scene_warnings = scene_resolution[4:]
    motion_refs, motion_warnings = motion_resolution[4:]
    out.extend(dict.fromkeys(scene_warnings + motion_warnings))
    all_refs = list(dict.fromkeys(scene_refs + motion_refs))
    out.extend(missing_ref_files(all_refs))

    return out
