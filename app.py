from flask import render_template, redirect, url_for, flash
from forms import RegistrationForm
from flask import Flask
from models import db,User
from dotenv import load_dotenv
from forms import LoginForm
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
        # Here you'd add user creation logic (add user to DB)
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('login'))  # or wherever you want
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Add authentication logic here later
    return render_template('login.html', form=form)







if __name__ =="__main__":
	with app.app_context():
	  db.create_all()
	app.run(debug=True)






