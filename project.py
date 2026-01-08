# ----------------------------
# Imports
# ----------------------------

import datetime as dt

# Utils
from utils.__init__ import init_db
#from utils.flick_utils import log_error, log_activity, send_email
from utils.db_handler import (check_user,add_user,add_book, delete_book, list_books, search_books, update_book,find_book,check_book,csv_importer,csv_exporter)


# ----------------------------
# Main CLI Interface
# ----------------------------

def main():
    init_db()

    user_id = None

    while True:
        choice = input("Login or Register? (l/r): ").strip().lower()

        if choice == "l":
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            user_id = check_user(username, password)

            if user_id:
                print("✅ Login successful.")
                break
            else:
                print("❌ Invalid username or password.")

        elif choice == "r":
            username = input("Choose a username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()

            user_id = add_user(username, email, password)

            if user_id:
                print("✅ Account created.")
                break
            else:
                print("❌ User already exists.")

        else:
            print("❌ Enter 'l' or 'r'.")

    # from here on, your entire app can safely rely on user_id
    print(f"User ID in session: {user_id}")

    while True:
        print("\n📚 Personal Library Manager")
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

        choice = input("Choose an option: ").strip()

        # ----------------------------
        # ADD BOOK
        # ----------------------------
        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()

            if not title or not author:
                print("❌ Title and author cannot be empty.")
                continue

            try:
                year = int(input("Year: ").strip())
                if year < 0:
                    raise ValueError
            except ValueError:
                print("❌ Year must be a valid positive number.")
                continue

            read_input = input("Have you read it? (y/n): ").strip().lower()
            if read_input not in ("y", "n"):
                print("❌ Enter 'y' or 'n'.")
                continue
            read = read_input == "y"

            genre = input("Genre/Tags (optional): ").strip()
            note = input("Note (optional): ").strip()

            success = add_book(user_id, title, author, year, genre, read, note)
            print("✅ Book added!" if success else "❌ Failed to add book.")

        # ----------------------------
        # LIST BOOKS
        # ----------------------------
        elif choice == "2":
            books = list_books(user_id)

            if not books:
                print("📭 No books found.")
                continue

            print("\nID | Title | Author | Year | Read | Genre | Note")
            print("-" * 80)
            for book in books:
                read_status = "✅" if book[5] else "❌"
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {read_status} | {book[6]} | ")
        # ----------------------------
        # SEARCH BOOKS
        # ----------------------------
        elif choice == "3":
            keyword = input("Search keyword (title/author): ").strip()

            if not keyword:
                print("❌ Search keyword cannot be empty.")
                continue

            results = search_books(user_id, keyword)

            if not results:
                print("🔍 No matching books found.")
                continue

            print("\nID | Title | Author | Year | Read | Genre | Note")
            print("-" * 80)
            for book in results:
                read_status = "✅" if book[5] else "❌"
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {read_status} | {book[6]} | ")

        # ----------------------------
        # UPDATE BOOK
        # ----------------------------
        elif choice == "4":
            try:
                book_id = int(input("Book ID to update: ").strip())
                if book_id <= 0:
                    raise ValueError
            except ValueError:
                print("❌ Invalid book ID.")
                continue

            title = input("New Title (leave blank to skip): ").strip() or None
            author = input("New Author (leave blank to skip): ").strip() or None

            year_input = input("New Year (leave blank to skip): ").strip()
            if year_input:
                try:
                    year = int(year_input)
                    if year < 0:
                        raise ValueError
                except ValueError:
                    print("❌ Invalid year.")
                    continue
            else:
                year = None

            read_input = input("Mark as read? (y/n/leave blank to skip): ").strip().lower()
            if read_input == "y":
                read = True
            elif read_input == "n":
                read = False
            elif read_input == "":
                read = None
            else:
                print("❌ Enter 'y', 'n', or leave blank.")
                continue

            genre = input("New Genre/Tags (leave blank to skip): ").strip() or None
            note = input("New Note (leave blank to skip): ").strip() or None

            updated = update_book(book_id, title, author, year, read, genre, note)
            print("✅ Book updated!" if updated else "❌ Failed to update.")

        # ----------------------------
        # DELETE BOOK
        # ----------------------------
        elif choice == "5":
            try:
                book_id = int(input("Book ID to delete: ").strip())
                if book_id <= 0:
                    raise ValueError
            except ValueError:
                print("❌ Invalid book ID.")
                continue

    
            if check_book(user_id,book_id):
                book=find_book(user_id,book_id)
                read_status = "✅" if book[5] else "❌"
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {read_status} | {book[6]} | ")

                confirm = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
                if confirm != "y":
                    print("❎ Delete cancelled.")
                    continue

                success = delete_book(book_id)
                print("✅ Book deleted!" if success else "❌ Could not delete.")
            else:
                print("❌ Could not delete. Book Id does not exist")
        
        # ----------------------------
        # Import Books into the DB
        # ----------------------------
        elif choice == "6":
            try:
               file_path=input("Enter the file path to the csv: ")
               csv_importer(user_id=user_id,file_path=file_path)
               print("Books imported sucesfully")
            except Exception as e:
                print("Failed during importing",e)

        # ----------------------------
        # Export Books as a CSV
        # ----------------------------
        elif choice == "7":
            try:
               csv_exporter(user_id)
               print("Files Exported Succesfully, Check DATA/export/your.csv")
            except Exception as e:
                print("Failed during importing",e)

        # ----------------------------
        # EXIT
        # ----------------------------
        elif choice == "8":
            print("👋 Goodbye!")
            break

        else:
            print("❗ Invalid option. Try again.")

if __name__ == "__main__":
    main()