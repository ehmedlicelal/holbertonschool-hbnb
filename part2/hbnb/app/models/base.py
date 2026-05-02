from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # This prevents SQLAlchemy from creating a 'basemodel' table

    # id: Uses a UUID string as the primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # created_at: Automatically set when the record is first created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # updated_at: Automatically updated every time the record is changed
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Standard save method (SQLAlchemy handles the session commit in the repo)"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        # Note: In Part 3, the Repository will handle db.session.commit()