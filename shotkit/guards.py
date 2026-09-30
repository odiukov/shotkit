"""Prompt construction guards.

Pure: no I/O, no external imports.
Encodes generative-model failure modes fixed by prompt wording:
  - i2v seed discipline
  - audio-bake discipline
  - dialogue parsing and lint
"""

from __future__ import annotations

import re
from typing import Optional

# Beyond this a time-stretched voiceover sounds chipmunky. Inlined from the tool's
# app/domain/audio/vo_fit.py so this module has no dependencies.
MAX_TEMPO = 1.15


# ---------------------------------------------------------------------------
# i2v safety
# ---------------------------------------------------------------------------


def i2v_safety_clause() -> str:
    """Iron rule: animate only what the start frame already contains."""
    return (
        "Animate only what is already visible in this frame; "
        "introduce no new people, objects, vehicles or text. "
        "Keep every subject's exact appearance and wardrobe for the whole clip. "
        "Natural, subtle motion only."
    )


def with_i2v_safety(motion_prompt: str) -> str:
    """Wrap an authored motion prompt with the i2v seed-discipline constraint."""
    m = motion_prompt.strip()
    return f"{m}. {i2v_safety_clause()}" if m else i2v_safety_clause()


# ---------------------------------------------------------------------------
# Keyframe-anchored reference render
# ---------------------------------------------------------------------------


def keyframe_anchor_clause() -> str:
    """Tell a reference-to-video model that reference #1 IS the opening frame.

    The reference path has no seed-frame slot: every image arrives as a peer reference
    (@Image1, @Image2, …). Without this the model treats the keyframe as one more mood
    board image and re-composes the shot.
    """
    return (
        "@Image1 is the EXACT opening frame: reproduce it as frame 0 — same composition, "
        "framing, wardrobe and lighting — then animate onward from it. "
        "The remaining reference images are the characters' exact likeness: every face, "
        "hairstyle and outfit must match them for the whole clip. "
        "Introduce no new people, objects or text. Natural, subtle motion only."
    )


def with_keyframe_anchor(motion_prompt: str) -> str:
    """Wrap an authored motion prompt with the keyframe-as-reference-#1 anchor."""
    m = motion_prompt.strip()
    return f"{m}. {keyframe_anchor_clause()}" if m else keyframe_anchor_clause()


# ---------------------------------------------------------------------------
# Audio discipline
# ---------------------------------------------------------------------------


def no_music_audio_clause() -> str:
    """No-music rule for video models that bake their own audio."""
    return (
        "Audio: only the diegetic environment and ambient sounds of this setting (plus any spoken dialogue). "
        "No music, no score, no soundtrack, no singing or humming."
    )


def with_audio_discipline(motion_prompt: str, generate_audio: bool) -> str:
    """Append the no-music clause when the clip will bake its own audio."""
    return (
        f"{motion_prompt} {no_music_audio_clause()}"
        if generate_audio
        else motion_prompt
    )


# ---------------------------------------------------------------------------
# Lint: music words
# ---------------------------------------------------------------------------

_MUSIC_WORDS = [
    "music",
    "musical",
    "song",
    "sing",
    "sings",
    "singing",
    "melody",
    "tune",
    "hum",
    "hums",
    "humming",
    "chant",
    "chants",
    "chanting",
    "lip-sync",
    "lip-syncs",
]


def lint_music_words(prompt: str) -> list[str]:
    """Return any music/singing words found in the prompt (warns about i2v lip-sync risk)."""
    text = (prompt or "").lower()
    found = []
    for w in _MUSIC_WORDS:
        pattern = r"\b" + w.replace("-", "[- ]?") + r"\b"
        if re.search(pattern, text):
            found.append(w)
    return found


# ---------------------------------------------------------------------------
# stripSpeakerPrefix
# ---------------------------------------------------------------------------

_PREFIX_RE = re.compile(r"^\s*([A-Za-z][A-Za-z .'\-]{0,29}):\s+(\S[\s\S]*)$")


def strip_speaker_prefix(line: str) -> str:
    """Strip a leading 1–3 word NAME: speaker label from a dialogue line."""
    m = _PREFIX_RE.match(line or "")
    name = m.group(1).strip() if m else None
    rest = m.group(2).strip() if m else None
    if name and rest and len(name.split()) <= 3:
        return rest
    return (line or "").strip()


# ---------------------------------------------------------------------------
# parseDialogue
# ---------------------------------------------------------------------------

# Segment shape: {"speaker": str, "kind": "spoken"|"vo", "text": str, "shot": int|None}
# "shot" is an optional [shot N] anchor pinning WHEN the segment lands in a multishot
# clip; None = unanchored (the engine places it, as before anchors existed).

