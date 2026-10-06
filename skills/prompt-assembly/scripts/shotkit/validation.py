"""Validation of the editable project JSON, using only the standard library."""

from __future__ import annotations

import math
import re

from shotkit.mentions import ref_index


STYLE = {"globalPreamble": str, "banned": str, "aspect": (str, type(None))}
LOOK = {"label": str, "description": str, "refImage": (str, type(None))}
SLOT = {"uri": str, "role": str, "note": str}
CHARACTER = {
    "id": str, "name": str, "canonicalDescription": str, "bodyPlan": str,
    "looks": [LOOK], "identityRefs": [str], "refKit": [SLOT],
    "referenceImages": [str], "gender": str, "voiceNote": str,
}
LOCATION = {
    "id": str, "name": str, "canonicalDescription": str,
    "lightingProfile": str, "views": [{"label": str, "uri": str}],
}
PROP = {"id": str, "name": str, "canonicalDescription": str, "uri": (str, type(None))}
BIBLE = {"style": STYLE, "characters": [CHARACTER], "locations": [LOCATION], "props": [PROP]}
SCENE = {
    "id": str, "locationId": str, "scenePrompt": str, "motionPrompt": str,
    "dialogue": str, "voiceover": str, "durationSec": (int, float),
    "generateAudio": bool, "aspect": (str, type(None)), "loop": bool,
    "banned": str, "posterFocusY": (int, float, type(None)),
}


def path_component(value: str, context: str) -> None:
    if not value.strip() or value in (".", "..") or any(c in value for c in "/\\\0\n\r"):
        raise ValueError(f"{context}: expected a non-empty name without path separators")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise ValueError(f"{context}: use English letters (A-Z, a-z), digits, underscores or hyphens only")


def validate(value, schema, context: str) -> None:
    if isinstance(schema, dict):
        if not isinstance(value, dict):
            raise ValueError(f"{context}: expected an object")
        unknown = value.keys() - schema.keys()
        if unknown:
            raise ValueError(f"{context}: unknown field(s): {', '.join(sorted(unknown))}")
        for key in ("id", "uri", "label", "name"):
            if schema.get(key) is str and key not in value:
                raise ValueError(f"{context}: missing required field {key}")
        for key, item in value.items():
            validate(item, schema[key], f"{context}.{key}")
        for key in ("id", "label"):
            if key in value:
                path_component(value[key], f"{context}.{key}")
        if "name" in value:
            name = value["name"]
            if not name.strip() or name != name.strip():
                raise ValueError(f"{context}.name: expected a non-empty name without surrounding whitespace")
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 .'\-]*", name):
                raise ValueError(f"{context}.name: use an English name")
            if schema is CHARACTER and not re.fullmatch(r"[A-Z][A-Za-z'\-]*(?: [A-Z][A-Za-z'\-]*){0,2}", name):
                raise ValueError(f"{context}.name: use one to three capitalized English words for dialogue speakers")
        if value.get("locationId"):
            path_component(value["locationId"], f"{context}.locationId")
        if value.get("aspect") is not None and "aspect" in schema:
            if not re.fullmatch(r"[1-9]\d*:[1-9]\d*", value["aspect"]):
                raise ValueError(f"{context}.aspect: expected a ratio such as 9:16")
        if "durationSec" in value and value["durationSec"] <= 0:
            raise ValueError(f"{context}.durationSec: must be positive")
        if "voiceover" in value and value["voiceover"].strip():
            raise ValueError(f"{context}.voiceover is removed; move narration to dialogue as 'VO: ...' and set generateAudio to true")
    elif isinstance(schema, list):
        if not isinstance(value, list):
            raise ValueError(f"{context}: expected an array")
        labels = set()
        for i, item in enumerate(value):
            validate(item, schema[0], f"{context}[{i}]")
            if isinstance(item, dict) and "label" in item:
                label = item["label"].strip().lower()
                if label in labels:
                    raise ValueError(f"{context}: duplicate label {label!r}")
                labels.add(label)
    else:
        allowed = schema if isinstance(schema, tuple) else (schema,)
        if type(value) not in allowed:
            names = "/".join(t.__name__ for t in allowed)
            raise ValueError(f"{context}: expected {names}")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{context}: must be finite")
        if isinstance(value, str):
            key = context.rsplit(".", 1)[-1].split("[", 1)[0]
            # Paths are filesystem data, not authored prompt text.
            if key not in {"uri", "refImage", "identityRefs", "referenceImages"}:
                if any(c.isalpha() and not c.isascii() for c in value):
                    raise ValueError(f"{context}: use English text only (A-Z, a-z); non-English letters are not supported")


def validate_bible(data: dict, context: str) -> None:
    validate(data, BIBLE, context)
    entities = [entity for kind in ("characters", "locations", "props")
                for entity in data.get(kind, [])]
    try:
        ref_index(entities)
    except ValueError as exc:
        raise ValueError(f"{context}: {exc}") from exc
