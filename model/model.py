from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime

db = SQLAlchemy()

class User(db.model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(80), nullable=False)
    passwd_hash = db.Column(db.String(120),nullable = False)
    isGuide = db.Column(db.Boolean, default=False)

    tours = db.relationship("Tour", backref="user", lazy=True)
    guide = db.relationship("Guide", back_populates="user")
    


class Guide(db.model):
    __tablename__ = "guides"
    nid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key = True, nullalbe=False)
    bio = db.Column(db.Text)
    
    #add review table

    #relationships
    #reviews = add reviews relationship
    user = db.relationship("User", back_populates="guide", cascade="all, delete-orphan")
    availability=db.relationship("Availability", back_populates="guide", cascade="all, delete-orphan")




class Tour(db.model):
    __tablename__ = "tours"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    isPreset = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    isComplete = db.Column(db.Boolean)

    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    #guide ids
    guide_nid = db.Column(db.Integer, nullable=False)

    #relationship def
    user = db.relationship("User", backref="tours", lazy=True)
    preset_tour = db.relationship("Preset_Tours", backref="tours", lazy=True)



class Preset_Tour(db.Model):
    __tablename__="preset_tours"
    id = db.Column(db.Integer, db.ForeingKey("tours.id"))
    title=db.Column(db.String(80), nullable=False)
    description=db.Column(db.Text, nullable=False)


class Availability(db.Model):
    __tablename__ = "availability"
    guide_id = db.Column(db.Integer, db.ForeignKey("guides.id"), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey("tours.id"))
    start_date = db.Column(db.Date, nullable=False, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    guide=db.relationship("Guide", back_populates="availability")

class Review(db.Model):
    __tablename__="reviews"
    #add stuff