# Speaker label: 1–3 Capitalised words (no period, so "Street." never swallowed), then ": ".
# Must be at string start or preceded by whitespace.
_LABEL_RE = re.compile(r"(?:^|\s)([A-Z][A-Za-z'\-]*(?:\s+[A-Z][A-Za-z'\-]*){0,2}):\s+")

# [shot 2] anchor at the head of a segment's text ("Skye: [shot 2] …", "VO: [shot 3] …").
_SHOT_ANCHOR_RE = re.compile(r"^\s*\[shot\s+(\d+)\]\s*", re.IGNORECASE)


def _strip_shot_anchor(text: str) -> tuple[str, Optional[int]]:
    m = _SHOT_ANCHOR_RE.match(text)
    return (text[m.end() :], int(m.group(1))) if m else (text, None)


def _tag_segment(speaker: str, text: str) -> dict:
    # The anchor may sit before or after the VO: tag; strip it wherever it leads.
    text, shot = _strip_shot_anchor(text)
    # Bare "VO: <words>" (no speaker) — the label regex reads "VO" as a speaker name,
    # but it is the narration tag, not a character.
    if speaker.strip().upper() == "VO":
        return {"speaker": "", "kind": "vo", "text": text.strip(), "shot": shot}
    m = re.match(r"^\s*VO:\s*(\S[\s\S]*)$", text, re.IGNORECASE)
    if m:
        vo_text = m.group(1)
        if shot is None:
            vo_text, shot = _strip_shot_anchor(vo_text)
        return {"speaker": speaker, "kind": "vo", "text": vo_text.strip(), "shot": shot}
    return {"speaker": speaker, "kind": "spoken", "text": text.strip(), "shot": shot}


# "[shot 2] VO:" — anchor written before the VO tag. Normalised to "VO: [shot 2]" so the
# label scan doesn't read "VO" as a new bare speaker and orphan the anchor.
_ANCHOR_BEFORE_VO_RE = re.compile(r"\[shot\s+(\d+)\]\s*VO:\s*", re.IGNORECASE)


def parse_dialogue(raw: str) -> list[dict]:
    """Split a StoryBodard-format dialogue string into ordered, labeled segments."""
    s = re.sub(r"\s+", " ", raw or "").strip()
    if not s:
        return []
    s = _ANCHOR_BEFORE_VO_RE.sub(lambda m: f"VO: [shot {m.group(1)}] ", s)

    marks: list[dict] = []
    for m in _LABEL_RE.finditer(s):
        full = m.group(0)
        lead = len(full) - len(full.lstrip())
        marks.append(
            {
                "name": m.group(1).strip(),
                "label_at": m.start() + lead,
                "text_at": m.end(),
            }
        )

    if not marks:
        seg = _tag_segment("", s)
        return [seg] if seg["text"] else []

    segs: list[dict] = []
    if marks[0]["label_at"] > 0:
        lead_text = s[: marks[0]["label_at"]].strip()
        if lead_text:
            segs.append(_tag_segment("", lead_text))

    for i, mark in enumerate(marks):
        end = marks[i + 1]["label_at"] if i + 1 < len(marks) else len(s)
        text = s[mark["text_at"] : end].strip()
        if text:
            segs.append(_tag_segment(mark["name"], text))

    # A segment that was ONLY an anchor/tag has no words to bake — drop it.
    return [seg for seg in segs if seg["text"]]


def spoken_segments(raw: str) -> list[dict]:
    return [s for s in parse_dialogue(raw) if s["kind"] == "spoken"]


def vo_segments(raw: str) -> list[dict]:
    return [s for s in parse_dialogue(raw) if s["kind"] == "vo"]


def voiceover_from_dialogue(raw: str) -> str:
    """Narrator text from VO-tagged segments, joined."""
    return " ".join(s["text"] for s in vo_segments(raw)).strip()


# ---------------------------------------------------------------------------
# spokenLineClause / narrationClause / withSpokenLine
# ---------------------------------------------------------------------------


