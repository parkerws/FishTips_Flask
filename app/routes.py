from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.models import User, Station
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from werkzeug.urls import url_parse
from datetime import datetime
import requests



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User Registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/tides')
@login_required
def tides():
    return render_template('tides.html', title='Tides')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.location = current_user.location
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/map')
def get_stations():
    stations = Station.query.all()
    station_list = [i.serialize() for i in stations]
    return jsonify(station_list)

@app.route('/map/convert_location/<location>')
def convert_location(location):
    if request.method == 'GET':
        print(location)
        google_endpoint = "https://maps.googleapis.com/maps/api/geocode/json?address="
        response = requests.get(google_endpoint+location+'&key='+app.config.get('GOOGLE_MAPS_API_KEY')).text
        print(response)
        return jsonify(response)

@app.route('/map/zip_search')
def zip_search():
    if request.method == 'GET':
        zip_code = request.args.get('location')
        print(zip_code)
        openmap_endpoint = "https://api.openweathermap.org/data/2.5/weather?zip="
        query = openmap_endpoint + zip_code + '&appid=' + app.config.get('OPENMAP_API_KEY') + "&units=imperial"
        print(query)
        response = requests.get(query).text
        print(response)
        return jsonify(response)

@app.route('/map/lat_lng_search')
def lat_lng_search():
    if request.method == 'GET':
        lat = request.args.get('lat')
        lon = request.args.get('lng')
        print(lat + ' ' + lon)
        openmap_endpoint = 'api.openweathermap.org/data/2.5/weather?'
        #response = requests.get(f'{openmap_endpoint}lat={lat}&lon={lon}&appid={app.config.get('OPENMAP_API_KEY')}')
        