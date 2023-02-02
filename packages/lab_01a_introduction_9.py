from __future__ import annotations


def printTypes(arg):
    if isinstance(arg, str):
        print("tekst", arg)
        return
    if isinstance(arg, int):
        print("integer", arg)
        return
    if isinstance(arg, float):
        print("float", arg)
        return


printTypes("ok")
printTypes(1)
printTypes(2.0)
