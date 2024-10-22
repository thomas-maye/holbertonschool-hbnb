from base_model import BaseModel
from email_validator import validate_email, EmailNotValidError
"""Module Define Users class """


class User(BaseModel):
    """Users class based on BaseModel class"""

    def __init__(self, first_name, last_name, email, is_admin):
        """
        Constructor for Users class

        Args:
            first_name (string): First name of the user
            last_name (string): Last name of the user
            email (string): Email address of the user
            is_admin (bool): Flag to check if the user has admin privileges
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store related Places

    def add_place(self, place):
        """Add a places to the places."""
        self.places.append(place)

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):

        length = len(value)

        if not isinstance(value, str):
            raise TypeError("First Name must be a String")

        if length > 50:
            raise ValueError("Required, maximum length of 50 characters")

        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):

        length = len(value)

        if not isinstance(value, str):
            raise TypeError("Last Name must be a String")

        if length > 50:
            raise ValueError("Required, maximum length of 50 characters")

        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        """
        Sets the email address for the user after validating and
        normalizing it.

        Args:
            value (str): The email address to set.

        Raises:
            EmailNotValidError: If the provided email is invalid.
        """
        email = value

        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized

        except EmailNotValidError as e:

            # The exception message is human-readable explanation of why it's
            # not a valid (or deliverable) email address.
            print(str(e))

        self.__email = email

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):

        if not isinstance(value, bool):
            raise TypeError("is_admin mut be a boolean")
        self.__is_admin = value
