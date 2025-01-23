from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Unique user ID
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    passwd_hash = db.Column(db.String(120), nullable=False)
    is_guide = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    tours = db.relationship("Tour", back_populates="user", lazy=True)
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    guide = db.relationship("Guide", back_populates="user", uselist=False)
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def get_id(self):
        return str(self.id)


class Guide(db.Model):
    __tablename__ = "guides"
    nid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Unique guide ID
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, unique=True)  # Foreign key to users table
    bio = db.Column(db.Text)

    reviews = db.relationship("Review", back_populates="guide", cascade="all, delete-orphan")
    availability = db.relationship("Availability", back_populates="guide", cascade="all, delete-orphan")
    user = db.relationship("User", back_populates="guide", uselist=False)
    tours = db.relationship("Tour", back_populates="guide")


class Tour(db.Model):
    __tablename__ = "tours"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)  # Foreign key to users
    guide_nid = db.Column(db.String(36), db.ForeignKey("guides.nid"), nullable=True)  # Foreign key to guides

    user = db.relationship("User", back_populates="tours")
    guide = db.relationship("Guide", back_populates="tours")


class Preset_Tour(db.Model):
    __tablename__ = "preset_tours"
    id = db.Column(db.Integer, db.ForeignKey("tours.id"), primary_key=True)  # Foreign key to tours table
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    availability = db.relationship("Availability", backref="preset_tour", lazy=True, cascade="all, delete-orphan")


class Availability(db.Model):
    __tablename__ = "availability"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guide_id = db.Column(db.String(36), db.ForeignKey("guides.nid", name="fk_availability_guide"), nullable=False)  # Foreign key to guides
    tour_id = db.Column(db.Integer, db.ForeignKey("preset_tours.id", name="fk_availability_tour"), nullable=True)  # Foreign key to preset_tours
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    guide = db.relationship("Guide", back_populates="availability")

    __table_args__ = (
        db.UniqueConstraint('guide_id', 'tour_id', name='uq_guide_tour'),
    )


class Review(db.Model):
    __tablename__ = "reviews"
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)  # Foreign key to users
    guide_id = db.Column(db.String(36), db.ForeignKey("guides.nid"), nullable=False)  # Foreign key to guides
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    __table_args__ = (db.PrimaryKeyConstraint("user_id", "guide_id"),)

    user = db.relationship("User", back_populates="reviews")
    guide = db.relationship("Guide", back_populates="reviews")
