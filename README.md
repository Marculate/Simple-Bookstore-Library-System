# Simple-Bookstore-Library-System
## Project Title and Purpose
This is a simple **Library Management System** built in Python.  
It runs in the **command line** and helps manage books, users, and borrowing records.

The goal of this project is to practice Python OOP concepts like classes, file handling, and exception handling in a real use case.

## Installation and Execution

### 1) Requirements
- Python 3.x installed

### 2) Run the project
1. Download or clone the project folder  
2. Open terminal in the project directory  
3. Run:

```bash
python main.py
```

## Example Usage
From the menu, you can:
- Add a new book
- Register a user
- Borrow a book
- Return a book
- View stored records

Example:
- User selects **Borrow Book**
- Enters user ID and ISBN
- System checks availability and creates a borrowing record

## Key Features
- Add, update, and view books
- Add and manage users
- Borrow and return book operations
- Overdue/return tracking through borrowing records
- CSV-based data storage (persistent data)

## Key Files
- `main.py` – command-line app flow and menu
- `Library.py` – core system logic and rules
- `Books.py` – book data model
- `Users.py` – user data model
- `Borrowing_Records.py` – borrowing record model
- `File_Handler.py` – CSV read/write operations
