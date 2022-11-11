import dataclasses


class InvalidName(Exception):
    pass


class InvalidPesel(Exception):
    pass


import re


@dataclasses.dataclass
class Person:
    first_name: str
    second_name: str
    pesel: int

    def __post_init__(self) -> None:
        if re.match(r"^[A-Za-z]+$", self.first_name) == None:
            raise InvalidName()

        if re.match(r"^[A-Za-z]+$", self.second_name) == None:
            raise InvalidName()

        if re.match(r"^\d{11}$", str(self.pesel)) == None:
            raise InvalidPesel()


if __name__ == "__main__":
    a = Person("jan", "kowalski", 99101576548)

    print(a)

    b = Person("jan", "kowalski", 9911576548)
