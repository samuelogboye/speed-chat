from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from wtform_fields import RegistrationForm, LoginForm
from dotenv import load_dotenv
import os
from models import db, User
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room

# Load environment variables from .env
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize SQLAlchemy with your Flask app
db.init_app(app)

# initialize socketio
socketio = SocketIO(app)
GROUPS = ["lounge", "news", "games", "coding", "random", "bible"]

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        password_hash = pbkdf2_sha256.hash(password)

        # Add user to database
        user = User(username=username, password=password_hash)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))


    return render_template('index.html', form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)

        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # if not current_user.is_authenticated:
    #     flash('Please login.', 'danger')
    #     return redirect(url_for('login'))
    return render_template('chat.html', username=current_user.username, groups=GROUPS)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect (url_for('login'))

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, group=data['group'], broadcast=True)


@socketio.on('join')
def join(data):
    join_room(data['group'])
    send({'msg': data['username'] + " has joined the " + data['group'] + " group."}, group=data['group'])


@socketio.on('leave')
def leave(data):
    leave_room(data['group'])
    send({'msg': data['username'] + " has left the " + data['group'] + " group."}, group=data['group'])


if __name__ == '__main__':
    socketio.run(app, debug=True)