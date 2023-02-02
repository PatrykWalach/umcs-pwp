from __future__ import annotations


class Punkt2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Punkt2D(self.x - other.x, self.y - other.y)


class Punkt3D(Punkt2D):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def __sub__(self, other):
        return Punkt2D(self.x - other.x, self.y - other.y, self.z - other.z)
