# 📚 Personal Library Manager – Project Roadmap (Fixed, Sane Version)

## Phase 0: Setup (DONE)

**Goal:** Establish folder structure, environment, and dependencies.

**Actions:**

1. Create project folder structure:

```
personal_library_manager/
│
├── project.py
├── DB/
│   └── library.db
├── utils/
│   ├── __init__.py
│   ├── db_handler.py
│   └── mail_handler.py   # placeholder, optional later
├── scripts/
│   └── dummy_data.py
├── tests/
│   ├── test_utils.py
│   └── test_models.py
├── requirements.txt
└── README.md
```

2. Initialize Python virtual environment and install dependencies.
3. Initialize Git repository for version control.

---

## Phase 1: Core Database Layer

**Goal:** Make a solid, testable SQLite backend.

**Modules:**

- `utils/db_handler.py` → All SQLite operations
- `scripts/dummy_data.py` → Insert sample records for testing

**Tasks:**

1. Implement SQLite database with columns:

   - `id` (INTEGER, PRIMARY KEY)
   - `title` (TEXT, NOT NULL)
   - `author` (TEXT)
   - `year` (INTEGER, optional)
   - `read` (BOOLEAN)

2. Create DB initialization function.

3. Implement CRUD functions:

   - `add_book()`
   - `get_book_by_id()`
   - `get_all_books()`
   - `update_book()`
   - `delete_book()`

---

## Phase 2: Input Validation & Error Handling

**Goal:** Prevent garbage input and avoid crashes like an adult program.

**Validation Rules to Implement:**

1. **Empty titles rejected**

   - Title cannot be empty or whitespace.
   - Raise a clear exception or return an error message.

2. **Invalid years handled**

   - Year must be:

     - An integer
     - Reasonable (e.g., 0 < year ≤ current year)

   - Non-numeric or future years fail gracefully.

3. **Non-existent IDs fail gracefully**

   - Updating or deleting a book ID that doesn’t exist:

     - Should not crash
     - Should return `False` or a meaningful error

4. Centralize validation logic inside `db_handler.py` or helper functions.

---

## Phase 3: Command Line Interface (CLI)

**Goal:** Make the project usable without any web nonsense.

**File:**

- `project.py`

**Tasks:**

1. Build a menu-based CLI:

   - Add book
   - View all books
   - Search book by ID or title
   - Update book
   - Delete book
   - Mark as read/unread

2. Validate user input before passing to DB functions.

3. Display clean, readable output.

---

## Phase 4: Advanced CLI Features

**Goal:** Show sophistication without overengineering.

**Features:**

1. Search books by:

   - Title
   - Author

2. Sort books:

   - By title
   - By year
   - By read status

3. Filter:

   - Read vs unread

4. Pagination for large libraries (simple offset/limit logic)

---

## Phase 5: Testing & Quality

**Goal:** Prove your code doesn’t panic under pressure.

**Tasks:**

1. Write pytest tests for:

   - All CRUD functions
   - Input validation failures
   - Edge cases

2. Test edge cases:

   - Empty database
   - Empty title input
   - Invalid year input
   - Non-existent IDs



---

## Phase 6: Documentation & Submission

**Goal:** Make it submission-ready for CS50P.

**Tasks:**

1. Write `README.md` including:

   - Project description
   - Features
   - Folder structure
   - How to run

2. Record a **3-minute demo video**:

   - Show CLI
   - Add, update, delete books
   - Show validation errors working

3. Submit using `submit50`.

---

## Phase 7: Stretch Goals (Optional, Only If Time Exists)

These are **extras**, not requirements:

- Export library to CSV
- Import from CSV
- Reading statistics (counts, percentages)

---
