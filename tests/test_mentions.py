import unittest

from shotkit.mentions import (
    mentioned_ref_ids,
    parse_ref_mentions,
    prompt_ref_issues,
    strip_mentions,
)

REFS = [
    {"id": "anna", "name": "Anna", "has_image": True},
    {"id": "anna_new", "name": "Anna New", "has_image": True},
    {"id": "cleo", "name": "Cleo", "has_image": True},
    {"id": "cleos_auto", "name": "Cleo's Auto", "has_image": True},
    {"id": "skye", "name": "Скай", "has_image": False},
]


class TestMentions(unittest.TestCase):
    def test_longer_token_wins_over_a_name_that_prefixes_it(self):
        # "@anna_new" must NOT resolve to the character named "Anna".
        self.assertEqual(mentioned_ref_ids("@anna_new walks in", REFS), {"anna_new"})

    def test_name_matches_across_an_apostrophe_consistently_across_resolvers(self):
        # "@Cleo's auto door" resolves to the location "Cleo's Auto" (the
        # longest-name-first alternation matches across the apostrophe). Verified
        # against the real app/domain/mentions.py: it resolves this the same way
        # everywhere. The historical production bug was prompt_ref_issues using a
        # SEPARATE, simpler regex that disagreed with this one and read "@Cleo"
        # instead — the fix was making every resolver share this exact pattern, so
        # this test pins that all of them still agree.
        text = "@Cleo's auto door"
        self.assertEqual(mentioned_ref_ids(text, REFS), {"cleos_auto"})
        self.assertEqual(prompt_ref_issues(text, REFS), {"unknown": [], "missing": []})

    def test_cyrillic_name_resolves(self):
        self.assertEqual(mentioned_ref_ids("@Скай turns", REFS), {"skye"})

    def test_strip_mentions_replaces_with_display_name_and_drops_selector(self):
        self.assertEqual(
            strip_mentions("@anna#wedding meets @cleo*", REFS), "Anna meets Cleo"
        )

    def test_strip_mentions_leaves_unknown_tokens_alone(self):
        self.assertEqual(strip_mentions("@nobody waits", REFS), "@nobody waits")

    def test_parse_view_selectors(self):
        got = {
            e["id"]: e["view"]
            for e in parse_ref_mentions("@anna and @cleo#night and @cleos_auto*", REFS)
        }
        self.assertEqual(got["anna"], "primary")
        self.assertEqual(got["cleo"], {"label": "night"})
        self.assertEqual(got["cleos_auto"], "all")

    def test_explicit_selector_beats_an_earlier_bare_mention(self):
        got = parse_ref_mentions("@cleo enters. @cleo#night leaves.", REFS)
        self.assertEqual(got, [{"id": "cleo", "view": {"label": "night"}}])

    def test_issues_report_unknown_and_missing(self):
        issues = prompt_ref_issues("@nobody and @Скай", REFS)
        self.assertEqual(issues["unknown"], ["@nobody"])
        self.assertEqual(issues["missing"], ["Скай"])

    def test_empty_ref_list_does_not_raise(self):
        self.assertEqual(mentioned_ref_ids("@anything", []), set())
        self.assertEqual(strip_mentions("@anything", []), "@anything")
        self.assertEqual(parse_ref_mentions("@anything", []), [])
