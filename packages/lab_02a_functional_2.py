from __future__ import annotations


def fib(n: int):
    i = 0
    yield i
    j = 1
    yield j

    next = i + j

    for k in range(n):
        yield next
        i = j
        j = next
        next = i + j


print(list(fib(20)))
