---
name: character-refs
description: |
  Keep a character's face, body and wardrobe stable across every generated image by
  building and reading role-labelled reference images (`refKit`) and named looks, and by
  setting the right anatomy plan before the first sheet renders. Load when the user is
  setting up a new character, asking why a character's face/build/outfit keeps drifting
  or swapping between renders, building or ordering a character's reference photos, adding
  a costume/state variant (a look), or working with a non-human character (an animal,
  a winged creature, a bird) whose reference sheet keeps coming back standing upright
  like a person.
---

# Character reference craft

## Consistency is a reference image, not prose

A character keeps the same face across shots for exactly one reason: a reference image
of that face conditions the render. No amount of prose fixes this. "She has the same
sharp cheekbones and grey eyes as always" is a sentence an image model reads fresh every
time, with nothing to compare it to — it is free to invent slightly different
cheekbones and eyes on every single render. A reference image is the only thing that
carries a face, a build, or a hairstyle from one generation to the next.

This is why the whole discipline in this skill exists: get one good reference image (or
a small labelled set of them) onto a character, and use it — everything else here is
about how to build that reference set correctly and how to make sure it actually
attaches to the render you're about to make.

## `canonicalDescription` is identity; clothing is a look

A character's `canonicalDescription` (in `bible.json`) is **identity only** — face,
hair, build, age. It is never clothing, and it never changes because a character puts on
a coat, gets soaked in the rain, or ages twenty years across the story. Those are
**looks**: named entries in the character's `looks` list, each with its own
`description` (the wardrobe/state text) and its own `refImage`.

A costume change or a durable state change (soaked, bloodied, in a wedding gown, aged
twenty years) is a new **look** on the same character. It is never a second character —
a second character entry has no path back to the original's face reference, and you'd be
starting the whole identity problem over from nothing.

The `primary` look is the default and must be generated first. Every other look
conditions on the primary's reference to hold the same face while the wardrobe changes
— generate `primary` before any other look, or the others have nothing correct to anchor
to.

## A tagged look injects its wardrobe text; a bare mention does not

`shotkit` keeps this distinction on purpose: mentioning a character with a look tag
(`@id#label`, e.g. `@mira#wedding`) pulls that look's `description` into the prompt as
wardrobe text alongside the reference image. A bare mention (`@mira`) attaches the
character's primary reference image but injects **no** wardrobe prose at all.

This matters because naming a garment in prose for a character who already has a
reference image is exactly the failure this whole discipline exists to prevent: a
concrete clothing word in the prompt text is read by the model as an instruction, and an
instruction beats a reference image every time. Describe the character's action or state
and let the reference dictate the costume; reach for a look tag only when you actually
want that look's wardrobe text to override what the bare reference would otherwise wear
in the shot.

## Role-labelled references

A single reference image can only show one thing — a face, a body, a garment — and
mixing several of those into one photo (a person modelling a coat) hands the model an
ambiguous instruction about what to copy. `shotkit`'s `refKit` lets you attach several
narrowly-scoped reference images to a character, each tagged with a **role** that tells
the render exactly what to take from it and what to ignore.

See `references/ref-roles.md` for the six roles, the two independent counting buckets,
the manifest contract that makes slot order load-bearing, and the real failure this
mechanism was built to stop.

## Non-human anatomy

A character that isn't human — an animal, a winged creature, a bird — needs its
`bodyPlan` set **before** its primary reference sheet is generated, or the sheet comes
back built for a humanoid: a dog standing upright with arms. See
`references/body-plans.md` for the four plans and when each applies.

## The workflow

1. Edit the character's entry in `bible.json` — identity in `canonicalDescription`,
   anatomy in `bodyPlan`, wardrobe/state variants in `looks`, and any role-labelled
   reference photos in `refKit`.
2. Run `shotkit sheet <character-id> --look <label>` (default label is `primary`). This
   writes `out/characters/<character-id>/<label>.sheet.txt` (the prompt) and
   `out/characters/<character-id>/<label>.sheet.refs.txt` (the reference image paths,
   in order) — or, with `--handoff`, prints both as one paste-ready block instead.
3. Generate that prompt in an image model, attaching the listed reference images **in
   the listed order** — see `prompt-assembly`'s contract for why the order is load-bearing.
4. Save the approved result and point the look's `refImage` at it in `bible.json`.

Generate `primary` first for every character; every other look depends on it.
