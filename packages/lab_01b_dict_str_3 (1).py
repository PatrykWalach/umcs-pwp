from __future__ import annotations

import sys


def search(lines, string):
    for line in lines:
        if string in line:
            print(line)


if sys.argv[1] != "-":
    f = open("plik4.txt")
    search(f.readlines(), sys.argv[2])
    f.close()
else:
    f = sys.stdin
    search(f.readlines(), sys.argv[2])
