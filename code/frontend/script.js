const map = L.map('map').setView([38.2466, 21.7345], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

const locations = [
    { name: 'University Crossroad', coords: [38.290672, 21.780164], color: '#00cccc' },
    { name: 'Agyias Beach', coords: [38.277013, 21.745342], color: '#0066ff' },
    { name: 'National Road Interchange', coords: [38.262128, 21.750417], color: '#800080' },
    { name: 'Patras Centre', coords: [38.246877, 21.735854], color: '#ff6600' },
    { name: 'Gounarh Road', coords: [38.245566, 21.730981], color: '#ff3366' },
    { name: 'South Park', coords: [38.237902, 21.725841], color: '#009900' },
    { name: 'Dasyllio', coords: [38.248858, 21.745578], color: '#1a481a' }
];

// Function to show the "City Points Info" section
function showCityPointsSection() {
    document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelector('.nav-button[data-section="city-points"]').classList.add('active');
    document.getElementById('city-points').classList.add('active');
    
    const locationSelect = document.getElementById('location-select');
    locationSelect.value = ""; // Reset dropdown so user has to select a location
    locationInfo.innerHTML = "<p>Please select a location to view the weather information.</p>"; // Show message to prompt selection
}

// Add markers to the map
locations.forEach(loc => {
    L.marker(loc.coords, {
        icon: L.divIcon({
            html: `<span style="color: ${loc.color}; font-size: 24px;">★</span>`,
            className: 'star-marker',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        })
    }).bindPopup(loc.name)
      .addTo(map)
      .on('click', () => {
          // When clicking on a marker, transition to the "City Points Info" section
          showCityPointsSection();
          const locationSelect = document.getElementById('location-select');
          locationSelect.value = loc.name; // Set dropdown to clicked location
          updateLocationInfo(loc.name); // Update info for the clicked location
      });
});

// Update the weather info based on the selected location
const locationData = {
    'University Crossroad': { temperature: '21°C', humidity: '65%', wind_speed: '10km/h', wind_direction: '80°', rain:'1.8mm', pressure:'1600hPA' },
    'Agyias Beach': { temperature: '24°C', humidity: '70%', wind_speed: '15km/h', wind_direction: '81°', rain:'1.8mm', pressure:'1070hPA' },
    'National Road Interchange': { temperature: '23°C', humidity: '75%', wind_speed: '20km/h', wind_direction: '80°', rain:'1.1mm', pressure:'1800hPA' },
    'Patras Centre': { temperature: '22°C', humidity: '80%', wind_speed: '18km/h', wind_direction: '82°' , rain:'1.6mm', pressure:'1400hPA'},
    'Gounarh Road': { temperature: '20°C', humidity: '60%', wind_speed: '12km/h', wind_direction: '70°', rain:'3.1mm', pressure:'1030hPA' },
    'South Park': { temperature: '19°C', humidity: '55%', wind_speed: '14km/h', wind_direction: '89°', rain:'2.1mm', pressure:'1020hPA' },
    'Dasyllio': { temperature: '18°C', humidity: '50%', wind_speed: '16km/h', wind_direction: '56°', rain:'6.1mm', pressure:'1020hPA' }
};

const locationSelect = document.getElementById('location-select');
const locationInfo = document.getElementById('location-info');

// Function to update the displayed weather information for the selected location
function updateLocationInfo(location) {
    const data = locationData[location];
    locationInfo.innerHTML = `
<div class="weather-item">
            <h3>Temperature</h3>
            <p>${data.temperature}</p>
        </div>
        <div class="weather-item">
            <h3>Humidity</h3>
            <p>${data.humidity}</p>
        </div>
        <div class="weather-item">
            <h3>Wind Speed</h3>
            <p>${data.wind_speed}</p>
        </div>
        <div class="weather-item">
            <h3>Wind Direction</h3>
            <p>${data.wind_direction}</p>
        </div>
        <div class="weather-item">
            <h3>Rain</h3>
            <p>${data.rain}</p>
        </div>
        <div class="weather-item">
            <h3>Pressure</h3>
            <p>${data.pressure}</p>
        </div>
    `;
}

// Update the weather info when a new location is selected from the dropdown
locationSelect.addEventListener('change', (event) => {
    const selectedLocation = event.target.value;
    if (selectedLocation) {
        updateLocationInfo(selectedLocation);
    } else {
        locationInfo.innerHTML = "<p>Please select a location to view the weather information.</p>"; // Show message if no location selected
    }
});

// Initialize with no location selected (info should prompt the user to select)
locationInfo.innerHTML = "<p>Please select a location to view the weather information.</p>";

// Get the user's geolocation
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, handleError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const userLat = position.coords.latitude;
    const userLon = position.coords.longitude;

    // Move the map to the user's location
    map.setView([userLat, userLon], 13);

    // Add a marker for the user's location
    L.marker([userLat, userLon])
        .addTo(map)
        .bindPopup("You are here!")
        .openPopup();

    // Optionally, update the location dropdown and weather info if needed
    // You can set the closest city based on distance, for example.
    // For simplicity, let's just display a message for now.
    locationSelect.value = ""; // Reset to no selection
    locationInfo.innerHTML = "<p>Please select a location to view the weather information.</p>"; // Prompt to select location
}

function handleError(error) {
    switch(error.code) {
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

// Call getLocation on page load
getLocation();

// Function to handle location click (based on your HTML structure)
function goToLocation(locationName) {
    showCityPointsSection(); // Show the City Points Info section
    const locationSelect = document.getElementById('location-select');
    locationSelect.value = locationName; // Set dropdown to clicked location
    updateLocationInfo(locationName); // Update info for the clicked location
}

// Set up the section navigation
document.querySelectorAll('.nav-button').forEach(button => {
    button.addEventListener('click', () => {
        document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        button.classList.add('active');
        document.getElementById(button.dataset.section).classList.add('active');
    });
});
