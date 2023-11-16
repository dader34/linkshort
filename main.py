#!/usr/bin/env python3
import os
from flask_migrate import Migrate
from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
from flask_restful import Api, Resource
from models import Link, db, app_url
import shortuuid


app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app,
  resources={
    "/shorten" : {
    "origins": [app_url],
    "methods": ["GET", "POST"]
  }
})

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

def generate_unique_short_url():
  while True:
    #Generate random combo with optional length
    new_short_url = shortuuid.ShortUUID().random(length=6)

    # Check if the generated short URL already exists in the database
    existing_link = Link.query.filter_by(
        short_url=f"{app_url}/r/{new_short_url}").first()
    if not existing_link:
      #If link doesnt exist, return a new one
      return f"{app_url}/r/{new_short_url}"


class Landing(Resource):
  def get(self):
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template("main.html",app_url=app_url),200,headers)
  
api.add_resource(Landing, '/')

class TopLinks(Resource):
  def get(self):
    headers = {'Content-Type': 'text/html'}
    top_links = Link.get_top_links()
    return make_response(render_template("top_links.html",
    top_links=[row.to_dict() for row in top_links]),200,headers)
  
api.add_resource(TopLinks, '/top-links')

class Links(Resource):
  def get(self):
    links = Link.query.all()
    return [row.to_dict() for row in links]
  
api.add_resource(Links, '/links')

class Shorten(Resource):
  def post(self):
    ip_address = request.headers.get('X-Real-IP', "")
    print(f"Request coming from: {'self' if not ip_address else ip_address}")

    if ip_address == "":

      long_url = request.json.get('url')

      if not long_url.startswith(app_url):
        short_url = generate_unique_short_url()
        # Check if the short URL already exists
        
        if existing_entry := Link.find_short_by_long(long_url):
  
          # If the short URL exists, don't overwrite the views, just return it
          print('Reusing link')
          return {
              'shortenedUrl': existing_entry.to_dict()['short_url'],
              'views': existing_entry.to_dict()['views']
          }
  
        else:
  
          # If the short URL doesn't exist, insert a new URL mapping with initial views set to 0
          try:
            new_link = Link(long_url=long_url, short_url=short_url)
            db.session.add(new_link)
            db.session.commit()
            print('Creating new link')
            return jsonify({'shortenedUrl': short_url, 'views': 0})
          except Exception as e:
            db.session.rollback()
            return {"error": e.args}
      else:
        return {'error': 'Invalid URL'}

    else:

      print('Request coming from a non-server IP')
      return {'error': 'You are not allowed to shorten URLs from this IP'}
    
api.add_resource(Shorten, '/shorten')

class Route(Resource):
  def get(self,code):
    headers = {'Content-Type': 'text/html'}
    if routing_link := Link.redirect_find_url(code):

      print('Redirecting to original link')
      try:
        Link.update_view_count(routing_link.to_dict()['short_url'])
      except Exception as e:
        return {"error":e.args}
      return make_response(render_template('redirect.html', entry=routing_link.to_dict()['long_url']),200,headers)

    else:

      print('Invalid url visited')
      return make_response(render_template('error.html', context=code),400,headers)

api.add_resource(Route, '/r/<string:code>')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5102)

# os.system("gunicorn -w 4 --bind 127.0.0.1:5101 main:app")
