from __future__ import annotations

import random
import typing

R = typing.TypeVar("R")
P = typing.ParamSpec("P")


class Track(typing.Generic[R, P]):
    history: typing.List[typing.Tuple[str, R]] = []

    def __init__(self, fn: typing.Callable[P, R]) -> None:
        self.fn = fn

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        r = self.fn(*args, **kwargs)
        self.history.append((self.fn.__name__, r))
        return r


if __name__ == "__main__":

    @Track
    def gen_int() -> int:
        return random.randint(0, 10)

    @Track
    def gen_float() -> float:
        return random.randint(0, 10) / random.randint(1, 10)

    for i in range(10):
        choices: typing.List[typing.Union[Track[float, []], Track[int, []]]] = [
            gen_int,
            gen_float,
        ]
        random.choice(choices)()

    cls: typing.Type[Track[typing.Any, typing.Any]] = Track
    print(cls.history)
