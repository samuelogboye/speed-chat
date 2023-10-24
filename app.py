from flask import Flask, render_template, jsonify, request
from wtform_fields import RegistrationForm
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
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Add user to database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB!"


    return render_template('index.html', form=reg_form)




if __name__ == '__main__':
    app.run(debug=True)