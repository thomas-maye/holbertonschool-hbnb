from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
import json

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
add_review_model = api.model('AddReview', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    #'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

update_review_model = api.model('UpdateReview', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(add_review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    def post(self):
        """Register a new review"""
        # Retrieve the current user from the JWT token
        current_user = json.loads(get_jwt_identity())

        # Store the user ID in the payload
        review_data = api.payload
        review_data['user_id'] = current_user['id']

        # Retrieve the place
        place = facade.get_place(api.payload['place_id'])

        # If the place does not exist, return a 404 error with the message "Place not found."
        if not place:
            return {'message': 'Place not found'}, 404

        # If the user is the owner of the place, return a 400 error with the message "You cannot review your own place."
        if current_user['id'] == place.owner.id:
            return {'message': 'You cannot review your own place.'}, 400
        
        # If the user has already reviewed the place, return a 400 error with the message "You have already reviewed this place."
        for review in place.reviews:
            if review.user.id == current_user['id']:
                return {'message': 'You have already reviewed this place.'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201

        except ValueError as e:
            return {'message': str(e)},

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
        return {'message': 'Review not found'}, 404

    @jwt_required()
    @api.expect(update_review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security='token')
    def put(self, review_id):
        """Update a review's information"""
        # Retrieve the current user from the JWT token
        current_user = json.loads(get_jwt_identity())

        review = facade.get_review(review_id)
        
        if not review:
            return {'message': 'Review not found'}, 404
        
        if review.user_id != current_user['id']:
            return {'message': 'Unauthorized action.'}, 403

        try:
            updated_review = facade.update_review(review_id, api.payload)
            if updated_review:
                return {'message': 'Review updated successfully'}, 200
            return {'message': 'Review not found'}, 404
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.doc(security='token')
    def delete(self, review_id):
        """Delete a review"""
        # Retrieve the current user from the JWT token
        current_user = json.loads(get_jwt_identity())

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        
        if review.user_id != current_user['id']:
            return {'message': 'Unauthorized action.'}, 403

        deleted_review = facade.delete_review(review_id)
        if deleted_review:
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404

@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @jwt_required()
    @api.expect(add_review_model)
    @api.doc(security='token')
    def put(self, review_id):
        """Update Review by an Admin"""
        
        current_user = json.loads(get_jwt_identity())
        
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'message': 'Review not found'}, 404
            
        updated_review_data = api.payload
        
        try:
            updated_review = facade.update_review(review_id, updated_review_data)
            
            if updated_review:
                return {'message': 'Review updated successfully'}, 200
            
            return {'message': 'Review not found'}, 404
        
        except ValueError as e:
            return {'message': str(e)}, 400
        
    @jwt_required()
    @api.doc(security='token')
    def delete(self, review_id):
        """Delete Review by an Admin"""
        
        current_user = json.loads(get_jwt_identity())
        
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'message': 'Review not found'}, 404    
        
        review = facade.get_review(review_id)
        deleted_review = facade.delete_review(review_id)
        
        if deleted_review:
            return {'message': 'Review deleted successfully'}, 200
