---
name: pov-scenes
description: |
  Author first-person / subjective-camera scenes for any video generator — the camera IS a
  character's eyes: a single continuous head-driven take with no cuts, hands/body visible in
  frame, and lens distortion that sells embodiment. Load when the user wants a POV shot,
  first-person perspective, "the camera is her eyes", found-footage / body-cam look, a panic
  or disorientation subjective, a drunk/dizzy/dream POV, or a flashback seen through someone's
  eyes. This skill handles the POV CRAFT; for everything else in the shot (body weight,
  environmental force, references, dialogue sizing) use the cinematic-scenes skill, and for
  episode/beat structure use short-drama-structure.
---

# POV / subjective-camera scene craft

## When to use

Trigger when the shot is **seen through a character's own eyes** — not a camera observing them, but the camera *being* them:

- "POV", "first-person", "the camera is her eyes", "from his point of view"
- "found footage", "body-cam", "helmet-cam", "she's filming it"
- "panic / disorientation / dizzy / drunk / dream POV", "everything spinning"
- "flashback through her eyes", "we see what he sees"

If the camera watches the character from outside, this is a normal observer shot — use **cinematic-scenes**, not this skill. POV is the deliberate exception to "camera as observer".

## Core principle

**POV = ONE continuous head-driven take, the camera literally the character's eyes, with the body in frame to prove it.** Three things make it read as first-person instead of "a low shaky camera near a person":

