# Frame guards — five wording rules for a single still frame (reference)

These five rules are about **wording a still-frame prompt** so an image model doesn't
misread it — `scenePrompt` as rendered by `shotkit frame` / `shotkit poster`, and the
keyframe prose you write for a seeded `i2v` / `ref-anchored` scene. They are separate
from the video-motion craft in SKILL.md and `failure-modes.md`: a still frame is
generated in complete isolation, with no memory of any other frame, so every one of
these failures shows up as a single bad image, not a bad clip.

Each rule below states the constraint, the failure it prevents, and a wrong/right pair.

## 1. Never say "insert" for a detail shot

**Rule.** When a beat calls for an extreme close-up of one detail — a ring, a note, a
key turning in a lock — never use the word "insert" to describe the framing. Word it as
a full-frame extreme macro that fills the whole image.

**Failure it prevents.** Image models read "insert" as a *layout* instruction, not a
shot-size instruction: they render a small picture-in-picture box — a little inset
photo — floating inside a larger frame, because that is what "insert" means in a page
layout, not in film grammar. The detail you wanted to fill the frame instead occupies a
quarter of it, boxed.

**Wrong:**
> An insert of the wedding ring on the table, catching the light.

**Right:**
> Full-frame extreme macro close-up of the wedding ring on the table, filling the frame
> edge to edge, catching the light — NOT an inset, no split screen, no picture-in-picture.

## 2. State the eyeline in any two-person frame

**Rule.** In any frame with two people who are looking at, talking to, or reacting to
each other, say explicitly where each of them is looking — "each looks at the other,
off-lens, no eye contact with the lens." When one of them deliberately looks away,
anchor the averted gaze to a concrete point ("eyes on the floor display"), never to
nothing.

**Failure it prevents.** Image models default an unposed face to staring straight into
the lens. Left unstated, two people "talking" in one frame both look at the camera
instead of at each other, and the frame reads as two separate POV shots glued together
rather than a scene between them. An averted gaze with no anchor reads as vacant or
dead-eyed for the same reason: the model has nowhere to point the eyes, so it defaults
toward the lens again or renders a blank stare.

**Wrong:**
> Mira and Dev stand in the kitchen, mid-conversation, warm evening light.

**Right:**
> Mira and Dev stand in the kitchen, mid-conversation, warm evening light. Each looks at
> the other, off-lens — no eye contact with the lens. Mira's chin is tilted slightly up
> toward Dev; Dev's gaze is level with hers.

## 3. Lock screen-left/right and facing across frames of one moment

**Rule.** When several frames cover one moment or one location from different angles,
pick and repeat, verbatim, each subject's screen-left/screen-right side and which way
they face, in every one of those frames. A cut-in, a push-in, or an over-the-shoulder
does **not** flip which side someone is on — only a deliberate, true 180° reverse angle
does, and only when you actually intend one.

**Failure it prevents.** Every still frame is generated with no knowledge of any other
frame. If frame 2's prompt doesn't repeat frame 1's blocking, the model is free to place
the same two people on whichever sides look natural for that single image — and half
the time it picks the opposite arrangement. Across a sequence of frames meant to be the
same moment, the subjects appear to teleport across the space from one frame to the
next.

**Wrong (frame 1, then frame 2 of the same conversation):**
> Frame 1: Rae stands on the left, facing right, arguing with Sam on the right, facing left.
> Frame 2 (a closer angle on Rae): Rae stands on the right, facing left.

**Right:**
> Frame 1: Rae stands screen-left, facing screen-right, arguing with Sam, screen-right,
> facing screen-left.
> Frame 2 (a closer angle on Rae, same moment — a push-in, not a reverse): Rae stands
> screen-left, facing screen-right, same as the wider frame; Sam remains screen-right,
> out of frame or at the edge.

## 4. Describe each subject exactly once per frame

**Rule.** Name and describe every present character or object a single time in a
frame's prompt. Do not mention them again through a second role or action phrase later
in the same prompt, even if it feels like you're just adding detail.

**Failure it prevents.** An image model treats a second description of "a woman in a red
coat" as a second person to render, even when you meant the same woman doing a second
thing. The model has no way to know the two mentions are the same subject — it renders
two of them. On a reverse angle where a second subject is present but out of focus,
describe them as an anonymous figure, not by re-invoking their name or role a second
time.

**Wrong:**
> Elena leans against the doorway, arms crossed. Further back, a woman in a green dress
> watches the argument from the hallway.
> (— when "a woman in a green dress" was meant to be Elena again, seen a second way.)

**Right:**
> Elena leans against the doorway, arms crossed, watching the argument play out in the
> hallway ahead of her.

For a genuine second, unnamed person in the background of a reverse angle:

> In the foreground, Elena leans against the doorway, arms crossed. Deep in the
> hallway behind her, a single out-of-focus figure passes — not a named character.

## 5. Describe each location angle fully — never by reference to another shot

**Rule.** Every frame that shows a location, or a new angle of one, must describe that
angle completely and concretely on its own terms. Never write "the same room as
before," "identical to the front," or any other phrase that points at a different
prompt for the details.

**Failure it prevents.** Each frame is generated in total isolation — the model
rendering frame 2 has never seen frame 1's prompt or its output. "Same as before" names
nothing this frame's model can act on, so it invents a room from scratch: a different
layout, different furniture, different light. A front view and its reverse angle are, to
the model, effectively two different places unless you write out what's actually in each
one.

**Wrong:**
> Reverse angle, same room as before, looking back toward the door.

**Right:**
> Reverse angle of the study: floor-to-ceiling bookshelves along the back wall, a worn
> leather armchair in the near-left corner, tall windows out of frame to the right, warm
> lamp light spilling across the rug — looking back toward the door.

If the location has a saved reference image, `@mention` it instead of re-describing it
from memory — see the main SKILL.md's "Location views & the reference budget" section
for how a reference view keeps this consistent across shots instead of relying on
prose.
