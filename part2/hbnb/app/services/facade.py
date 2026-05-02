from app.persistence.repository import SQLAlchemyRepository
# If you created the user_repository, import it here:
# from app.persistence.user_repository import UserRepository 

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        # 1. Switch to SQLAlchemy Repositories
        # If you created the specialized UserRepository, use: self.user_repo = UserRepository()
        self.user_repo = SQLAlchemyRepository(User) 
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # --- User Methods ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        # SQLAlchemyRepository handles this cleanly now
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    # --- Amenity Methods ---
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # --- Place Methods ---
    def create_place(self, place_data):
        # 2. SQLAlchemy only needs the Foreign Key (owner_id), 
        # but we still check if the user exists first.
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner.id  # Pass the ID instead of the object
        )
        
        # Handle amenities
        amenity_ids = place_data.get('amenities', [])
        for amt_id in amenity_ids:
            amenity = self.get_amenity(amt_id)
            if amenity:
                place.amenities.append(amenity) # SQLAlchemy handles the Join Table!

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # --- Review Methods ---
    def create_review(self, review_data):
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))
        
        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")

        # 3. Pass the Foreign Keys
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=place.id,
            user_id=user.id
        )
        
        self.review_repo.add(new_review)
        # We NO LONGER need to manually add the review to a place's list. 
        # SQLAlchemy's "backref" handles that automatically!
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews # SQLAlchemy handles fetching these from the DB

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # 4. We NO LONGER need to manually remove it from the Place's list.
        # SQLAlchemy deletes the row, and it automatically disappears from place.reviews
        return self.review_repo.delete(review_id)