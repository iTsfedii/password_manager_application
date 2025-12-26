from flask import render_template, redirect, url_for, flash
from forms import RegistrationForm
from flask import Flask
from models import db,User
from dotenv import load_dotenv
from forms import LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
import os
load_dotenv()
app= Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')

#print("Loaded SECRET_KEY:" , app.config['SECRET_KEY'])



# This line sets up SQLite as your database, in a file called info.db in your project folder

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




@app.route('/')
def home():
 return"welcom to the password manager"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('login'))  # or wherever you want to go
    return render_template('register.html', form=form)


from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Make sure you have a dashboard route
        else:
            flash('Login failed. Try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)





if __name__ =="__main__":
	with app.app_context():
	  db.create_all()
	app.run(debug=True)






