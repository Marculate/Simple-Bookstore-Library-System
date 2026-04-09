class Users:

    def __init__(
            self, user_id, name, email, registration_date
    ):
        self.user_id = user_id.strip()
        self.name = name.strip()
        self.email = self.validation_for_email(email)
        self.registration_date = registration_date.strip()





    def validation_for_email(self, email):
        cleaned_email = email.strip()
        indexing_email = cleaned_email.find('@')
        if indexing_email < 1 or "." not in cleaned_email[indexing_email:]:
            raise ValueError("Invalid email address")
        return cleaned_email


    def update_email(self, new_email):
        self.email = self.validation_for_email(new_email)


    def update_name(self, new_name):
        if not new_name.strip():
            raise ValueError("Name cannot be blank")
        self.name = new_name.strip()






    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            name=data['name'],
            email=data['email'],
            registration_date=data['registration_date']
        )




    def __str__(self):
        return (
            f"[{self.user_id}] {self.name} | email: {self.email} | Registered on:{self.registration_date}"
        )