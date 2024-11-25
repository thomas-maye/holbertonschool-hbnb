from app.models.base_model import BaseModel
from app.models.user import User
from app import db
from sqlalchemy.orm import relationship
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """Place class that inherits from BaseModel."""
   
    __tablename__ = 'places'

    title = db.Column(db.String(36), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def remove_review(self, review):
        """Remove a review from the place."""
        if review in self.reviews:
            self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
