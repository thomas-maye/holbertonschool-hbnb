from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(
        required=True, description='Latitude of the place'),
    'longitude': fields.Float(
        required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner data')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description,
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        return [{
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                } for place in places], 200


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Fetch a place by its ID"""
        
        place_data = facade.get_place(place_id)

        owner_id = place_data.owner_id
        print(f"owner_id: {owner_id}")
        
        if owner_id is None:
            raise ValueError("Owner ID can't be None")

        owner_data = facade.get_user(owner_id)
        print(f"owner_data : {owner_data}")
        
        if owner_data is None:
            raise ValueError("Owner data can't be None")

        if not place_data:
            return {'error': 'Place not found'}, 404

        return {
            'id': place_data.id,
            'title': place_data.title,
            'description': place_data.description,
            'price': place_data.price,
            'latitude': place_data.latitude,
            'longitude': place_data.longitude,
            'owner': {
                'id': owner_id,
                'first_name': owner_data.first_name,
                'last_name': owner_data.last_name,
                'email': owner_data.email
            },
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place by its ID"""
        place_data = api.payload
        try:
            updated_place = facade.update_place(place_id, place_data)
            if updated_place:
                return {'id': updated_place.id,
                        'title': updated_place.title}, 200
            return {'error': 'Place not found'}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
