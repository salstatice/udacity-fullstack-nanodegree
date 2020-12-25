#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime
import re
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *

from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

# import setup and db from models
setup_db(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models. Import from models
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  '''
  Display list of venues grouped by city location. The list is
  organized alphbatically by state and with the smallest id first.

  Expected client input: none
  Return: render 'venue.html' with venues data in json format
    {
      "city": name of city,
      "state": name of state,
      "venues": {
        "id": venue id,
        "name": venue name,
      }
    }

  '''
  data=[]
  cities = Venue.query.distinct(Venue.city, Venue.state).order_by('state').all()
  for city in cities:
    venues_list=[]
    venues = Venue.query.filter_by(city=city.city, state=city.state).order_by('id').all()
    for venue in venues:
      venues_list.append({
        "id": venue.id,
        "name": venue.name
      })
    data.append({
      "city": city.city,
      "state": city.state,
      "venues": venues_list
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  '''
  Perform Search. Display list of venues that partially match client input
  search string. The return list is currently unordered. Potentially be 
  ordered by number of upcomming shows.

  Expected client input: search_term
  Return: render 'search_venues.html' with venues data in json format
    {
      "count": num of venues matched for search,
      "data": {
        "id": venue id,
        "name": venue name,
        "num_upcoming_shows": num of upcoming show for venue,
      }
    }

  '''
  search_string = '%' + request.form.get('search_term') + '%'
  venues = Venue.query.filter(Venue.name.ilike(search_string))
  venue_list=[]
  for venue in venues:
    num_upcoming_show = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>=datetime.now()).count()
    venue_list.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_show
    })
  response={
    "count": len(venue_list),
    "data": venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term'))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  '''
  Display details for individual venue.

  Expect client input: venue_id
  Return: render 'show_venues.html' with venue data in json format
  {
    "id": 
    "name": 
    "genres": array of string
    "address": 
    "city": 
    "state":
    "phone": string,
    "website": url,
    "facebook_link": url,
    "seeking_talent": boolean,
    "seeking_description": string,
    "image_link": url,
    "past_shows": [{
      "artist_id": 
      "artist_name": 
      "artist_image_link": url
     }],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
   }
  '''
  venue = Venue.query.filter_by(id=venue_id).first()
  # the query return venue.genres as a list of characters e.g.: ['{','J','A','Z','Z','}']
  genre_list= re.split(r'[\"\{\}\,]',''.join(venue.genres))
  # to remove empty item in genre_list
  venue.genres=[i for i in genre_list if i]
  
  venue_past_shows = db.session.query(Show).join(Venue).filter(Venue.id==venue_id).filter(Show.start_time<=datetime.now()).all()
  venue_upcoming_shows = db.session.query(Show).join(Venue).filter(Venue.id==venue_id).filter(Show.start_time>=datetime.now()).all()
  past_shows_list = []
  upcoming_shows_list = []

  for show in venue_past_shows:
    past_shows_list.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    })
  for show in venue_upcoming_shows:
    upcoming_shows_list.append({
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    })
  venue.past_shows = past_shows_list
  venue.past_shows_count = len(past_shows_list)
  venue.upcoming_shows = upcoming_shows_list
  venue.upcoming_shows_count = len(upcoming_shows_list)
  
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  '''Generate form for adding new venue'''
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  '''
  Create a new venue entry base on client input

  Expected: name, city, state, address, phone and genres are required
  If the request is succeessful, redirect to home.html and display message 
  'Venue [name] was successfully listed!'
  If there's error, redirect to home.html and display message 'An error ocurred.
  Venue [name] canld not be listed.
  '''
  form=VenueForm(request.form)
  if form.validate():  
    try:
      name = request.form['name']
      city = request.form['city'].title()
      state = request.form['state']
      address = request.form['address'].title()
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      image_link = request.form['image_link']
      website = request.form['website']
      facebook_link = request.form['facebook_link']
      if request.form.get('seeking_talent') is None:
        seeking_talent = False
      else:
        seeking_talent = True
      seeking_description = request.form['seeking_description']
      
      new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link, website=website, facebook_link=facebook_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()  
    return render_template('pages/home.html')
  else:
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  '''
  Display list of artist from database ordered alphabatically by name

  Expected user input: none
  Return: render artists.html with artists data in list of dict
  [{
    "id":
    "name":
  }]
  '''

  data=[]
  artists = Artist.query.order_by('name').all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  '''
  Perform Search. Display list of artists that partially match client input
  search string. The return list is currently unordered. Potentially be 
  ordered by number of upcomming shows.

  Expected client input: search_term
  Return: render 'search_artists.html' with artists data in json format
    {
      "count": num of matched result,
      "data": {
        "id": artist id,
        "name": artist name,
        "num_upcoming_shows": num of upcoming show for artist,
      }
    }
  '''

  search_string = '%' + request.form.get('search_term') + '%'
  artists = Artist.query.filter(Artist.name.ilike(search_string))
  artist_list=[]
  for artist in artists:
    num_upcoming_show = Show.query.filter(Show.artist_id==artist.id).filter(Show.start_time>=datetime.now()).count()
    artist_list.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_show
    })
  response={
    "count": len(artist_list),
    "data": artist_list
   }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  '''
  Display details for individual venue.

  Expect client input: venue_id
  Return: render 'show_venues.html' with venue data in json format
  {
    "id": 
    "name": 
    "genres": array of string
    "city": 
    "state":
    "phone": string,
    "website": url,
    "facebook_link": url,
    "seeking_venue": boolean,
    "seeking_description": string,
    "image_link": url,
    "past_shows": [{
      "venue_id": 
      "venue_name": 
      "venue_image_link": url
    }],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
   }
  '''

  artist = Artist.query.filter_by(id=artist_id).first()
  # the query return artist.genres as a list of characters e.g.: ['{','J','A','Z','Z','}']
  genre_list= re.split(r'[\"\{\}\,]',''.join(artist.genres))
  # to remove empty item in genre_list
  artist.genres=[i for i in genre_list if i]
  
  artist_past_shows = db.session.query(Show).join(Artist).filter(Artist.id==artist_id).filter(Show.start_time<=datetime.now()).all()
  artist_upcoming_shows = db.session.query(Show).join(Artist).filter(Artist.id==artist_id).filter(Show.start_time>=datetime.now()).all()
  past_shows_list=[]
  upcoming_shows_list=[]
  
  for show in artist_past_shows:
    past_shows_list.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": str(show.start_time)
    })
  for show in artist_upcoming_shows:
    upcoming_shows_list.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": str(show.start_time)
    })
  artist.past_shows = past_shows_list
  artist.past_shows_count = len(past_shows_list)
  artist.upcoming_shows = upcoming_shows_list
  artist.upcoming_shows_count = len(upcoming_shows_list)

  return render_template('pages/show_artist.html', artist=artist)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  '''Generate form for adding new artist'''
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  '''
  Create a new artist entry base on client input

  Expected: name, city, state, phone and genres are required
  If the request is succeessful, redirect to home.html and display message 
  'Artist [name] was successfully listed!'
  If there's error, redirect to home.html and display message 'An error ocurred.
  Artist [name] canld not be listed.
  '''
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form=ArtistForm(request.form)
  if form.validate():  
    try:
      name = request.form['name']
      city = request.form['city'].title()
      state = request.form['state']
      phone = request.form['phone']
      genres = request.form.getlist('genres')
      image_link = request.form['image_link']
      website = request.form['website']
      facebook_link = request.form['facebook_link']
      if request.form.get('seeking_venue') is None:
        seeking_venue = False
      else:
        seeking_venue = True
      seeking_description = request.form['seeking_description']
      
      new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, website=website, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
    return render_template('pages/home.html')
  else:
    print(form.validate)
    print(form.errors)
    return render_template('forms/new_artist.html', form=form)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  '''Display list of shows at /shows ordered by showtime'''
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data=[]
  shows = Show.query.order_by('start_time').all()
  for show in shows:
    #venue = Venue.query.filter_by(id=show.venue_id).first()
    #artist = Artist.query.filter_by(id=show.artist_id).first()
    data.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

#  Create Show
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  '''Render form for creating new show'''
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  '''
  Add a new show to the database
  
  Expected input: artist_id and venue_id that match the primary key in table
  Artist and Venue repectively. Expect start_time to be in datetime format.
  If successful, render home.html with message 'Show was successfully listed!'
  If error, render home.html with message 'An error occured. Show could not
  be listed.'
  '''

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(new_show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
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
    app.run()

# Or specify port manually:

'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
