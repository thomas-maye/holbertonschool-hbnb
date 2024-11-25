from app.models.base_model import BaseModel
from app import db
import uuid
from sqlalchemy.orm import relationship
from app.models.place_amenity import place_amenity

class Amenity(BaseModel):
    """Amenity class that inherits from BaseModel."""
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    