from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required, UserMixin
import json

from .forms import *
from .models import *
import hashlib

from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError

@app.route('/register', methods=['GET', 'POST'])
def register():
  registerForm = RegisterForm()

  if registerForm.validate_on_submit():
    
    if registerForm.password.data != registerForm.confirm_password.data:
      flash('Passwords do not match', 'danger')
    else: # create a new user and add to database
      user = Users(username=registerForm.username.data, email=registerForm.email.data, password=hashlib.sha256(registerForm.password.data.encode()).hexdigest())
      try:
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully', 'success')
        return redirect(url_for('login'))
      except IntegrityError:
        db.session.rollback()
        flash('Username or email already exists', 'danger')
  return render_template('register.html', form=registerForm, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
  loginForm = LoginForm()

  if loginForm.validate_on_submit():
    # check if user exists
    user = Users.query.filter_by(email=loginForm.email.data).first()
    password_hash = hashlib.sha256(loginForm.password.data.encode()).hexdigest()
    if user != None and user.password == password_hash:
      login_user(user)
      flash('Logged in successfully', 'success')
      return redirect(url_for('index'))
    else:
      flash('Invalid email or password', 'danger')
  return render_template('login.html', form=loginForm, title='Login')

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logged out successfully', 'success')
  return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
  gamesList = Games.query.all()
  return render_template('index.html', games=gamesList, title='All Games', header='Games')

@app.route('/game/<int:id>', methods=['GET', 'POST'])
@login_required
def gameReview(id):
  form=ReviewForm()

  gameDetails = Games.query.filter_by(id=id).first()
  gameReviews = gameDetails.reviews.all()

  if form.validate_on_submit():
    try:
      review=Reviews(content=form.content.data, user_id=current_user.id, game_id=id)
      db.session.add(review)
      db.session.commit()
      flash('Review added successfully', 'success')
      return redirect(url_for('gameReview', id=id))
    except IntegrityError:
      db.session.rollback()
      flash('You have reviewed this game', 'danger')
  return render_template('gameDetails.html', game=gameDetails, reviews=gameReviews, form=form, title=gameDetails.title)

@app.route('/delete_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def deleteReview(review_id):

  # check if review belongs to the current user
  review=Reviews.query.filter_by(id=review_id).first()
  game_id = review.game_id

  if review.user_id != current_user.id:
    flash('You are not authorized to delete this review', 'danger')
    return redirect(url_for('gameReview', id=game_id))
  
  else:
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted successfully', 'success')
    return redirect(url_for('gameReview', id=game_id))
  
@app.route('/liked')
@login_required
def liked():

  likedGames = Users.query.filter_by(id=current_user.id).first().collection
  return render_template('index.html', games=likedGames, name=current_user.username, title='Liked Games', header='Liked Games')

@app.route('/manage-likes', methods=['POST'])
@login_required
def likes():
  data = json.loads(request.data)
  game_id = int(data.get('game_id'))
  game = Games.query.filter_by(id=game_id).first()

  if data.get('action') == 'add':
    if game not in current_user.collection:
      current_user.collection.append(game)
      db.session.commit()
      flash ('Game added to collection', 'success')
    
  else:
    try:
      current_user.collection.remove(game)
      db.session.commit()
      flash ('Game removed from collection', 'success')
    except (ValueError):
      pass

  return json.dumps({'new_like_count': len(game.playedUsers)})

# @app.route('/sort/genre')
# def sort_genre():
#   games = Games.query.order_by(Games.genre).all()
#   return render_template('index.html', games=[game[0] for game in games], title='All Games', header='Sorted by Genre')