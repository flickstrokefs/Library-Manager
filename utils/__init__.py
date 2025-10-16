import sqlite3

def init_db():
    """Initialize the SQLite database only if the tables don't exist."""
    conn = sqlite3.connect("DB/library.db")
    c = conn.cursor()

    # Check if tables already exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    user_table = c.fetchone()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    book_table = c.fetchone()

    if user_table and book_table:
        print("Database already initialized.")
        conn.close()
        return

    # Create users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create books table
    c.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        genre TEXT,
        read BOOLEAN DEFAULT 0,
        note TEXT,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")
