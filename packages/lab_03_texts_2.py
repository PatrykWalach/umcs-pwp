from __future__ import annotations

import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = f.read()

    for g in re.finditer(
        r"(?:(?:(https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?((?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::(\d{2,5}))?(/[^\s?#]*)?(\?[^\s#]*)?(#\S*)?",
        data,
    ):
        print(f"ADRES: {g.group()}")
        print(f"protokół: {g.group(1)}")
        print(f"adres domenowy: {g.group(2)}")
        print(f"port: {g.group(3)}")
        print(f"ścieżka: {g.group(4)}")
        print(f"parametry: {g.group(5)}")
        print(f"kotwica: {g.group(6)}")
