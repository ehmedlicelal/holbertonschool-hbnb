from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner  # Expects a User object
        self.amenities = []  # List to store Amenity instances
        self.reviews = []    # List to store Review instances

    def _validate_price(self, value):
        if value < 0:
            raise ValueError("Price must be a non-negative float.")
        return float(value)

    def _validate_latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return float(value)

    def _validate_longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return float(value)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)