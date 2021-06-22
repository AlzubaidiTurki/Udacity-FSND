#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
# $env:FLASK_APP=app.py
# $env:FLASK_ENV = "development"

import json
from re import search
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Artist, Venue, Show
import sys
from sqlalchemy.sql import text
from sqlalchemy import func
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
# TODO: #DONE connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():


  ''' OLD solultion
  class Area():
    city = ""
    state = ""
    venues = []
    def __init__(self, city, state, venue):
      self.city = city
      self.state = state
      self.venues.append(venue)
    def __repr__(self):
      return f'city: {self.city}, state: {self.state}, venues: {self.venues} \n'
    pass
  for row in sql:
    entry = {}
    print(f'row city = {row.city}, row state = {row.state}')
    venues = Venue.query.filter_by(city = row.city).filter_by(state = row.state).all()
    for venue in venues:
      venue.num_upcoming_shows = Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time >= datetime.datetime.now()).count()
      print(f'count {venue.num_upcoming_shows}')
      data.append(Area(city = row.city, state = row.state, venue = venue))
  '''
  data = []
  sql = Venue.query.distinct(Venue.city, Venue.state) # get every differnt combination of city and state.
  for row in sql:
    entry = {}
    entry['city'] = row.city
    entry['state'] = row.state
    entry['venues'] = []
    venues = Venue.query.filter_by(city = row.city).filter_by(state = row.state).all()
    for venue in venues:
      entry['venues'].append({
        'id' : venue.id,
        'name': venue.name,
        'num_upcoming_shows': Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time >= datetime.datetime.now()).count()
      })
    data.append(entry)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: #DONE implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {'count': 0, 'data':[]}
  search_term = request.form.get('search_term', '')
  sql = Venue.query.filter(func.lower(Venue.name).contains(func.lower(search_term)))
  for row in sql.all():
    response['count'] = response['count'] +1
    response['data'].append(row)
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  ''' OLD solution
  venue = Venue.query.filter_by(id = venue_id).first()
  venue.genres = list(venue.genres.split(', '))
  venue.past_shows = []
  venue.upcoming_shows = []
  venue.past_shows_count = 0
  venue.upcoming_shows_count = 0
  shows = Show.query.filter(Show.venue_id == venue.id).all()
  for show in shows:
    entry = {}
    artist = Artist.query.get(show.artist_id)
    entry['artist_id'] = artist.id
    entry['artist_name'] = artist.name
    entry['artist_image_link'] = artist.image_link
    entry['start_time'] = str(show.start_time)
    if show.start_time >= datetime.datetime.now():
      venue.upcoming_shows.append(entry)
      venue.upcoming_shows_count = venue.upcoming_shows_count + 1
    else:
        venue.past_shows.append(entry)
        venue.past_shows_count =   venue.past_shows_count +1
  '''
  data = {}
  venue = Venue.query.get(venue_id)
  data = venue.__dict__ # return every data attribute of object as dictionary.
  data['genres'] =  data['genres'].split(',') # string to list conversion, to parse correclty in the front-end.

  # new keys that does not exist in our object. (see old solution, see the difference? don't know which one is better practice though, probably this one.)
  data['past_shows'] = []
  data['upcoming_shows'] = []
  data['past_shows_count'] = 0
  data['upcoming_shows_count'] = 0

  show_time = str() # to put the show in correct list (past_shows or upcoming_Shows)
  shows = Show.query.filter(Show.venue_id == venue.id).all()
  for show in shows:
    if show.start_time >= datetime.datetime.now():
      show_time = 'upcoming_shows'
    else:
      show_time = 'past_shows'
    data[show_time].append({
      'artist_id': show.artist_id,
      'artist_name': Artist.query.get(show.artist_id).name,
      'artist_image_link': Artist.query.get(show.artist_id).image_link,
      'start_time': str(show.start_time)
    })

  data['past_shows_count'] = len(data['past_shows'])
  data['upcoming_shows_count'] = len(data['upcoming_shows'])
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
 
  
  ''' OLD SOLUTION
  try:
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    seeking_talent = request.get_json()['seeking_talent']
    if seeking_talent == 'y':
      seeking_talent = True
    seeking_description = request.get_json()['seeking_description']
    venue = Venue(name = name, city = city, state = state, address = address, phone = phone, genres = ", ".join(genres), # Convert from list to string.
    facebook_link = facebook_link, image_link = image_link, website_link = website_link, seeking_talent = seeking_talent,
    seeking_description = seeking_description)
    db.session.add(venue)
    db.session.commit()
    
  except:
    db.session.rollback()
    print('#ERROR POST VENUE#', sys.exc_info())

  finally:
    db.session.close()
  '''
  validation_flag = False
  error_flag = False
  form = VenueForm(request.form)
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    address = form.address.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data

    if form.seeking_talent.data == 'y':
      seeking_talent = True
    else:
      seeking_talent = False

    seeking_description = form.seeking_description.data

    if form.validate():
      venue = Venue(name = name, city = city, state = state, address = address, phone = phone, genres = ", ".join(genres), # Convert list to string.
                    facebook_link = facebook_link, image_link = image_link, website_link = website_link, seeking_talent = seeking_talent,
                     seeking_description = seeking_description)
      db.session.add(venue)
      db.session.commit()
    else:
      validation_flag = True

  except:
    db.session.rollback()
    print('#ERROR POST VENUE#', sys.exc_info())
    error_flag = True

  finally:
    db.session.close()

  if error_flag:
    flash('SORRY! An error occurred. Venue ' + name + ' could not be listed.')
  elif validation_flag:
    flash(f'ERROR in form fields, check: \n {form.errors} \n Venue {name} could not be listed.')
  else:
    flash('Venue ' + name + ' was successfully listed!')

  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO MISSING clicking that button delete it from the db then redirect the user to the homepage
  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
  except:
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  
  flash(f'Venue {venue.name} deleted sucessfully.')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  response = {'count': 0, 'data':[]}
  search_term = request.form.get('search_term', '')

  sql = Artist.query.filter(func.lower(Artist.name).contains(func.lower(search_term)))
  for row in sql.all():
    response['count'] = response['count'] +1
    response['data'].append(row)

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  ''' OLD Solution
  artist = Artist.query.get(artist_id)
  artist.genres = list(artist.genres.split(', '))
  artist.past_shows = []
  artist.upcoming_shows = []
  artist.past_shows_count = 0
  artist.upcoming_shows_count = 0

  shows = Show.query.filter(Show.artist_id == artist.id).all()
  for show in shows:
    entry = {}
    venue = Venue.query.get(show.venue_id)
    entry['venue_id'] = venue.id
    entry['venue_name'] = venue.name
    entry['venue_image_link'] = venue.image_link
    entry['start_time'] = str(show.start_time)
    if show.start_time >= datetime.datetime.now():
      artist.upcoming_shows.append(entry)
      artist.upcoming_shows_count = artist.upcoming_shows_count + 1
    else:
      artist.past_shows.append(entry)
      artist.past_shows_count = artist.past_shows_count +1
  '''
  # same logic as show_venu function. please read the comments there.
  data = {}
  artist = Artist.query.get(artist_id)
  data = artist.__dict__
  data['genres'] =  data['genres'].split(',')

  data['past_shows'] = []
  data['upcoming_shows'] = []
  data['past_shows_count'] = 0
  data['upcoming_shows_count'] = 0

  show_time = str()
  shows = Show.query.filter(Show.artist_id == artist.id).all()
  for show in shows:
    if show.start_time >= datetime.datetime.now():
      show_time = 'upcoming_shows'
    else:
      show_time = 'past_shows'
    data[show_time].append({
      'venue_id': show.artist_id,
      'venue_name': Venue.query.get(show.venue_id).name,
      'venue_image_link': Venue.query.get(show.venue_id).image_link,
      'start_time': str(show.start_time)
    })

  data['past_shows_count'] = len(data['past_shows'])
  data['upcoming_shows_count'] = len(data['upcoming_shows'])

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  if artist is None:
    return redirect(url_for('index'))

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.get(artist_id)

  if artist is None:
    return redirect(url_for('index'))
  validation_flag = False
  error_flag = False
  form = ArtistForm(request.form)
  try:
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.website_link = form.website_link.data
    artist.seeking_description = form.seeking_description.data

    if form.seeking_venue.data == 'y':
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    
    if form.validate():
      db.session.commit()
    else:
      validation_flag = True

  except:
    db.session.rollback()
    print('#EDIT ARTIST POST ERROR#', sys.exc_info())

  if error_flag:
    flash('SORRY! An error occurred. Venue ' + form.name.data + ' could not be listed.')
  elif validation_flag:
    flash(f'ERROR in form fields, check: \n {form.errors} \n Artist {form.name.data} could not be edited.')
  else:
    flash('Artist ' + form.name.data + ' was successfully edited!')

  db.session.close() # it gives me "object out of session" error if i include this stamtent in finally calause

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue is None:
    return redirect(url_for('index'))
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.get(venue_id)
  if venue is None:
    return redirect(url_for('index'))

  validation_flag = False
  error_flag = False
  form = VenueForm(request.form)
  try:
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.website_link = form.website_link.data

    if form.seeking_talent.data == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False

    venue.seeking_description = form.seeking_description.data

    if form.validate():
      db.session.commit()
    else:
      validation_flag = True

  except:
    db.session.rollback()
    print('#ERROR POST VENUE#', sys.exc_info())
    error_flag = True

  if error_flag:
    flash('SORRY! An error occurred. Venue ' + form.name.data + ' could not be listed.')
  elif validation_flag:
    flash(f'ERROR in form fields, check: \n {form.errors} \n Venue {form.name.data} could not be listed.')
  else:
    flash('Venue ' + form.name.data + ' was successfully listed!')
  db.session.close() # it gives me "object out of session" error if i include this stamtent in finally calause

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  ''' OLD Solution
  try:
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    facebook_link = request.get_json()['facebook_link']
    image_link = request.get_json()['image_link']
    website_link = request.get_json()['website_link']
    seeking_venue = request.get_json()['seeking_venue']
    if seeking_venue == 'y':
      seeking_venue = True
    seeking_description = request.get_json()['seeking_description']
    artist = Artist(name = name, city = city, phone = phone, state = state, genres = ", ".join(genres),
    facebook_link = facebook_link, image_link = image_link, website_link = website_link, seeking_venue = seeking_venue,
    seeking_description = seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully listed!')

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + name + ' could not be listed.')

  finally:
    db.session.close()
    return render_template(url_for('index'))
  '''
  validation_flag = False
  error_flag = False
  form = ArtistForm(request.form)
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    genres = form.genres.data
    facebook_link = form.facebook_link.data
    image_link = form.image_link.data
    website_link = form.website_link.data
    seeking_description = form.seeking_description.data

    if form.seeking_venue.data == 'y':
      seeking_venue = True
    else:
      seeking_venue = False
    
    if form.validate():
      artist = Artist(name = name, city = city, state = state, phone = phone, genres = ", ".join(genres), # Convert from list to string.
                      facebook_link = facebook_link, image_link = image_link, website_link = website_link, seeking_venue = seeking_venue,
                      seeking_description = seeking_description)
      db.session.add(artist)
      db.session.commit()
    else:
      validation_flag = True

  except:
    db.session.rollback()
    print('#ERROR POST ARTIST#', sys.exc_info())
    error_flag = True

  finally:
    db.session.close()

  if error_flag:
    flash('SORRY! An error occurred. Venue ' + name + ' could not be listed.')
  elif validation_flag:
    flash(f'ERROR in form fields, check: \n {form.errors} \n Artist {name} could not be listed.')
  else:
    flash('Venue ' + name + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  data = []

  shows = Show.query.all()
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    row = {}
    row['venue_id'] = show.venue_id
    row['venue_name'] = venue.name
    row['artist_id'] = show.artist_id
    row['artist_name'] = artist.name
    row['artist_image_link'] = artist.image_link
    row['start_time'] = str(show.start_time)
    data.append(row)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  error_flag = False
  try:
    show = Show(artist_id = request.form['artist_id'],
                venue_id = request.form['venue_id'],
                start_time = request.form['start_time'] )
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    print(f'#ERROR# POST SHOW', sys.exc_info())
    error_flag = True
  finally:
    db.session.close()

  if error_flag:
    flash('Error occured, the new show could not be added.')
  else:
    flash('Show was successfully listed!')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(DEBUG=True)


# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''