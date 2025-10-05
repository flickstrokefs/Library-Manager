# ----------------------------
# Utility Functions
# ----------------------------

#importing much needed modules
import sqlite3

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect("DB/library.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            read INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_book(title: str, author: str, year: int, read: bool = False) -> bool:
    """Add a book to the library database."""
    try:
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
        c.execute(
        "INSERT INTO books (title, author, year, read) VALUES (?, ?, ?, ?)",
        (title, author, year, int(read))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
def list_books() -> list:
    """Return all books as a list of tuples."""
    try:
       conn = sqlite3.connect("DB/library.db")
       c = conn.cursor()
       c.execute("SELECT id, title, author, year, read FROM books")
       books = c.fetchall()
       conn.close()
       return books
    except Exception as e:
        print(e)
        return []
def search_books(keyword: str) ->list:
    """Search for books by title or author containing the keyword."""
    try:
       conn = sqlite3.connect("DB/library.db")
       c = conn.cursor()
       c.execute("""
        SELECT id, title, author, year, read FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
       results = c.fetchall()
       conn.close()
       return results
    except Exception as e:
        print(e)
        return []

def update_book(book_id: int, title: str = None, author: str = None, year: int = None, read: bool = None) -> tuple:
    """Update book info by ID; only provided fields are updated."""
    try:
       conn = sqlite3.connect("DB/library.db")
       c = conn.cursor()
       if title:
           c.execute("UPDATE books SET title = ? WHERE id = ?", (title, book_id))
       if author:
           c.execute("UPDATE books SET author = ? WHERE id = ?", (author, book_id))
       if year:
           c.execute("UPDATE books SET year = ? WHERE id = ?", (year, book_id))
       if read is not None:
           c.execute("UPDATE books SET read = ? WHERE id = ?", (int(read), book_id))
       conn.commit()
       conn.close()
       return True
    except Exception as e:
        print(e)
        return False

def delete_book(book_id: int) -> bool:
    """Delete a book by its ID."""
    try:
       conn = sqlite3.connect("DB/library.db")
       c = conn.cursor()
       c.execute("DELETE FROM books WHERE id = ?", (book_id,))
       conn.commit()
       conn.close()
       return True
    except Exception as e:
        print(e)
        return False

