from __future__ import annotations


def string_to_dict(keysValuesString):
    return dict(subString.split(":") for subString in keysValuesString.split("\n"))


print(
    string_to_dict(
        """k1: v1
k2: v2
k3: v3"""
    )
)
