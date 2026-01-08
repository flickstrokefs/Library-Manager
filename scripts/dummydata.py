import os
import sqlite3
import csv
from pathlib import Path
from dotenv import load_dotenv

base = Path(__file__).resolve().parent.parent
ENV = base / ".env"
DB = base / "DATA" / "DB"
file_path = Path(__file__).resolve().parent / "dummy.csv"
load_dotenv()

def make_dummy():
    if ENV.exists():
        name = os.getenv("USER")
        password = os.getenv("PASS")
        mail = os.getenv("MAIL")
    else:
        name = "user"
        password = "password"
        mail = "somegeneriname@somegenericdomain.com"
        
    ls = (name, mail, password)  # order must match DB columns

    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        
        conn.execute("BEGIN")

        # insert user
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ls)
        user_id = c.lastrowid

        rows = []
        target = Path(file_path)

        with target.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for book in reader:
                book.pop(0)       # drop CSV id
                book.append(user_id)
                rows.append(book)

        # insert books
        c.executemany(
            """INSERT INTO books (title, author, year, genre, read, note, user_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            rows
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError as e:
        print("DB Integrity Error:", e)
        conn.rollback()
        conn.close()
        return False
