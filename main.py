from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import string
import secrets

app = Flask(__name__)
app_url = "http://127.0.0.1:5101"
CORS(app,
     resources={
         "/shorten": {
             "methods": ["GET", "POST"]
         }
     })

try:
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS url_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL
        );
    ''')
except sqlite3.Error as e:
    print(e)
  
def get_db():
  db = sqlite3.connect('urls.db')
  db.row_factory = sqlite3.Row
  return db


def generate_random_url(original_url, length=10):
  characters = string.ascii_letters + string.digits
  random_url = ''.join(
      secrets.choice(characters) for _ in range(length if length > 4 else 5))
  db = get_db()
  cursor = db.cursor()
  all_entries = cursor.execute("SELECT * FROM url_mapping WHERE long_url = ?",(original_url,)).fetchone()
  if(all_entries):
    print('Re-Using link')
    return all_entries[1]
  else:
    print('Creating new link')
    return f"{app_url}/r/" + random_url


@app.route('/')
def hello_world():
  return render_template("main.html",app_url=app_url)

@app.route('/links')
def links():
  db = get_db()
  cursor = db.cursor()
  books = cursor.execute("SELECT * FROM url_mapping").fetchall()
  cursor.close()
  db.close()
  return jsonify([dict(row) for row in books])


# database[long_url]: short_url
@app.route('/shorten', methods=['POST'])
def shorten_url():
  if (request.method == "POST"):
    ip_address = request.headers.get('X-Real-IP', "")
    print(f"Request comming from: {ip_address}")
    #check if request came from server or not
    if (ip_address == ""):
      long_url = request.json.get('url')
      # parsed = urllib.parse.quote(long_url, safe='')
      short_url = generate_random_url(long_url, length=5)
      db = get_db()
      cursor = db.cursor()

      cursor.execute(
          '''
      INSERT OR IGNORE INTO url_mapping (long_url, short_url) VALUES (?, ?)
      ''', (long_url, short_url))

      cursor.connection.commit()

      print('Sending url to frontend')
      print(f'Link: {short_url}')
      print(f'Original link was: {long_url}')
      return jsonify({'shortenedUrl': short_url})
    else:
      print('Request comming from non server IP')
      return jsonify(
          {'error': 'You are not allowed to shorten URLs from this IP'})


@app.route('/r/<code>')
def route(code):
    db = get_db()
    cursor = db.cursor()
    all_entries = cursor.execute("SELECT * FROM url_mapping WHERE short_url = ?",(f'{app_url}/r/{code}',)).fetchone()
    if(all_entries):
      print('Redirecting to original link')
      return render_template('redirect.html',entry=all_entries[2])
    else:
      print('Invalid url visited')
      return render_template('error.html',context=code)



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5101)
