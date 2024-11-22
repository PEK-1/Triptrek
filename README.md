Trip Tracker Application
Overview
The Trip Tracker application is a web-based platform designed to help users plan, manage, and share their travel itineraries. Users can log in, create accounts, add trips, and save details such as accommodation, transport, budget, and places visited. The application allows users to search for trips, view their trip history, and generate detailed itineraries based on their inputs.

Features
User Authentication: Secure login and sign-up for users.
Trip Management: Add, view, delete, and search trips.
Trip Details: Manage detailed trip information such as accommodation, transport, places visited, and more.
Search Functionality: Search for trips based on destination name.
Itinerary Generator: Create and view detailed trip itineraries.
Responsive Design: Mobile-friendly and optimized for all devices.
Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask)
Database: SQLite (Flask-based database)
Libraries:
Flask for the web framework
Setup Instructions
Prerequisites
Python 3.x
Pip (Python package manager)
Installing
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/trip-tracker.git
cd trip-tracker
Create a Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate  # For Windows
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up the Database:

The application uses an SQLite database that will be created automatically when you first run the app.

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Application:

bash
Copy code
flask run
The app will be running on http://127.0.0.1:5000.

Database Setup
The application uses SQLite by default for local storage.
When running the app for the first time, the database will be automatically set up.
User data, including trips, will be stored in the database.
API Endpoints
Login

GET /log: Renders the login page.
POST /log: Authenticates the user.
Logout

GET /logout: Logs the user out and redirects to the login page.
Sign Up

GET /sign_up: Renders the sign-up page.
POST /sign_up: Registers a new user.
Add Trip

POST /addTrip: Adds a new trip to the user's profile.
View My Trips

GET /mytips: Displays all trips added by the logged-in user.
Search Trips

GET /search: Searches for trips by destination.
Delete Trip

DELETE /delete_trip/<int:trip_id>: Deletes a specific trip.
Generate Itinerary

POST /submit: Generates an itinerary based on the provided trip details.
Generate Day Plan

POST /generate_day_plan: Generates a detailed day plan for a selected trip.
Usage
Login: After registering, you can log in to the app using your email and password.
Add a Trip: Once logged in, you can add new trips, specifying the place, dates, and other trip details.
Search Trips: You can search for trips by destination to view others’ trips.
View Trips: All your trips will be displayed under your profile, where you can edit or delete them.
Itinerary Generator: Generate a detailed itinerary for your trip, including specific activities and places to visit.
Folder Structure
php
Copy code
trip-tracker/
│
├── app.py               # Main application file (Flask app)
├── templates/           # HTML templates
│   ├── index.html       # Home page
│   ├── login.html       # Login page
│   ├── sign_up.html     # Sign-up page
│   ├── mytips.html      # User's trips page
│   └── ...
├── static/              # Static files (CSS, JS, images)
│   ├── css/             # CSS files
│   ├── js/              # JavaScript files
│   └── ...
├── requirements.txt     # Required Python libraries
├── config.py            # Configuration file (app settings)
└── models.py            # Database models (SQLAlchemy)
Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add new feature').
Push to your fork (git push origin feature-branch).
Create a new Pull Request.
