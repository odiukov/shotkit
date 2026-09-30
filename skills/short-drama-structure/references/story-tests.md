# Story tests — the critic gate (reference)

Run these seven tests against the beat list **before you turn the episode into scene files** — before writing a single `scenes/*.json`, and long before generating anything. Any failure = add or rewrite the missing beat and do NOT build until it passes. Cheap now, expensive once the scenes, prompts and clips exist.

All content that reaches scene fields is **English only**; keep these examples in English so they can be copied. Talk to the author in the chat's language.

## Run them as a hostile critic, not the author

You wrote the outline, so it *feels* fine — that is exactly the blind spot. Enforce an **information boundary**, not just good intentions:

- **Only what is literally written in the beat list / cast / choices is admissible.** Your intent, your memory of "I meant that to land in S1", and any "(plan: …)" annotation are **inadmissible** — if it isn't in a beat's on-screen text, it does not exist for the critic.
- **Grade guilty until the artifact proves innocent.** A bare "PASS" is a FAIL. The artifact is the table/ledger the test asks for, built only by quoting beat text. No artifact = you didn't run it.
- **Find at least one real problem before any PASS.** Found nothing? You read as the author — re-read cold.
- If your runtime can dispatch a subagent, give this pass to a fresh agent whose only input is the outline text. **If it can't (Claude Desktop / claude.ai): run the inline fresh-eyes protocol instead — it is mandatory, not optional:**
  1. Finish and freeze the outline. Do not edit it during the gate.
  2. Take the tests ONE AT A TIME. For each: re-read the outline top to bottom *as a hostile reviewer who has never seen it*, write the verdict (`PASS` / `FAIL: <one-line reason>`) **before** reading the next test.
  3. Never batch verdicts; never soften a FAIL because "it's close." A FAIL means you revise the outline and re-run that test from scratch.
  4. Output the final gate as a table: test → verdict → evidence line from the outline.

## The seven tests

1. **Spine** — State the episode's ONE dramatic question in a line; does every scene move it? (Fail → cut/rewrite the drifting scene.) **Two-sided question** ("rescuer or kidnapper?", "friend or trap?") → the Setup ledger must show an on-screen plant for **BOTH** horns; a dilemma seeded on one side only is an unearned payoff at the cliffhanger.
2. **Escalation** — Do stakes rise scene to scene, with a visible price of losing? (Fail → no two scenes at equal pressure; raise the cost.)
3. **Chemistry** — Does each key pairing run on opposed wants / shifting status shown in behaviour? (Fail → replace narrated feeling with action and subtext.)
4. **Hook** — Does scene 1 grab on screen, does every scene end on a pull, does the cliffhanger leave the spine hanging? (Fail → open later/hotter; add the end-of-scene pull.)
5. **Causality** — *Chain*: link the beats with "therefore / but" (not "and then"); each cause visible on screen. (Fail → if reordering two scenes is harmless, the chain is broken; add the connective beat.)
6. **Setup ledger** (generative — catches new variants) — build a table, one row per payoff: `payoff (beat#) | the exact on-screen action/line that planted it (beat#)`. Fill the plant column ONLY by quoting the earlier beat's written text — a "(plan: …)" note or your intent does not count. Any row whose plant column you can't fill from real beat text is an unearned payoff → write the plant into that beat. Cover knowledge, stakes, abilities, and every twist/reveal.
7. **Silent-film test** (catches the flat, static clip *before* it is rendered) — see below.

Only after all seven pass — each with its artifact shown — do you ask the author to approve the plot.

## Silent-film test — is every beat PLAYABLE?

The other six tests grade the story. This one grades whether the story can be **filmed**. It exists because the single most common defect in a finished clip is not a plot hole — it is that the actors stand still and nothing happens, and that is decided *here*, in the beat text, not in the shot prompt. A beat that names only an internal state ("she realizes he lied", "tension builds", "he decides to fight back") has nothing for a camera to record, and no amount of shot craft downstream can rescue it.

**Build the artifact — one row per scene:**

| Scene | The physical action the camera sees | Tier | Verdict |
|---|---|---|---|
| S1 | Caroline drives the loaded tray up into Lana's chest; food goes down her front; the tray hits the floor | Act (hook) | PASS |
| S4 | Mara packs his suitcase — folding each shirt flat, then stops pressing them and starts dropping them in | Activity | PASS |
| S5 | "Lana realizes she has been set up" | — | **FAIL** — a stage direction, not a scene |

**Every scene gets a row. No exemptions** — a row whose action column reads "she takes it silently" or "they look at each other" is a FAIL.

Fill the action column **only** by quoting what the beat literally says a body does. "She realizes / decides / understands / feels" is not an action. If the column cannot be filled, the beat FAILS — rewrite it around an **activity** the emotion can play against (see short-drama-structure → "Writing a beat that can actually be filmed").

**Then check the tiers across the whole episode:**

- **Any scene with no action at all** → a static clip waiting to happen. Give it an activity.
- **An Act (slap, shove, smash, tray tipped) anywhere other than the hook or a reversal** → soap opera. Downgrade it to an activity or an event.
- **A twist carried by a spoken line with no physical act on it** → it will render as a talking head. Land the line on a body: the file slides across the table, the ring goes down, the photo goes face-down.
- **A scene whose action list is thinner than its planned duration** (roughly one happening per 3 seconds) → the clip will have dead air. Add a happening, or shorten the scene.

## Avoid

- Episodic beats with no spine — events that never ask one question.
- Unplayable beat — an internal state ("she realizes", "he decides") standing in for a scene. It renders as a person standing still.
- The slap reflex — answering a static beat with an Act instead of an activity. Acts belong on the hook and the reversals; everywhere else it is soap opera.
- Exposition standing in for conflict — people explaining the plot instead of fighting over it.
- "And-then" chains — scenes that follow in time instead of causing each other.
- Narrated emotion — telling the viewer how characters feel instead of showing it collide.
- Unearned payoff — a reaction, stake, or twist with no on-screen plant.
- One-sided dilemma — a two-sided spine with only one horn seeded on screen.
