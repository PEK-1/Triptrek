from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .models import Trip, MapData  # Import the Trip model
from .opni import generate_itinerary, generate_day_plan
from .wether import www, get_lat_lon
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from . import db

views = Blueprint('views', __name__)

@views.route('/logo')
def index():
    return render_template("index.html")

@views.route('/home', methods=['GET'])
@login_required
def home():
    # Fetch map data for the current user
    user_map_data = MapData.query.filter_by(user_id=current_user.id).all()
    map_data = [{"country": data.country, "color": data.color, "note": data.note} for data in user_map_data]
    return render_template("home.html", user=current_user, map_data=map_data)


@views.route('/save_map_data', methods=['POST'])
@login_required
def save_map_data():
    data = request.get_json()
    country = data.get('country')
    color = data.get('color')
    note = data.get('note')

    if not country:
        return jsonify({"error": "Country is required"}), 400

    # Check if the map data already exists for this user and country
    existing_data = MapData.query.filter_by(user_id=current_user.id, country=country).first()

    if existing_data:
        # Update the existing record
        existing_data.color = color
        existing_data.note = note
    else:
        # Create a new record
        new_map_data = MapData(user_id=current_user.id, country=country, color=color, note=note)
        db.session.add(new_map_data)

    db.session.commit()
    return jsonify({"message": "Map data saved successfully"}), 200


@views.route('/reset_map', methods=['POST'])
@login_required
def reset_map():
    # Delete all map data for the current user
    MapData.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"message": "Map data reset successfully"}), 200
@views.route('/')
def form():
    return render_template("form.html")

@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Retrieve the 'query' parameter from the URL
    if query:
        # Query the Trip model for places that match the search term
        destinations = Trip.query.filter(Trip.place.ilike(f'%{query}%')).all()
    else:
        destinations = []  # No query parameter means show no results
    
    # Prepare the results to include the user's name and date added
    destinations_data = [{
        "place": destination.place,
        "days": destination.days,
        "trip_description": destination.trip_description,
        "budget": destination.budget,
        "date_added": destination.date_added.strftime('%Y-%m-%d'),  # Format the date
        "user_name": destination.user.first_name  # Get the first name of the user
    } for destination in destinations]
    
    return render_template('search_results.html', destinations=destinations_data)


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

@views.route('/delete_trip/<int:trip_id>', methods=['DELETE'])
@login_required
def delete_trip(trip_id):
    trip_to_delete = Trip.query.get(trip_id)
    if trip_to_delete and trip_to_delete.user_id == current_user.id:
        db.session.delete(trip_to_delete)
        db.session.commit()
        return {'message': 'Trip deleted successfully'}, 200
    return {'message': 'Trip not found'}, 404


@views.route('/get_user_trips', methods=['GET'])
@login_required
def get_user_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).all()
    trips_data = [{
        "id": trip.id,  # Ensure you're sending the id
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


@views.route('/submit', methods=['POST'])
def submit():
    # Collect data from the form
    place = request.form['place']
    visit_date = request.form['visit_date']
    days = request.form['days']
    requirements = request.form['requirements']

    # Store data in the session
    session['place'] = place
    session['visit_date'] = visit_date
    session['days'] = days
    session['requirements'] = requirements

    # Generate itinerary
    itinerary_text = generate_itinerary(place, visit_date, days, requirements)

    # Format itinerary text for HTML output
    itinerary_html = "<div>"
    days_list = itinerary_text.split("\n\n")  # Assuming double newlines separate different days

    for day in days_list:
        if day.strip():
            # Extract title (e.g., "Day 1")
            lines = day.strip().split("\n")
            day_title = lines[0].strip()  # The first line is the title
            details = "<br>".join(line.strip() for line in lines[1:] if line.strip())  # Join details with <br>

            # Add to itinerary HTML
            itinerary_html += f"<div class='day'><h2>{day_title}</h2><p>{details}</p></div>"

    itinerary_html += "</div>"

    # Render the formatted itinerary in a template
    return render_template("itinerary.html", itinerary=itinerary_html)

@views.route('/makemyday')
def day():
    return render_template('locate.html')

@views.route('/set_location', methods=['POST'])
def set_location():
    data = request.get_json()
    location = data.get('location')  # Get location (latitude, longitude or city name)

    if not location:
        return jsonify({"error": "Location is required"}), 400

    # Store location in session
    session['location'] = location
    return jsonify({"status": "Location set successfully"})

@views.route('/generate_day_plan', methods=['POST'])
def generate_day_plan_route():
    location = session.get('location')

    if not location:
        return jsonify({"error": "Location not set"}), 400

    # If location is in lat, lon format (e.g. "lat, lon"), we need to split it
    if ',' in location:
        lat, lon = map(float, location.split(','))
    else:
        # If location is a city name, use geocoding to get lat/lon
        lat, lon = get_lat_lon(location)

    if lat is None or lon is None:
        return jsonify({"error": "Unable to get latitude and longitude for the location."}), 400

    # Initialize TimezoneFinder to get the timezone based on latitude and longitude
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)

    if timezone_str is None:
        return jsonify({"error": "Unable to find timezone for this location."}), 400

    # Get the current time in the timezone
    timezone = pytz.timezone(timezone_str)
    local_time = datetime.now(timezone)  # Get the current local time

    # Format the local time to "HH:MM"
    formatted_time = local_time.strftime('%H:%M')

    # Generate temperature and day plan
    temp = www(location)
    day_plan = generate_day_plan(location, temp, formatted_time)

    # Return the plan in JSON format to be displayed on the frontend
    return jsonify({"day_plan": day_plan})
