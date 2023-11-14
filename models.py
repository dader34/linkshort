from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

app_url = "http://127.0.0.1:5101" #Replace with app url and port, you can set this at the bottom of main.py

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Link(db.Model, SerializerMixin):
  __tablename__ = 'links'

  id = db.Column(db.Integer, primary_key=True)
  long_url = db.Column(db.String(500))
  views = db.Column(db.Integer, default=0)
  created_at = db.Column(db.DateTime, default=db.func.now())
  short_url = db.Column(db.String(500),unique=True)
  
  @classmethod
  def get_top_links(cls):
    return Link.query.order_by(Link.views.desc()).limit(5).all()

  @classmethod
  def all(cls):
    return Link.query.all()

  @classmethod
  def find_short_by_long(cls,long_url):
    return Link.query.filter_by(long_url=long_url).first()

  @classmethod
  def redirect_find_url(cls,code):
    return Link.query.filter_by(short_url=f'{app_url}/r/{code}').first()

  @classmethod
  def update_view_count(cls,short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
      link.views += 1
      db.session.commit()
    return Link

  def __repr__(self):
    return f"Link object with properties:\nlong_url: {self.long_url}\nshort_url: {self.short_url}\nviews: {self.views}\ncreated_at: {self.created_at}"
