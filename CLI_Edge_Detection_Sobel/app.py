"""Launch the Image Edge Detector GUI."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from edge_detector.gui import main

if __name__ == "__main__":
    main()

