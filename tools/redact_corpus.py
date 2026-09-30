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

Everything else — shot descriptions, dialogue lines, episode/scene titles,
character/location/prop descriptions — is prose, and prose is replaced by a
deterministic filler vocabulary (the NATO alphabet for letters, small synthetic integers
for digits), run for run. The substitution operates on maximal runs of letters OR digits
outside a kept span: every letter-run becomes one filler word, every digit-run becomes
one filler number, and nothing else about the text moves — no whitespace is added or
removed, no run is merged or split. Because the lints this corpus exists to exercise
(`lint_dialogue_fit`, `lint_vo_fit`) work from `len(text.split())`, a substitution that
never touches whitespace preserves every word count exactly, run for run, without having
to reverse-engineer which specific runs a lint reads.

`synopsis` is dropped entirely, not redacted: `grep -rl synopsis shotkit/` returns
nothing — no shotkit code reads it — so it has no test value, and (having been written
as free narrative prose, not shot-craft jargon) it was the corpus's largest leak surface.
A first version of this script redacted synopsis text-only, which missed digit runs
entirely (a five-times-repeated dollar figure survived verbatim, next to a prop literally
named `cashiers_check` — a real, load-bearing plot fact). Digits are now redacted too,
everywhere outside the spans this module keeps verbatim, which closes that class of leak
for every remaining field — but synopsis was cut outright rather than re-redacted, since
removing a field with zero test value is strictly safer than trusting a second version of
the same transform to have finally found every leak in free prose.
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

# Matches a maximal run of letters OR a maximal run of digits — never both at once, so
# "3600K" is two separate runs ("3600", then "K") and each gets its own, independently
# deterministic replacement.
_WORD_OR_DIGITS_RE = re.compile(r"[A-Za-z][A-Za-z']*|\d+")

# Digit-run filler: strictly increasing synthetic integers starting from a base chosen
# to sit ABOVE any plausible in-story number (camera angles 0-360, colour temperatures in
# the thousands, a six-figure cashier's check) — not merely above the shot/timecode
# counts this corpus uses. A small sequential base (10, 11, 12, ...) was tried first and
# rejected: with several hundred digit runs across 49 scenes, it collided by coincidence
# with ordinary 2-3 digit camera-angle values that also appear, unredacted, in the real
# export (e.g. a real "220" from "220 km/h" and a filler "220" from the sequence landing
# on the same integer by chance) — a false-positive class the leak scan below exists to
# catch, and did. A six-digit base leaves no plausible overlap with anything in this
# corpus's domain, and is never revisited, so it cannot coincidentally reproduce ANY real
# figure from the source, small or large.
_DIGIT_FILLER_BASE = 900001


class _Counter:
    def __init__(self) -> None:
        self.n = 0
        self.d = 0

    def next_word(self) -> str:
        w = _FILLER[self.n % len(_FILLER)]
        self.n += 1
        return w

    def next_digits(self) -> str:
        v = _DIGIT_FILLER_BASE + self.d
        self.d += 1
        return str(v)


def _redact_prose(text: str, counter: _Counter) -> str:
    """Replace every letter-run and every digit-run in *text* with filler, in place.

    Whitespace and punctuation are untouched, so `len(text.split())` before and after
    is identical by construction — each run (whatever its content) is replaced by
    exactly one whitespace-free token, one-for-one.
    """

    def repl(m: re.Match) -> str:
        orig = m.group(0)
        if orig[0].isdigit():
            return counter.next_digits()
        w = counter.next_word()
        return w.capitalize() if orig[0].isupper() else w

    return _WORD_OR_DIGITS_RE.sub(repl, text)


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


def _filler_phrase(counter: _Counter, n: int = 3) -> str:
    """*n* filler words, capitalised as a sentence, for a field with no source text at
    all (a made-up description, a style preamble) — built straight from the filler
    vocabulary rather than an authored English sentence run through `_redact`, so this
    script's OWN boilerplate can never coincidentally contain a real word that also
    happens to appear in the source text (the leak scan below flags exactly that class
    of false positive, and it once did: "light"/"soft"/"fingers" from an earlier,
    English-language version of this boilerplate)."""
    words = [counter.next_word() for _ in range(n)]
    return (words[0].capitalize() + " " + " ".join(words[1:]) + ".").strip()


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------


