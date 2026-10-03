# Motion & dialogue discipline (reference)

## Keyframe = SHOT 1

When a scene has a seed frame (`i2v`, or `ref-anchored` with its `--keyframe`), that
frame **is** the first instant of the clip. An i2v-style render only animates *forward*
from what the still already shows — it cannot cut away to a setup the frame doesn't
contain. If your motion prompt's first beat needs a different composition than the
keyframe shows, the keyframe is wrong, not the motion prompt.

Titles, captions and any other on-screen UI are **post overlays**, composited after
generation, not something a keyframe or motion prompt should ask the generator to
render.

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

## Dialogue and narration share one field

All speech lives in `dialogue` and is generated in the clip with `generateAudio: true`.
A plain speaker-labelled line (`Skye: I never asked for this.`) is on-camera,
lip-synced speech. A `VO:` segment (`VO: some words` or `Skye: VO: some words`)
is off-screen narration generated in the same audio track, with no speaking face.

For a named narrator, keep the speaker label consistent and set `gender` and optional
`voiceNote` in `bible.json`. These steer the generated voice but do not guarantee an
identical voice across clips. Narration has no separate field or synthesis step.
Budget the combined spoken and VO text at roughly two words per second.

## `[shot N]` anchors

On a multishot clip, pin *when* a dialogue or narration segment lands with a `[shot N]`
anchor at its head — `Skye: [shot 2] <words>`, `VO: [shot 3] <words>`. The anchor must
point at a `SHOT N` your `motionPrompt` actually declares in its shot list; an anchor
pointing at a shot number the motion prompt never wrote is flagged by `shotkit lint` as
an error. Leaving a segment unanchored is legal — the generator places it at its own
discretion — but on a multishot clip an unanchored segment can land anywhere, so anchor
anything that must speak in a specific shot.

Avoid anchoring an on-camera line and a `VO:` segment to the **same** shot number.
`shotkit` builds one sentence per anchored segment and joins them all into the same
motion prompt — an anchored spoken line becomes "In SHOT 2, `<speaker>` speaks this line
aloud, naturally and in sync: …", and an anchored `VO:` segment becomes "In SHOT 2, an
off-screen narrator voice-over says, no narrator appears on camera: …". Anchor both
kinds to the same `SHOT 2` and the assembled prompt states both sentences about that one
shot — a face speaking in sync, and, in the same breath, narration from someone who
"appears on camera" nowhere. `shotkit lint`'s `lint_shot_anchors` does not catch this: it
only checks that an anchor points at a shot the motion prompt declares, not who else is
anchored there. **This is a recorded observation, not a guess:** this pack's own
`cinematic-scenes/references/failure-modes.md` records the mechanism directly — an
on-camera face already in frame absorbs the VO line as its own lip-synced speech instead
of staying off-screen — and the same rule is repeated in `short-drama-structure/SKILL.md`
and `pov-scenes/SKILL.md`. Give the narration its own shot — an insert, a reaction, a wide
with nobody speaking — inside the same scene, and anchor it there instead.

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
- `shotkit lint`'s music-word check (`lint_music_words`) flags the bare word regardless
  of negation — "no music" trips it exactly like "music" does. **Reasoning, not
  independently verified:** the working assumption behind that design is that a
  generator baking its own audio can read even a negated music word as a push toward a
  musical or lip-sync register, showing up as lip-sync artefacts in a scene with no
  singing intended — which is why the lint doesn't try to parse the negation away.

You don't need to author a no-music disclaimer yourself: when `generateAudio` is true,
`shotkit` already appends its own audio-discipline clause to the assembled motion prompt.
Where this actually bites is an innocent **ambient** word in your own authored text — "a
radio mid-song," "the refrigerator's hum" — which trips the same lint check that catches
a real music reference. Prefer a synonym that isn't on the list: "whirr," "rumble,"
"roar," "a radio talk-voice" instead of "hum" or "song."
