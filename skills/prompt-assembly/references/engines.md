# Choosing a motion mode for your generator (reference)

`shotkit motion` supports three mutually exclusive modes. Picking the right one comes
down to one question: **what shape of input does your target video generator expect?**

## The three modes

- **`t2v`** — no seed frame at all. `shotkit` composes the motion prompt straight from
  your `motionPrompt` text plus whichever reference images your `@mention`s resolve to.
  This is the mode to reach for when your generator takes a text prompt (optionally with
  reference images) and produces a clip with no separate "starting image" input, or when
  you deliberately want the camera free to move, reveal or reframe rather than locked to
  a pre-composed still.

- **`i2v`** — a genuine seed frame exists. Run `shotkit frame` first, generate that
  prompt in an image model, get the still approved, then run `shotkit motion --mode
  i2v` and hand the approved still directly to your video generator's own dedicated
  image-to-video / start-frame input. Use this mode only when your generator actually
  has that separate seed-frame input, and only when you specifically want to lock the
  opening composition before motion starts.

- **`ref-anchored --keyframe PATH`** — the hybrid, for a generator that has **no**
  separate seed-frame input but does accept a flat list of reference images. Generate
  the keyframe exactly as you would for `i2v`, then pass it as `--keyframe`; `shotkit`
  puts that frame first in `out/<stem>.refs.txt` and writes an explicit instruction into
  the prompt that reference #1 IS frame 0 to reproduce and animate onward from. Without
  that instruction, a reference-only generator has no way to know one of its several
  peer reference images is supposed to be the exact opening frame rather than one more
  mood-board image to draw inspiration from — it would just re-compose the shot instead
  of continuing from it. `ref-anchored` always requires `--keyframe`; the CLI refuses
  the mode without one.

## Picking one for a given generator

Ask, in order:

1. **Does the generator have a distinct "starting image" / "image-to-video" slot,
   separate from any reference-image input?** If yes → `i2v`.
2. **Does the generator only take a flat list of reference images, with no separate seed
   slot, but you still want to lock a specific opening composition?** → `ref-anchored`.
3. **Otherwise (no seed slot needed, or you want the freest camera)** → `t2v`, the
   default and, for most scenes, the stronger path — it isn't fighting a pre-composed
   still to produce a push-in, a reveal, or a tilt.

A seed-frame endpoint and a flat reference-image array are usually **mutually
exclusive** features of a given generator's API — that split is exactly why
`ref-anchored` exists as its own mode rather than folding into `i2v`: it's built for the
generator that only offers the second shape but still needs the first behavior.

## Typical duration bounds

Hosted video generators commonly cap clip length somewhere in the 5–10 second range;
others extend to around 15 seconds. Since the exact ceiling varies by generator and
shotkit has no built-in per-model catalog, treat **3–15 seconds** as the permissive
envelope worth designing a scene's `durationSec` around, and check your specific
generator's actual limit before committing to the upper end of that range.

## Typical reference caps and the two-bucket count

Reference-conditioned image and video models commonly bound how many reference images
they'll actually honor per generation — a frequently-seen cap is around 9 images total,
sometimes split into separate caps per bucket (see `character-refs/references/ref-roles.md`
for the two buckets: character-consistency references vs. object-fidelity references).
Past whichever cap your generator enforces, the model doesn't refuse — it silently drops
or blends the surplus, and you get a render that looks plausible but is missing
something you attached. `shotkit` has no built-in catalog of per-model caps (there's no
single generator it assumes), so it can't enforce this for you automatically; when you
know your target generator's real numbers, check your scene's resolved reference count
against them yourself (`out/<stem>.refs.txt` is the ground truth for what actually got
attached) before spending a render on a kit you suspect is oversized.
