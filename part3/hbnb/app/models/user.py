from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError
import re
import bcrypt


"""Module Define Users class """


class User(BaseModel):
    """Users class based on BaseModel class"""

    def __init__(self, first_name, last_name, email, password, is_admin=False):
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
        self.reviews = []  # List to store related Reviews
        self.__password = None

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

        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(regex, value):
            raise EmailNotValidError("Email format not valid.")

        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized

        except EmailNotValidError as e:
            print(str(e))

        self.__email = email

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):

        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        self.__is_admin = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.__password = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.__password, password)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.hash_password(value)
