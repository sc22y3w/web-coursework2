from app import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

class Users(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(64), unique=True)
  password = db.Column(db.String(64))
  collection = db.relationship('Games', secondary='collection')

  def playedGames(self, games):
    return games in self.collection

class Games(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  genre = db.Column(db.String(100), nullable=False)
  year = db.Column(db.Integer, nullable=False)
  platform = db.Column(db.String(100), nullable=False)
  image = db.Column(db.String(100))
  price = db.Column(db.Float, nullable=False)
  description = db.Column(db.String(2000))
  playedUsers = db.relationship('Users', secondary='collection', overlaps='collection')

class Reviews(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.Text)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  game_id = db.Column(db.Integer, db.ForeignKey('games.id'))

  user = db.relationship('Users', backref=db.backref('reviews', lazy='dynamic'))
  game = db.relationship('Games', backref=db.backref('reviews', lazy='dynamic'))

collection = db.Table('collection', db.Model.metadata, 
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')), 
                      db.Column('game_id', db.Integer, db.ForeignKey('games.id')))
