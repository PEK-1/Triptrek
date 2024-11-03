from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Trip  # Import the Trip model
from . import db

views = Blueprint('views', __name__)

@views.route('/logo')
def index():
    return render_template("index.html")

@views.route('/home', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/')
def form():
    return render_template("form.html")

@views.route('/submit', methods=['POST'])
def submit():
    # Existing form submission code
    place = request.form['place']
    visit_date = request.form['visit_date']
    days = request.form['days']
    requirements = request.form['requirements']
    # Generate itinerary (existing functionality)

@views.route('/addTrip', methods=['GET', 'POST'])
@login_required
def add_trip():
    if request.method == 'POST':
        # Collect trip details from the form
        place = request.form['place']
        days = request.form['days']
        month = request.form['month']
        budget = request.form['budget']
        accommodation = request.form['accommodation']
        transport = request.form['transport']
        local_travel = request.form['local_travel']
        places_visited = request.form['places_visited']
        food_recommendations = request.form['food_recommendations']
        trip_description = request.form['trip_description']
        
        # Create a new Trip instance
        new_trip = Trip(
            user_id=current_user.id,
            place=place,
            days=days,
            month=month,
            budget=budget,
            accommodation=accommodation,
            transport=transport,
            local_travel=local_travel,
            places_visited=places_visited,
            food_recommendations=food_recommendations,
            trip_description=trip_description
        )
        
        # Add the new trip to the database
        db.session.add(new_trip)
        db.session.commit()
        
        flash('Trip added successfully!', category='success')
        return redirect(url_for('views.mytips'))

    return render_template("addNewTrip.html")

@views.route('/mytips')
@login_required
def mytips():
    return render_template("mytips.html", user=current_user)

@views.route('/get_user_trips', methods=['GET'])
@login_required
def get_user_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    trips_data = [{
        "place": trip.place,
        "date": trip.month,
        "days": trip.days,
        "budget": trip.budget,
        "accommodation": trip.accommodation,
        "transport": trip.transport,
        "local_travel": trip.local_travel,
        "places_visited": trip.places_visited,
        "food_recommendations": trip.food_recommendations,
        "trip_description": trip.trip_description
    } for trip in trips]
    return jsonify(trips_data)

