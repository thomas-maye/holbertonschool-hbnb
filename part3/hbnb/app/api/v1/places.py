from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
import json


api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True,
                          description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.doc(security='token')
    def post(self):
        """Register a new place"""
        current_user = json.loads(get_jwt_identity())
        place_data = api.payload
        place_data['owner_id'] = current_user['id']
        try:
            new_place = facade.create_place(place_data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,
        } for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Fetch a place by its ID"""

        # Get the place data
        place_data = facade.get_place(place_id)
        if not place_data:
            return {'error': 'Place not found'}, 404

        # Return the place data along with the owner data
        return {
            'id': place_data.id,
            'title': place_data.title,
            'description': place_data.description,
            'price': place_data.price,
            'latitude': place_data.latitude,
            'longitude': place_data.longitude,
            'owner': {
                'id': place_data.owner.id,
                'first_name': place_data.owner.first_name,
                'last_name': place_data.owner.last_name,
                'email': place_data.owner.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place_data.amenities],
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    def put(self, place_id):
        """Update a place by its ID"""
        # Retrieve the current user's from the JWT token
        current_user = json.loads(get_jwt_identity())
 
        place = facade.get_place(place_id)
        
        if place.owner.id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Update the place data
            place_data = api.payload
            place_data['owner_id'] = current_user['id']
            updated_place = facade.update_place(place_id, place_data)
            if updated_place:
                return {
                    "message": "Place updated successfully"
                }, 200

            # Return an error if the place is not found
            return {'error': 'Place not found'}, 404

        except ValueError as e:
            # Return an error if the input data is invalid
            return {'error': str(e)}, 400


@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenity(Resource):
    @api.response(200, 'Amenity added to place successfully')
    @api.response(404, 'Place or amenity not found')
    def post(self, place_id, amenity_id):
        """Add an amenity to a place"""
        try:
            # Add the amenity to the place
            facade.add_amenity_to_place(place_id, amenity_id)
            return {
                "message": "Amenity added to place successfully"
            }, 200

        except ValueError as e:
            # Return an error if the place or amenity is not found
            return {'error': str(e)}, 404

    def delete(self, place_id, amenity_id):
        """Remove an amenity from a place"""
        try:
            # Remove the amenity from the place
            facade.remove_amenity_from_place(place_id, amenity_id)
            return {
                "message": "Amenity removed from place successfully"
            }, 200

        except ValueError as e:
            # Return an error if the place or amenity is not found
            return {'error': str(e)}, 404


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        reviews = facade.get_reviews_by_place(place_id)

        if not place:
            return {'message': 'Place not found'}, 404
        
        if not reviews:
            return {'message': 'Reviews not found'}, 404

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in reviews], 200