from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place class that inherits from BaseModel."""

    def __init__(self, title, price, latitude, longitude, owner_id,
                 description=None):
        super().__init__()
        self._title = title
        self._description = description if description else ""
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
        self._owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        self.validate()

    @property
    def title(self):
        """Getter method for title attribute."""
        return self._title

    @title.setter
    def title(self, value):
        """Setter method for title attribute"""
        if len(value) > 100:
            raise ValueError("Title exceeds maximum length")
        self._title = value

    @property
    def description(self):
        """Getter method for description attribute."""
        return self._description

    @description.setter
    def description(self, value):
        """Setter method for description attribute"""
        self._description = value

    @property
    def price(self):
        """Getter method for price attribute."""
        return self._price

    @price.setter
    def price(self, value):
        """Setter method for price attribute"""
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        """Getter method for latitude attribute."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Setter method for latitude attribute"""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        """Getter method for longitude attribute."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter method for longitude attribute"""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def owner_id(self):
        """Getter method for owner attribute."""
        return self._owner_id

    @owner_id.setter
    def owner(self, value):
        """Setter method for owner attribute"""
        self._owner_id = value

    def validate(self):
        """Validate the attributes of the place."""
        self.title = self._title
        self.price = self._price
        self.latitude = self._latitude
        self.longitude = self._longitude

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def update(self, place_data):
        """Update the place attributes based on the provided data."""
        if 'title' in place_data:
            self.title = place_data['title']
        if 'description' in place_data:
            self.description = place_data['description']
        if 'price' in place_data:
            self.price = place_data['price']
        if 'latitude' in place_data:
            self.latitude = place_data['latitude']
        if 'longitude' in place_data:
            self.longitude = place_data['longitude']
        if 'owner_id' in place_data:
            self.owner_id = place_data['owner_id']
        self.validate()
