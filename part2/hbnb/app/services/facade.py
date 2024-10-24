from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place


class HBnBFacade:
    def __init__(self, place_repo=None, user_repo=None, amenity_repo=None):
        self.place_repo = InMemoryRepository()  # Repository for places
        self.user_repo = InMemoryRepository()   # Repository for users
        self.amenity_repo = InMemoryRepository()  # Repository for amenities

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
    def validate_place_data(self, place_data):
        """Validate the place data."""
        if 'price' in place_data:
            price = place_data['price']
            if price < 0:
                raise ValueError("Price must be a non-negative float.")

        if 'latitude' in place_data:
            latitude = place_data['latitude']
            if not (-90 <= latitude <= 90):
                raise ValueError("Latitude must be between -90 and 90.")

        if 'longitude' in place_data:
            longitude = place_data['longitude']
            if not (-180 <= longitude <= 180):
                raise ValueError("Longitude must be between -180 and 180.")

        owner_id = place_data.get('owner_id')
        if not self.user_repo.get(owner_id):
            raise ValueError("Invalid owner_id. User does not exist.")

    def create_place(self, place_data):
        self.validate_place_data(place_data)  # Validate attributes

        place_attrs = {
            'title': place_data['title'],
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner_id': place_data['owner_id'],
            'description': place_data.get('description', "")
        }

        place = Place(**place_attrs)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            # Include owner and amenities
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = [self.amenity_repo.get(
                amenity_id) for amenity_id in place.amenities]
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
