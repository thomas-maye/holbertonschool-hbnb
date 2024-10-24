from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        aminities_data = api.payload
        try:
            new_amenity = facade.create_amenity(aminities_data)
        except ValueError as e:
            return {'message': str(e)}, 400
        return {'name': new_amenity}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve details of an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity, 200
        return {'message': 'Amenity not found'}, 404

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenities_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenities_data)
        except ValueError as e:
            return {'message': str(e)}, 400
        if updated_amenity:
            return {'message': 'Amenity updated successfully'}, 200
        return {'message': 'Amenity not found'}, 404
