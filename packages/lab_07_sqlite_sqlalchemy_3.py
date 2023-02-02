from __future__ import annotations

import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("11_3.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Book
        (id INTEGER PRIMARY KEY,
        name TEXT,
        author TEXT)
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Checkout
        (id INTEGER PRIMARY KEY,
        bookId INTEGER,
        readerId INTEGER)
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Reader
        (id INTEGER PRIMARY KEY,
        name TEXT)
        """
        )
        cursor.execute(
            """
        INSERT OR REPLACE INTO Reader
        VALUES (1,'Remigiusz')"""
        )
        cursor.execute(
            """
        INSERT OR REPLACE INTO Book
        VALUES (1,'Wiedźmak','Andrzej')"""
        )
        cursor.execute(
            """
        INSERT OR REPLACE INTO Checkout
        VALUES (1,1,1)"""
        )
        conn.commit()

        for row in cursor.execute("SELECT * FROM Book"):
            print(row)
