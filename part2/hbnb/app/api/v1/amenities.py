from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'title': fields.String(required=True, description='Title of the amenity'),
    'description': fields.String(description='Description of the amenity')
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

            new_amenity = facade.create_amenity(aminites_data)


        except ValueError as e:
            return {'message': str(e)}, 400

            return {'name' : }

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.__dict__ for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Retrieve details of an amenity by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return amenity.__dict__, 200
        except ValueError as e:
            return {'message': str(e)}, 404

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity"""
        try:
            updated_amenity = facade.update_amenity(amenity_id, api.payload)
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
