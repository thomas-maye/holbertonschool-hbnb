from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class that inherits from BaseModel."""
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) > 50:
            raise ValueError("Amenity name exceeds maximum length")
        self.__name = value
