from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user')  # <-- Add this line!
})

@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # 1. Check if email exists
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        # 2. Try to create user (this triggers model validation)
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id, 
                'first_name': new_user.first_name, 
                'last_name': new_user.last_name, 
                'email': new_user.email
            }, 201
        except ValueError as e:
            # This catches the "Invalid email format" error from the model
            return {'error': str(e)}, 400