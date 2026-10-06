"""Domain mention helpers.

Pure: resolves @id / @name mentions in free text. No I/O.
Project identifiers and names use English letters only.
"""

from __future__ import annotations

import re
from typing import Union


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
# A view selector parsed from a mention suffix:
#  - 'primary'  -> bare `@id` (the default reference view)
#  - 'all'      -> `@id*` (every stored view, capped later by the ref budget)
#  - {'label': str}  -> `@id#label` (the one stored view whose label matches)
ViewSel = Union[str, dict]  # 'primary' | 'all' | {'label': str}

def ref_index(refs: list[dict]) -> dict[str, dict]:
    """Build one unambiguous, case-insensitive namespace for IDs and names."""
    index = {}
    ids = set()
    for ref in refs:
        key = ref["id"].lower()
        if key in ids:
            raise ValueError(f"duplicate entity id {ref['id']!r} (case-insensitive)")
        ids.add(key)
        index[key] = ref
    for ref in refs:
        key = (ref.get("name") or "").strip().lower()
        if not key:
            continue
        if key in index and index[key] is not ref:
            raise ValueError(f"ambiguous entity name {ref['name']!r}: conflicts with another name or id")
        index[key] = ref
    return index


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _build_pattern(refs: list[dict]) -> str:
    """Return the combined token pattern for named refs + generic id."""
    named = [r for r in refs if (r.get("name") or "").strip()]
    # Sort names longest-first so "@Red Key" wins over a hypothetical "@Red".
    sorted_names = sorted(named, key=lambda r: len(r["name"]), reverse=True)
    name_alts = [re.escape(r["name"]) for r in sorted_names]
    # Always emit BOTH capture groups (named-alt | generic-id) so group indices stay
    # stable for callers that read m.group(2)/m.group(3). When there are no named refs
    # we make group 1 a never-matching branch `(?!)` instead of dropping it — otherwise
    # the group count shifts and mentioned_ref_ids/strip_mentions/parse_ref_mentions
    # raise IndexError on any @mention.
    joined = "|".join(name_alts) if name_alts else r"(?!)"
    # The trailing lookahead is load-bearing. Alternation is ordered, so without it a ref
    # NAMED "Anna" latches onto the prefix of "@anna_new" and wins — the generic-id branch,
    # which would have read the whole token, never runs. The mention then resolves to the
    # BASE character (wrong reference image into the scene) and strip_mentions leaves the
    # "_new" tail dangling. A mention must end at a non-token character.
    return rf"@(?:({joined})|([A-Za-z0-9_-]+))(?![A-Za-z0-9_-])"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def mentioned_ref_ids(text: str, refs: list[dict]) -> set:
    """Resolve `@id` / `@name` mentions to the set of matched ref ids."""
    out: set[str] = set()
    if not text:
        return out
    by_key = {key: ref["id"] for key, ref in ref_index(refs).items()}

    pat = _build_pattern(refs)
    for m in re.finditer(pat, text, flags=re.IGNORECASE):
        token = (m.group(1) or m.group(2) or "").lower().strip()
        ref_id = by_key.get(token)
        if ref_id:
            out.add(ref_id)
    return out


def strip_mentions(text: str, refs: list[dict]) -> str:
    """Replace resolved `@id`/`@name` mentions with the entity's display name.

    Drops any trailing `#label` or `*` view selector. Unknown @tokens are left
    untouched. Intended to clean the outgoing copy sent to image/video models.
    """
    if not text:
        return text
    by_key = {key: ref.get("name") or ref["id"] for key, ref in ref_index(refs).items()}

    tok = _build_pattern(refs)
    # Consume any trailing `#label` / `*` selector along with the `@`.
    pat = rf"(?:{tok})(?:#[A-Za-z0-9_-]+|\*)?"

    def _replace(m: re.Match) -> str:
        token = (m.group(1) or m.group(2) or "").lower().strip()
        return by_key.get(token, m.group(0))  # unknown mention: leave as-is

    return re.sub(pat, _replace, text, flags=re.IGNORECASE)


def parse_ref_mentions(text: str, refs: list[dict]) -> list[dict]:
    """Resolve `@id` / `@id#view` / `@id*` mentions to entities + view selectors.

    Returns one entry per matched id; if an id appears both bare and with an
    explicit selector, the explicit one wins.
    """
    if not text:
        return []
    by_key = {key: ref["id"] for key, ref in ref_index(refs).items()}

    tok = _build_pattern(refs)
    # Optional trailing selector: `#label` or `*`, directly after the id/name.
    pat = rf"(?:{tok})(#[A-Za-z0-9_-]+|\*)?"

    sel: dict[str, ViewSel] = {}
    for m in re.finditer(pat, text, flags=re.IGNORECASE):
        token = (m.group(1) or m.group(2) or "").lower().strip()
        ref_id = by_key.get(token)
        if not ref_id:
            continue
        suffix = m.group(3)  # group 3 is the optional selector
        if suffix == "*":
            view: ViewSel = "all"
        elif suffix and suffix.startswith("#"):
            view = {"label": suffix[1:].lower()}
        else:
            view = "primary"
        prev = sel.get(ref_id)
        # Explicit selector overrides a bare 'primary' seen earlier.
        if prev is None or (prev == "primary" and view != "primary"):
            sel[ref_id] = view

    return [{"id": ref_id, "view": v} for ref_id, v in sel.items()]


# ---------------------------------------------------------------------------
# Reference issues — port of web/ui/src/viewmodels/prompt.ts::promptRefIssues
# ---------------------------------------------------------------------------
# This scan MUST agree with `parse_ref_mentions` above, token for token — it is the
# source of both the editor's red error chips (the "erroneous tags" a director sees)
# and the batch-generate eligibility filter. Any disagreement tells the author one
# story while the generator acts on another.
#
# It used to deliberately use a SIMPLER regex to mirror the editor's own tokenizer.
# That was the bug, not the design: the editor read `@Cleo's auto door` as the
# character `@Cleo` while this resolver read the location `Cleo's Auto` (longest-name-
# first alternation matches across the apostrophe), so the UI chipped one entity and a
# different entity's reference went to the model. The tool this was ported from fixed
# its own editor (web/ui/src/viewmodels/prompt.ts::buildMentionRe) to share this exact
# pattern — that file lives in a different, private repo this one has no access to, so
# it cannot be "kept in lockstep" from here; this note is historical context for why
# the regex is built this way, not a cross-repo maintenance obligation.


def prompt_ref_issues(text: str, refs: list[dict]) -> dict:
    """Reference problems in a prompt, mirroring prompt.ts::promptRefIssues.

    `refs` entries carry `{id, name, has_image}`. Returns:
      - `unknown`: `@token`s that resolve to no entity (broken references)
      - `missing`: display names of entities that resolve but have NO reference image

    Both block a single-scene generate today, so both make a scene ineligible for
    the "generate all videos" batch.
    """
    unknown: list[str] = []
    missing: list[str] = []
    by_key = ref_index(refs)
    # Same token shape as parse_ref_mentions: consume the optional `#label`/`*` selector
    # so a look tag is never mistaken for a broken reference of its own.
    pat = rf"(?:{_build_pattern(refs)})(?:#[A-Za-z0-9_-]+|\*)?"
    for m in re.finditer(pat, text or "", flags=re.IGNORECASE):
        token = (m.group(1) or m.group(2) or "").strip()
        ent = by_key.get(token.lower())
        if ent is None:
            unknown.append(f"@{token}")
        elif not ent.get("has_image"):
            missing.append(ent.get("name") or f"@{token}")
    return {"unknown": unknown, "missing": missing}
