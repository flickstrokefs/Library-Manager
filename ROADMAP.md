# Personal Library Manager - Project Roadmap

## Phase 0: Setup
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
│   ├── db_handler.py
│   └── mail_handler.py
├── scripts/
│   └── dummy_data.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_book.html
│   └── edit_book.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── tests/
│   ├── test_utils.py
│   └── test_models.py
├── requirements.txt
└── README.md
```

2. Initialize Python virtual environment and install dependencies.
3. Initialize Git repository for version control.

---

## Phase 1: Core Database & CLI
**Goal:** Make the backend functional before adding Flask.

**Modules:**
- `utils/db_handler.py` → SQLite operations
- `utils/mail_handler.py` → Email notifications (later)
- `scripts/dummy_data.py` → For testing

**Tasks:**
1. Implement SQLite database with columns: `id`, `title`, `author`, `read` (boolean).
2. Add CRUD functions in `db_handler.py`.
3. Write pytest tests for all DB functions in `tests/test_utils.py`.
4. Write a CLI in `project.py` to test DB functions.

---

## Phase 2: Flask Integration
**Goal:** Turn your CLI into a sleek web interface.

**Tasks:**
1. Setup Flask in `project.py` with routes:
   - `/` → Home, list books
   - `/add` → Add book form
   - `/edit/<id>` → Edit book form
   - `/delete/<id>` → Delete book
   - `/toggle_read/<id>` → Toggle read/unread
   - Optional: `/search` → Search results
2. Create HTML templates using Jinja2.
3. Create `base.html` with consistent header, nav bar, and footer.
4. Place CSS, JS, and images in `static/`.

---

## Phase 3: Advanced Features
**Goal:** Make the project sophisticated, reflecting your learning.

**Ideas:**
1. Search, sort, and filter books.
2. Pagination for large libraries.
3. User authentication with login/signup.
4. Email notifications for new books or reminders.
5. REST API endpoints for books.

---

## Phase 4: Styling & UX
**Goal:** Make it look fabulous, elegant, and sleek.

**Actions:**
1. Use Bootstrap or Tailwind CSS.
2. Add JavaScript interactions (toggle read/unread, live search suggestions).
3. Add icons for actions (delete, edit, read).
4. Add dark/light theme toggle.
5. Add subtle animations for UI enhancements.

---

## Phase 5: Testing & Quality
**Goal:** Ensure project is robust.

**Tasks:**
1. Write pytest tests for DB functions, API routes, and mail notifications.
2. Test form validations in Flask.
3. Test edge cases (empty DB, long titles, special characters).
4. Optional: Add logging for debugging.

---

## Phase 6: Documentation & Submission
**Goal:** Make it presentable and ready for CS50P.

**Tasks:**
1. Write README.md including project title, description, video link, folder structure, and features.
2. Record 3-minute demo video showcasing features.
3. Submit using `submit50`.

---

## Phase 7: Stretch Goals (Optional)
- Deploy project to Heroku, Render, or Fly.io.
- Add REST API authentication.
- Integrate with Google Books API for covers and metadata.
- Add user comments/notes on books.
- Add charts/statistics for reading trends.

---

**Outcome:**
Following this roadmap will result in a **modular, elegant, fully-functional web application** that demonstrates your skills in **Flask, SQLite, HTML/CSS/JS, API design, and testing**.

