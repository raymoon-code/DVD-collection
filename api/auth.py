from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import traceback

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # T: Add code to verify user credentials
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            new_user = User.query.filter_by(username=username).first()
            if password !=confirm_password:
                flash('password and confirm password does not match.', category='error')
            elif new_user:
                flash('Username already exists', category='error')
            else:
                new_user = User(username= username, password=generate_password_hash(password,method='sha256') )
                db.session.add(new_user)
#                 db.session.flush()
                db.session.commit()     
                login_user(new_user, remember=True)   
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            # user = request.form.get('username')
        return render_template("signup.html",user=current_user)
    except Exception as e:
        error_message = traceback.format_exc()
        return render_template('error.html', error=error_message)
