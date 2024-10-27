from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.place_repo = InMemoryRepository()  # Repository for places
        self.user_repo = InMemoryRepository()   # Repository for users
        self.amenity_repo = InMemoryRepository()  # Repository for amenities
        self.review_repo = InMemoryRepository()  # Repository for reviews

    """
    User
    """
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update(user_id, user_data)
            return user
        return None

    """
    Places
    """
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
        owner = self.user_repo.get(place_data['owner_id'])
        place = Place(title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return place
        return None

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.validate_place_data(place_data)  # Validate data before updating
        place = self.get_place(place_id)
        if place:
            place.owner = self.get_user(place_data['owner_id'])
            self.place_repo.update(place_id, place_data)
            return place
        return None

    """
    Amenities
    """
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
        return amenities
    
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        place.add_amenity(amenity)
        return place

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        place.remove_amenity(amenity)
        return place

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
        # Logic will be implemented in later tasks
        pass

    """
    Reviews
    """
    def create_review(self, review_data):
        # avant de créer la review il faut déja valider que le user et la place
        # existent
        user = self.get_user(review_data.get('user_id'))
        place = self.get_place(review_data.get('place_id'))

        if not user or not place:
            raise ValueError("Invalid user or place ID")

        rating = review_data.get('rating')
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        # Créer une nouvelle instance de Review
        new_review = Review(
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
            raise ValueError("Review not found")

        return place.reviews


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
