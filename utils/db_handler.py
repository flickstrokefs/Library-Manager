# ----------------------------
# Utility Functions
# ----------------------------

import sqlite3
from pathlib import Path
import csv

base=Path(__file__).resolve().parent.parent
DB = base / "DATA"  /"DB" 
CSV = base / "DATA" / "EXPORT"

#user functions
def check_user(username: str, password: str):
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")

        c.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

        row = c.fetchone()
        conn.close()

        if row:
            return row[0]   # user_id

        
    except sqlite3.IntegrityError:
        return None
    
def add_user(username: str, email: str, password: str):
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")

        c.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )

        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id

    except sqlite3.IntegrityError:
        return None





#book functions
def add_book(user_id: int, title: str, author: str, year: int, genre: str, read: bool = False, note: str = None) -> bool:
    """Add a book to the library database."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("""
            INSERT INTO books (user_id, title, author, year, genre, read, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, author, year, genre, int(read), note))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error in add_book:", e)
        return False

def search_books(user_id: int, keyword: str) -> list:
    """Search for books by title or author for a specific user."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("""
            SELECT id, title, author, year, read, genre, note 
            FROM books 
            WHERE user_id = ? AND (title LIKE ? OR author LIKE ?)
        """, (user_id, f"%{keyword}%", f"%{keyword}%"))
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        print("Error in search_books:", e)
        return []
    
def check_book(user_id: int, book_id : int) -> bool:
    """Check if a book exists and belongs a specific user."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("""
            SELECT title 
            FROM books 
            WHERE user_id = ? AND id = ? 
        """, (user_id,book_id))
        results = c.fetchone()
        conn.close()
        return results is not None
        
    except Exception as e:
        print("Error in check_books:", e)
        return []
    
def find_book(user_id: int, book_id : int) -> tuple:
    """find if a book exists and belongs a specific user."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("""
            SELECT id, title, author, year, read, genre, note
            FROM books 
            WHERE user_id = ? AND id = ? 
        """, (user_id,book_id))
        results = c.fetchone()
        conn.close()
        return results
        
    except Exception as e:
        print("Error in find_books:", e)
        return []

    
def list_books(user_id: int) -> list:
    """Return all books for a specific user as a list of tuples."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("""
            SELECT id, title, author, year, read, genre, note 
            FROM books 
            WHERE user_id = ?
        """, (user_id,))
        books = c.fetchall()
        conn.close()
        return books
    except Exception as e:
        print("Error in list_books:", e)
        return []


def update_book(book_id: int, title: str = None, author: str = None, year: int = None, genre: str = None, read: bool = None, note: str = None) -> bool:
    """Update book info by ID; only provided fields are updated."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        if title:
            c.execute("UPDATE books SET title = ? WHERE id = ?", (title, book_id))
        if author:
            c.execute("UPDATE books SET author = ? WHERE id = ?", (author, book_id))
        if year:
            c.execute("UPDATE books SET year = ? WHERE id = ?", (year, book_id))
        if genre:
            c.execute("UPDATE books SET genre = ? WHERE id = ?", (genre, book_id))
        if read is not None:
            c.execute("UPDATE books SET read = ? WHERE id = ?", (int(read), book_id))
        if note is not None:
            c.execute("UPDATE books SET note = ? WHERE id = ?", (note, book_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error in update_book:", e)
        return False


def delete_book(book_id: int) -> bool:
    """Delete a book by its ID."""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error in delete_book:", e)
        return False


#csv handler
def csv_exporter(user_id: int) -> bool :
    """Exports all the user data to a csv file"""
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()
        conn.execute("BEGIN")
        c.execute("select username from users where id = ?",(user_id,))
        username=c.fetchone()[0]
        c.execute("""
            SELECT b.id, title, author, year, read, genre, note 
            FROM books b
            where  user_id = ?
        """, (user_id,))
        books = c.fetchall()
        filname =  CSV / f"{username}.csv" 
        filname.touch(exist_ok=True)
        File=open(filname,mode="r+",newline="\n")
        writeread=csv.writer(File)
        writeread.writerow(["id","title","author","year","genre","read","note"])
        writeread.writerows(books)
        File.close()
        conn.close()
        return True
    except Exception as e:
        print("Error in csv_exporter:", e)
        return False

def csv_importer(user_id: int, file_path: str) -> bool:
    try:
        conn = sqlite3.connect(DB / "library.db")
        c = conn.cursor()

        rows = []
        target = Path(file_path)

        with target.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # yeet header if it exists
            for book in reader:
                book.pop(0)
                book.append(user_id)
                rows.append(book)

        conn.execute("BEGIN")
        c.executemany(
            """INSERT INTO books (title, author, year, genre, read, note, user_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            rows
        )
        conn.commit()

        c.close()
        conn.close()
        return True

    except Exception as e:
        print("Error in csv_importer:", e)
        return False

