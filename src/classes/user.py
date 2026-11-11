class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    def can_cancel_booking(self, booking):
        return self.role in ["curator", "admin"] or booking.user == self
