from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place class that inherits from BaseModel."""

    def __init__(self, title, price, latitude, longitude, owner_id, owner=None, description=None):
        super().__init__()
        self._title = title
        self._description = description if description else ""
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
        self.owner_id = owner_id
        self._owner = owner  # Attribut owner
        self.reviews = []
        self.amenities = []
        self.validate()

    @property
    def title(self):
        """Title of the place."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title of the place."""
        if len(value) > 100:
            raise ValueError("Title exceeds maximum length")
        self._title = value

    @property
    def description(self):
        """Description of the place."""
        return self._description

    @description.setter
    def description(self, value):
        """Set the description of the place."""
        self._description = value

    @property
    def price(self):
        """Price of the place."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price of the place."""
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        """Latitude of the place."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude of the place."""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        """Longitude of the place."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude of the place."""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def owner_id(self):
        """ID of the owner of the place."""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Set the ID of the owner of the place."""
        if not value:
            raise ValueError("Owner ID cannot be None or empty")
        self._owner_id = value

    def validate(self):
        """Validate the attributes of the place."""
        self.title = self._title
        self.price = self._price
        self.latitude = self._latitude
        self.longitude = self._longitude
        self.owner_id = self._owner_id  # Validation de owner_id

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
