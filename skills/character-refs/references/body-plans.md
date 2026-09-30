# Non-human anatomy — `bodyPlan` (reference)

A character's reference sheet lays out a fixed panel structure — a hero head/face
close-up, a head-rotation grid, several full-body panels, side and rear angles. That
layout is built around a specific anatomy, and by default it assumes a **person**: a
standing biped with arms, hands and a T-pose. Set `bodyPlan` on a non-human character
in `bible.json` **before** generating its primary sheet, or the sheet comes back with
that anatomy anyway — a dog standing upright on two legs with human arms, because
nothing told the layout otherwise.

There is no separate CLI flag for this — `bodyPlan` is a field on the character entry in
`bible.json`, and `shotkit sheet` reads whatever value is set there each time it runs. If
you change it after a sheet already exists, the next `shotkit sheet` run for that
character simply builds the prompt for the new plan; there's nothing else to reset.

## The four plans

- **`humanoid`** — the default. Any unset or unrecognised value degrades to this, so an
  ordinary human character needs no `bodyPlan` field at all.
- **`quadruped`** — a four-legged animal (a dog, a horse, a lion). The sheet drops the
  T-pose and arms entirely: full-body panels show the animal standing squarely on all
  four legs, and the layout gives the left/right profile panels extra width, because a
  quadruped's silhouette carries more identity than its frontal view does — the opposite
  of a human sheet.
- **`wingedQuadruped`** — four legs plus wings (a griffin, a dragon). Same four-legged
  base as `quadruped`, with one full-body panel showing the wings folded and another
  showing them fully spread — a folded-only sheet gives a video model nothing to animate
  a wingbeat from.
- **`avian`** — a bird. Two legs, not four, plus wings; one panel folded, one panel
  spread, and a perched pose in place of a walking gait.

Every non-humanoid plan carries an explicit anatomy guard in the prompt — "no T-pose, no
arms, no hands, no fingers, no human shoulders spread horizontally, no upright bipedal
stance." **Reasoning, not independently verified:** the guard exists as a negative
alongside the positive description because the observed failure (an unset `bodyPlan`
producing a standing, armed dog) suggests a positive description of the anatomy alone
may not be enough to hold it — the working assumption is that stating the humanoid
defaults are explicitly OFF does more than describing the correct anatomy on its own.

## Setting it

```json
{
  "id": "rex",
  "name": "Rex",
  "canonicalDescription": "A large grey wolfhound, wiry coat, one torn ear.",
  "bodyPlan": "quadruped",
  "looks": [{"label": "primary", "description": "no collar", "refImage": ""}]
}
```

Set `bodyPlan` before running `shotkit sheet rex --look primary` for the first time.
Generating the primary sheet with the wrong plan set (or none) wastes a render on a
sheet built for the wrong anatomy — fix `bodyPlan` and re-run rather than trying to
prompt your way out of a humanoid-laid-out sheet after the fact.