1. **The camera IS the eyes** — it moves on the neck, looks where attention goes, never floats free.
2. **One unbroken take, no cuts** — a cut to any other angle instantly breaks the first-person illusion (you've left their head).
3. **The body sells it** — their own hands / arms / feet enter frame and act; without that the viewer reads it as third-person.

## The engine fact that defines this skill: most video models DEFAULT to cutting

Left alone, most engines insert angle changes — which **destroys** POV (any cut leaves the character's head). So a POV `motionPrompt` must forbid it **explicitly**, every time:

> "ONE continuous shot, first-person POV, the camera IS [name]'s eyes, **no cuts, no zoom**, natural head movement."

Without `no cuts, no zoom` the engine will cut between angles and the POV collapses. This is non-negotiable and is the single most common POV failure.

## Authoring a POV motionPrompt

Build it as one self-contained `motionPrompt` (the default no-keyframe path, `shotkit motion --mode t2v`; POV is inherently a held take, so it is never a multi-shot):

1. **Open with the lock line.** "ONE continuous shot, first-person POV, the camera IS the viewer's eyes, no cuts, no zoom, natural head movement, 15s, 9:16." **Name the POV character WITHOUT an `@`** (plain "Maya" or "the viewer") — an `@mention` would attach their reference and render them as a second body. The `@` is only for the OTHER characters and the location.
2. **Lens + embodiment optics — but keep the frame FULL-BLEED, never an eye-shaped mask.** A POV reads through a slightly **wide-angle lens with mild distortion** and (sparingly) **subtle chromatic aberration**; add **motion blur on fast head turns**. These sell "this is an eye, not a tripod." **The trap:** the phrase "the camera IS the eyes" plus any cue that draws attention to the **frame edges** ("distortion/aberration/vignette *near the edges*") makes most engines render a literal **eye-shaped / goggle / binocular / porthole mask** — a dark curved border framing the shot, as if peering through eyeholes. POV is a normal full-frame camera view, NOT a mask. So: spread the optics **across the whole image** ("gentle barrel curvature across the whole image"), keep aberration faint and un-localized, and **state the full-bleed lock explicitly**: *"the picture fills the entire rectangular 9:16 frame edge to edge as an ordinary camera view — NO vignette, NO dark border, NO eye-shaped / goggle / binocular / porthole mask, NOT looking through eyeholes; the frame corners stay square and bright."* Avoid the words *vignette / eyeholes / through her eyes* in the optics line.
3. **Head-driven motion, dialed to the emotion** — this is the main performance:
   - **Calm/observing POV:** "gentle natural head movement, small settling micro-drifts, eyeline leads each look, breath even."
   - **Panic/chaos POV:** "hyper-chaotic handheld, completely unstabilized, constant micro-jitters, aggressive head swings, abrupt jerks, frequent over-rotation and harsh correction, near motion-blur loss, no smoothness." (The full-chaos register — only for genuine panic/violence; it is nauseating if overused.)
4. **Own hands visible — entering from the BOTTOM edge ONLY.** The viewer's own hands/forearms come up from the **bottom** of frame (as when you glance down at your own hands), reaching, gripping, wiping the lens — **never reaching in from the left or right side** (side-entry reads as a *second person's* hand). Besides the hands, the only other self-body you may show is a **downward glance** at their own lap, legs, feet, cuffs or wristwatch. Reusable clause to paste into a hands shot: *"first-person POV at eye level, the viewer's own hands/forearms entering from the bottom edge of the frame — no face, no shoulders, no torso, not seen from the side or over the shoulder."* Describe what those hands DO each beat.
   - **NEVER describe the POV character's own torso or posture.** No chest, shoulders, back, collar, lapel, tie, and no "seated / leaning back / lying down" — each one forces the model to render a whole second person *with a face* at the frame edge. Their body simply isn't on screen; only hands-from-below and the downward glance exist.
5. **What they look at = the edit.** Since there are no cuts, the "coverage" is the eyeline: she *looks* from the door to the knife to his face — write the look-targets in order, as one continuous sweep, not as separate shots.
6. **Ambient = breath + raw SFX, no score.** POV lives on first-person sound: "Ambient: her own breathing close and fast, cloth rustle as she moves, room tone; raw SFX only, no score." (Music is a post layer anyway — see cinematic-scenes.)

## Identity & references in POV — the inversion

POV inverts the usual identity problem, and the biggest mistake is treating the POV character like a normal cast member:

- **NEVER `@mention` the POV character as a subject in their own POV scene.** Their reference image is a face + body — attach it and the model renders **that person, with a face, a second time** at the edge of frame. That is the #1 first-person failure. The POV character is the *viewer*, not a rendered person; leave them out of the scene's `@mention`s entirely. (They can still exist in the bible for other episodes — just never placed in this frame.)
- **Their hands match by inline PROSE, not a ref.** Since you don't `@mention` them, hand skin-tone and sleeves are held by writing them in every shot ("the viewer's own hands, warm mid-tone skin, rolled white sleeves") — not by an attached face ref.
- **Other characters and the location ARE seen normally** — `@mention` and reference-anchor them exactly as in cinematic-scenes; they still drift without refs. The ref budget is freer here because the POV character takes none.
- **Showing the POV character's own face (reflection) is an advanced, risky move.** A mirror/window/screen reflection is the only way to show their face without cutting out of POV — but because their ref is NOT attached, the reflected face has nothing to match and the model invents a stranger. If you must do it, attach their character ref for *that one reflection shot only* and `@mention` it just there; otherwise avoid the reflection and keep the face unseen.

## Other characters: contact and eyeline come TO the lens

The POV character has no on-screen body, so everything another character does to them must be routed **toward the lens**, not onto a body that isn't there:

- **Contact comes to the camera.** When another character touches, embraces, whispers to, or reaches for the POV character, only **that other character's** hand / arm / face enters frame toward the lens — "her arm slides into frame past the lens", "his face dips close beside the lens". **Never** write the contact as landing on the POV character's own chest / shoulder / back — those don't exist on screen, and describing them spawns a second visible body.
- **Eyeline goes INTO the lens (the inversion).** Because the camera *is* the POV character's eyes, anyone speaking or reacting TO them looks **straight into the lens** — "she meets the viewer's eyes, looking directly into the lens". In a normal observer shot that dead-to-camera look is a bug; in POV it is the *correct* eyeline. But characters talking **to each other** inside the POV character's view still look **at each other**, not the lens.
- **Reveals must already be in the frame, not walk into an empty one.** Reveal a new character **within the take** — the head turns and they are already in frame as the look lands, or they step toward the lens — never have someone walk into an empty POV frame, especially on i2v, where there's nothing in the start frame to animate and the model hallucinates them in. (POV is one no-cut take, so the reveal is a **head-turn**, not a cut *to* them.)

## Composing with the other skills

- **Body weight, environmental force, grounded performance, reference rules, dialogue/voiceover sizing, vertical 9:16 framing** — all from **cinematic-scenes**. POV does not replace those; it only changes the camera to first-person and forces a single no-cut take.
- **Where a POV scene sits in the episode** (a panic POV as the hook, a subjective flashback as a reveal) — from **short-drama-structure**.
- **Dialogue in POV:** the POV character's own lines are off-screen voice (they have no on-camera face to lip-sync) — never a plain `dialogue` line. Two homes for them: a `VO:`-prefixed `dialogue` segment (`Skye: VO: <line>`) asks a native-audio engine to bake the voice into the clip (the voice still varies clip-to-clip; add a `[shot N]` anchor — `Skye: VO: [shot 2] <line>` — to pin when it lands in a multishot take), or the `voiceover` field (a separate TTS pass, the story-wide narrator voice — consistent across scenes, but it is the NARRATOR's voice, not the character's). Pick one per scene, never both. **Fit the line to the clip either way:** the baked segment sizes like dialogue (~2 words/sec of `durationSec`), and the `voiceover` field only compresses ~1.15× before it's sped up or cut off — budget ≈ `durationSec × 2.3` words there. A tense POV beat is often short; don't let the line outrun it. Other characters speaking *to camera* use plain `dialogue` (they're looking down the lens).
- **A POV scene is ONE shot, so it holds ONE voice.** With no cuts there is only `SHOT 1` — so a `VO:` segment and another character's on-camera line inevitably share it, and a native-audio engine lip-syncs the narration onto that character's face: the POV character's inner voice comes out of the person in front of them. A POV scene therefore carries **either** the POV character's `VO:` narration **or** an on-camera line from someone else, never both. Need both beats? Split them into two scenes (the narration scene stays POV; the spoken beat can too). The `voiceover` field is the one exception — it's a post TTS track that never enters the motion prompt, so it can't be lip-synced. See cinematic-scenes → "One voice per shot".
- **Pin the POV character's baked voice — this is the case that bites hardest.** Every POV line runs through the engine-voiced `VO:` path (there's no lip-synced alternative for an off-screen character), so an unpinned narrator voice is exactly where clip-to-clip drift — including a gender flip — shows up most. The `Skye: VO: <line>` label names the speaker, but naming alone doesn't hold the voice: keep that character's `canonicalDescription` consistent as a nudge, and if the POV character's narration must be identical across the whole episode, move it to the `voiceover` field instead of `VO:` and hold that TTS voice constant yourself.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| POV cuts to other angles / leaves first-person | Most engines default to cutting; no lock clause | Add "ONE continuous shot, no cuts, no zoom, natural head movement" — non-negotiable |
| Reads as a third-person low/shaky shot, not first-person | No body in frame; camera floats free of a neck | Put the character's own hands/arms in frame acting every beat; tie motion to the head ("the view swings as she turns her head") |
| Nauseating / unwatchable shake | Used the full-chaos register for a calm scene | Dial to "gentle natural head movement, small micro-drifts"; reserve hyper-chaotic handheld for real panic/violence |
| A second body with the POV character's face appears at the frame edge | The POV character was `@mentioned` (ref renders them) OR their torso/posture was described | Don't `@mention` the POV character at all; never describe their chest/shoulders/back/seating — only hands-from-below + a downward glance |
| Their own hands drift (wrong skin tone / sleeves) shot to shot | Hand look held by nothing — there's no face ref to anchor it (and you must NOT add one) | Hold it with inline prose in every shot ("own hands, warm mid-tone skin, rolled white sleeves") — not by `@mention`ing the POV character |
| Contact (a hug, a hand on the shoulder) renders a whole second visible body | The touch was described as landing on the POV character's own body | Route it TO the lens — only the other character's arm/face enters frame past the lens; never describe contact on the POV character's chest/shoulder |
| A character hallucinates into a POV shot mid-clip | Someone "walks into" an empty POV frame; on i2v nothing is in the start frame to animate | Reveal them by turning the head to where they already are (or as they step toward the lens) — never into an empty frame; POV doesn't cut, so there's no cutting *to* them |
| Reflection of the POV face renders a stranger | Their ref isn't attached (you didn't `@mention` them), so the reflected face has nothing to match | Attach their character ref for that one reflection shot only, or skip the reflection and keep the face unseen |
| An eye-shaped / goggle / binocular / porthole MASK frames the POV shot (dark curved border, as if peering through eyeholes) | "the camera IS the eyes" + edge-localized optics ("distortion/aberration/vignette *near the edges*") make the model draw a literal eye outline around the frame | Spread the optics across the WHOLE image, drop the words *vignette/eyeholes/through her eyes*, and state the full-bleed lock: "fills the entire rectangular frame edge to edge as an ordinary camera view — NO vignette, NO eye-shaped/goggle/binocular/porthole mask; corners stay square and bright." See "Lens + embodiment optics" |
| Background crowd REORIENTS between the POV shot and the shots around it (people who sat backs-to-camera now face camera; the room/windows mirror) | A POV shot was cut against an OBJECTIVE shot taken from the OPPOSITE side of the room — the POV looks one way, the entrance/reverse looks the other, crossing the 180° line, so the model re-seats everyone to face whoever is "looking" | Keep the POV and its neighbouring objective shots on the SAME side of the line: pick ONE camera side, fix which wall the door/board and the windows are on, and seat the crowd ONE way (e.g. "all facing the front toward the camera, only heads turn") in EVERY shot. Don't shoot the entrance from behind the crowd and the POV from in front. Root-check the location ref too — if its seating faces the "wrong" way, the render fights the prose; re-anchor a location view whose orientation matches, or stage to the orientation the ref already shows |
| Feels staged / no urgency | Eyeline aimless, no look-targets | Write the look order explicitly (door → knife → his face) as one continuous sweep; the eyeline IS the coverage |

## Pitfalls

1. **Never let it cut.** One held take or it isn't POV. State "no cuts, no zoom" always.
2. **The POV character is the VIEWER, not a cast member.** Don't `@mention` them, don't describe their torso/posture — only their hands (from the bottom edge) and a downward glance exist. Putting them in frame spawns a second body with a face — the #1 failure.
3. **Show the hands, never the body.** Hands from below separate POV from a shaky observer shot; a described chest/shoulder/seat ruins it.
4. **Route contact and eyeline TO the lens.** Others' touch enters past the lens; anyone addressing the POV character looks into the lens.
5. **Match the shake to the emotion.** Full-chaos register is for panic only; most POV wants calm natural head movement.
6. **Don't forget it's still grounded.** Weight, breath, environmental force, references for the OTHER characters — all the cinematic-scenes pillars still apply; POV only changes the camera, not the story.
7. **POV speaker → off-screen voice.** The first-person character has no on-camera face; their lines are never plain lip-synced `dialogue` — use a `VO:`-prefixed `dialogue` segment (engine-baked) or the `voiceover` field (TTS narrator voice), one per scene.
