from __future__ import annotations

import os


def genFileNames():
    files = os.listdir()
    for file in files:
        if file.endswith(".py"):
            yield file


print([x for x in genFileNames()])
