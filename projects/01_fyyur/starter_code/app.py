#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config.DevConfig')
db.init_app(app)

migrate = Migrate(app, db)

# connect to a local postgresql database || DONE || connection in config.py

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
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
  venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  data=[]
  for venue in venues:
    data.append({
      'city': venue.city,
      'state':venue.state,
      'venues': Venue.query.filter(Venue.city==venue.city).filter(Venue.state==venue.state).all()
    })
  # replace with real venues data. || DONE || 
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #implement search on artists with partial string search. Ensure it is case-insensitive. || DONE ||
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = db.session.query(Venue).filter_by(Venue.name.ilike('%' + request.form.get('search_term', '')))
  reponse = {
    'count': len(search),
    'data': search
  }
  

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  

@app.route('/artist/search', methods=['POST'])
def search_artist():
  search = db.session.query(Artist).filter_by(Artist.name.ilike('%' + request.form.get('search_term', '')))
  reponse = {
    'count': len(search),
    'data': search
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  





@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  upcoming_shows = []
  past_shows = []
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    if show.start_time > datetime.now():
      upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time
        
      })
    else:
      past_shows.append({
        "artist_id": artist.id ,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time
        
      })
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "website": venue.website,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  # shows the venue page with the given venue_id || DONE || 
  #replace with real venue data from the venues table, using venue_id || DONE || 
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)

  #insert form data as a new Venue record in the db, instead || DONE || 

  error = False
  body ={}
  if form.validate():


    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      image_link = request.form['image_link']
      genres = request.form['genres']
      facebook_link = request.form['facebook_link']
      website = request.form['website']
      seeking_talent = True if request.form['seeking_talent'] in ('y') else False
      seeking_description = request.form['seeking_description']
      venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,genres=genres,facebook_link=facebook_link,website=website,seeking_talent=seeking_talent,seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    #modify data to be the data object returned from db insertion || DONE || 
    # on successful db insert, flash success || DONE || 
    # on unsuccessful db insert, flash an error instead. || DONE || 
    except:
      print(sys.exc_info())
      error = True
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    flash(form.errors)
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using || DONE || 
  error = False
  body={}
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  #modify data to be the data object returned from db insertion || DONE || 
  # on successful db insert, flash success
  
  # on unsuccessful db insert, flash an error instead. || DONE || 
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.values['venue_id'] + ' could not be Deleted.')
  finally:
    db.session.close()
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  #replace with real data returned from querying the database || DONE || 
  return render_template('pages/artists.html', artists=Artist.query.order_by('id').all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  #implement search on artists with partial string search. Ensure it is case-insensitive. || DONE || 
  search = db.session.query(Artist).filter_by(Artist.name.ilike('%' + request.form.get('search_term', '')))
  reponse = {
    'count': len(search),
    'data': search
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).all()
  upcoming_shows = []
  past_shows = []
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    if show.start_time > datetime.now():
      upcoming_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time
        
      })
    else:
      past_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time
        
      })

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "website": artist.website,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)
  # shows the venue page with the given venue_id
  #replace with real venue data from the venues table, using venue_id || DONE || 
   
   

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm() 
  artist = Artist.query.filter_by(id=artist_id).first()
  #populate form with fields from artist with ID <artist_id> || DONE || 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist = Artist.query.filter_by(id=artist_id).first()
  #take values from the form submitted, and update existing || DONE || 
  # artist record with ID <artist_id> using the new attributes
  error = False
  body={}
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form['genres']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website']
    artist.seeking_venue = True if request.form['seeking_venue'] in ('y') else False
    artist.seeking_description = request.form['seeking_description']
    artist.facebook_link = request.form['facebook_link']
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully Updated!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + request.values['artist_id'] + ' could not be Edited.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))


   

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  
  #populate form with values from venue with ID <venue_id> || DONE ||
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  #take values from the form submitted, and update existing || DONE || 
  # artist record with ID <artist_id> using the new attributes
  error = False
  body={}
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form['genres']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website']
    venue.seeking_talent = True if request.form['seeking_talent'] in ('y') else False
    venue.seeking_description = request.form['seeking_description']
    
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully Updated!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.values['venue_id'] + ' could not be Edited.')
  finally:
    db.session.close()
  #take values from the form submitted, and update existing || DONE || 
  # here implemnt same as artist
  # venue record with ID <venue_id> using the new attributes

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = VenueForm(request.form) 
  error = False
  body ={}
  if form.validate():

    try:
      
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      phone = request.form['phone']
      genres = request.form['genres']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website']
      seeking_venue = True if request.form['seeking_venue'] in ('y') else False
      seeking_description = request.form['seeking_description']
      artist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link,website=website,seeking_venue=seeking_venue,seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')


    #modify data to be the data object returned from db insertion || DONE || 

    # on successful db insert, flash success || DONE || 
    
    # on unsuccessful db insert, flash an error instead. || DONE || 
    except:
      error = True
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    flash(form.errors)
  # Same as venue
  # called upon submitting the new artist listing form
  #insert form data as a new Venue record in the db, instead || DONE || 
  #modify data to be the data object returned from db insertion || DONE || 

  # on successful db insert, flash success

  #on unsuccessful db insert, flash an error instead. || DONE || 
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  shows = Show.query.order_by(Show.artist_id).all()
  data = [] 
  for show in shows:
    venue = Venue.query.get(show.venue_id)
    artist = Artist.query.get(show.artist_id)
    data.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time
      })

  # add for loop same as venue
  # use mocup data to build the jeson
  # displays list of shows at /shows
  # replace with real venues data. || DONE || 
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  body = {}
  try:
    aritist = request.form['artist_id']
    venue = request.form['venue_id']
    start_time = request.form['start_time']
    show = Show(artist_id=aritist,venue_id=venue,start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    print(sys.exc_info())
    error = True
    db.session.rollback()
    flash('An error occurred. Show  could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

  # called to create new shows in the db, upon submitting new show listing form
  #insert form data as a new Show record in the db, instead || DONE || 

  # on successful db insert, flash success
  
  #on unsuccessful db insert, flash an error instead. || DONE || 
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

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
