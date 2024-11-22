// Function to get the user's location using the browser's geolocation API
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    // Get latitude and longitude from the browser's geolocation API
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    document.getElementById("location").value = `${lat},${lon}`;
    document.getElementById("manualLocation").style.display = "none";
    document.getElementById("submitBtn").style.display = "inline";
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

// Show the manual location input field
function showManualLocation() {
    document.getElementById("manualLocation").style.display = "inline";
    document.getElementById("submitBtn").style.display = "inline";
}

// Function to submit location and time to the backend
function submitForm() {
    let location = document.getElementById("location").value;
    if (location === "") {
        location = document.getElementById("manualLocationInput").value;
    }

    // Get the current time in ISO 8601 format
    const currentTime = new Date().toISOString();

    // Send the location and time to the backend
    fetch('/set_location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            location: location,
            time: currentTime, // Include time
        }),
    })
        .then(response => response.json())
        .then(() => {
            // Proceed to generate the day plan after setting location and time in the session
            return fetch('/generate_day_plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
        })
        .then(response => response.json())
        .then(data => {
            // Display the generated itinerary
            document.getElementById("itinerary").innerHTML = data.day_plan;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
