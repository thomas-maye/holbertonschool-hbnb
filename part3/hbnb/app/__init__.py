from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

from app.api.v1.auth import api as auth_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.users import api as users_ns
import config

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    authorizations = {
        'token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type in the *"Value"* input box below: **"Bearer &lt;JWT&gt;"**, where JWT is the token',
        }
    }

    api = Api(
        app, version='1.0',
        title='HBnB API',
        authorizations=authorizations,
        description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app