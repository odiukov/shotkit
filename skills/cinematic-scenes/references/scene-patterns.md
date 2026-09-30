# Scene patterns (reference)

Battle-tested starting templates, written **t2v-native**: each is one full self-contained
`motionPrompt` following the canonical skeleton (header → style/lens + WB → shots → locks →
ambient). Replace bracketed ids with real bible ids. All are 9:16 defaults.

Patterns are grouped by **energy register**. **Start in CHARGED** — it is the drama default.
KINETIC is for the hook and the reversals. **HELD is the earned exception**, not a starting
point: reach for it only when the stillness *is* the event, and never because you could not
think of what should happen. Four of these five used to be HELD oners, and that is exactly
what made clips read static.

Every pattern must still clear the dynamism gate: a motion channel in every shot (BODY /
CAMERA / WORLD), one WORLD event per clip, an activity under every quiet beat, no dead air —
and **no shot that merely continues the previous one**. A dead scene (nobody does anything)
is allowed nowhere except an idle loop scene; none of these templates is one, including the HELD
ones. Keep the banned phrasings out of the prose you derive from them: "in silence",
"neither speaking", "they stand and look at each other", "the tension builds".

**Seeded mode (opt-in only):** when the user asks to lock a keyframe, derive the `scenePrompt` by
extracting the still ingredients from the pattern's opening (style/lens, framing + `@mentions`,
settled body, environmental force in frame) and keep the rest as the `motionPrompt`.

HELD patterns MUST keep their "ONE continuous shot, NO cuts, no zoom" opener — most engines
default to cutting and will split the take without it.

**Voiceover budget:** the `voiceover` field is tempo-fit to the scene and only compresses
up to ~1.15× — budget ≈ `durationSec × 2.3` words (~2.3 words/sec at natural pace). Size any
narration you add to these templates to their stated duration; a longer, richer `motionPrompt`
doesn't earn the VO more room.

---

## CHARGED — the drama default

### Confrontation with a status flip (activity + reversal)

The workhorse. Two people, opposed wants, the upper hand changes — and it plays **against an
activity**, so nobody is standing and talking.

- **motionPrompt**:
  ```
  4 shots, 12s total, 9:16.
  35mm anamorphic, naturalistic skin tones, hard overhead office light, WB locked 4300K, shallow depth of field, slight desaturation.
  SHOTS:
  SHOT 1 [0:00–0:03] 47° MEDIUM, eye-level — handheld, reframing as she works — @lana clears the long table in @boardroom, stacking folders two at a time, sleeves pushed up, weight swinging from hip to hip with each reach; @caroline stands frame-left in the doorway, not helping, watching. Late sun through the blinds throws hard bars across the table. Hard cut.
  SHOT 2 [0:03–0:06] 29° CLOSE, HIGH ANGLE 30° down on @lana — slow push — @lana keeps stacking through the line, not looking up; her hands do not stop, but the stack goes down harder. Cut ON the moment her hand lands flat on the last folder. Hard cut.
  SHOT 3 [0:06–0:09] 29° CLOSE, LOW ANGLE on @caroline — static — @caroline steps in from the @boardroom doorway; she lifts the top folder off the finished stack and lets it drop open on the table, pages fanning. Hard cut ON the drop.
  SHOT 4 [0:09–0:12] 47° MEDIUM TWO-SHOT, eye-level — camera pushes in past @caroline's shoulder — @lana straightens for the first time, sets both palms on the @boardroom table and takes the folder back, sliding it out from under @caroline's hand; the fanned pages drag across the wood. She holds the look. Hold.
  LOCKS: @lana stays frame-right facing screen-left and @caroline frame-left facing screen-right in every shot; the folder stack stays on the table's near edge; skin tone even and constant across all cuts.
  Ambient: air-conditioning whirr, folders knocking on wood, the paper fan of the dropped file → the room tone drops flat as the folder slides back; no score, diegetic ambient only.
  ```
- **generateAudio**: true. **dialogue**: the confrontation lines, ~2 words/sec, `[shot N]`-anchored.
- Critical: the status flip is carried by **who is handling the object** — Caroline takes the folder, Lana takes it back. Never play a status flip on two faces alone; give the power a physical token that changes hands.

### Quiet beat played against an activity (the anti-boredom template)

This is the pattern that replaces "she stands at the window and feels something".