def _character(c: dict, counter: _Counter) -> dict:
    return {
        "id": c["id"],
        "name": c["name"],
        "canonicalDescription": _filler_phrase(counter),
        "bodyPlan": "humanoid",
        "looks": [
            {
                "label": "primary",
                "description": _filler_phrase(counter, n=2),
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
        "canonicalDescription": _filler_phrase(counter),
        "lightingProfile": _filler_phrase(counter, n=2),
        "views": [{"label": "primary", "uri": f"refs/{loc['id']}-primary.png"}],
    }


def _prop(p: dict, counter: _Counter) -> dict:
    return {
        "id": p["id"],
        "name": p["name"],
        "canonicalDescription": _filler_phrase(counter),
        "uri": f"refs/{p['id']}.png",
    }


def _scene(s: dict, loc_id_by_name: dict, counter: _Counter) -> dict:
    # `synopsis` is dropped, not redacted — see the module docstring. No shotkit code
    # reads it, and it was the corpus's largest leak surface.
    return {
        "id": s["id"],
        "locationId": loc_id_by_name.get(s.get("location"), ""),
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
            "globalPreamble": _filler_phrase(counter, n=4),
            "banned": _filler_phrase(counter, n=3),
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


# ---------------------------------------------------------------------------
# Leak scan — an independent check, not sharing the redactor's own assumptions
# ---------------------------------------------------------------------------
# This does NOT reuse `_WORD_OR_DIGITS_RE`, `_redact`, or any of the KEEP patterns
# above: it re-derives every token (alphabetic, numeric, or mixed) straight from the
# ORIGINAL export's free-text fields and asserts none of them survives verbatim in the
# redacted output's STRING VALUES, except a short, hand-written allow-list. A scan that
# reused the redactor's own "what counts as a word" definition could only ever confirm
# the redactor's own assumptions — which is exactly how a five-times-repeated digit run
# (a dollar figure, next to a prop named `cashiers_check`) made it into a committed file
# despite an earlier, narrower, alphabetic-only leak scan passing clean.
_TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9']{2,}")
_MENTION_LABEL_RE = re.compile(r"@[\w-]+(?:#([\w-]+)|\*)?")


def _iter_strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _iter_strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _iter_strings(v)
    elif isinstance(o, str):
        yield o


def _allow_list(export: dict) -> set:
    """Every token permitted to survive verbatim, and only those — each one here
    because the brief requires KEEPING it, never because redacting it was inconvenient.
    """
    allow = set()
    # Bible ids and names (characters, locations, props) — kept verbatim by design.
    for kind in ("characters", "locations", "props"):
        for e in export["bible"][kind]:
            for m in _TOKEN_RE.finditer(e["id"] + " " + e["name"]):
                allow.add(m.group(0).lower())
    # `@id#label` label suffixes — part of a mention token kept verbatim in place.
    for ep in export["episodes"]:
        for s in ep["scenes"]:
            for f in ("motionPrompt", "dialogue"):
                for m in _MENTION_LABEL_RE.finditer(s.get(f) or ""):
                    if m.group(1):
                        for t in _TOKEN_RE.finditer(m.group(1)):
                            allow.add(t.group(0).lower())
    # The structural markers this corpus's tests depend on.
    allow.add("shot")
    allow.add("vo")
    return allow


def _verify_no_leaks(export: dict, story: dict) -> set:
    """Return the allow-list used, after asserting no other original token survived.

    Raises SystemExit(1) — loudly, not a warning — if anything outside the allow-list
    is found verbatim in the redacted output, so a future regeneration can't silently
    reintroduce this bug class.
    """
    orig_tokens = set()
    for ep in export["episodes"]:
        for s in ep["scenes"]:
            for f in (
                "scenePrompt",
                "motionPrompt",
                "dialogue",
                "voiceover",
                "synopsis",
            ):
                for m in _TOKEN_RE.finditer(s.get(f) or ""):
                    orig_tokens.add(m.group(0).lower())
        for m in _TOKEN_RE.finditer(ep.get("title") or ""):
            orig_tokens.add(m.group(0).lower())
    for m in _TOKEN_RE.finditer(export.get("series") or ""):
        orig_tokens.add(m.group(0).lower())

    allow = _allow_list(export)
    red_values = " ".join(_iter_strings(story)).lower()

    leaked = [
        tok
        for tok in sorted(orig_tokens)
        if tok not in allow
        and re.search(rf"(?<![a-z0-9]){re.escape(tok)}(?![a-z0-9])", red_values)
    ]
    if leaked:
        print(
            f"LEAK SCAN FAILED: {len(leaked)} original token(s) survived verbatim "
            f"outside the allow-list: {leaked}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(
        f"leak scan clean: 0 of {len(orig_tokens)} original tokens survived "
        f"outside the {len(allow)}-token allow-list",
        file=sys.stderr,
    )
    return allow


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: redact_corpus.py /path/to/manifest.json", file=sys.stderr)
        raise SystemExit(2)
    export_path = pathlib.Path(sys.argv[1])
    export = json.loads(export_path.read_text(encoding="utf-8"))
    story = transform(export)

    _verify_no_leaks(export, story)

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
