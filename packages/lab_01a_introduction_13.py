from __future__ import annotations

import math


def pierwiastki_trojmianu(A, B, C):
    delta = pow(B, 2) - 4 * A * C
    if delta < 0:
        return "brak pierwiastków"
    x1 = (-B + math.sqrt(delta)) / (2 * A)
    if delta == 0:
        return x1

    x2 = (-B - math.sqrt(delta)) / (2 * A)
    return [x1, x2]


print(pierwiastki_trojmianu(2, 5, 4))
