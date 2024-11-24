from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from flask import jsonify

api = Namespace('auth', security='token', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get email, password from request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(json.dumps({
        'id': str(user.id),
        'is_admin': user.is_admin
        })
        )
         
        # Step 4: Return the JWT token to the client
        return jsonify(access_token=access_token)

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.doc(security='token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = json.loads(get_jwt_identity())  # Retrieve the user's identity from the token
        return jsonify(message='Hello, user ' + current_user['id'])
