import sqlite3
import pytest

from utils import db_handler as db


# ----------------------------
# Pytest Fixtures
# ----------------------------
@pytest.fixture(scope="function")
def test_db(tmp_path, monkeypatch):
    # Create an isolated temporary DB file
    test_db_file = tmp_path / "library.db"

    # Make sure db_handler connects to THIS db
    real_connect = sqlite3.connect
    monkeypatch.setattr(
        db.sqlite3,
        "connect",
        lambda _: real_connect(test_db_file)
    )

    # Build tables we actually need
    conn = sqlite3.connect(test_db_file)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            read INTEGER,
            note TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Insert a dummy user for functions that need user_id = 1
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
              ("test_user", "x@x.com", "pass"))
    conn.commit()
    conn.close()

    yield
    # tmp_path auto-cleans after the test run, no manual unlink needed


# ----------------------------
# CRUD TESTS
# ----------------------------
def test_add_book_success(test_db):
    success = db.add_book(1, "1984", "George Orwell", 1949, "Dystopian", True, "Classic")
    assert success is True


def test_list_books_returns_books(test_db):
    db.add_book(1, "Dune", "Frank Herbert", 1965, "Sci-Fi", False, None)
    books = db.list_books(1)

    assert len(books) == 1
    assert books[0][1] == "Dune"


def test_search_books_finds_match(test_db):
    db.add_book(1, "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy", True, None)
    results = db.search_books(1, "Hobbit")

    assert len(results) == 1
    assert results[0][1] == "The Hobbit"


def test_search_books_empty_result(test_db):
    results = db.search_books(1, "Nonexistent")
    assert results == []


def test_check_book_true_when_exists(test_db):
    db.add_book(1, "Foundation", "Asimov", 1951, "Sci-Fi", False, None)
    book_id = db.list_books(1)[0][0]

    assert db.check_book(1, book_id) is True


def test_find_book_returns_tuple(test_db):
    db.add_book(1, "Neuromancer", "Gibson", 1984, "Cyberpunk", True, None)
    book_id = db.list_books(1)[0][0]

    book = db.find_book(1, book_id)
    assert book is not None
    assert book[1] == "Neuromancer"


def test_update_book_changes_data(test_db):
    db.add_book(1, "Old Title", "Author", 2000, "Genre", False, None)
    book_id = db.list_books(1)[0][0]

    updated = db.update_book(book_id, title="New Title", read=True)
    assert updated is True

    book = db.find_book(1, book_id)
    assert book[1] == "New Title"
    assert book[4] == 1  # read flag


def test_delete_book_removes_entry(test_db):
    db.add_book(1, "To Delete", "Author", 2020, "Genre", False, None)
    book_id = db.list_books(1)[0][0]

    deleted = db.delete_book(book_id)
    assert deleted is True

    assert db.list_books(1) == []
