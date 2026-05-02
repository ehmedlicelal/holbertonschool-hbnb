from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# ... (Keep amenity_model, user_model, review_model here) ...

# 1. NEW: A specific model for user input (Creating/Updating)
# Notice we removed 'owner_id' because the JWT token handles it!
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenities': fields.List(fields.String, description='List of Amenity IDs')
})

# 2. Keep your original model for the output responses
place_model = api.model('Place', {
    # ... your original fields ...
})

@api.route('/')
class PlaceList(Resource):
    
    @api.expect(place_input_model) # Use the input model here
    @jwt_required() 
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity() 
        
        place_data = api.payload
        place_data['owner_id'] = current_user_id # Securely assign ownership behind the scenes

        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'owner_id': new_place.owner_id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve all places (Public)"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'latitude': p.latitude,
            'longitude': p.longitude
        } for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
            'reviews': [{'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id} for r in place.reviews]
        }, 200

    @api.expect(place_input_model) # Use input model for updates too
    @jwt_required()
    def put(self, place_id):
        """Update a place (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Verify the logged-in user owns this place OR is an admin
        if place.owner_id != current_user_id and not is_admin:
            return {'error': 'Unauthorized: You do not own this place'}, 403

        facade.update_place(place_id, api.payload)
        return {'message': 'Place updated successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Get all reviews for a specific place (Public)"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [{
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id
        } for r in reviews], 200