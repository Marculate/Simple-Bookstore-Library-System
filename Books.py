class Book:

    #Information storage about a Book
    def __init__(
            self, isbn, title, author, pub_year, tot_copies = 1, available_copies = None
    ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.pub_year = int(pub_year)
        self.tot_copies = int(tot_copies)
        if tot_copies <= 0:
            raise ValueError("Copies must be at least 1.")
        if available_copies is None:
            self.available_copies = self.tot_copies
        else:
            self.available_copies = int(available_copies)


    def is_it_available(self):
        return self.available_copies >= 1


    def book_borrow(self):
        if not self.is_it_available():
            raise ValueError(
                f"There are no copies left of {self.title} to be borrowed."
            )
        self.available_copies = self.available_copies - 1



    def return_book(self):
        if self.available_copies >= self.tot_copies:
            raise ValueError(
                f"There are no copies of {self.title} that are borrowed."
            )
        self.available_copies += 1

    def num_copies_update(self, new_sum_copies):
        loaned_copies = self.tot_copies - self.available_copies
        if new_sum_copies < loaned_copies:
            raise ValueError(
                f"Number of copies on loan ({loaned_copies}) cannot be higher than the total copies ({self.tot_copies})."
            )


    def into_dict(self):
        return {
            "ISBN": self.isbn,
            "Title": self.title,
            "Author": self.author,
            "pub_year": self.pub_year,
            "Total Copies": self.tot_copies,
            "Available Copies": self.available_copies
        }


    @classmethod
    def from_dict(cls, data):
        return cls(
            isbn=data["ISBN"],
            title=data["Title"],
            author=data["Author"],
            pub_year=int(data["Publishing Year"]),
            tot_copies=int(data["Total Copies"]),
            available_copies=int(data["Available Copies"])
        )





    def __str__(self):
        book_status = f"{self.available_copies} out of {self.tot_copies} available"
        return (
            f"[{self.ISBN}] {self.title} by {self.author}, {self.pub_year} - {book_status} "
        )