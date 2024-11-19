from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

jwt = JWTManager()
bcrypt = Bcrypt()

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

    authorizations = {
        'token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Type in the *"Value"* input box below: **"Bearer &lt;JWT&gt;"**, where JWT is the token',
        }
    }
    
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        authorizations=authorizations)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    jwt.init_app(app)
    bcrypt.init_app(app)

    return app
