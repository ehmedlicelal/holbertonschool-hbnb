from app import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # In SQL, we store the IDs (Foreign Keys)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__()
        self.text = kwargs.get('text')
        self.rating = kwargs.get('rating')
        self.place_id = kwargs.get('place_id')
        self.user_id = kwargs.get('user_id')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return value

    @validates('text')
    def validate_text(self, key, value):
        if not value or not value.strip():
            raise ValueError("Review text cannot be empty.")
        return value