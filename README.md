---

# 📚 Personal Library Manager

Video Demo: *https://youtu.be/bTEwOJZbZNY?si=9sfdxQPLFkeEQj6z*

### Description

Personal Library Manager is a CLI-based Python application designed to help users maintain their own private book catalog. The program allows users to register/login, add books, search titles, update entries, export/import CSV data, and manage their entire personal reading collection directly from the terminal.

This project fulfills the CS50P final project requirements by providing:

* A Python application containing `main()` and multiple helper functions
* Database-backed persistent storage via SQLite
* Testable CRUD operations for books and users
* CSV import/export capabilities for interoperability
* Pagination, filtering, and sorting for larger libraries
* Modular code organization using `utils/` package

The final result is a fully functional personal library system that remains lightweight and offline-first while still providing modern usability features.

---

## 🚀 Features

### ✔ User Accounts

* Register new users with email + password
* Login validation against SQLite database
* Session-limited actions based on user ID

### ✔ Book Management

Users can:

* Add books with fields: title, author, year, genre, read-status, notes
* Search books by title or author (with pagination)
* List books with:

  * Filtering (genre or read status)
  * Sorting (title, author, year, genre, read)
  * Pagination (page-by-page viewing)
* Update book details individually
* Delete books with confirmation

### ✔ CSV Support

* **Export** books to `DATA/EXPORT/username.csv`
* **Import** books from CSV with bulk insertion

CSV schema supported:

```
id,title,author,year,read,genre,note
```

### ✔ CLI Enhancements

* Colored terminal prompts using `colorama`
* Unicode icons for better readability
* Friendly error handling and input validation

---

## 🏗 Project Structure

The project uses a simple modular layout:

```
personal_library_manager/
│
├── project.py              # Main CLI entry point (contains main())
├── utils/
│   ├── __init__.py         # DB initialization
│   └── db_handler.py       # CRUD + CSV helper functions
├── scripts/
│   ├── dummy.py            # Data initialization
│   └── dummy.csv           # Source of data
├── DATA/
│   ├── DB/
│   │   └── library.db      # SQLite database
│   └── EXPORT/
│       └── ...             # Generated CSV files
├── tests/
│   └── test_project.py     # pytest test cases
├── requirements.txt
├── .gitignore
├── ROADMAP.md
└── README.md
```

---

## 🗄 Database Schema

SQLite stores users and books with the following tables:

### `users`

| Column   | Type                |
| -------- | ------------------- |
| id       | INTEGER PRIMARY KEY |
| username | TEXT UNIQUE         |
| email    | TEXT                |
| password | TEXT                |

### `books`

| Column  | Type                |
| ------- | ------------------- |
| id      | INTEGER PRIMARY KEY |
| user_id | INTEGER (FK)        |
| title   | TEXT                |
| author  | TEXT                |
| year    | INTEGER             |
| genre   | TEXT                |
| read    | INTEGER (0/1)       |
| note    | TEXT                |

---

## 🧪 Testing

`pytest` tests are provided for database CRUD logic including:

* Adding users
* Adding books
* Searching books
* Updating books
* Deleting books

These tests use temporary test databases to avoid polluting real user data.

---

## 🛠 How to Run

### **1. Install dependencies**

```
pip install -r requirements.txt
```

### **2. Run the program**

```
python project.py
```

### **3. Use the CLI:**

You will be prompted to either **Login** or **Register**, then may:

* Add books
* List with filters
* Search by keyword
* Update entries
* Delete entries
* Import/Export CSV

---

## 📦 Dependencies

Listed in `requirements.txt`:

```
colorama
python-dotenv
```

(SQLite is included with Python.)

---

## 💡 Design Notes & Decisions

* **CLI-based UX** was chosen for simplicity and portability
* **SQLite** provides persistence without requiring setup or servers
* **colorama** improves readability in terminal environments
* **CSV interop** makes backups and migrations trivial
* **Pagination** prevents huge outputs from overwhelming users
* **Sorting & Filtering** allow efficient navigation for large libraries
* **Separation of concerns** keeps `project.py` lean and testable

---


## ⚖️ Tradeoffs & Alternatives

While the chosen design keeps the project lightweight and portable, it also introduces some tradeoffs worth noting:

### **1. CLI vs GUI/Web Interface**

**Chosen:** CLI (terminal-based)
**Tradeoff:**

* Pros: Simple to implement, portable, zero setup, works offline.
* Cons: Less intuitive for non-technical users, limited visual capabilities.

**Alternative:** Flask/Django Web UI or Electron GUI would improve accessibility but increase complexity.

---

### **2. SQLite vs Full DBMS**

**Chosen:** SQLite
**Tradeoff:**

* Pros: Serverless, fast for local use, cross-platform, ideal for single-user applications.
* Cons: No concurrency control for multi-user access, limited scaling.

**Alternative:** PostgreSQL/MySQL would support multi-user scenarios but require a running database service and credentials.

---

### **3. Plain-Text Password Storage**

**Chosen for simplicity in CS50 context:** Plain-text storage in SQLite
**Tradeoff:**

* Pros: Minimal implementation required for the scope of a learning project.
* Cons: Not secure for real-world deployments.

**Alternative:** Hashing with bcrypt/argon2 + salted storage for production-grade systems.

---

### **4. CSV for Import/Export**

**Chosen:** CSV file I/O
**Tradeoff:**

* Pros: Human-readable, interoperable with Excel/Google Sheets, trivial to parse.
* Cons: No schema validation, no type enforcement, doesn’t handle nested metadata.

**Alternative:**

* JSON/YAML for more structured metadata
* REST API sync or cloud storage for multi-device usage

---

### **5. Synchronous Blocking I/O**

**Chosen:** Traditional blocking input/output
**Tradeoff:**

* Pros: Simplifies implementation and reduces bugs in a CLI environment.
* Cons: Cannot run background tasks (e.g., API fetches or reminders) without threading or async.

**Alternative:**

* `asyncio` or threaded workers if real-time background operations were needed.

---

### **6. Local Storage Only**

**Chosen:** User library stored locally under `DATA/`
**Tradeoff:**

* Pros: Works offline, user-controlled, GDPR-friendly by accident.
* Cons: No syncing across machines, data loss if the directory is deleted.

**Alternative:**

* Cloud sync (Dropbox/Google Drive API)
* Web backend with REST endpoints

---

### **7. Testing Layer Scope**

**Chosen:** Unit tests for CRUD + db utilities
**Tradeoff:**

* Pros: Covers core logic, database interaction is validated.
* Cons: No integration testing for full workflows (login + CRUD + export).

**Alternative:**

* Integration + end-to-end tests (pytest + tempfile DB or mock filesystem)

---

### **Conclusion**

The design choices prioritize **simplicity, portability, and educational value** over production-level scalability or UX polish. For a CS50P final project, these tradeoffs are reasonable and intentional; if evolved into a real-world tool, the above areas provide a clear roadmap for improvement.

---


## 🎓 Final Note

Personal Library Manager was built from scratch for the CS50P Final Project and demonstrates proficiency with Python modules, file organization, SQLite databases, CLI design, data persistence, and software testing.

---

