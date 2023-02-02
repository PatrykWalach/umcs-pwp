from __future__ import annotations

import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = f.read()

    for g in re.finditer(
        r"(\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\b\.){3}\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\b(\s(\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\b\.){3}\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\b|/([0-9](?!\d)|[1-2]\d|3[0-2]))",
        data,
    ):

        print(g.group())
