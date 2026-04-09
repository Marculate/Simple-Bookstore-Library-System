import uuid
from datetime import date, timedelta
from Classes.Books import Book
from Classes.Users import Users
from Classes.Borrowing_Records import Borrowing_Records
from File_Handling_Utilities.File_Handler import FileHandler


class Library:
    DEFAULT_LOAN_PERIOD = 16

    BOOKS_FILE = "books.csv"
    USERS_FILE = "users.csv"
    BORROW_REC_FILE = "borrowing_records.csv"

    BOOKS_FIELDS = [
        "ISBN",
        "Title",
        "Author",
        "Publishing Year",
        "Total Copies",
        "Available Copies"
    ]
    USERS_FIELDS = ["user_id", "name", "email", "registration_date"]
    BORROW_REC_FIELDS = [
        "Borrow Record ID",
        "User ID",
        "ISBN",
        "Borrow Date",
        "Due Date",
        "Return Date",
    ]

    def __init__(self, data_directory="data"):
        self.file_handler = FileHandler(data_directory)
        self.books = {}
        self.users = {}
        self.records = {}

        self.file_handler.file_exist_confirmation(self.BOOKS_FILE, self.BOOKS_FIELDS)
        self.file_handler.file_exist_confirmation(self.USERS_FILE, self.USERS_FIELDS)
        self.file_handler.file_exist_confirmation(
            self.BORROW_REC_FILE, self.BORROW_REC_FIELDS
        )

    def load_all_data(self):
        self.books.clear()
        self.users.clear()
        self.records.clear()

        for row in self.file_handler.read_csv_file(self.BOOKS_FILE):
            book = Book.from_dict(row)
            self.books[book.isbn] = book

        for row in self.file_handler.read_csv_file(self.USERS_FILE):
            user = Users.from_dict(row)
            self.users[user.user_id] = user

        for row in self.file_handler.read_csv_file(self.BORROW_REC_FILE):
            if row.get("Return Date") == "":
                row["Return Date"] = None
            record = Borrowing_Records.from_dict(row)
            self.records[record.borrow_record_id] = record

    def save_books(self):
                rows = [book.into_dict() for book in self.books.values()]
                self.file_handler.write_csv_file(self.BOOKS_FILE, rows, self.BOOKS_FIELDS)

    def save_users(self):
        rows = [
            {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "registration_date": user.registration_date,
            }
            for user in self.users.values()
        ]
        self.file_handler.write_csv_file(self.USERS_FILE, rows, self.USERS_FIELDS)

    def save_records(self):
        rows = [record.todict() for record in self.records.values()]
        self.file_handler.write_csv_file(self.RECORDS_FILE, rows, self.RECORDS_FIELDS)

    def save_all_data(self):
        self.save_books()
        self.save_users()
        self.save_records()

    def add_book(self, isbn, title, author, pub_year, tot_copies=1):
        isbn = str(isbn).strip()
        if isbn in self.books:
            raise ValueError(f"Book with ISBN '{isbn}' already exists.")
        self.books[isbn] = Book(isbn, title, author, pub_year, tot_copies)
        self.save_books()
        return self.books[isbn]

    def get_book(self, isbn):
        return self.books.get(str(isbn).strip())

    def list_books(self):
        return sorted(self.books.values(), key=lambda item: item.title.lower())

    def add_user(self, user_id, name, email, registration_date=None):
        user_id = str(user_id).strip()
        if user_id in self.users:
            raise ValueError(f"User with ID '{user_id}' already exists.")
        if registration_date is None:
            registration_date = date.today().isoformat()
        self.users[user_id] = Users(user_id, name, email, registration_date)
        self.save_users()
        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(str(user_id).strip())

    def list_users(self):
        return sorted(self.users.values(), key=lambda item: item.name.lower())

    def _next_record_id(self):
        nums = []
        for key in self.records.keys():
            if key.startswith("BR-"):
                try:
                    nums.append(int(key.split("-")[1]))
                except (IndexError, ValueError):
                    pass
        return f"BR-{(max(nums) + 1) if nums else 1:04d}"

    def borrow_book(self, user_id, isbn, borrow_date=None, loan_days=None):
        user = self.get_user(user_id)
        if user is None:
            raise ValueError(f"User ID '{user_id}' not found.")

        book = self.get_book(isbn)
        if book is None:
            raise ValueError(f"ISBN '{isbn}' not found.")

        if not book.is_it_available():
            raise ValueError(f"No available copies for '{book.title}'.")

        if loan_days is None:
            loan_days = self.DEFAULT_LOAN_DAYS

        if borrow_date is None:
            borrow_dt = date.today()
        else:
            borrow_dt = date.fromisoformat(str(borrow_date))

        due_dt = borrow_dt + timedelta(days=int(loan_days))

        record = Borrowing_Records(
            borrow_record_id=self._next_record_id(),
            user_id=user.user_id,
            isbn=book.isbn,
            borrow_date=borrow_dt.isoformat(),
            due_date=due_dt.isoformat(),
            return_date=None,
        )

        book.book_borrow()
        self.records[record.borrow_record_id] = record

        self.save_books()
        self.save_records()
        return record

    def return_book(self, borrow_record_id, return_date=None):
        record_id = str(borrow_record_id).strip()
        record = self.records.get(record_id)

        if record is None:
            raise ValueError(f"Borrow record '{record_id}' not found.")
        if record.is_returned:
            raise ValueError(f"Borrow record '{record_id}' already returned.")

        book = self.get_book(record.isbn)
        if book is None:
            raise ValueError(f"Book with ISBN '{record.isbn}' not found.")

        record.mark_as_returned(return_date)
        book.return_book()

        self.save_books()
        self.save_records()
        return record

    def list_all_records(self):
        return list(self.records.values())

    def list_active_records(self):
        return [record for record in self.records.values() if not record.is_returned]

    def list_overdue_records(self):
        return [record for record in self.records.values() if record.isoverdue()]

    def list_user_records(self, user_id):
        user_id = str(user_id).strip()
        return [record for record in self.records.values() if record.user_id == user_id]