- **motionPrompt**:
  ```
  3 shots, 10s total, 9:16.
  35mm, naturalistic skin tones, soft north window light, WB locked 5600K, shallow depth of field, 35mm film grain.
  SHOTS:
  SHOT 1 [0:00–0:04] 47° MEDIUM, eye-level — slow truck right, following her hands — @mara packs @suitcase open on the bed in @bedroom, folding his shirts in hard, fast creases and pressing each one flat with the heel of her hand; the bed compresses under the case. Hard cut.
  SHOT 2 [0:04–0:07] 12° tele INSERT, HIGH ANGLE straight down — static — her hands stop mid-fold over @suitcase; a folded shirt still held; held on the 12° long lens. Hard cut ON the stop.
  SHOT 3 [0:07–0:10] 29° CLOSE, eye-level — slow push — @mara in @bedroom looks up and away from @suitcase, eyes fixing on the window; then she goes back to folding, and this time she does not press the shirt flat — she drops it in. Hold.
  LOCKS: @suitcase stays open on the bed frame-right in every shot; @mara stays frame-left facing screen-right; skin tone even and constant across all cuts.
  Ambient: cloth on cloth, the case leather creaking, a radiator ticking → the folding stops and the room tone opens up; no score, diegetic ambient only.
  ```
- **generateAudio**: true. **dialogue**: empty, or one short line.
- Critical: the realization is never named and the face barely moves — it lands entirely in **how the activity changes** (pressed flat → dropped in). This is the highest-value template in the file; use it whenever you would otherwise have written a static emotional hold.

### Entrance / arrival in power (KINETIC-leaning)

- **motionPrompt**:
  ```
  3 shots, 9s total, 9:16.
  35mm anamorphic, naturalistic skin, cold corridor fluorescents against warm office lamps, WB locked 4000K, halation on highlights, 180° shutter motion blur.
  SHOTS:
  SHOT 1 [0:00–0:03] 84° WIDE, LOW ANGLE — hard tracking, backing away at her walking pace — @skye pushes through the double doors of @lobby with the flat of her hand; both doors swing wide and bounce off their stops behind her, and she does not slow for them. Out-of-focus staff cross frame in the foreground, close to the lens. Hard cut ON the second door hitting its stop.
  SHOT 2 [0:03–0:06] 12° tele INSERT, GROUND-LEVEL — static, she walks toward and past the lens — her heels strike the polished @lobby floor in even, unhurried weight; each step throws a hard reflection; held on the 12° long lens. Hard cut ON the step.
  SHOT 3 [0:06–0:09] 29° CLOSE, LOW ANGLE — handheld follow at her shoulder — @skye's face in the @lobby, eyes fixed ahead, not scanning the room; behind her the doors are still rocking. She does not break stride. Hold.
  LOCKS: @skye's direction of travel stays constant — she moves screen-left to screen-right in every shot and never doubles back; the doors stay behind her; skin tone even and constant across all cuts.
  Ambient: door hardware banging, heels on stone in a hard reverberant room, office noise dropping away as she passes → near-silence on the last shot; no score, diegetic ambient only.
  ```
- **generateAudio**: true.
- Critical: foreground bodies crossing close to the lens (shot 1) are the parallax multiplier — they do most of the kinetic work for almost no words.

### Action sequence (foot chase, grounded multi-shot) — KINETIC

- **motionPrompt**:
  ```
  4 shots, 12s total, 9:16.
  35mm, naturalistic color, overcast daylight, handheld vérité, WB locked 6500K, 180° shutter motion blur on fast actions.
  SHOTS:
  SHOT 1 [0:00–0:04] 47° MEDIUM, eye-level — handheld follow two paces behind, breathing with his stride — @runner mid-stride at 20 km/h in the narrow alley between @brickwalls, stride compact, arms tucked, shoulder leading; wet pavement catching the gray sky. Hard cut.
  SHOT 2 [0:04–0:06] 12° tele INSERT, ground-level — static — @runner's feet hammer through a puddle in the @brickwalls alley, spray kicking off each strike; held on the 12° long lens. Hard cut ON the foot strike.
  SHOT 3 [0:06–0:09] 63° MEDIUM-WIDE, low angle — static, he runs TOWARD camera — @runner takes a steel trash can with his hip without slowing: the can goes over, lid ringing on the concrete, a loose plastic bag tumbling past in the wind between @brickwalls. Hard cut ON the impact.
  SHOT 4 [0:09–0:12] 29° CLOSE, eye-level — handheld — @runner glances back once over his shoulder, breath ragged, then forward; a brief lens flare as he passes an open doorway in @brickwalls.
  LOCKS: @runner's direction of travel stays constant — the shots view it from behind, ground-level or head-on, he never doubles back; the same jacket stays zipped in every shot; skin tone even and constant across all cuts.
  Ambient: footsteps on wet concrete, his breathing irregular and close, the can ringing on concrete, distant city traffic; no score, diegetic ambient only.
  ```
