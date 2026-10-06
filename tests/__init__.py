"""Load the bundled runtime for repository tests without installing the skills."""

import pathlib
import sys

RUNTIME = pathlib.Path(__file__).resolve().parent.parent / "skills/prompt-assembly/scripts"
sys.path.insert(0, str(RUNTIME))
