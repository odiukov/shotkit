"""The crop band a vertical poster is shown through when a story-card UI crops it.

A 9:16 poster is often generated at full height but displayed through a LANDSCAPE
card, so only a horizontal band of it is ever on screen. The band's height is fixed
by the card geometry; its vertical position is the author's `focusY` (0 = band at
the very top of the poster, 1 = at the very bottom).

A shotkit user has no particular card of their own, so the constants below are the
Short Drama story-card's geometry, kept as the default because they are the numbers
`compose_clause`'s wording was tuned against. `compose_clause` stays available and
parameterised, but is meant to be emitted only when the scene actually asks for a
crop band (e.g. a `posterFocusY` field present in the scene data).
"""

from __future__ import annotations

# Poster pixels, as generated (9:16).
POSTER_W = 1152
POSTER_H = 2048

# The widest phone we design for (440pt logical width, e.g. iPhone Pro Max) minus the
# list's 16pt padding on each side. Widest device = shortest visible band, so a frame
# drawn from these numbers is what EVERY phone is guaranteed to show. Narrower phones
# reveal a little more above and below, never less: the card is 280pt tall on every
# screen, so a narrower one scales the poster down further and its 280pt cover a taller
# slice. An iPhone 16 Pro (402pt) shows 16%–59% where this band says 17%–56%.
#
# The prompt below deliberately keeps to this guaranteed band — asking for atmosphere in
# an area a narrow phone happens to reveal costs nothing, while composing for the narrow
# phone would push faces out of frame on a Pro Max. The preview does NOT: posterCrop.ts
# draws this band solid inside a dashed CARD_W_NARROWEST one, so the author sees the
# range instead of a single frame their own device disagrees with.
CARD_W = 408.0
CARD_H = 280.0

# Of the card's 280pt, the bottom 112 sit under the title gradient (transparent → the
# surface colour) plus the title/description block. Pixels there are technically
# visible but unreadable as art.
CARD_SCRIM_H = 112.0

DEFAULT_FOCUS_Y = 0.28


def band_fraction() -> float:
    """How much of the poster's height the story card shows (0..1)."""
    # cover-scale is driven by width here: the card is wider-than-tall, the poster is
    # far taller-than-wide, so the image is scaled to the card's width and overflows
    # vertically. Rendered height = CARD_W * (POSTER_H / POSTER_W).
    rendered_h = CARD_W * (POSTER_H / POSTER_W)
    return CARD_H / rendered_h


def crop_band(focus_y: float = DEFAULT_FOCUS_Y) -> tuple[float, float]:
    """(top, bottom) of the visible band as fractions of the poster's height."""
    f = min(1.0, max(0.0, focus_y))
    frac = band_fraction()
    top = f * (1.0 - frac)
    return top, top + frac


def clean_band(focus_y: float = DEFAULT_FOCUS_Y) -> tuple[float, float]:
    """The part of the visible band that is NOT under the title gradient."""
    top, bottom = crop_band(focus_y)
    return top, bottom - (bottom - top) * (CARD_SCRIM_H / CARD_H)


def compose_clause(focus_y: float = DEFAULT_FOCUS_Y) -> str:
    """Prompt sentence telling the model to put the subject where the card will show it."""
    top, bottom = crop_band(focus_y)
    clean_top, clean_bottom = clean_band(focus_y)

    def pct(v: float) -> int:
        return int(round(v * 100))

    return (
        "Composition constraint — the story-list card crops this poster to a horizontal band: "
        f"only {pct(top)}%–{pct(bottom)}% of the frame height is ever on screen, and the lower "
        "part of that band is covered by a title gradient. Place the subject's face and every "
        f"key detail between {pct(clean_top)}% and {pct(clean_bottom)}% from the top, and keep "
        "that area free of text or empty sky. The top "
        f"{pct(top)}% and bottom {pct(1.0 - bottom)}% are cropped away — put only atmosphere there."
    )
