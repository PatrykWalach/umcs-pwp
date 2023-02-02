from __future__ import annotations

import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = f.read()

    for g in re.finditer(
        r"\d{1,2}\.\d{2}\.\d{4}|\d{1,2}\s+[I]+\s+\d{4}|\d{1,2}\s+(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)\s+\d{4}",
        data,
    ):

        print(g.group())
