from app import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates

# 1. The Join Table for the Many-to-Many relationship
# This table exists only in the database to link Places and Amenities
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign Key to the User (The owner)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    # One-to-Many: One place has many reviews
    reviews = db.relationship('Review', backref='place', lazy=True, cascade="all, delete-orphan")
    
    # Many-to-Many: Uses the 'secondary' table defined above
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')

    def __init__(self, **kwargs):
        super().__init__()
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.price = kwargs.get('price')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')
        self.owner_id = kwargs.get('owner_id')

    # SQLAlchemy Validators
    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be a non-negative float.")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return float(value)
    