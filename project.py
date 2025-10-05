#importing much needed modules
from dotenv import load_dotenv

#importing from utils
from utils.db_handler import (init_db,add_book,delete_book,list_books,search_books,update_book,)

# ----------------------------
# Main CLI Interface
# ----------------------------

def main():
    init_db()
    while True:
        try:
            print("\nPersonal Library Manager")
            print("""
            1. Add Book
            2. List Books 
            3. Search Books 
            4. Update Book 
            5. Delete Book 
            6. Exit """)
            choice = input("Choose an option: ")
    
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                year = int(input("Year: "))
                read_input = input("Have you read it? (y/n): ").strip().lower()
                read = True if read_input == "y" else False
                add_book(title, author, year, read)
                print("Book added!")
            elif choice == "2":
                books = list_books()
                print("\nID | Title | Author | Year | Read")
                print("-" * 50)
                for book in books:
                    read_status = "Yes" if book[4] else "No"
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {read_status}")
            elif choice == "3":
                keyword = input("Search keyword: ")
                results = search_books(keyword)
                print("\nID | Title | Author | Year | Read")
                print("-" * 50)
                for book in results:
                    read_status = "Yes" if book[4] else "No"
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {read_status}")
            elif choice == "4":
                book_id = int(input("Book ID to update: "))
                title = input("New Title (leave blank to skip): ") or None
                author = input("New Author (leave blank to skip): ") or None
                year_input = input("New Year (leave blank to skip): ")
                year = int(year_input) if year_input else None
                read_input = input("Mark as read? (y/n/leave blank to skip): ").strip().lower()
                read = True if read_input == "y" else False if read_input == "n" else None
                update_book(book_id, title, author, year, read)
                print("Book updated!")
            elif choice == "5":
                book_id = int(input("Book ID to delete: "))
                delete_book(book_id)
                print("Book deleted!")
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option, try again.")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()