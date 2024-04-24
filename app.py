import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime as dt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sif.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login' # default login route
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():  # put application's code here
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    default_route_function = 'userdirectory'
    default_member_route_function = 'myprofile'

    if request.method == 'GET':
        # Determine where to redirect user if they are already logged in
        if current_user and current_user.is_authenticated:
            if current_user.role == 'BOARD':
                return redirect(url_for(default_route_function))
            elif current_user.role in ['MEMBER', 'ALUMNI']:
                return redirect(url_for(default_member_route_function, member_id=0))
        else:
            redirect_route = request.args.get('next')
            return render_template('login.html', redirect_route=redirect_route)

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect_route = request.form.get('redirect_route')

        user = User.query.filter_by(username=username).first()

        # Validate user credentials and redirect them to initial destination
        if user and check_password_hash(user.password, password):
            login_user(user)

            if current_user.role == 'BOARD':
                return redirect(redirect_route if redirect_route else url_for(default_route_function))
            elif current_user.role in ['MEMBER', 'ALUMNI']:
                return redirect(
                    redirect_route if redirect_route else url_for(default_member_route_function, member_id=0))
        else:
            flash(f'Your login information was not correct. Please try again.', 'error')

        return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/home')
def homepage():  # put application's code here
    return render_template('home.html')


# alumni has access

@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile():
    if request.method == 'GET':
        # Get the current user's ID
        user_id = current_user.user_id

        # Query the Member table to find the profile information of the current user
        member = Member.query.filter_by(user_id=user_id).first()

        if member:
            # If the member is found, render the edit profile form
            return render_template('editprofile.html', member=member, action='update')
        else:
            # If the member is not found, display an error message
            flash("Error: Profile not found", 'error')
            return redirect(url_for('myprofile'))

    elif request.method == 'POST':
        # Get the current user's ID
        user_id = current_user.user_id

        # Query the Member table to find the profile information of the current user
        member = Member.query.filter_by(user_id=user_id).first()

        if member:
            try:
                # Update the member's profile information based on the form data received
                member.name = request.form['name']
                member.grad_date = request.form['grad_date']
                member.join_date = request.form['join_date']
                member.mem_status = request.form['mem_status']
                member.mem_category = request.form['mem_category']
                member.mem_phone = request.form['mem_phone']
                member.email = request.form['email']
                member.mem_linkedin = request.form['mem_linkedin']
                # Update other fields as needed

                # Commit the changes to the database
                db.session.commit()

                # Flash a success message
                flash("Profile successfully updated!", 'success')

                # Redirect the user to their profile page
                return redirect(url_for('myprofile'))
            except Exception as e:
                # If an exception occurs during the update process, handle it here
                flash("Error: Failed to update profile", 'error')
                # Redirect the user back to the edit profile page with the form populated
                return redirect(url_for('editprofile'))

        else:
            # If the member is not found, display an error message
            flash("Error: Profile not found", 'error')

        # Redirect the user to their profile page
        return redirect(url_for('myprofile'))
@app.route('/userdirectory')
def userdirectory():  # put application's code here
    return render_template('userdirectory.html')


@app.route('/myprofile')
@login_required
def myprofile():
    # Get the current user's ID
    user_id = current_user.user_id

    # Query the Member table to find the profile information of the current user
    member = Member.query.filter_by(user_id=user_id).first()

    if member:
        # If the member is found, display their profile information
        return render_template('editprofile.html', member=member, action='view')
    else:
        # If the member is not found (which should not happen in a properly configured system), display an error message
        flash("Error: Profile not found", 'error')
        return redirect(url_for('home'))  # Redirect to the home page or another appropriate page

@app.route('/addprofile', methods= ['GET', 'POST'])
@login_required
def addprofile():
    if request.method == "GET":
        return render_template('profile_entry.html')



