# Instructions for Claude: install shotkit

You are being pointed at this file because someone wants shotkit installed. Read it,
install it, verify it, then tell them what they can do next. This file is addressed to
you, not to them — `README.md` is the one written for a person.

## What this folder is

A Claude Code plugin: six skills that teach cinematic prompt craft, plus a `shotkit` CLI
that assembles finished prompts and the ordered list of reference images each prompt talks
about. It works with any text-to-image / text-to-video generator. It ships no dependencies
— standard library Python 3.9 or newer, nothing to `pip install`.

## The one trap, read this before running anything

**The repository root and the Python package inside it are both named `shotkit`.**

```
shotkit/              <- the repo root: this is what gets installed
  .claude-plugin/     <- only here
  skills/             <- only here
  shotkit/            <- the Python package. NOT what gets installed.
```

Run `cp -R shotkit …` from *inside* the repo and you silently copy the Python package —
no `skills/`, no `.claude-plugin/`. The copy succeeds, the install appears to work, and
the skills never load. Nothing tells you why.

**So: always use an absolute path to the repo root.** Establish it first and reuse it:

```bash
SHOTKIT="$(cd /path/to/shotkit && pwd)"   # adjust to where this folder actually is
ls "$SHOTKIT/.claude-plugin/plugin.json"  # must exist — if it does not, you have the package
```

If that `ls` fails, you are pointed one level too deep. Go up one directory.

## Pick one of three installs

Ask the person which they want only if it is unclear. Otherwise **default to option 1** —
it is the fewest moving parts.

### 1. Copy the folder (default)

Claude Code auto-loads anything under `~/.claude/skills/` as a plugin. No install command,
no restart beyond starting a new session.

```bash
cp -R "$SHOTKIT" ~/.claude/skills/shotkit
```

### 2. Local marketplace

For someone who prefers plugins managed by the CLI.

```bash
claude plugin marketplace add "$SHOTKIT"
claude plugin install shotkit@shotkit
```

### 3. Shipped with a repository

So that everyone who opens a given repo in Claude Code gets it with no per-person step.
**Both commands are required** — `marketplace add` alone registers the source but enables
nothing for anyone else:

```bash
cd /path/to/their/repo
claude plugin marketplace add "$SHOTKIT" --scope project
claude plugin install shotkit@shotkit --scope project
git add .claude/settings.json
git commit -m "chore: add shotkit plugin"
```

The pointer lands in `.claude/settings.json` at that repo's root. That file is what makes
it work for the next person, so it has to be committed.

## Verify — do not skip this

Two checks. Run both and report both.

```bash
claude plugin details shotkit
```

Must list **six** skills: `cinematic-scenes`, `pov-scenes`, `short-drama-structure`,
`character-refs`, `prompt-assembly`, `scene-from-scratch`. Fewer than six almost always
means the `shotkit`-inside-`shotkit` trap above — check what actually landed at the
install path and redo it with an absolute path to the repo root.

```bash
cd "$SHOTKIT" && python3 -m unittest discover -s tests
```

All tests must pass. Golden fixtures protect the original prompt-building rules;
workflow and validation tests cover project loading, reference generation, settings,
and narration through `VO:` in `dialogue`. The assembled project prompts include
shotkit-specific behavior, including the shared motion style preamble.

If Python is older than 3.9, say so and stop — that is the floor.

## Then tell them how to start

Keep it to a few lines. Something like:

> Installed, six skills loaded, tests green. Start a new session and say what you want —
> for example *"I want a scene where she hands him a folder in a bank lobby and he doesn't
> take it."* I will ask what the characters look like, set up a project folder, give you
> the prompts to generate their reference sheets, and then the finished scene prompt with
> the images listed in attach order.

Mention that each project lives in its own folder and that naming that folder's path in a
later session lets you pick the work back up rather than start over.

## If they ask what it does before installing

`README.md` covers it. The short version: you describe a scene, Claude writes the shot
list and dialogue using the craft skills, and `shotkit` assembles the full prompt — the
who-is-who clause built from the character descriptions, the speech and narration clauses
bound to their shot numbers, the audio discipline — plus the reference images in the exact
order the prompt's own numbering depends on.
