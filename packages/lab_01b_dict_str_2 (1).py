from __future__ import annotations

import sys


def string_to_dict(keysValuesString):
    return dict(subString.split(":") for subString in keysValuesString.split("\n"))


with open("plik3.txt") as f:
    data = f.read()

print(string_to_dict(data)[sys.argv[1]])
