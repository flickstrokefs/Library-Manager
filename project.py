# ----------------------------
# Imports
# ----------------------------

from dotenv import load_dotenv

# Utils
from utils.__init__ import init_db
from utils.flick_utils import log_error, log_activity, send_email
from utils.db_handler import add_book, delete_book, list_books, search_books, update_book

# ----------------------------
# Main CLI Interface
# ----------------------------

def main():

    init_db()

    user_id = int(input("Enter your user ID: "))  # Simulated login for now

    while True:
        try:
            print("\n📚 Personal Library Manager")
            print("""
            1. ➕ Add Book
            2. 📖 List Books 
            3. 🔍 Search Books 
            4. ✏️ Update Book 
            5. ❌ Delete Book 
            6. 🚪 Exit
            """)
            choice = input("Choose an option: ").strip()

            if choice == "1":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                year = int(input("Year: ").strip())
                read_input = input("Have you read it? (y/n): ").strip().lower()
                read = read_input == "y"
                genre = input("Genre/Tags (optional): ").strip()
                note = input("Note (optional): ").strip()
                success = add_book(user_id, title, author, year, genre, read, note)
                print("✅ Book added!" if success else "❌ Failed to add book.")

            elif choice == "2":
                books = list_books(user_id)
                print("\nID | Title | Author | Year | Read | Genre | Note")
                print("-" * 80)
                for book in books:
                    read_status = "✅" if book[5] else "❌"
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {read_status} | {book[6]} | ")

            elif choice == "3":
                keyword = input("Search keyword (title/author): ").strip()
                results = search_books(user_id, keyword)
                print("\nID | Title | Author | Year | Read | Genre | Note")
                print("-" * 80)
                for book in results:
                    read_status = "✅" if book[5] else "❌"
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {read_status} | {book[6]} | {book[7]}")

            elif choice == "4":
                book_id = int(input("Book ID to update: ").strip())
                title = input("New Title (leave blank to skip): ").strip() or None
                author = input("New Author (leave blank to skip): ").strip() or None
                year_input = input("New Year (leave blank to skip): ").strip()
                year = int(year_input) if year_input else None
                read_input = input("Mark as read? (y/n/leave blank to skip): ").strip().lower()
                read = True if read_input == "y" else False if read_input == "n" else None
                genre = input("New Genre/Tags (leave blank to skip): ").strip() or None
                note = input("New Note (leave blank to skip): ").strip() or None

                updated = update_book(book_id, title, author, year, read, genre, note)
                print("✅ Book updated!" if updated else "❌ Failed to update.")

            elif choice == "5":
                book_id = int(input("Book ID to delete: ").strip())
                success = delete_book(book_id)
                print("✅ Book deleted!" if success else "❌ Could not delete.")

            elif choice == "6":
                print("👋 Goodbye!")
                break

            else:
                print("❗ Invalid option. Try again.")

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()