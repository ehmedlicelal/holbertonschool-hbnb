from app import db, bcrypt
from app.models.base import BaseModel
from sqlalchemy.orm import validates
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships: These allow you to access a user's places/reviews easily
    # e.g., user_obj.places will return a list of Place objects
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def __init__(self, **kwargs):
        super().__init__()
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.is_admin = kwargs.get('is_admin', False)
        if 'password' in kwargs:
            self.hash_password(kwargs['password'])

    # Password Logic
    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies the password hash."""
        return bcrypt.check_password_hash(self.password, password)

    # SQLAlchemy Validators (Replacing your manual Part 2 logic)
    @validates('email')
    def validate_email(self, key, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    @validates('first_name', 'last_name')
    def validate_not_empty(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key.replace('_', ' ').capitalize()} cannot be empty")
        return value.strip()