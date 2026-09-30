import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

EXPECTED = {
    "cinematic-scenes",
    "pov-scenes",
    "short-drama-structure",
    "character-refs",
    "prompt-assembly",
}

# Anything naming the tool this craft was extracted from.
#
# "short drama" as two words is the GENRE and stays allowed — the skills are about it.
# Only the tool's own single-word name, its MCP tool names and its gate vocabulary are
# forbidden.
TOOL_WORDS = re.compile(
    r"\bMCP\b|shortdrama|update_character|generate_character_look|"
    r"animate_scene|attach_location_reference|apply_style_preset|update_style|"
    r"link_branch|set_scene_branch|mergeSceneId|PAID_TOOLS|tools/list",
    re.IGNORECASE,
)


class TestSkillLayout(unittest.TestCase):
    def test_all_five_skills_exist(self):
        found = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        self.assertEqual(found, EXPECTED)

    def test_every_skill_has_frontmatter_naming_itself(self):
        for name in EXPECTED:
            with self.subTest(skill=name):
                text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"), name)
                head = text.split("---", 2)[1]
                self.assertRegex(head, rf"^name:\s*{re.escape(name)}\s*$", name)
                self.assertIn("description:", head)


class TestNoToolCoupling(unittest.TestCase):
    def test_no_skill_references_the_tool_it_came_from(self):
        for md in SKILLS.rglob("*.md"):
            with self.subTest(file=str(md.relative_to(ROOT))):
                hits = TOOL_WORDS.findall(md.read_text(encoding="utf-8"))
                self.assertEqual(hits, [], f"{md.name}: {hits}")

    def test_branching_is_gone(self):
        self.assertFalse(
            (SKILLS / "short-drama-structure" / "references" / "branching.md").exists()
        )
        for md in SKILLS.rglob("*.md"):
            with self.subTest(file=str(md.relative_to(ROOT))):
                self.assertNotIn("mergeSceneId", md.read_text(encoding="utf-8"))
