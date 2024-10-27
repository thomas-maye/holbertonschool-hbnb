from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place class that inherits from BaseModel."""

    def __init__(self, title, description, price, latitude,
                 longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """Title of the place."""
        return self.__title

    @title.setter
    def title(self, value):
        """Set the title of the place."""
        if len(value) > 100:
            raise ValueError("Title exceeds maximum length")
        self.__title = value

    @property
    def description(self):
        """Description of the place."""
        return self.__description

    @description.setter
    def description(self, value):
        """Set the description of the place."""
        self.__description = value

    @property
    def price(self):
        """Price of the place."""
        return self.__price

    @price.setter
    def price(self, value):
        """Set the price of the place."""
        if value <= 0:
            raise ValueError("Price must be positive")
        self.__price = value

    @property
    def latitude(self):
        """Latitude of the place."""
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude of the place."""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self.__latitude = value

    @property
    def longitude(self):
        """Longitude of the place."""
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude of the place."""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self.__longitude = value

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("user must be an instance of User")
        else:
            self.__owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def remove_review(self, review):
        """Remove a review from the place."""
        if review in self.reviews:
            self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
