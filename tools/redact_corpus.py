"""Vendor a real story export into a structurally-real, textually-synthetic test corpus.

Run with the path to a Short Drama publish-manifest export (NOT committed anywhere in
this repo — the export itself never enters version control, only this script's output
does):

    python3 tools/redact_corpus.py /path/to/manifest.json

Writes:
    tests/corpus/story.json       one JSON document: style, bible entities, scenes.
    tests/corpus/refs/*.png       tiny placeholder reference images, one per bible
                                   entity, so a project built from story.json resolves
                                   every reference with no "missing file" noise.

What is KEPT verbatim (this is the whole point of the corpus — the resolver has to
survive real structure, not friendly synthetic fixtures):
  - every `@id`, `@id#label`, `@id*` mention token, in place
  - `SHOT N [0:00-0:04]` headers and their timecodes (motionPrompt)
  - `[shot N]` anchors and the speaker label in front of them (dialogue: "Newscaster:
    VO: [shot 1] ...")
  - `durationSec`, per scene
  - the bible's entity ids and names
  - the number of scenes and episodes

Everything else — synopses, shot descriptions, dialogue lines, episode/scene titles,
character/location/prop descriptions — is prose, and prose is replaced by a
deterministic filler vocabulary (the NATO alphabet, cycled). The substitution is
alphabetic-word-for-alphabetic-word: every run of letters outside a kept span becomes
one filler word, and nothing else about the text moves — no whitespace is added or
removed, no word is merged or split. Because the lints this corpus exists to exercise
(`lint_dialogue_fit`, `lint_vo_fit`) work from `len(text.split())`, a substitution that
never touches whitespace preserves every word count exactly, run for run, without having
to reverse-engineer which specific runs a lint reads.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "tests" / "corpus"

# ---------------------------------------------------------------------------
# Deterministic filler vocabulary
# ---------------------------------------------------------------------------
# The NATO alphabet: recognizably a placeholder, contains no word this pack's own
# lints treat specially (no music/singing words, no "cut" phrases, no non-Latin
# script), and cycles in a fixed, reviewable order rather than by any RNG.
_FILLER = [
    "alpha",
    "bravo",
    "charlie",
    "delta",
    "echo",
    "foxtrot",
    "golf",
    "hotel",
    "india",
    "juliet",
    "kilo",
    "lima",
    "mike",
    "november",
    "oscar",
    "papa",
    "quebec",
    "romeo",
    "sierra",
    "tango",
    "uniform",
    "victor",
    "whiskey",
    "xray",
    "yankee",
    "zulu",
]

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']*")


class _Counter:
    def __init__(self) -> None:
        self.n = 0

    def next(self) -> str:
        w = _FILLER[self.n % len(_FILLER)]
        self.n += 1
        return w


def _redact_prose(text: str, counter: _Counter) -> str:
    """Replace every alphabetic word in *text* with one filler word, in place.

    Whitespace, digits, punctuation and newlines are untouched, so `len(text.split())`
    before and after is identical by construction.
    """

    def repl(m: re.Match) -> str:
        orig = m.group(0)
        w = counter.next()
        return w.capitalize() if orig[0].isupper() else w

    return _WORD_RE.sub(repl, text)


# ---------------------------------------------------------------------------
# Kept spans
# ---------------------------------------------------------------------------
_MENTION = r"@[\w-]+(?:#[\w-]+|\*)?"
_SHOT_HEADER = r"SHOT\s+\d+\s*\[\s*\d+:\d{2}\s*-\s*\d+:\d{2}\s*\]"
_SHOT_ANCHOR = r"(?i:\[shot\s+\d+\])"
# Up to 3 capitalised words then ": " — the same shape shotkit/guards.py's own
# _LABEL_RE looks for (a speaker name, or the "VO:" tag). Dialogue-only: motionPrompt's
# own section headers ("LOCKS:", "Ambient:") are prose and get redacted like anything
# else in that field.
_SPEAKER_LABEL = r"(?:^|(?<=\s))[A-Z][A-Za-z'\-]*(?:\s+[A-Z][A-Za-z'\-]*){0,2}:\s+"

_KEEP_MOTION = re.compile(rf"{_MENTION}|{_SHOT_HEADER}")
_KEEP_DIALOGUE = re.compile(rf"{_MENTION}|{_SHOT_ANCHOR}|{_SPEAKER_LABEL}")
_KEEP_NONE = re.compile(r"(?!)")  # never matches — whole text is prose


def _redact(text: str, keep: "re.Pattern[str]", counter: _Counter) -> str:
    if not text:
        return text
    out: list = []
    pos = 0
    for m in keep.finditer(text):
        out.append(_redact_prose(text[pos : m.start()], counter))
        out.append(m.group(0))
        pos = m.end()
    out.append(_redact_prose(text[pos:], counter))
    return "".join(out)


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------


def _character(c: dict, counter: _Counter) -> dict:
    return {
        "id": c["id"],
        "name": c["name"],
        "canonicalDescription": _redact(
            f"{c['name']}, a person in this story.", _KEEP_NONE, counter
        ),
        "bodyPlan": "humanoid",
        "looks": [
            {
                "label": "primary",
                "description": _redact("their usual clothes", _KEEP_NONE, counter),
                "refImage": f"refs/{c['id']}-primary.png",
            }
        ],
        "identityRefs": [],
        "refKit": [],
        "referenceImages": [],
        "gender": "",
        "voiceNote": "",
    }


def _location(loc: dict, counter: _Counter) -> dict:
    return {
        "id": loc["id"],
        "name": loc["name"],
        "canonicalDescription": _redact(
            f"{loc['name']}, a place in this story.", _KEEP_NONE, counter
        ),
        "lightingProfile": _redact("even daylight", _KEEP_NONE, counter),
        "views": [{"label": "primary", "uri": f"refs/{loc['id']}-primary.png"}],
    }


def _prop(p: dict, counter: _Counter) -> dict:
    return {
        "id": p["id"],
        "name": p["name"],
        "canonicalDescription": _redact(
            f"{p['name']}, an object in this story.", _KEEP_NONE, counter
        ),
        "uri": f"refs/{p['id']}.png",
    }


def _scene(s: dict, loc_id_by_name: dict, counter: _Counter) -> dict:
    return {
        "id": s["id"],
        "locationId": loc_id_by_name.get(s.get("location"), ""),
        "synopsis": _redact(s.get("synopsis") or "", _KEEP_NONE, counter),
        "scenePrompt": _redact(s.get("scenePrompt") or "", _KEEP_MOTION, counter),
        "motionPrompt": _redact(s.get("motionPrompt") or "", _KEEP_MOTION, counter),
        "dialogue": _redact(s.get("dialogue") or "", _KEEP_DIALOGUE, counter),
        "voiceover": _redact(s.get("voiceover") or "", _KEEP_NONE, counter),
        "durationSec": s.get("durationSec"),
        "generateAudio": True,
        "aspect": "9:16",
        "loop": False,
        "banned": "",
    }


def transform(export: dict) -> dict:
    counter = _Counter()
    bible = export["bible"]
    loc_id_by_name = {loc["name"]: loc["id"] for loc in bible["locations"]}

    episodes = []
    scenes = []
    for ep in export["episodes"]:
        ep_scenes = [_scene(s, loc_id_by_name, counter) for s in ep["scenes"]]
        scenes.extend(ep_scenes)
        episodes.append(
            {
                "number": ep["number"],
                "id": ep["id"],
                "title": _redact(ep.get("title") or "", _KEEP_NONE, counter),
                "sceneIds": [s["id"] for s in ep_scenes],
            }
        )

    return {
        "series": _redact(export.get("series") or "", _KEEP_NONE, counter),
        "style": {
            "globalPreamble": "photoreal cinematic, soft natural light, 35mm",
            "banned": "text, watermark, extra fingers",
        },
        "characters": [_character(c, counter) for c in bible["characters"]],
        "locations": [_location(loc, counter) for loc in bible["locations"]],
        "props": [_prop(p, counter) for p in bible["props"]],
        "episodes": episodes,
        "scenes": scenes,
    }


def _write_placeholder_refs(story: dict) -> None:
    refs_dir = OUT_DIR / "refs"
    refs_dir.mkdir(parents=True, exist_ok=True)
    names = set()
    for c in story["characters"]:
        for lk in c["looks"]:
            if lk.get("refImage"):
                names.add(pathlib.Path(lk["refImage"]).name)
    for loc in story["locations"]:
        for v in loc["views"]:
            names.add(pathlib.Path(v["uri"]).name)
    for p in story["props"]:
        if p.get("uri"):
            names.add(pathlib.Path(p["uri"]).name)
    for name in sorted(names):
        (refs_dir / name).write_bytes(b"\x89PNG")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: redact_corpus.py /path/to/manifest.json", file=sys.stderr)
        raise SystemExit(2)
    export_path = pathlib.Path(sys.argv[1])
    export = json.loads(export_path.read_text(encoding="utf-8"))
    story = transform(export)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "story.json").write_text(
        json.dumps(story, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    _write_placeholder_refs(story)
    print(
        f"wrote {len(story['scenes'])} scenes, {len(story['episodes'])} episodes to {OUT_DIR}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
