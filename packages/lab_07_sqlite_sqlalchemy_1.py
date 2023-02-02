from __future__ import annotations

import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("11_1.db") as conn:
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
        INSERT OR REPLACE INTO Book
        VALUES (1,'Wiedźmak','Andrzej')"""
        )
        conn.commit()

        cursor.execute(
            """
        INSERT INTO Book
        VALUES (2,'Precedens','Frost')"""
        )

        conn.rollback()

        for row in cursor.execute("SELECT * FROM Book"):
            print(row)
