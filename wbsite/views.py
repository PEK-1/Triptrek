from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
from flask_login import login_required, current_user
from .opni import generate_itinerary
#from .models import Note
#from . import db
#import json

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
    itinerary_html = "<h1>Your Travel Itinerary</h1><div>"
    days_list = itinerary_text.split("Day")  # Split by day

    for day in days_list:
        if day.strip():
            day_title = "Day" + day.split(":")[0].strip()
            details = ":".join(day.split(":")[1:]).strip().replace("\n", "<br>")
            itinerary_html += f"<div class='day'><h2>{day_title}</h2><p>{details}</p></div>"

    itinerary_html += "</div>"

    # Render the formatted itinerary in a template
    return render_template("itinerary.html", itinerary=itinerary_html)

@views.route('/locate')
def locate():
    return render_template("locate.html")


