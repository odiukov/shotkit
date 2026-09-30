"""The package imports and the plugin manifests are well-formed JSON."""

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestSkeleton(unittest.TestCase):
    def test_package_imports(self):
        import shotkit  # noqa: F401

    def test_plugin_manifest(self):
        data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(data["name"], "shotkit")
        self.assertIn("version", data)

    def test_marketplace_manifest(self):
        data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(data["name"], "shotkit")
        self.assertEqual(data["plugins"][0]["name"], "shotkit")
        self.assertEqual(data["plugins"][0]["source"], "./")
