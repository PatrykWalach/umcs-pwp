from __future__ import annotations

import sqlalchemy
from sqlalchemy import Column, Integer, String, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = "Book"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    checkouts = relationship("Checkout")


class Reader(Base):
    __tablename__ = "Reader"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    checkouts = relationship("Checkout")


class Checkout(Base):
    __tablename__ = "Checkout"
    id = Column(Integer, primary_key=True)
    bookId = Column(Integer, sqlalchemy.ForeignKey("Book.id"))
    readerId = Column(Integer, sqlalchemy.ForeignKey("Reader.id"))


if __name__ == "__main__":
    engine = sqlalchemy.create_engine("sqlite:///11_4.db", echo=True)

    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    insert(Book, prefixes="OR REPLACE").values(id=1, name="Wiedźmak", author="Andrzej")
    insert(Reader, prefixes="OR REPLACE").values(id=1, name="Remigiusz")
    insert(Checkout, prefixes="OR REPLACE").values(id=1, bookId=1, readerId=1)

    session.commit()

    for book in session.query(Book).all():
        print(book.id, book.name, book.author)
