from __future__ import annotations

import typing

T = typing.TypeVar("T")


def filter(
    predicate: typing.Callable[[T], bool], list: typing.List[T]
) -> typing.List[T]:
    return [l for l in list if predicate(l)]


def predicate(n: int) -> bool:
    return n % 7 == 0 and n % 3 == 0


print(filter(predicate, range(0, 1000)))
