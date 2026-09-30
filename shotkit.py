#!/usr/bin/env python3
"""shotkit entrypoint.

Run from a project directory:

    python3 "$CLAUDE_PLUGIN_ROOT/shotkit.py" frame s01
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from shotkit.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
