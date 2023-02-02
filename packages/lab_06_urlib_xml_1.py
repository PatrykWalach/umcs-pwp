from __future__ import annotations

import typing
import urllib.request
from xml.dom import minidom

if __name__ == "__main__":
    response = urllib.request.urlopen("http://www.money.pl/rss/")

    html: str = response.read()

    document: minidom.Node = minidom.parseString(html)
    items: typing.Iterable[minidom.Node] = document.getElementsByTagName("item")

    for el in items:
        titles: typing.Iterable[minidom.Node] = el.getElementsByTagName("title")
        descriptions: typing.Iterable[minidom.Node] = el.getElementsByTagName(
            "description"
        )
        links: typing.Iterable[minidom.Node] = el.getElementsByTagName("link")

        print(
            "\n\t".join(
                [
                    "· " + ", ".join(n.firstChild.data for n in titles),
                    ", ".join(n.firstChild.data for n in descriptions),
                    ", ".join(n.firstChild.data for n in links),
                ]
            )
        )
