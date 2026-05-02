from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# 1. Instantiate extensions globally (but don't bind them to an app yet)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="development"):
    app = Flask(__name__)
    
    # 2. Load configurations (This will include your SQLALCHEMY_DATABASE_URI)
    from config import config
    app.config.from_object(config[config_class])

    # 3. Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # 4. Initialize the API
    api = Api(app, version='1.0', title='HBnB API', 
              description='HBnB Application API', doc='/api/v1/')

    # Import namespaces inside the function to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    # 5. Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app