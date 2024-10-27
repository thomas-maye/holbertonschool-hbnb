from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User
"""Review module for our HBnB project.

This module contains the Review class, which defines reviews for places
in our HBnB project.
"""


class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("The text of the Review can't be empty")
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("The rating must be a number from 1 to 5")
        self.__rating = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise TypeError("place must be an instance of Place")
        else:
            self.__place = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, User):
            raise TypeError("user must be an instance of User")
        else:
            self.__user = value

