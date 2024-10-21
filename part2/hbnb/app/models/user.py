from base_model import BaseModel
"""Module Define Users class """


class Users(BaseModel):
    """Users class based on BaseModel class"""

    def __init__(self, first_name, last_name, email, is_admin):
        """Constructor for Users class"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.admin = is_admin
        self.places = []  # List to store related Places
        self.reviews = []  # List to store related reviews

    def add_place(self, place):
        """Add a places to the places."""
        self.places.append(place)
