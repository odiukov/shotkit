# Instructions for Claude Code or Codex: install shotkit

If you were pointed at this file to install shotkit, install it in the target
project, verify it, then explain how to start. If asked only to edit these
instructions, do not install anything.

## Scope and requirements

Install only at the target project's level. Infer the project from the request or
current workspace; ask for its path only if unclear. Do not install skills,
plugins, launchers or dependencies at user or system level.

Python 3.9 or newer is required. There are no third-party dependencies, API keys,
network calls or `pip install` steps. The installer below targets macOS/Linux and
requires filesystem symlink support.

## One command for both agents

Use an absolute path to this repository's `install.py`, and pass the existing
project directory. The installer locates its source skills relative to itself,
so it works from any working directory and with spaces in paths:

```bash
python3 /absolute/path/to/shotkit/install.py "/absolute/path/to/your/project"
```

This copies six skill folders into `.agents/skills/` and creates one relative
symlink per skill in `.claude/skills/`. Codex reads the canonical folders; Claude
Code reads the same files through the links. There is only one installed copy of
each skill, its references and its executable resources.

```text
<project>/
  .agents/skills/
    cinematic-scenes/
    pov-scenes/
    short-drama-structure/
    character-refs/
    prompt-assembly/
      SKILL.md
      references/
      scripts/
        shotkit.py
        shotkit/
        template/
    scene-from-scratch/
  .claude/skills/
    cinematic-scenes -> ../../.agents/skills/cinematic-scenes
    pov-scenes -> ../../.agents/skills/pov-scenes
    short-drama-structure -> ../../.agents/skills/short-drama-structure
    character-refs -> ../../.agents/skills/character-refs
    prompt-assembly -> ../../.agents/skills/prompt-assembly
    scene-from-scratch -> ../../.agents/skills/scene-from-scratch
```

The CLI, Python package and templates are already bundled inside `prompt-assembly`.
Do not create a separate `.shotkit` directory, copy the whole repository, or copy
`README.md`, `INSTALL.md`, plugin metadata, development tools or tests into the
project. The installed skills need neither the source checkout nor
`CLAUDE_PLUGIN_ROOT`. Commands resolve `scripts/shotkit.py` relative to the loaded
`prompt-assembly/SKILL.md`; no machine-specific paths are written into skill files.
The project can move without reinstalling.

These are local skills in both agents. Do not additionally register the same
skills through Claude marketplace commands: that would create another discovery
route. `.claude-plugin/` stays in the source repository for users who explicitly
choose packaged plugin distribution; it is not part of this local installation.

See [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code skills and symlinks](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## Repeated runs, updates and older installations

A repeated run skips identical installed skills and reuses the correct Claude
links. It can restore missing skill folders or links. Before writing anything, it
checks all six destinations and refuses different existing skills, unrelated
Claude folders or links, and redirected parent directories. It never overwrites
local edits. Python caches are ignored when copying and comparing.

For an update, compare any differing installed skills with the source. Preserve
local edits and move the folders being replaced to a backup **outside all
skill-discovery directories**, then rerun the same command. Preserve unrelated
skills and Claude configuration. Existing Claude links to the canonical folders
can remain in place while those folders are replaced.

For the older `.shotkit` layout, back up the six old skill folders and `.shotkit`
first, compare and preserve local edits, then move them out of the way and run the
installer. Do not leave duplicate skills in a discoverable backup folder. Remove
only user-level copies confirmed to belong to an earlier attempt when the user's
migration request covers them. Never delete unrelated user skills.

## Verify the installation

Run the source checks from the complete source repository:

```bash
python3 --version
python3 -m unittest discover
```

Then, from the target project's root, run the **installed** CLI:

```bash
python3 .agents/skills/prompt-assembly/scripts/shotkit.py --help
python3 .claude/skills/prompt-assembly/scripts/shotkit.py styles
```

For a functional check, choose a new scratch film directory, run `init`, then
`status` and `sheet hero --handoff` with `--project` pointing at that directory.
Check that the generated sheet prompt and `.refs.txt` exist. Starter reference
images do not exist yet; a successful CLI check does not mean images were generated.
Do not initialize into the repository root or overwrite an existing film.

Confirm all six canonical skill folders exist, the six Claude symlinks resolve to
them, and there is no separate `.shotkit` runtime. Open a session in the target
project and inspect skill discovery: Codex CLI/IDE has `/skills`; Claude uses its
`/` skill menu. Do not claim either agent discovered the skills based only on file
copies or Python tests. Report which discovery checks were actually performed.

## Tell the user how to start

Report the installation path, verification result and any unverified discovery
step. Keep it brief. For example, in Codex:

```text
$scene-from-scratch Create a scene where she hands him a folder in a bank lobby and he doesn't take it. Use /absolute/path/to/my-film as the film project folder.
```

In Claude Code, invoke `/scene-from-scratch` with the same request. Each film lives
in its own folder; naming that folder in a later session lets the agent resume it.
`README.md` explains the workflow for a person.
