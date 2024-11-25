from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User
from app import db
from sqlalchemy.orm import relationship
"""Review module for our HBnB project.

This module contains the Review class, which defines reviews for places
in our HBnB project.
"""


class Review(BaseModel):
    """Review class that inherits from BaseModel."""
    __tablename__ = 'reviews'

    text = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
