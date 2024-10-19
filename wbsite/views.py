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

    # Redirect to opni.py (you need to set this route in opni.py)
    itinerary = generate_itinerary(place, visit_date, days, requirements)

    # Print the itinerary result instead of rendering a template
    return f"<h1>Your Travel Itinerary</h1><p>{itinerary}</p>"


'''@views.route('/', methods=['POST'])
@login_required
def add_note():  
    note_text = request.form.get('note')

    if len(note_text) < 1:
        flash('Note is too short!', category='error') 
    else:
        new_note = Note(data=note_text, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('pack your bags to go!', category='success')

    return redirect(url_for('views.home'))

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})'''
