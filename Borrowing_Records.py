from datetime import date, datetime

class Borrowing_Records:
    def __init__(
            self, borrow_record_id, user_id, isbn, borrow_date, due_date, return_date=None
    ):

            self.borrow_record_id = borrow_record_id.strip()
            if not self.borrow_record_id:
                raise ValueError("Borrow record ID is required")

            self.user_id = str(user_id).strip()
            if not self.user_id:
                raise ValueError("User ID is required")


            self.isbn = str(isbn).strip()
            if not self.isbn:
                raise ValueError("ISBN is required")


            self.borrow_date = self.todate_str(borrow_date, "Borrow Date")
            self.due_date = self.todate_str(due_date, "Due Date")

            borrow = self.parsedate(self.borrow_date, "Borrow Date")
            due = self.parsedate(self.due_date, "Due Date")
            if due < borrow:
                raise ValueError(
                    f"Due Date ({due_date}) cannot be before borrow Date ({borrow_date})"
                )

            cleaned_return_date = self.todate_str(
                return_date, "Return Date", allow_blank=True
            )

            if cleaned_return_date is None:
                self.return_date = None
            else:
                returned = self.parsedate(cleaned_return_date, "Return Date")
                if returned < borrow:
                    raise ValueError(
                        f"Return Date ({returned} cannot be before borrow Date ({borrow})"
                    )
                self.return_date = cleaned_return_date

    @staticmethod
    def todate_str(value, field_name, allow_blank=False):
        if value is None:
            if allow_blank:
                return None
            raise ValueError(f"Field {field_name} is required")
        if isinstance(value, datetime):
            return value.date().isoformat()
        if isinstance(value, date):
            return value.isoformat()


        cleaned_value = str(value).strip()
        if not cleaned_value:
            if allow_blank:
                return None
            raise ValueError(f"Field {field_name} is required")

        parsed_value = Borrowing_Records.parsedate(cleaned_value, field_name)
        return parsed_value.isoformat()



    @staticmethod
    def parsedate(value, field_name):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError(
                f"{field_name} is not a valid date, it must be in YYYY-MM-DD format"
                             ) from exc


    @property
    def is_returned(self, return_date=None):
        return self.return_date is not None


    def mark_as_returned(self, return_date=None):
        if self.is_returned:
            raise   ValueError(
                f"This record ({self.borrow_record_id}) is already returned"
            )
        cleaned_return_date = self.todate_str(
            return_date,
            field_name="Return Date",
            allow_blank=True
        )
        if cleaned_return_date is None:
            self.return_date = date.today().isoformat()
            return

        borrow = self.parsedate(self.borrow_date, "Borrow Date")
        returned = self.parsedate(self.cleaned_return_date, "Return Date")
        if returned < borrow:
            raise ValueError(
                f"Return Date ({returned} cannot be before borrow Date ({borrow})"
            )
        self.return_date = cleaned_return_date



    def isoverdue(self):
        if self.is_returned:
            return False
        due = self.parsedate(self.due_date, "Due Date")
        return date.today() > due


    def daysuntil_due(self):
        if self.is_returned:
            return 0
        due = self.parsedate(self.due_date, "Due Date")
        return (due - date.today()).days


    def todict(self):
        return {
            "Borrow Record ID": self.borrow_record_id,
            "User ID": self.user_id,
            "ISBN": self.isbn,
            "Borrow Date": self.borrow_date,
            "Due Date": self.due_date,
            "Return Date": self.return_date,
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            borrow_record_id=data["Borrow Record ID"],
            user_id=data["User ID"],
            isbn=data["ISBN"],
            borrow_date=data["Borrow Date"],
            due_date=data["Due Date"],
            return_date=data["Return Date"],
        )


    def __str__(self):
        if self.is_returned:
            status = f"Returned on {self.return_date}"
        elif self.isoverdue():
            status = "Overdue"
        else:
            status = f"Not Returned - Due Date {self.due_date}"
        return (
            f"Borrow Record ID: {self.borrow_record_id} | User ID: {self.user_id} | ISBN: {self.isbn} "
            f"(Borrowed: {self.borrow_date}, [{status}]"
        )