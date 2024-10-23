from app.persistence.repository import InMemoryRepository
from app.models.place import Place


class HBnBFacade:
    def __init__(self, place_repo=None, user_repo=None, amenity_repo=None):
        self.place_repo = InMemoryRepository()  # Repository for places
        self.user_repo = InMemoryRepository()   # Repository for users
        self.amenity_repo = InMemoryRepository()  # Repository for amenities


    def create_place(self, place_data):
        # Validate attributes
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

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            # Include owner and amenities
            place.owner = self.user_repo.get(place.owner_id) 
            place.amenities = [self.amenity_repo.get(amenity_id) for amenity_id in place.amenities]
            return place
        return None

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            # Update attributes and validate as needed
            if 'price' in place_data:
                price = place_data['price']
                if price < 0:
                    raise ValueError("Price must be a non-negative float.")
                place.price = price
            
            if 'latitude' in place_data:
                latitude = place_data['latitude']
                if not (-90 <= latitude <= 90):
                    raise ValueError("Latitude must be between -90 and 90.")
                place.latitude = latitude
            
            if 'longitude' in place_data:
                longitude = place_data['longitude']
                if not (-180 <= longitude <= 180):
                    raise ValueError("Longitude must be between -180 and 180.")
                place.longitude = longitude

            place.update(place_data)  # Assuming the Place class has an update method
            return place
        return None
