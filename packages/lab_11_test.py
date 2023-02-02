# 1
# def generator(input: str, search: chr):
#     for i, c in enumerate(input):
#         if c == search:
#             yield i
#
# if __name__ == '__main__':
#     for i in generator('PyCharm', 'a'):
#         print(i)


# 2
# napis = '\nTestowy\n\n \t\t\t ciąg \r\t znaków\n'
#
# if __name__ == '__main__':
#     print('_'.join(napis.split()))
# 3
# import sqlite3
#
# sql_test_table = '''CREATE TABLE IF NOT EXISTS test (
#
#                 id integer,
#
#                 name text,
#
#                 value real
#                 )'''
#
# if __name__ == '__main__':
#     conn = sqlite3.connect("b.sqlite3")
#     conn.execute(sql_test_table)
#     conn.commit()
# 4
# import subprocess
#
# try:
#     subprocess.run(["ech", "Hello World!"], check=True, shell=True, capture_output=True)
# except subprocess.CalledProcessError:
#     print('Zdarzył się błąd')
# 5
# l = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
#
# if __name__ == '__main__':
#     print(l[4::3])
# 6
# class MojWyjatek(Exception):
#     def __init__(self):
#         super().__init__("Zdarzył się wyjątek")
#
#
# try:
#     raise MojWyjatek()
# except MojWyjatek as ex:
#     print(ex)
# 7
# l = [1, 2, [31, 32, [331, 332, [3331, 3332, 3333]], 4]]
# import typing
#
#
# def print_l(l: typing.List[typing.Any]) -> None:
#     print([e for e in l if not isinstance(e, list)])
#
#     for e in l:
#         if isinstance(e, list):
#             print_l(e)
#
#
# if __name__ == "__main__":
#     print_l(l)
# 8
# l = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
#
# print()
# 9
# class A():
#     def funkcja(self):
#         print("Wywolanie A")
#
#
# class B(A):
#     def funkcja(self):
#         print("Wywolanie B")
#         super().funkcja()
#
#
# class C(B):
#     def funkcja(self):
#         print("Wywolanie C")
#         super().funkcja()
#
#
# kc = C()
#
# kc.funkcja()
# 10


# from xml.dom import minidom
#
# doc = minidom.parseString(
#
#     '''<mdomtest>
#
#         <el id="1">
#
#             <test>T1</test>
#
#             <test>T12</test>
#
#         </el>
#
#         <el id="2">
#
#             <test>T2</test>
#
#             <test>T22</test>
#
#         </el>
#
#     </mdomtest>'''
#
# )
#
# import xml.dom.minidom
#
# if __name__ == '__main__':
#     el: xml.dom.minidom.Element = doc.getElementsByTagName('el')[1]
#     el: xml.dom.minidom.Element = el.getElementsByTagName('test')[1]
#     text: xml.dom.minidom.Text = el.firstChild
#
#     print(text.data)

# 11


# import re
#
# tekst = "To jest test. To jest przykład działania testowych wyrażeń regularnych."
#
# finditerObj = re.finditer(r"jest|testowych|test", tekst)
#
# for m in finditerObj:
#     print(m.group())


# 12
# class MyAdd(int):
#     def __add__(self, other):
#         return MyAdd(super().__add__(other))
#
#
# print(MyAdd(1) + MyAdd(2))
# print(type(MyAdd(1) + MyAdd(2)))

# 13
from __future__ import annotations

print(
    '\\a\\a\\aTest\\x44\\b\\b\\b\\bowy\\n\\n \\t\\t\\t ciąg \\r\\t\\0\\33 "znaków"\\n"'
)
