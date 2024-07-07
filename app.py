from flask import Flask, request, jsonify, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug import 

from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        
        session['username'] = user.username
        
        return redirect(f'/users/{user.username}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
    
    return render_template('login.html', form=form)

@app.route('secret')
def secret():
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    return render_template('secret.html')

@app.route('logout')
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>')
def user_detail(username):
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    user = User.query.get(username)
    return render_template('user_detail.html', user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    
    session.pop('username')
    return redirect('/register')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback.add_feedback(title, content, username)
        
        db.session.add(feedback)
        db.session.commit()
        
        return redirect(f'/users/{username}')
    
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    feedback = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        
        return redirect(f'/users/{feedback.username}')
    
    return render_template('update_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash('Please login first!', 'danger')
        return redirect('/login')
    
    feedback = Feedback.query.get(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    
    return redirect(f'/users/{feedback.username}')