from base_model import BaseModel
import uuid4
"""Review module for our HBnB project.

This module contains the Review class, which defines reviews for places
in our HBnB project.
"""

class Review(BaseModel):

    def __init__(self, text, rating, place, user):
        super().__init__()
        self._text = text
        self._rating = rating
        self._place = place
        self._user = user


    @property
    def text(self):
        return self._text


    @text.setter
    def text(self, value):
        if not value:
            raise ValueError("The text of the Review can't be empty")
        self._text = value


    @property
    def rating(self):
        return self._rating


    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not ( 1 <= value <= 5):
            raise ValueError("The rating must be a number from 1 to 5")
        self._rating = value


    @property
    def user(self):
        return self._user


    @user.setter
    def user(self, value):
        if not isinstance(value, uuid4):
            raise TypeError("User id must uuid4")
        else:
            self.user = value


    @property
    def place(self):
        return self._place


    @place.setter
    def place(self, value):
        if not isinstance(value, uuid4):
            raise TypeError("Place id must uuid4")
        else:
            self.place = value
