import sqlite3
from pathlib import Path
import csv

base = Path(__file__).resolve().parent.parent
DB_DIR = base / "DATA" / "DB"
CSV_DIR = base / "DATA" / "EXPORT"
DB_FILE = DB_DIR / "library.db"


def _connect():
    # enable foreign keys if you ever add constraints
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ----------------------------
# USER FUNCTIONS
# ----------------------------

def check_user(username: str, password: str):
    try:
        with _connect() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        return None


def add_user(username: str, email: str, password: str):
    try:
        with _connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


# ----------------------------
# BOOK CRUD
# ----------------------------

def add_book(user_id: int, title: str, author: str, year: int, genre: str, read: bool = False, note: str = None) -> bool:
    try:
        with _connect() as conn:
            conn.execute("""
                INSERT INTO books (user_id, title, author, year, genre, read, note)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, title, author, year, genre, int(read), note))
            return True
    except sqlite3.Error as e:
        print("Error in add_book:", e)
        return False


def search_books(user_id: int, keyword: str) -> list:
    try:
        with _connect() as conn:
            results = conn.execute("""
                SELECT id, title, author, year, read, genre, note
                FROM books
                WHERE user_id = ? AND (title LIKE ? OR author LIKE ?)
            """, (user_id, f"%{keyword}%", f"%{keyword}%")).fetchall()
            return results
    except sqlite3.Error as e:
        print("Error in search_books:", e)
        return []


def check_book(user_id: int, book_id: int) -> bool:
    try:
        with _connect() as conn:
            row = conn.execute("""
                SELECT 1 FROM books WHERE user_id = ? AND id = ?
            """, (user_id, book_id)).fetchone()
            return row is not None
    except sqlite3.Error as e:
        print("Error in check_book:", e)
        return False


def find_book(user_id: int, book_id: int) -> tuple | None:
    try:
        with _connect() as conn:
            row = conn.execute("""
                SELECT id, title, author, year, read, genre, note
                FROM books
                WHERE user_id = ? AND id = ?
            """, (user_id, book_id)).fetchone()
            return row
    except sqlite3.Error as e:
        print("Error in find_book:", e)
        return None


def list_books(user_id: int) -> list:
    try:
        with _connect() as conn:
            return conn.execute("""
                SELECT id, title, author, year, read, genre, note
                FROM books
                WHERE user_id = ?
            """, (user_id,)).fetchall()
    except sqlite3.Error as e:
        print("Error in list_books:", e)
        return []


def update_book(book_id: int, title: str = None, author: str = None, year: int = None, read: bool = None, genre: str = None, note: str = None) -> bool:
    try:
        with _connect() as conn:
            fields, values = [], []

            if title:
                fields.append("title = ?")
                values.append(title)
            if author:
                fields.append("author = ?")
                values.append(author)
            if year is not None:
                fields.append("year = ?")
                values.append(year)
            if read is not None:
                fields.append("read = ?")
                values.append(int(read))
            if genre:
                fields.append("genre = ?")
                values.append(genre)
            if note is not None:
                fields.append("note = ?")
                values.append(note)

            if not fields:
                return False  # nothing to update

            values.append(book_id)
            sql = f"UPDATE books SET {', '.join(fields)} WHERE id = ?"
            cur = conn.execute(sql, values)

            return cur.rowcount > 0
    except sqlite3.Error as e:
        print("Error in update_book:", e)
        return False


def delete_book(book_id: int) -> bool:
    try:
        with _connect() as conn:
            cur = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            return cur.rowcount > 0
    except sqlite3.Error as e:
        print("Error in delete_book:", e)
        return False


# ----------------------------
# CSV IMPORT / EXPORT
# ----------------------------

def csv_exporter(user_id: int) -> bool:
    try:
        with _connect() as conn:
            username = conn.execute(
                "SELECT username FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            if not username:
                return False

            rows = conn.execute("""
                SELECT id, title, author, year, genre, read, note
                FROM books
                WHERE user_id = ?
            """, (user_id,)).fetchall()

        CSV_DIR.mkdir(parents=True, exist_ok=True)
        file = CSV_DIR / f"{username[0]}.csv"

        with file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "author", "year", "genre", "read", "note"])
            writer.writerows(rows)

        return True

    except Exception as e:
        print("Error in csv_exporter:", e)
        return False


def csv_importer(user_id: int, file_path: str) -> bool:
    try:
        rows = []
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                row.pop(0)  # yeet id column
                row.append(user_id)
                rows.append(row)

        with _connect() as conn:
            conn.executemany("""
                INSERT INTO books (title, author, year, genre, read, note, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, rows)

        return True

    except Exception as e:
        print("Error in csv_importer:", e)
        return False
