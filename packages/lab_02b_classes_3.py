from __future__ import annotations


class kolo:
    def __init__(self, rozmiar, rodzajFelgi):
        self.__rozmiar = rozmiar
        self.__rodzajFelgi = rodzajFelgi

    def setrozmiar(self, rozmiar):
        self.__rozmiar = rozmiar

    def setrodzajFelgi(self, rodzajFelgi):
        self.__rodzajFelgi = rodzajFelgi

    def get_info(self):
        return {"rozmiar kola": self.__rozmiar, "rodzaj felgi": self.__rodzajFelgi}


class silnik:
    def __init__(self, pojemnosc, rodzajPaliwa):
        self.__pojemnosc = pojemnosc
        self.__rodzajPaliwa = rodzajPaliwa

    def setPojemnosc(self, pojemnosc):
        self.__pojemnosc = pojemnosc

    def setRodzajPaliwa(self, rodzajPaliwa):
        self.__rodzajPaliwa = rodzajPaliwa

    def get_info(self):
        return {
            "pojemnosc silnika": self.__pojemnosc,
            "rodzaj paliwa": self.__rodzajPaliwa,
        }


class skrzynia:
    def __init__(self, iloscBiegow, typ):
        self.__iloscBiegow = iloscBiegow
        self.__typ = typ

    def setIloscBiegow(self, iloscBiegow):
        self.__iloscBiegow = iloscBiegow

    def setTyp(self, typ):
        self.__typ = typ

    def get_info(self):
        return {"ilosc biegow": self.__iloscBiegow, "typ skrzyni": self.__typ}


class samochod(kolo, silnik, skrzynia):
    def __init__(
        self,
        marka,
        kolor,
        rozmiarKola="----",
        rodzajFelgi="----",
        pojemnoscSilnika="----",
        rodzajPaliwa="----",
        iloscBiegow="----",
        typSkrzyni="----",
    ):
        super(samochod, self).__init__(rozmiarKola, rodzajFelgi)
        super(kolo, self).__init__(pojemnoscSilnika, rodzajPaliwa)
        super(silnik, self).__init__(iloscBiegow, typSkrzyni)
        self.__marka = marka
        self.__kolor = kolor

    def setMarka(self, marka):
        self.__marka = marka

    def setKolor(self, kolor):
        self.__kolor = kolor

    def get_info(self):
        return {
            "marka samochodu": self.__marka,
            "kolor": self.__kolor,
            **super(samochod, self).get_info(),
            **super(kolo, self).get_info(),
            **super(silnik, self).get_info(),
        }


print("\nSam 1:\n")
sam1 = samochod("Fiat", "sedan")
print(sam1.get_info())
print("\nSam 2:\n")
sam2 = samochod(
    marka="Ford",
    kolor="initial D",
    rozmiarKola=17,
    rodzajFelgi="alu",
    pojemnoscSilnika=1600,
    rodzajPaliwa="benzyna",
    iloscBiegow=6,
    typSkrzyni="manual",
)
print(sam2.get_info())
