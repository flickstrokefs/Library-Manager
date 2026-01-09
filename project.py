# ----------------------------
# Imports
# ----------------------------

import datetime as dt
from colorama import init, Fore, Style
init(autoreset=True)

COLORS = {
    "success": Fore.GREEN,
    "error": Fore.RED,
    "warn": Fore.YELLOW,
    "info": Fore.CYAN,
    "normal": Fore.WHITE
}

#defiing colours
def printc(msg, level="normal", bright=False):
    color = COLORS.get(level, Fore.WHITE)
    style = Style.BRIGHT if bright else ""
    print(style + color + msg)

def prompt(msg, level="info", bright=False):
    color = COLORS.get(level, Fore.WHITE)
    style = Style.BRIGHT if bright else ""
    return style + color + msg + Fore.RESET


# Utils
from utils.__init__ import init_db
from utils.db_handler import (check_user, add_user, add_book, delete_book,
                              list_books, search_books, update_book, find_book,
                              check_book, csv_importer, csv_exporter)

# ----------------------------
# Main CLI Interface
# ----------------------------

def main():
    init_db()

    user_id = None

    while True:
        choice = input(prompt("Login or Register? (l/r): ")).strip().lower()

        if choice == "l":
            username = input(prompt("Username: ")).strip()
            password = input(prompt("Password: ")).strip()

            user_id = check_user(username, password)

            if user_id:
                printc("✅ Login successful.", "success")
                break
            else:
                printc("❌ Invalid username or password.", "error")

        elif choice == "r":
            username = input(prompt("Choose a username: ")).strip()
            email = input(prompt("Email: ")).strip()
            password = input(prompt("Password: ")).strip()

            user_id = add_user(username, email, password)

            if user_id:
                printc("✅ Account created.", "success")
                break
            else:
                printc("❌ User already exists.", "error")

        else:
            printc("❌ Enter 'l' or 'r'.", "error")

    printc(f"User ID in session: {user_id}", "info")

    while True:
        printc("\n📚 Personal Library Manager", "info", bright=True)
        print("""
        1. ➕ Add Book
        2. 📖 List Books 
        3. 🔍 Search Books 
        4. ✏️ Update Book 
        5. ❌ Delete Book
        6. 📥 Import CSV
        7. 📤 Export CSV
        8. 🚪 Exit
        """)

        choice = input(prompt("Choose an option: ")).strip()

        # --- ADD BOOK ---
        if choice == "1":
            title = input(prompt("Title: ")).strip()
            author = input(prompt("Author: ")).strip()

            if not title or not author:
                printc("❌ Title and author cannot be empty.", "error")
                continue

            try:
                year = int(input(prompt("Year: ")).strip())
                if year < 0:
                    raise ValueError
            except ValueError:
                printc("❌ Year must be a valid positive number.", "error")
                continue

            read_input = input(prompt("Have you read it? (y/n): ")).strip().lower()
            if read_input not in ("y", "n"):
                printc("❌ Enter 'y' or 'n'.", "error")
                continue

            read = read_input == "y"
            genre = input(prompt("Genre/Tags (optional): ")).strip()
            note = input(prompt("Note (optional): ")).strip()

            success = add_book(user_id, title, author, year, genre, read, note)
            printc("✅ Book added!" if success else "❌ Failed to add book.", "success" if success else "error")

        # --- LIST BOOKS ---
        elif choice == "2":
            books = list_books(user_id)

            if not books:
                printc("📭 No books found.", "warn")
                continue

            filter_field = input(prompt("Filter by genre or read? (g/r/blank): ")).strip().lower()
            if filter_field == "g":
                genre = input(prompt("Enter genre: ")).strip().lower()
                books = [b for b in books if b[5] and genre in b[5].lower()]
            elif filter_field == "r":
                read_filter = input(prompt("Read status (y/n): ")).strip().lower()
                if read_filter == "y":
                    books = [b for b in books if b[4] == 1]
                elif read_filter == "n":
                    books = [b for b in books if b[4] == 0]

            SORT_FIELDS = {"title": 1, "author": 2, "year": 3, "genre": 5, "read": 4}
            sort_key = input(prompt("Sort by (title/author/year/genre/read or blank): ")).strip().lower()
            if sort_key in SORT_FIELDS:
                index = SORT_FIELDS[sort_key]
                books.sort(key=lambda b: b[index])

            PAGE_SIZE = 5
            total = len(books)
            page = 0

            while True:
                start = page * PAGE_SIZE
                end = start + PAGE_SIZE
                chunk = books[start:end]

                if not chunk:
                    printc("No more results.", "warn")
                    break

                printc("\nID | Title | Author | Year | Read | Genre | Note", "info", bright=True)
                printc("-" * 80, "info")

                for book in chunk:
                    read_status = "✅" if book[4] else "❌"
                    printc(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {read_status} | {book[5]} | {book[6]}")

                cmd = input(prompt("\nEnter (n)ext, (p)revious, (e)xit: ")).strip().lower()

                if cmd == "n":
                    if end < total:
                        page += 1
                    else:
                        printc("No more pages.", "warn")
                elif cmd == "p":
                    if page > 0:
                        page -= 1
                    else:
                        printc("Already on first page.", "warn")
                else:
                    break

        # --- SEARCH BOOKS ---
        elif choice == "3":
            keyword = input(prompt("Search keyword (title/author): ")).strip()

            if not keyword:
                printc("❌ Search keyword cannot be empty.", "error")
                continue

            results = search_books(user_id, keyword)

            if not results:
                printc("🔍 No matching books found.", "warn")
                continue

            PAGE_SIZE = 5
            total = len(results)
            page = 0

            while True:
                start = page * PAGE_SIZE
                end = start + PAGE_SIZE
                chunk = results[start:end]

                if not chunk:
                    printc("No more results.", "warn")
                    break

                printc("\nID | Title | Author | Year | Read | Genre | Note", "info", bright=True)
                printc("-" * 80, "info")

                for book in chunk:
                    read_status = "✅" if book[4] else "❌"
                    printc(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {read_status} | {book[5]} | {book[6]}")

                cmd = input(prompt("\nEnter (n)ext, (p)revious, (e)xit: ")).strip().lower()
                if cmd == "n":
                    if end < total:
                        page += 1
                    else:
                        printc("No more pages.", "warn")
                elif cmd == "p":
                    if page > 0:
                        page -= 1
                    else:
                        printc("Already on first page.", "warn")
                else:
                    break

        # --- UPDATE BOOK ---
        elif choice == "4":
            try:
                book_id = int(input(prompt("Book ID to update: ")).strip())
                if book_id <= 0:
                    raise ValueError
            except ValueError:
                printc("❌ Invalid book ID.", "error")
                continue

            if not check_book(user_id, book_id):
                printc("❌ No such book for your account.", "error")
                continue

            title = input(prompt("New Title (leave blank to skip): ")).strip() or None
            author = input(prompt("New Author (leave blank to skip): ")).strip() or None

            year_input = input(prompt("New Year (leave blank to skip): ")).strip()
            if year_input:
                try:
                    year = int(year_input)
                    if year < 0:
                        raise ValueError
                except ValueError:
                    printc("❌ Invalid year.", "error")
                    continue
            else:
                year = None

            read_input = input(prompt("Mark as read? (y/n/leave blank to skip): ")).strip().lower()
            if read_input == "y":
                read = True
            elif read_input == "n":
                read = False
            elif read_input == "":
                read = None
            else:
                printc("❌ Enter 'y', 'n', or leave blank.", "error")
                continue

            genre = input(prompt("New Genre/Tags (leave blank to skip): ")).strip() or None
            note = input(prompt("New Note (leave blank to skip): ")).strip() or None

            updated = update_book(book_id, title, author, year, read, genre, note)
            printc("✅ Book updated!" if updated else "❌ Failed to update.", "success" if updated else "error")

        # --- DELETE BOOK ---
        elif choice == "5":
            try:
                book_id = int(input(prompt("Book ID to delete: ")).strip())
                if book_id <= 0:
                    raise ValueError
            except ValueError:
                printc("❌ Invalid book ID.", "error")
                continue

            if not check_book(user_id, book_id):
                printc("❌ No such book for your account.", "error")
                continue

            book = find_book(user_id, book_id)
            read_status = "✅" if book[4] else "❌"
            printc(f"Deleting: {book[1]} by {book[2]} ({book[3]}) {read_status}", "warn")

            confirm = input(prompt("Are you sure? (y/n): ")).strip().lower()
            if confirm != "y":
                printc("❎ Delete cancelled.", "warn")
                continue

            success = delete_book(book_id)
            printc("✅ Book deleted!" if success else "❌ Could not delete.", "success" if success else "error")

        # --- IMPORT CSV ---
        elif choice == "6":
            file_path = input(prompt("Enter the CSV file path: ")).strip()
            success = csv_importer(user_id, file_path)
            printc("📥 Import successful!" if success else "❌ Import failed.", "success" if success else "error")

        # --- EXPORT CSV ---
        elif choice == "7":
            success = csv_exporter(user_id)
            printc("📤 Export successful! Check DATA/EXPORT/" if success else "❌ Export failed.", "success" if success else "error")

        # --- EXIT ---
        elif choice == "8":
            printc("👋 Goodbye!", "info")
            break

        else:
            printc("❗ Invalid option. Try again.", "error")


if __name__ == "__main__":
    main()
