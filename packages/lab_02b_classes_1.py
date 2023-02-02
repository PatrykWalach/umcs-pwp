from __future__ import annotations

import functools
import math


@functools.total_ordering
class LiczbaZespolona:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def modul(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __str__(self):
        return str(self.real) + "+i" + str(self.imag)

    def __add__(self, other):
        return LiczbaZespolona(self.real + other.real, self.imag + other.imag)

    def __mul__(self, other):
        return LiczbaZespolona(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __sub__(self, other):
        return LiczbaZespolona(self.real - other.real, self.imag - other.imag)

    def __truediv__(self, other):
        return LiczbaZespolona(
            (self.real * other.real + self.imag * other.imag)
            / (other.real**2 + other.imag**2),
            (self.imag * other.real - self.real * other.imag)
            / (other.real**2 + other.imag**2),
        )

    def __lt__(self, other):
        if isinstance(other, LiczbaZespolona):
            return self.real < other.real
        return NotImplemented


za = LiczbaZespolona(1, 1)
zb = LiczbaZespolona(2, 2)
print("za = %s" % za)
print("zb = %s" % zb)
print("%s + %s = %s" % (za, zb, (za + zb)))
print("%s - %s = %s" % (za, zb, (za - zb)))
print("%s * %s = %s" % (za, zb, (za * zb)))
print("modul(za) = %s" % (za.modul()))
print("modul(zb) = %s" % (zb.modul()))
print("%s / %s = %s" % (za, zb, (za / zb)))
print(f"{za == zb=}")
