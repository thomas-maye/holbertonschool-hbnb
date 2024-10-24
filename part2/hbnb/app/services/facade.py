from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
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
        name = amenity_data.get('name')

        if not name:
            raise ValueError('Amenity name is required')

            new_amenity = Amenity(id=str(uuid.uuid4()),
                                  name=name)
            self.amenity_repo.add(new_amenity)
            return new_amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get_by_id(amenity_id)
        if not amenity:
            raise ValueError('Amenity not found')
        return amenity


def get_all_amenities(self):
    return self.amenity_repo.get_all()


def update_amenity(self, amenity_id, amenity_data):
    amenity = self.amenity_repo.get_by_id(amenity_id)
    if not amenity:
        raise ValueError('Amenity not found')

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        self.amenity_repo.update(amenity)
        return amenity
