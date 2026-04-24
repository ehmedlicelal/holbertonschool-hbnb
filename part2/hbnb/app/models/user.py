import re
from app.models.base import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_not_empty(first_name, "First name")
        self.last_name = self._validate_not_empty(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_not_empty(self, value, field_name):
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()

    def _validate_email(self, email):
        # Regular expression for basic email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email