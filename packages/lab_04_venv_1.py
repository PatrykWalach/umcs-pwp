from __future__ import annotations

import re


class InvalidEmailError(Exception):
    pass


class Adres:
    def __init__(self, email: str):
        if re.match(r"^\w+@\w+\.\w+$", email) == None:
            raise InvalidEmailError()
        self.email = email
        super().__init__()


if __name__ == "__main__":
    a = Adres("j_kowalski@gmail.com")
    b = Adres("j.kowalski@gmail.com")
