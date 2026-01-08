import os
import sqlite3
import pytest

from pathlib import Path

base=Path(__file__).resolve().parent.parent
DB = base / "DATA" / "DB" 



from utils.db_handler import (
    add_book,
    search_books,
    list_books,
    update_book,
    delete_book,
    check_book,
    find_book,
)

TEST_DB = DB / "library.db"


# ----------------------------
# Pytest Fixtures
# ----------------------------

@pytest.fixture(scope="function")
def test_db(monkeypatch):
    os.makedirs("DB", exist_ok=True)

    # Save the real connect function
    real_connect = sqlite3.connect

    conn = real_connect(TEST_DB)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            read INTEGER,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

    # Patch connect safely
    monkeypatch.setattr(
        sqlite3,
        "connect",
        lambda _: real_connect(TEST_DB)
    )

    yield

    os.remove(TEST_DB)


# ----------------------------
# CRUD TESTS
# ----------------------------

def test_add_book_success(test_db):
    success = add_book(
        user_id=1,
        title="1984",
        author="George Orwell",
        year=1949,
        genre="Dystopian",
        read=True,
        note="Classic"
    )
    assert success is True


def test_list_books_returns_books(test_db):
    add_book(1, "Dune", "Frank Herbert", 1965, "Sci-Fi", False, None)
    books = list_books(1)

    assert len(books) == 1
    assert books[0][1] == "Dune"


def test_search_books_finds_match(test_db):
    add_book(1, "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy", True, None)

    results = search_books(1, "Hobbit")
    assert len(results) == 1
    assert results[0][1] == "The Hobbit"


def test_search_books_empty_result(test_db):
    results = search_books(1, "Nonexistent")
    assert results == []


def test_check_book_true_when_exists(test_db):
    add_book(1, "Foundation", "Isaac Asimov", 1951, "Sci-Fi", False, None)

    books = list_books(1)
    book_id = books[0][0]

    assert check_book(1, book_id) is True


def test_find_book_returns_tuple(test_db):
    add_book(1, "Neuromancer", "William Gibson", 1984, "Cyberpunk", True, None)

    book_id = list_books(1)[0][0]
    book = find_book(1, book_id)

    assert book is not None
    assert book[1] == "Neuromancer"


def test_update_book_changes_data(test_db):
    add_book(1, "Old Title", "Author", 2000, "Genre", False, None)
    book_id = list_books(1)[0][0]

    updated = update_book(
        book_id,
        title="New Title",
        read=True
    )

    assert updated is True

    book = find_book(1, book_id)
    assert book[1] == "New Title"
    assert book[4] == 1  # read flag


def test_delete_book_removes_entry(test_db):
    add_book(1, "To Delete", "Author", 2020, "Genre", False, None)
    book_id = list_books(1)[0][0]

    deleted = delete_book(book_id)
    assert deleted is True

    assert list_books(1) == []
