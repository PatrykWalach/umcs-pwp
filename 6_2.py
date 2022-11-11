import re


class NameError(Exception):
    pass


class IPError(Exception):
    pass


class MaskError(Exception):
    pass


class IpConfig:
    def __init__(self, name: str, adres: str, mask: str):
        self.set_name(name)
        self.set_mask(mask)
        self.set_adres(adres)
        super().__init__()

    def set_adres(self, adres: str) -> None:
        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", adres) == None:
            raise IPError()
        self.__adres = adres

    def set_name(self, name: str) -> None:
        if re.match(r"^\w+$", name) == None:
            raise NameError()
        self.__name = name

    def set_mask(self, mask: str) -> None:
        if re.match(r"^/\d{1,2}$", mask) == None:
            raise MaskError()
        self.__mask = mask


if __name__ == "__main__":
    a = IpConfig("jkowalski", "192.168.0.1", "/24")
    b = IpConfig("jkowalski", "192.168..1", "/24")
