#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from flask_migrate import Migrate
from models import Link, db, app_url
import shortuuid


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app,
     resources={
         "/shorten": {
             "origins": [app_url],
             "methods": ["GET", "POST"]
         }
     })

db.init_app(app)

migrate = Migrate(app, db)

def generate_unique_short_url():
  while True:
    # Generate a short URL using shortuuid or any other method you prefer
    new_short_url = shortuuid.ShortUUID().random(length=6)

    # Check if the generated short URL already exists in the database
    existing_link = Link.query.filter_by(
        short_url=f"{app_url}/r/{new_short_url}").first()
    if not existing_link:
      return f"{app_url}/r/{new_short_url}"

@app.route('/')
def hello_world():

  return render_template("main.html",app_url=app_url)

@app.route('/top-links')
def top_links():

  top_links = Link.get_top_links()
  return render_template("top_links.html",
  top_links=[row.to_dict() for row in top_links])

@app.route('/links')
def links():

  links = Link.all()
  return jsonify([row.to_dict() for row in links])

@app.route('/shorten', methods=['POST'])
def shorten_url():

  if request.method == "POST":

    ip_address = request.headers.get('X-Real-IP', "")
    print(f"Request coming from: {'self' if not ip_address else ip_address}")

    if ip_address == "":

      long_url = request.json.get('url')

      if not long_url.startswith(app_url):
        short_url = generate_unique_short_url()
        # Check if the short URL already exists
        existing_entry = Link.find_short_by_long(long_url)
        print(long_url)
        print(existing_entry)
        if existing_entry:
  
          # If the short URL exists, don't overwrite the views, just return it
          print('Reusing link')
          return jsonify({
              'shortenedUrl': existing_entry.to_dict()['short_url'],
              'views': existing_entry.to_dict()['views']
          })
  
        else:
  
          # If the short URL doesn't exist, insert a new URL mapping with initial views set to 1
          new_link = Link(long_url=long_url, short_url=short_url)
          db.session.add(new_link)
          db.session.commit()
          print('Creating new link')
          return jsonify({'shortenedUrl': short_url, 'views': 1})
      else:
        return jsonify({'error': 'Invalid URL'})

    else:

      print('Request coming from a non-server IP')
      return jsonify(
          {'error': 'You are not allowed to shorten URLs from this IP'})

@app.route('/r/<code>')
def route(code):

  routing_link = Link.redirect_find_url(code)
  if (routing_link):

    print('Redirecting to original link')
    Link.update_view_count(routing_link.to_dict()['short_url'])
    return render_template('redirect.html', entry=routing_link.to_dict()['long_url'])

  else:

    print('Invalid url visited')
    return render_template('error.html', context=code)

# if __name__ == '__main__':
#   app.run(host='127.0.0.1', port=5101)

os.system("gunicorn -w 4 --bind 127.0.0.1:5101 main:app")