def spoken_line_clause(raw_dialogue: str) -> str:
    """Build the §9-safe motion-prompt clause for on-camera lip-synced speech.

    Unanchored segments keep the legacy phrasing (the engine places them). When any
    segment carries a [shot N] anchor, every segment gets its own sentence so the
    anchored ones can name their shot: 'In SHOT 2, <speaker> speaks…'.
    """
    spoken = spoken_segments(raw_dialogue)
    if not spoken:
        return ""
    if not any(s["shot"] for s in spoken):
        if len(spoken) == 1:
            return f'The on-camera character speaks this line aloud, naturally and in sync: "{spoken[0]["text"]}".'
        turns = ", then ".join(
            f'{s["speaker"] or "the next character"} says "{s["text"]}"' for s in spoken
        )
        return f"Each on-camera speaker voices their own line aloud, naturally and in sync, in turn: {turns}."
    parts: list[str] = []
    for s in spoken:
        who = s["speaker"] or "the on-camera character"
        line = f'{who} speaks this line aloud, naturally and in sync: "{s["text"]}".'
        parts.append(f"In SHOT {s['shot']}, {line}" if s["shot"] else line)
    return " ".join(parts)


def narrator_voice_map(characters: list[dict]) -> dict:
    """Build a pure speaker→{gender,voiceNote} map keyed by lower-cased character name.

    Infra (boards.py) passes the project's characters; the domain never touches the store.
    """
    out: dict = {}
    for c in characters or []:
        name = (c.get("name") or "").strip().lower()
        if name:
            out[name] = {
                "gender": (c.get("gender") or ""),
                "voiceNote": (c.get("voiceNote") or ""),
            }
    return out


def _narrator_descriptor(speaker: str, voices: dict | None) -> str:
    """Return the '<gender> (<note>) ' prefix for a VO speaker, or '' when unset/unresolved.

    An empty return means the caller keeps the legacy generic phrasing (backward compatible).
    """
    if not voices or not speaker:
        return ""
    v = voices.get(speaker.strip().lower())
    if not v:
        return ""
    gender = (v.get("gender") or "").strip().lower()
    if gender not in ("male", "female", "neutral"):
        return ""
    label = "gender-neutral" if gender == "neutral" else gender
    note = (v.get("voiceNote") or "").strip()
    return f"{label} ({note}) " if note else f"{label} "


def narration_clause(raw_dialogue: str, voices: dict | None = None) -> str:
    """Build the motion-prompt clause for engine-baked off-screen narration (VO: segments).

    The engine voices this as baked audio (NOT the TTS narrator track). [shot N] anchors pin
    a segment to its shot. When *voices* resolves a segment's speaker to a gender, that gender
    (and any voiceNote) is named so the engine stops flipping the narrator's voice; otherwise
    the phrasing is exactly the legacy generic clause.
    """
    vo = vo_segments(raw_dialogue)
    if not vo:
        return ""
    descs = [_narrator_descriptor(s["speaker"], voices) for s in vo]
    if not any(descs):
        # No gender info → legacy behaviour, byte-for-byte.
        if not any(s["shot"] for s in vo):
            joined = " ".join(s["text"] for s in vo).strip()
            return f'An off-screen narrator voice-over says, no narrator appears on camera: "{joined}".'
        parts: list[str] = []
        for s in vo:
            line = f'an off-screen narrator voice-over says, no narrator appears on camera: "{s["text"]}".'
            parts.append(
                f"In SHOT {s['shot']}, {line}" if s["shot"] else line.capitalize()
            )
        return " ".join(parts)
    # Gendered path: one clause per segment, each carrying its narrator descriptor.
    parts = []
    for s, desc in zip(vo, descs):
        line = f'an off-screen {desc}narrator voice-over says, no narrator appears on camera: "{s["text"]}".'
        if s["shot"]:
            parts.append(f"In SHOT {s['shot']}, {line}")
        else:
            parts.append(line[0].upper() + line[1:])
    return " ".join(parts)


def with_spoken_line(
    motion_prompt: str, raw_dialogue: str, voices: dict | None = None
) -> str:
    """Append the baked-speech clauses (on-camera lines + VO: narration) to a motion prompt."""
    clauses = " ".join(
        c
        for c in (
            spoken_line_clause(raw_dialogue),
            narration_clause(raw_dialogue, voices),
        )
        if c
    )
    if not clauses:
        return motion_prompt
    m = motion_prompt.strip()
    return f"{m} {clauses}" if m else clauses


# ---------------------------------------------------------------------------
# lintDialogueFit
# ---------------------------------------------------------------------------

_WORDS_PER_SEC = 2
_CLIP_CEILING_S = 15


