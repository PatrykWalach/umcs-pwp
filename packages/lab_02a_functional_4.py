from __future__ import annotations


def sortPoints(points):
    points.sort(key=lambda p: sum(v**2 for v in p))
    return points


print(sortPoints([(1, 1), (3, 3), (2, 2), (5, 5)]))
