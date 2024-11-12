// static/tripFunctions.js

async function fetchUserTrips() {
    try {
        const response = await fetch('/get_user_trips');
        const trips = await response.json();
        displayTrips(trips);
    } catch (error) {
        console.error('Error fetching trips:', error);
    }
}

function displayTrips(trips) {
    const tripContainer = document.getElementById('tripContainer');
    tripContainer.innerHTML = ''; // Clear previous trips

    trips.forEach(trip => {
        const tripItem = document.createElement('div');
        tripItem.classList.add('trip-item');

        const tripTitle = document.createElement('div');
        tripTitle.classList.add('trip-title');
        tripTitle.textContent = trip.place;

        const tripSubtitle = document.createElement('div');
        tripSubtitle.classList.add('trip-subtitle');
        tripSubtitle.textContent = `Date: ${trip.date}`;

        const tripDetails = document.createElement('div');
        tripDetails.classList.add('trip-details');
        tripDetails.innerHTML = `
            <p><strong>Days:</strong> ${trip.days}</p>
            <p><strong>Budget:</strong> $${trip.budget}</p>
            <p><strong>Accommodation:</strong> ${trip.accommodation}</p>
            <p><strong>Transport:</strong> ${trip.transport}</p>
            <p><strong>Local Travel:</strong> ${trip.local_travel}</p>
            <p><strong>Places Visited:</strong> ${trip.places_visited}</p>
            <p><strong>Food Recommendations:</strong> ${trip.food_recommendations}</p>
            <p><strong>Trip Description:</strong> ${trip.trip_description}</p>
        `;

        tripTitle.addEventListener('click', () => {
            tripDetails.style.display = tripDetails.style.display === 'none' ? 'block' : 'none';
        });

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteTrip(trip.id);

        tripItem.appendChild(tripTitle);
        tripItem.appendChild(tripSubtitle);
        tripItem.appendChild(tripDetails);
        tripItem.appendChild(deleteButton); // Append delete button

        tripContainer.appendChild(tripItem);
    });
}

async function deleteTrip(tripId) {
    const confirmation = confirm('Are you sure you want to delete this trip?');
    if (confirmation) {
        try {
            const response = await fetch(`/delete_trip/${tripId}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                alert('Trip deleted successfully!');
                fetchUserTrips(); // Refresh trips
            } else {
                const errorData = await response.json(); // Get response data
                alert('Failed to delete trip: ' + errorData.message); // Show error message
            }
        } catch (error) {
            console.error('Error deleting trip:', error);
            alert('An error occurred while deleting the trip.');
        }
    }
}

document.addEventListener('DOMContentLoaded', fetchUserTrips);