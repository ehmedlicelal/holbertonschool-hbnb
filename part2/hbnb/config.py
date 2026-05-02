import os

class Config:
    # Existing keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # This creates a 'development.db' file in your project root
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///development.db')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}