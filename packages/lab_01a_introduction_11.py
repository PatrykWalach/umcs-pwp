from __future__ import annotations


def wypisz_do_list(lastIndex):
    return [i for i in range(0, lastIndex, 3 * 7)]


print(wypisz_do_list(100))
