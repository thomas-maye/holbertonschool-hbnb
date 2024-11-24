from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

from app.services import initialize_facade  # Import the facade initializer

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-thomas"  # JWT Secret Key
    app.config.from_object(config_class)  # Load configuration

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        # Ensure tables are created
        db.create_all()

        # Initialize the facade
        initialize_facade(app)

        # Import namespaces after app context to avoid circular imports
        from app.api.v1.auth import api as auth_ns
        from app.api.v1.reviews import api as reviews_ns
        from app.api.v1.places import api as places_ns
        from app.api.v1.amenities import api as amenities_ns
        from app.api.v1.users import api as users_ns

        # API authorizations for JWT
        authorizations = {
            'token': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Type in the *"Value"* input box below: **"Bearer <JWT>"**, where JWT is the token',
            }
        }

        # Initialize the Flask-RESTx API
        api = Api(
            app, version='1.0',
            title='HBnB API',
            authorizations=authorizations,
            description='HBnB Application API',
            doc='/api/v1/'  # Swagger UI at /api/v1/
        )

        # Register namespaces
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