- **generateAudio**: true.
- Critical: keep the stride compact — "sprinting" over-renders as bouncy, weightless action-hero pose. The hip/can contact pays the **force triad** (force → contact → the can going over): that consequence is what gives the run mass. Location `@mentioned` in every shot line, travel direction locked, or the alley re-invents itself per cut.

### Humiliation hook (KINETIC — the Act, earned)

The one place a strong physical Act is not only allowed but required: scene 1 of a revenge/glow-up engine.

- **motionPrompt**:
  ```
  4 shots, 10s total, 9:16.
  35mm anamorphic, naturalistic skin, hard overhead cafeteria light, WB locked 4300K, 180° shutter motion blur, slight desaturation.
  SHOTS:
  SHOT 1 [0:00–0:03] 63° MEDIUM-WIDE, eye-level — handheld, drifting in — @lana carries a loaded tray through @canteen between crowded tables, both hands under it, weight braced; the crowd is alive from the first frame, none of them motionless — small shifts, murmurs, turning heads. Hard cut.
  SHOT 2 [0:03–0:05] 47° MEDIUM, eye-level — static — @caroline's hand comes in from frame-left and drives the tray's edge UP: the tray tips against @lana's chest, food leaving it in one arc. RAMPS TO SLOW MOTION on the tip. Hard cut ON the food leaving the tray.
  SHOT 3 [0:05–0:07] 29° CLOSE, LOW ANGLE — static — SNAPS BACK TO FULL SPEED: the food lands down @lana's front in @canteen, sauce running, the tray clattering flat on the floor; her hands are still up where the tray was. Hard cut.
  SHOT 4 [0:07–0:10] 18° CLOSE-UP, eye-level — slow push — @lana in @canteen, food down her front, does not wipe it off, does not cry; she lifts her chin one degree and looks straight at @caroline. Behind her the whole @canteen has gone still and is watching. Hold on her eyes.
  LOCKS: @lana stays frame-right facing screen-left and @caroline frame-left facing screen-right in every shot; the spill stays down @lana's front from the moment it lands and is identical in every later shot — it never fades, wipes off or cleans up; skin tone even and constant across all cuts.
  Ambient: canteen roar of two hundred voices → the tray hits the floor and the room drops to a single held hush, one chair scraping; no score, diegetic ambient only.
  ```
- **generateAudio**: true. **dialogue**: the taunt, `[shot 2]`-anchored.
- Critical: the spill is a **continuity entity** — anchor it as a prop (`@stained_uniform`) from this clip's frame and `@mention` it in every scene onward, with the "identical, never disappears" prose. Note "does not wipe it off": a removal-implying verb would render the stain gone.

---

## HELD — the earned exception

Use these **only** when the stillness is itself the event. If you cannot say why, you have not
chosen HELD — you defaulted into it, and the clip will read flat.

### Emotional close-up (the decision landing)

Earned because the character is **unable to move** — the stillness is the beat.

- **motionPrompt**: `ONE continuous shot, NO cuts, no zoom, 8s, 9:16. 35mm anamorphic, naturalistic skin tones, soft north-facing window light, WB locked 5600K, shallow depth of field. 18° FOV, slow push from medium to tight close-up over the full duration, ending at her eyes. @woman at the @kitchen window has just torn @letter open; the torn envelope is still in her left hand and she does not put it down. Weight settled on her left foot, shoulders low; daylight catches the side of her face, dust visible in the beam, the curtain stirring faintly. She reads to the end. Her thumb goes through the paper's edge where she is gripping it. Her eyes glass over but she does not blink; she swallows once. Then she folds the letter in half, once, and holds it against her chest. Ambient: refrigerator whirr, a distant radio low under the noise floor, paper creasing under her grip → the crease stops and the room tone holds; no dialogue, no score.`
- **dialogue**: empty. **generateAudio**: true. **durationSec**: 8 — not 15. Do not stretch a held beat to fill a slot.
- Critical: no tears, no telegraphed grief. But note the clip still has a WORLD event (the letter is opened, then folded) and a CAMERA move (the push). A HELD register is not a zero-channel shot — it is *one* shot, still doing something.

