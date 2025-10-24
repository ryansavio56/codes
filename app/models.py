from __future__ import annotations
from datetime import datetime
from . import db

class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)  # e.g., resort, retreat, mindfulness spot
    has_wifi = db.Column(db.Boolean, default=False)  # should be False for detox, but configurable
    allows_screens = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('Image', backref='destination', cascade='all, delete-orphan')

    def primary_image(self) -> 'Image | None':
        if not self.images:
            return None
        # prefer explicit primary if marked; else first
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0]

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
