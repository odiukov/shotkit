# Motion & dialogue discipline (reference)

## Keyframe = SHOT 1

When a scene has a seed frame (`i2v`, or `ref-anchored` with its `--keyframe`), that
frame **is** the first instant of the clip. An i2v-style render only animates *forward*
from what the still already shows — it cannot cut away to a setup the frame doesn't
contain. If your motion prompt's first beat needs a different composition than the
keyframe shows, the keyframe is wrong, not the motion prompt.

Titles, captions, choice buttons and any other on-screen UI are **post overlays**,
composited after generation. Never write them into a keyframe or a motion prompt asking
the model to render them — a generative video/image model does not render legible,
stable UI text, and even a lucky single frame won't hold across a clip.

## Multishot lives in the motion prompt

To cut between camera angles inside **one** clip, write the shots inline in
`motionPrompt` as a sequence:

```
N-shot sequence in one continuous clip, hard cuts between shots. <setting>.
SHOT 1 — <type>: <action>. HARD CUT.
SHOT 2 — <type>: <action>. HARD CUT.
SHOT 3 — <type>: <action>.
```

One beat is one clip. Don't split a single beat across extra scenes just to get more
cuts — reach for a multishot `motionPrompt` on the one scene instead. Each `SHOT N`
label is also what a `[shot N]` dialogue anchor points at (below), so number them
sequentially from 1.

## Dialogue vs. voiceover — two fields, two different jobs

`dialogue` and `voiceover` are separate scene fields that ask for fundamentally
different things:

- **`dialogue`** is everything meant to be **baked into the clip's own audio** by the
  generator itself, when `generateAudio` is on.
  - A plain speaker-labelled line (`Skye: I never asked for this.`) is **on-camera,
    lip-synced speech** — the character in frame is expected to say it, mouth moving.
  - A `VO:`-prefixed segment (`VO: some words`, or `Skye: VO: some words`) is
    **engine-voiced, off-screen narration**, baked into the same clip's audio but with
    no face on camera saying it.
- **`voiceover`** is a wholly separate narration track, produced by a **separate
  text-to-speech step outside the clip generator** and laid in afterward, never
  lip-synced.

Put narration in **exactly one** of the two, never both on the same scene — that's
double narration. Reach for a `VO:` segment in `dialogue` for a one-off aside baked into
this clip; reach for the `voiceover` field when the same narrator needs to sound
identical across every scene of a story, since a TTS track you hold constant yourself is
the only way to guarantee that. `shotkit` has no built-in voice catalog and does not pin
a narrator's baked voice to anything about the character automatically — if a `VO:`
narrator needs to sound consistent scene to scene, that consistency is on you (or
whatever TTS step renders the separate `voiceover` track), not something `shotkit` tracks
or infers from the character's description.

## `[shot N]` anchors

On a multishot clip, pin *when* a dialogue or narration segment lands with a `[shot N]`
anchor at its head — `Skye: [shot 2] <words>`, `VO: [shot 3] <words>`. The anchor must
point at a `SHOT N` your `motionPrompt` actually declares in its shot list; an anchor
pointing at a shot number the motion prompt never wrote is flagged by `shotkit lint` as
an error. Leaving a segment unanchored is legal — the generator places it at its own
discretion — but on a multishot clip an unanchored segment can land anywhere, so anchor
anything that must speak in a specific shot.

Never anchor an on-camera line and a `VO:` segment to the **same** shot number: with a
face already in that frame, the engine reads both speech events over that one face, and
the narration comes out lip-synced to the wrong character. Give the narration its own
shot — an insert, a reaction, a wide with nobody speaking — inside the same scene.

## Size baked speech to ~2 words per second of clip duration

Every word that gets baked into the clip's own audio (a plain line, a `VO:` segment) has
to fit the time it's spoken over. Budget roughly **2 words per second** of the clip's
duration for baked speech:

- **Too short** for the words it's carrying, and the generator ad-libs or garbles the
  rest to fit the time it has.
- **Too long** for the clip's duration, and the line is simply cut off before it
  finishes.

`shotkit lint` checks the fit for you against the scene's `durationSec` and flags both
directions — too little dialogue for a long, silent-feeling clip, and too much for the
time available.

## No music or singing words in any prompt

Never write "music," "song," "sing," "melody," "chant," "hum," or similar words into a
motion prompt — not even to negate them ("no music"). Two separate reasons:

- Music is a **post-production layer**, laid in during editing, never something a scene
  prompt should be asking a video/image generator to produce.
- On an i2v-style generator that bakes its own audio, these words — even negated — read
  as a push toward a musical or lip-sync register the model then tries to honor, which
  shows up as lip-sync artefacts even in a scene with no singing intended.

You don't need to author a no-music disclaimer yourself: when `generateAudio` is true,
`shotkit` already appends its own audio-discipline clause to the assembled motion prompt.
Where this actually bites is an innocent **ambient** word in your own authored text — "a
radio mid-song," "the refrigerator's hum" — which trips the same lint check that catches
a real music reference. Prefer a synonym that isn't on the list: "whirr," "rumble,"
"roar," "a radio talk-voice" instead of "hum" or "song."