### Intimacy (restrained, close)

Earned because the beat plays at **low amplitude** — but it still turns, and it still ends somewhere.

- **motionPrompt**: `ONE continuous shot, NO cuts, no zoom, 10s, 9:16. 35mm, naturalistic skin tones, warm low-key practical light from @bedsidelamp, WB locked 3200K, shallow depth of field. 29° FOV, slow push over the full duration onto the contact point between their foreheads. @a and @b sit close on the edge of @bed; one rests their forehead against the other's temple; the lamp throws warm light across one side of both faces, the room behind falls to shadow, bedding compressed where they sit. One hand finds the other's and turns it palm-up, thumb moving once across the knuckles; the other hand closes on it. Then @a reaches past @b and switches off @bedsidelamp — the warm side-light dies and the room drops to the blue window spill, both faces going to silhouette, and neither hand lets go. Ambient: room tone, a faint clock ticking, soft fabric movement → the lamp switch clicks and the room tone opens up; no score, diegetic ambient only.`
- **generateAudio**: true. **dialogue**: empty, or one short line.
- Critical: intimacy plays at low amplitude — resist a kiss, a tear, a sob; the engine over-renders all three. But low amplitude is **not** zero: the take still has a CAMERA move (the push), a WORLD event (the lamp goes out), and a small BODY turn (the hand opening). Never write this beat as "they sit together in silence" — that is a dead scene, and only an idle loop scene is allowed to be one.

### Driving (interior lock)

Earned because the car is the motion — the camera locks so the world moves past.

- **motionPrompt**: `ONE continuous shot, NO cuts, no zoom, 8s, 9:16. 35mm anamorphic, naturalistic skin tones, low-key interior with passing exterior light, WB locked 3800K, shallow depth of field. 29° FOV, locked-off frame with slight handheld breathing, eye-level from the passenger side. @driver alone behind the wheel of @car on a two-lane highway at dusk, holding a steady 90 km/h; hands at 9 and 3, grip relaxed, jaw set. He glances at the rearview mirror once, then back to the road; then his hand leaves the wheel, kills the radio, and returns. Light from passing streetlamps and oncoming headlights sweeps across his face in slow rhythmic bands; dust motes in the side-window light; the highway behind the glass out of focus, moving at speed. Ambient: tire roar on asphalt, faint heater fan, a radio talk-voice low under the noise floor → the radio cuts dead and the tire roar floods the cabin; no score, no dialogue.`
- **dialogue**: empty. **voiceover**: optional narration. **generateAudio**: true.
- Critical: lock the frame or use gentle handheld breathing only — an aggressive cabin camera is a music video, not film. Without the NO-cuts opener the engine will cut the cabin into angles. Note the radio kill: even a locked driving hold gets one WORLD event, and the ambient arc rides it.

### Environmental interaction (weather as character, held truck)

- **motionPrompt**: `ONE continuous shot, NO cuts, no zoom, 10s, 9:16. 35mm anamorphic, naturalistic color, late-afternoon overcast with a slight teal cast, WB locked 6500K. 47° FOV, slow truck right at her walking pace, framing @woman medium-wide in profile with the sea beyond; horizon stays level. @woman walks the coastal @cliffpath into a 40 km/h onshore wind: grass laid flat, her coat pressed to her body, salt spray in the air, gray churning sea below. Wind catches her hair from camera-left; she does not push it back; she pulls her collar tighter once, weight settling into each step against the slope. Gulls hold position against the wind overhead. Ambient: wind through grass, distant surf, gull calls, her soft footsteps on the path; no dialogue, no score.`
- **generateAudio**: true.
- Critical: the wind must shape hair AND coat AND grass AND gulls — single-element wind reads as a fan on set. Quantify it (km/h) instead of "strong wind". The BODY channel is filled by the walk and the CAMERA by the truck; this is a held take that is still moving.
