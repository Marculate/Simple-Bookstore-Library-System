from datetime import date
from main_library_scripts.Library import Library




def pause():
    input("\nPress Enter to continue...")


def books_menu(lib):
    while True:
        print("\nBooks Menu")
        print("1. List books")
        print("2. Add book")
        print("3. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            all_books = lib.list_books()
            if not all_books:
                print("No books found.")
            else:
                for book in all_books:
                    print(book)
            pause()

        elif choice == "2":
            isbn = input("ISBN: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            year = input("Publishing year: ").strip()
            copies = input("Total copies: ").strip()

            try:
                lib.add_book(isbn, title, author, int(year), int(copies))
                print("Book added.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def users_menu(lib):
    while True:
        print("\nUsers Menu")
        print("1. List users")
        print("2. Add user")
        print("3. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            all_users = lib.list_users()
            if not all_users:
                print("No users found.")
            else:
                for user in all_users:
                    print(user)
            pause()

        elif choice == "2":
            user_id = input("User ID: ").strip()
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            reg_date = input(
                "Registration date (YYYY-MM-DD), leave empty for today: "
            ).strip()

            if not reg_date:
                reg_date = date.today().isoformat()

            try:
                lib.add_user(user_id, name, email, reg_date)
                print("User added.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def records_menu(lib):
    while True:
        print("\nBorrow/Return Menu")
        print("1. Borrow book")
        print("2. Return book")
        print("3. Active records")
        print("4. Overdue records")
        print("5. Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            user_id = input("User ID: ").strip()
            isbn = input("ISBN: ").strip()
            days = input("Loan days (empty for default): ").strip()

            try:
                if not days:
                    record = lib.borrow_book(user_id, isbn)
                else:
                    record = lib.borrow_book(user_id, isbn, loan_days=int(days))
                print(f"Borrowed. Record ID: {record.borrow_record_id}")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "2":
            record_id = input("Borrow Record ID: ").strip()
            return_date = input(
                "Return date YYYY-MM-DD (empty for today): "
            ).strip()
            if not return_date:
                return_date = None

            try:
                lib.return_book(record_id, return_date)
                print("Returned.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "3":
            active_records = lib.list_active_records()
            if not active_records:
                print("No active records.")
            else:
                for record in active_records:
                    print(record)
            pause()

        elif choice == "4":
            overdue_records = lib.list_overdue_records()
            if not overdue_records:
                print("No overdue records.")
            else:
                for record in overdue_records:
                    print(record)
            pause()

        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def main():
    lib = Library("data")
    lib.load_all_data()

    while True:
        print("\nLibrary System")
        print("1. Books")
        print("2. Users")
        print("3. Borrow/Return")
        print("4. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            books_menu(lib)
        elif choice == "2":
            users_menu(lib)
        elif choice == "3":
            records_menu(lib)
        elif choice == "4":
            print("Bye")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
