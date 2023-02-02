from __future__ import annotations


def countsWords(string):
    return [(s, len(s)) for s in string.split()]


print(countsWords("Foo bar"))
