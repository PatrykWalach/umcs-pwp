def print_subclasses(cls: type[object]) -> None:
    def print_subclass(cls: type[object], depth:int=0) -> None:
        print("|   "* depth+"+" + "---" + cls.__name__)

        for cls in cls.__subclasses__():
            print_subclass(cls, depth=depth + 1)

    print(cls.__name__)

    for cls in cls.__subclasses__():
        print_subclass(cls)


if __name__ == "__main__":
    print_subclasses(Exception)
