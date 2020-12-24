#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

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
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config.DevConfig')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# connect to a local postgresql database || DONE || connection in config.py

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship("Show", back_populates="Venue")

    #implement any missing fields, as a database migration using Flask-Migrate || DONE || Added genres

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship("Show", back_populates="Venue")

    #implement any missing fields, as a database migration using Flask-Migrate || DONE || 

#Implement Show and Artist models, and complete all model relationships and properties, as a database migration. || DONE || 

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time = db.Column(db.DateTime(timezone=True))
  venue = db.relationship("Venue", back_populates="show", lazy='dynamic')
  Artist = db.relationship("Artist", back_populates="show", lazy='dynamic')
  


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
  # replace with real venues data. || DONE || 
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  #implement search on artists with partial string search. Ensure it is case-insensitive. || DONE ||
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  db.session.query(Venue).filter_by(Venue.name.ilike(Venue.name),Venue.name.lower(Venue.name)).first()


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  db.session.close()

@app.route('/artist/search', methods=['POST'])
def search_artists():
  db.session.query(Artist).filter_by(Artist.name.ilike(Artist.name),Artist.name.lower(Artist.name)).first()
  db.session.close()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  





@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    try:
    venue_id = request.get['venue.id']
    
    venue = Venue.query.get(venue.id)
    Venue.id = venue.id
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
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

  #insert form data as a new Venue record in the db, instead || DONE || 

  error = False
  body{}
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    image_link = request.form['image_link']
    genres = request.form['genres']
    facebook_link = request.form['facebook_link']
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,genres=genres,facebook_link=facebook_link)
    db.session.add(venue)
    db.session.commit()

  #modify data to be the data object returned from db insertion || DONE || 

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # on unsuccessful db insert, flash an error instead. || DONE || 
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using || DONE || 
    error = False
  body{}
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  #modify data to be the data object returned from db insertion || DONE || 
  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
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
  return render_template('pages/artists.html', artists=Artist.query.order_by('id').all()))

@app.route('/artists/search', methods=['POST'])
def search_artists():
  #implement search on artists with partial string search. Ensure it is case-insensitive. || DONE || 
  db.session.query(Artist).filter_by(Artist.name.ilike(Artist.name),Artist.name.lower(Artist.name)).first()
  db.session.close()
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  #replace with real venue data from the venues table, using venue_id || DONE || 
   artist = Artist.query.filter_by(artist_id=id).first()

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=artist_id)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm() 
  artist = Artist.query.filter_by(id=artist_id).first()
  db.session.commit()
  db.session.close()
  #populate form with fields from artist with ID <artist_id> || DONE || 
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  db.session.commit()
  db.session.close()
  #populate form with values from venue with ID <venue_id> || DONE ||
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  #take values from the form submitted, and update existing || DONE || 

  # venue record with ID <venue_id> using the new attributes
  venuenew = Venue.query.filter_by(id=venue_id).first().update(Venue.venue)
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  #insert form data as a new Venue record in the db, instead || DONE || 
  #modify data to be the data object returned from db insertion || DONE || 

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  #on unsuccessful db insert, flash an error instead. || DONE || 
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data. || DONE || 
  # num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/shows.html', Shows=Show.query.order_by('id').all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  #insert form data as a new Show record in the db, instead || DONE || 

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  #on unsuccessful db insert, flash an error instead. || DONE || 
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
