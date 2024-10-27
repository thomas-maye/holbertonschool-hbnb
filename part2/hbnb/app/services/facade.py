from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
import uuid


class HBnBFacade:
    def __init__(self):
        self.place_repo = InMemoryRepository()  # Repository for places
        self.user_repo = InMemoryRepository()   # Repository for users
        self.amenity_repo = InMemoryRepository()  # Repository for amenities

    def create_user(self, user_data):
        user = User(**user_data)
        user.save()
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def validate_place_data(self, place_data):
        # Validate the place data.

        if 'price' in place_data:
            if place_data['price'] < 0:
                raise ValueError("Price must be a non-negative float.")

        if 'latitude' in place_data:
            if not (-90 <= place_data['latitude'] <= 90):
                raise ValueError("Latitude must be between -90 and 90.")

        if 'longitude' in place_data:
            if not (-180 <= place_data['longitude'] <= 180):
                raise ValueError("Longitude must be between -180 and 180.")

        if not self.user_repo.get(place_data['owner_id']):
            raise ValueError("Invalid owner_id. User does not exist.")

    def create_place(self, place_data):
        self.validate_place_data(place_data)
        place = Place(**place_data)
        place.save()
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            # Include owner and amenities
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = self.amenity_repo.get_by_attribute('place_id',
                                                                 place_id)
            return place
        return None

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.validate_place_data(place_data)  # Validate data before updating
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)  # Update the place attributes
            return place
        return None

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by its ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        amenities = self.amenity_repo.get_all()
        for amenity in amenities:
            for key, value in amenity.__dict__.items():
                if isinstance(value, list):
                    amenity.__dict__[key] = value
        return amenities

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
        # Logic will be implemented in later tasks
        pass


    def create_review(self, review_data):
        # avant de créer la review il faut déja valider que le user et la place
        # existent
        user = self.user_repo.get(review_data.get('user_id'))
        place = self.place_repo.get(review_data.get('place_id'))

        if not user or not place:
            raise ValueError("Invalid user or place ID")

        rating = review_data.get('rating')
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        # Créer une nouvelle instance de Review
        review_id= str(uuid.uuid4())   # donner un ID unique a la review
        new_review = Review(
            id=review_id,
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        # Save la review dans le review_repo(liste des reviews)
        self.review_repo.add(new_review)
        return new_review

    # Method pour avoir la review par son ID
    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    # Method pour afficher toutes les reviews
    def get_all_reviews(self):
        return self.review_repo.get_all()

    # Method pour afficher toutes les reviews depuis une place
    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Récupérer toutes les reviews et filtrer par place
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]


    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)


    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        self.review_repo.delete(review_id)
        return review
