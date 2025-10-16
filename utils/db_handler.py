# ----------------------------
# Utility Functions
# ----------------------------

import sqlite3


def add_book(user_id: int, title: str, author: str, year: int, genre: str, read: bool = False, note: str = None) -> bool:
    """Add a book to the library database."""
    try:
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
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
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
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
    
def list_books(user_id: int) -> list:
    """Return all books for a specific user as a list of tuples."""
    try:
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
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
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
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
        conn = sqlite3.connect("DB/library.db")
        c = conn.cursor()
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Error in delete_book:", e)
        return False
