from __future__ import annotations

import sys

with open(sys.argv[1]) as f:
    data = f.read()

lines = data.count("\n")
print(f"linie {lines}")
print(f"słowa {len(data.split())}")
print(f"znaki {len(data)}")
