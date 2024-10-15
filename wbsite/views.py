from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

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


@views.route('/', methods=['POST'])
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

    return jsonify({})
