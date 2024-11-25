from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import json

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            "id": new_amenity.id,
            "name": new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, "No amenities found")
    def get(self):
        """Retrieve a list of all amenities"""
        amenities_list = facade.get_all_amenities()

        if not amenities_list:
            return {"message": "No amenities found"}, 404

        return [{
            "id": amenity.id,
            "name": amenity.name
        } for amenity in amenities_list], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return {
            "id": amenity.id,
            "name": amenity.name,
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": updated_amenity.id,
            "name": updated_amenity.name
        }, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.doc(security='token')
    def post(self):
        """Create Aminity by an Admin"""
        
        current_user = json.loads(get_jwt_identity())
        
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        
        amenity_data = api.payload
        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400
        new_amenity = facade.create_amenity(amenity_data)
        return {
            "id": new_amenity.id,
            "name": new_amenity.name
        }, 201
        
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.doc(security='token')
    def put(self, amenity_id):
        """Update Aminities by an Admin"""
        
        current_user = json.loads(get_jwt_identity())
        
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        # Logic to update an amenity
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        if not amenity_data or not amenity_data.get("name"):
            return {"error": "Invalid input data"}, 400
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        
        return {
            "id": updated_amenity.id,
            "name": updated_amenity.name
        }, 200