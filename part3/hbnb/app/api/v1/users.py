from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
import json

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, descritpion='User password')
})


@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token') 
    def post(self):
        """Register a new user (only by an Admin)"""
        user_data = api.payload

        # Retrieve the current user from the JWT token
        current_user = json.loads(get_jwt_identity())

        # Check if the user is admin
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Simulate email uniqueness check
        # (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)

        return {'id': new_user.id, 'message': 'User successfully created'}, 201

    @api.response(200, "User list retrieve")
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_all_users()
        if not users:
            return {'error': 'No users found'}, 404

        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email}
            for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, "User Updated")
    @api.doc(security='token') 
    def put(self, user_id):
        """Update User information and only admin can update email and password"""
        # Retrieve the current user from the JWT token
        current_user = json.loads(get_jwt_identity())

        # Get the user data from the request payload
        user_data = api.payload

        # Get the user
        user = facade.get_user(user_id)

        # Check if the user exists
        if not user:
            return {"error": "User not found"}, 404
        
        # Check if the user is admin
        if current_user.get('is_admin'):
            #  Administrators can modify any user, including changing the email and password, but must ensure that the email is not duplicated.
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already in use"}, 400

        else:
            # Check if the user is the same as the current user
            if user.id != current_user['id']:
                return {"error": "Unauthorized action"}, 403
            
            # Check if email and password fields are present in the request payload
            if 'email' in user_data or 'password' in user_data:
                # Check if the user is trying to modify email or password
                if user_data['email'] != user.email or not user.verify_password(user_data['password']):
                    return {"error": "You cannot modify email or password."}, 400
            else:
                user_data['email'] = user.email
                user_data['password'] = user.password

        # Update the user data
        user = facade.update_user(user_id, user_data)

        # Return the updated user data
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
