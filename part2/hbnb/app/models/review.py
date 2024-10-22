from base_model import BaseModel
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
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if not isinstance(value, str):
            raise TypeError("User id must uuid4")
        else:
            self.__user = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, str):
            raise TypeError("Place id must uuid4")
        else:
            self.__place = value
