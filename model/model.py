from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    passwd_hash = db.Column(db.String(120), nullable=False)
    isGuide = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    tours = db.relationship("Tour", backref="user", lazy=True)
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    guide = db.relationship("Guide", back_populates="user")
    
    @property
    def is_active(self):
        return self.active  # Ensure user is active for log




class Guide(db.Model):
    __tablename__ = "guides"
    nid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)
    bio = db.Column(db.Text)

    reviews = db.relationship("Review", back_populates="guide", cascade="all, delete-orphan")
    availability = db.relationship("Availability", back_populates="guide", cascade="all, delete-orphan")
    user = db.relationship("User", back_populates="guide")


class Tour(db.Model):
    __tablename__ = "tours"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    isPreset = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    isComplete = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    guide_nid = db.Column(db.Integer, nullable=False)
    guide_user_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['guide_nid', 'guide_user_id'],
            ['guides.nid', 'guides.user_id']
        ),
    )


class Preset_Tour(db.Model):
    __tablename__ = "preset_tours"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tours.id"), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Availability(db.Model):
    __tablename__ = "availability"
    guide_id = db.Column(db.Integer, db.ForeignKey("guides.nid"),primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey("tours.id"), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    guide = db.relationship("Guide", back_populates="availability")


class Review(db.Model):
    __tablename__ = "reviews"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    guide_id = db.Column(db.Integer, db.ForeignKey("guides.nid"), nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint("user_id", "guide_id"),)

    # Define relationships for back_populates
    user = db.relationship("User", back_populates="reviews")
    guide = db.relationship("Guide", back_populates="reviews")

