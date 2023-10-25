from flask import Flask, render_template, redirect, url_for
from wtform_fields import RegistrationForm, LoginForm
from dotenv import load_dotenv
import os
from models import db, User

# Load environment variables from .env
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize SQLAlchemy with your Flask app
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()

    # Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Add user to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('index.html', form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        return "Logged in, finally!"

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)