def lint_dialogue_fit(
    raw_dialogue: str, duration_sec: Optional[float] = None
) -> Optional[str]:
    """Warn when baked on-camera speech doesn't fit the clip slot."""
    words = sum(
        len(s["text"].split())
        for s in spoken_segments(raw_dialogue)
        if s["text"].strip()
    )
    if not words:
        return None
    needed = words / _WORDS_PER_SEC
    if needed > _CLIP_CEILING_S:
        return (
            f"spoken dialogue ~{needed:.0f}s exceeds the {_CLIP_CEILING_S}s clip ceiling "
            "— split the line across scenes"
        )
    if duration_sec is not None:
        if needed > duration_sec:
            return (
                f"spoken dialogue ~{needed:.0f}s longer than the {duration_sec}s clip "
                "— it will be cut off; raise duration or trim the line"
            )
        if duration_sec - needed > max(2, duration_sec * 0.5):
            return (
                f"spoken dialogue ~{needed:.0f}s fills under half the {duration_sec}s clip "
                "— the video model (t2v/i2v) may ad-lib gibberish; shorten the clip or add a line"
            )
    return None


_VO_WORDS_PER_SEC = 2.3  # Aura-2 natural pace; tunable (see spec Open Questions)


def lint_vo_fit(
    voiceover_text: str, duration_sec: Optional[float] = None
) -> Optional[str]:
    """Warn when the standalone TTS narrator VO won't fit the scene slot.

    Estimate is word-count based (pre-synthesis, free). Auto-fit compresses up to
    MAX_TEMPO, so a VO fits a slot when needed <= slot * MAX_TEMPO; between slot and
    that ceiling it only fits by speeding up.
    """
    words = len((voiceover_text or "").split())
    if not words:
        return None
    needed = words / _VO_WORDS_PER_SEC
    if duration_sec is not None and duration_sec > 0:
        if needed > duration_sec * MAX_TEMPO:
            return (
                f"voiceover ~{needed:.0f}s longer than the {duration_sec:.0f}s clip "
                "— it will be cut off; trim the narration or raise the duration"
            )
        if needed > duration_sec:
            return (
                f"voiceover ~{needed:.0f}s slightly over the {duration_sec:.0f}s clip "
                f"— it will be sped up (≤{MAX_TEMPO:g}×) to fit; trim for a natural pace"
            )
        return None
    if needed > _CLIP_CEILING_S:
        return (
            f"voiceover ~{needed:.0f}s exceeds the {_CLIP_CEILING_S}s clip ceiling "
            "— split it across scenes"
        )
    return None


# "SHOT 2" markers of a multishot motion prompt — what a [shot N] anchor points at.
_SHOT_MARK_RE = re.compile(r"\bSHOT\s+(\d+)\b", re.IGNORECASE)


def lint_shot_anchors(raw_dialogue: str, motion_prompt: str) -> Optional[str]:
    """Warn when [shot N] anchors point at shots the motion prompt never declares."""
    anchors = sorted({s["shot"] for s in parse_dialogue(raw_dialogue) if s["shot"]})
    if not anchors:
        return None
    shots = {int(n) for n in _SHOT_MARK_RE.findall(motion_prompt or "")}
    if not shots:
        listed = ", ".join(f"[shot {n}]" for n in anchors)
        return (
            f"dialogue anchors {listed} but motionPrompt has no 'SHOT N — …' structure "
            "— write the shots inline or drop the anchors"
        )
    missing = [n for n in anchors if n not in shots]
    if missing:
        miss = ", ".join(str(n) for n in missing)
        have = ", ".join(str(n) for n in sorted(shots))
        return f"dialogue anchors shot(s) {miss} but motionPrompt only declares SHOT {have}"
    return None


# ---------------------------------------------------------------------------
# frameSafetyTail
# ---------------------------------------------------------------------------


def frame_safety_tail(banned: str = "") -> str:
    """Clean-frame + negative tail for a still keyframe."""
    base = "Keep the frame clean of any on-screen text, captions, subtitles, watermarks, logos or UI overlays."
    neg = banned.strip()
    return f"{base}\nAvoid: {neg}" if neg else base


# ---------------------------------------------------------------------------
# referenceLayoutClause
# ---------------------------------------------------------------------------


def reference_layout_clause(num_chars: int = 0) -> str:
    """Stop a still keyframe echoing a multi-panel sheet / turnaround layout.

    Character references are contact sheets (a portrait, a grid of face angles, a
    row of full-body turnarounds), and props generated before the single-frame
    switch are object turnaround boards. Image models otherwise reproduce that
    panel layout — rendering a diptych / split-screen instead of one scene.
    Keyframe-only: the t2v/i2v video path is intentionally fed the sheet and must
    NOT get this. ``num_chars`` (>1) adds an explicit "put all N in one shared
    frame" line — branch/fork scenes @mention several characters, so several
    sheets stack and the grid-echo pull compounds.
    """
    base = (
        "OUTPUT FORMAT — the single most important thing to get right: render ONE "
        "photographic frame, a single continuous image edge to edge. A reference image "
        "here IS a multi-panel character sheet (one large hero portrait, a grid of head "
        "angles, a row of full-body turnaround poses) or an object sheet — it is a "
        "REFERENCE for identity ONLY. Read a character sheet only for the person's face, "
        "hair and wardrobe; read an object sheet only for the object's shape, colour and "
        "material. Do NOT reproduce its layout in ANY form: no grid, no panels, no gutters "
        "or dividers, no insets, no split-screen, no diptych, no contact sheet, no collage, "
        "no thumbnail strip, no repeated angles of the same subject, no character-sheet "
        "layout. Render exactly ONE instance of each character and each object, posed "
        "naturally inside the single scene."
    )
    if num_chars > 1:
        base += (
            f" There are {num_chars} characters in this frame — place all {num_chars} of "
            "them together in the same single shared frame, interacting in one scene; never "
            "as separate panels, insets or side-by-side portraits."
        )
    return base


