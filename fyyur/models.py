from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

'''
show = db.Table('show',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id', primary_key = True)),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id', primary_key = True)),
    db.Column('date', db.DateTime()))
'''

# Association Object. https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-pattern
class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable = False)
    start_time = db.Column(db.DateTime())
    venue = relationship('Venue', back_populates='artists')
    artist = relationship('Artist', back_populates='venues')
    def __rpr__(self):
        return (f'<Artist ID: {self.artist_id}, Venue ID: {self.venue_id}, start time: {self.start_time}')

# My design choice is that any venue or artist can post their info. on the website,
# but they must share at least one way to communicate and that is their phone.
# since not everyone have their own website, and not everyone intersted in facebook.
# also, phone is a quick way to communicate, and via calling we can get the location and etc.
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), default = 'N/A')
    state = db.Column(db.String(120), default = 'N/A')
    address = db.Column(db.String(), default = 'N/A')
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.String(120), default = 'N/A')
    image_link = db.Column(db.String(500), default = 'N/A')
    facebook_link = db.Column(db.String(120), default = 'N/A')
    website_link = db.Column(db.String(), default = 'N/A')
    seeking_talent  = db.Column(db.Boolean(), default = False)
    seeking_description = db.Column(db.String(), default = 'N/A')
    artists = db.relationship('Show', back_populates='venue')

    def __repr__(self):
        return f'''<ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state}, Phone: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}
        website_link: {self.website_link}, seeking_talent: {self.seeking_talent}, seeking_description: {self.seeking_description} >'''


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), default = 'N/A')
    state = db.Column(db.String(120), default = 'N/A')
    phone = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.String(120), default = 'N/A')
    image_link = db.Column(db.String(500), default = 'N/A')
    facebook_link = db.Column(db.String(120), default = 'N/A')
    website_link = db.Column(db.String(), default = 'N/A')
    seeking_venue = db.Column(db.Boolean(), default = False)
    seeking_description = db.Column(db.String(), default = 'N/A')
    venues = db.relationship('Show', back_populates='artist')
    
    def __repr__(self):
        return f'''<ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state}, Phone: {self.genres}, image_link: {self.image_link}, facebook_link: {self.facebook_link}
        website_link: {self.website_link}, looking_for_venues: {self.seeking_venue}, seeking_description: {self.seeking_description}>'''