# ---------------------------------------------------------------------------
# Prompt-field lints (export-pipeline-hardening)
# ---------------------------------------------------------------------------

# Cyrillic, CJK, kana, Hangul, Arabic — scripts that silently degrade the video
# model's understanding. Accented Latin (café) is fine and NOT matched.
_NON_LATIN_RE = re.compile(r"[Ѐ-ӿ぀-ヿ㐀-䶿一-鿿가-힯؀-ۿ]")

_CUT_RE = re.compile(
    r"\b(cut to|hard cut|smash cut|match cut|cut back)\b", re.IGNORECASE
)


def lint_non_latin(text: str) -> Optional[str]:
    """Reject non-Latin script in prompt fields (all prompt fields must be English)."""
    hits = _NON_LATIN_RE.findall(text or "")
    if not hits:
        return None
    sample = "".join(hits[:8])
    return f"non-English characters in prompt field ({sample!r}) — all prompt fields must be English"


def lint_cut_budget(motion_prompt: str, duration_sec: Optional[float]) -> Optional[str]:
    """Warn when explicit cuts exceed ~1 per 2.5s of clip time."""
    cuts = len(_CUT_RE.findall(motion_prompt or ""))
    budget = max(1, int(round((duration_sec or 5.0) / 2.5)))
    if cuts <= budget:
        return None
    return (
        f"{cuts} cuts in a {duration_sec or 5.0:g}s clip (budget ≈{budget}) — "
        "over-cut multishots strobe; merge shots or extend durationSec"
    )


def lint_no_mentions(motion_prompt: str) -> Optional[str]:
    """Warn when a motion prompt anchors no @references at all."""
    if "@" in (motion_prompt or ""):
        return None
    return (
        "motionPrompt has no @mention — identities will drift; "
        "anchor every on-screen character (and #views where relevant)"
    )


# ---------------------------------------------------------------------------
# Identity-description hygiene
# ---------------------------------------------------------------------------

# Sentences authored FOR the bible editor, not for a generator: "Identity only —
# no clothing here.", "Identity/species only — no rider, no saddle here." They tell
# a human (or the director model) what belongs in canonicalDescription; the field is
# then pasted verbatim into scene and turnaround prompts, where the words survive as
# literal content. "no clothing" next to a description of a person's body reads to a
# provider's pre-generation moderator as a request for the opposite of what it says —
# negation is not reliably parsed — and the whole job comes back rejected as sensitive.
_IDENTITY_DIRECTIVE = re.compile(
    r"(?i)\b(?:identity\s*/\s*species|identity|species|face\s+and\s+hair)\s+only\b"
)
# "No clothing." / "No rider, no saddle." — the directive's own trailing clause when
# the author ended the sentence early. Dropped only in the wake of a directive, so a
# meaningful negation elsewhere ("No beard.") is left alone.
_ONLY_NEGATIONS = re.compile(r"(?i)^(?:(?:and\s+)?no\s+[^,;]+[,;]?\s*)+[.!?]*$")
_SENTENCE = re.compile(r"[^.!?]*[.!?]+|[^.!?]+$")


def clean_identity_description(description: str) -> str:
    """Drop bible-authoring directives from a canonical description before prompting.

    Returns the description with every "Identity only …" sentence (and the bare "no X"
    clause trailing one) removed, whitespace normalised. Everything else is preserved
    verbatim — this strips instructions, it does not rewrite the author's prose.
    """
    kept: list[str] = []
    dropped_previous = False
    for m in _SENTENCE.finditer(description or ""):
        s = m.group(0).strip()
        if not s:
            continue
        if _IDENTITY_DIRECTIVE.search(s):
            dropped_previous = True
            continue
        if dropped_previous and _ONLY_NEGATIONS.match(s):
            continue
        dropped_previous = False
        kept.append(s)
    return " ".join(kept)
