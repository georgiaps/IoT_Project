window.onload = function() {
    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });
};

// Weather icon mapping
const weatherIconsDay = {
    'clear sky': 'weather icons/clear sky day.png',
    'few clouds': 'weather icons/few clouds day.png',
    'scattered clouds': 'weather icons/scattered clouds day.png',
    'broken clouds': 'weather icons/broken clouds.png',
    'overcast clouds': 'weather icons/broken clouds.png',
    'shower rain': 'weather icons/shower rain.png',
    'light rain': 'weather icons/shower rain.png',
    'moderate rain': 'weather icons/shower rain.png',
    'heavy intensity rain': 'weather icons/shower rain.png',
    'very heavy rain': 'weather icons/shower rain.png',
    'extreme rain': 'weather icons/shower rain.png',
    'rain': 'weather icons/rain.png',
    'drizzle': 'weather icons/rain.png',
    'drizzle rain': 'weather icons/rain.png',
    'thunderstorm': 'weather icons/thunderstorm.png',
    'thunderstorm with light rain': 'weather icons/thunderstorm.png',
    'thunderstorm with rain': 'weather icons/thunderstorm.png',
    'thunderstorm with heavy rain': 'weather icons/thunderstorm.png',
    'thunderstorm with drizzle': 'weather icons/thunderstorm.png',
    'light thunderstorm': 'weather icons/thunderstorm.png',
    'heavy thunderstorm': 'weather icons/thunderstorm.png',
    'snow': 'weather icons/snow.png',
    'light snow': 'weather icons/snow.png',
    'light rain and snow': 'weather icons/snow.png',
    'mist': 'weather icons/mist.png', 
    'haze': 'weather icons/mist.png', 
    'fog': 'weather icons/mist.png', 
    'dust': 'weather icons/mist.png',            
};

const weatherIconsNight = {
    'clear sky': 'weather icons/clear sky night.png',
    'few clouds': 'weather icons/few clouds night.png',
    'scattered clouds': 'weather icons/scattered clouds night.png',
    'broken clouds': 'weather icons/broken clouds.png',
    'overcast clouds': 'weather icons/broken clouds.png',
    'shower rain': 'weather icons/shower rain.png',
    'light rain': 'weather icons/shower rain.png',
    'moderate rain': 'weather icons/shower rain.png',
    'heavy intensity rain': 'weather icons/shower rain.png',
    'very heavy rain': 'weather icons/shower rain.png',
    'extreme rain': 'weather icons/shower rain.png',
    'rain': 'weather icons/rain.png',
    'drizzle': 'weather icons/rain.png',
    'drizzle rain': 'weather icons/rain.png',
    'thunderstorm': 'weather icons/thunderstorm.png',
    'thunderstorm with light rain': 'weather icons/thunderstorm.png',
    'thunderstorm with rain': 'weather icons/thunderstorm.png',
    'thunderstorm with heavy rain': 'weather icons/thunderstorm.png',
    'thunderstorm with drizzle': 'weather icons/thunderstorm.png',
    'light thunderstorm': 'weather icons/thunderstorm.png',
    'heavy thunderstorm': 'weather icons/thunderstorm.png',
    'snow': 'weather icons/snow.png',
    'light snow': 'weather icons/snow.png',
    'light rain and snow': 'weather icons/snow.png',
    'mist': 'weather icons/mist.png', 
    'haze': 'weather icons/mist.png', 
    'fog': 'weather icons/mist.png', 
    'dust': 'weather icons/mist.png',            
};

// Function to update city weather overview
function updateCityWeather(data) {
    if (!data || !data.Patras || !data.Patras.weather) return;

    const cityWeather = data.Patras.weather || {};;
    
    // Update weather icon
    const weatherIcon = document.getElementById('weather-icon');
    const description = cityWeather.Description?.toLowerCase() || 'clear sky';
    weatherIcon.src = weatherIconsDay[description] || 'default weather.png';


    // Helper function to handle display values with units
    const displayValue = (value, unit) => {
        if (value !== undefined && value !== null && value !== '') {
            return value + unit;
        }
        return '--';
    };
    
    // Update weather data
    document.getElementById('city-description').textContent = cityWeather.Description || '--';
    document.getElementById('city-temperature').textContent = displayValue(cityWeather.Temperature, '°C');
    document.getElementById('city-humidity').textContent = displayValue(cityWeather.Humidity, '%');
    document.getElementById('city-wind-speed').textContent = displayValue(cityWeather['Wind Speed'], ' km/h');
    document.getElementById('city-rain').textContent = displayValue(cityWeather.Rain, ' mm');
}

function fetchGeneralCityWeather() {
    fetch('http://172.20.10.6:8080/api/city-data')
        .then(response => response.json())
        .then(data => {
            updateCityWeather(data);
        })
        .catch(error => console.error('Error fetching city data:', error));
}

// Call this when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchGeneralCityWeather();
});

const map = L.map('map').setView([38.273530, 21.730154], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

const locations = [
    { name: 'Rio-Antirrio Bridge', coords: [38.320745, 21.773224], color: '#6d6a82' },
    { name: 'University Crossroad', coords: [38.290672, 21.780164], color: '#7091e6' },
    { name: 'University of Patras', coords: [38.286860,21.787316], color: '#27489c' },
    { name: 'Kastelokampos', coords: [38.2893, 21.7739], color: '#566487' },
    { name: 'Agyias Beach', coords: [38.277013, 21.745342], color: '#3d52a0' },
    { name: 'Kato Sychaina', coords: [38.2652,21.757], color: '#303a5c' },
    { name: 'National Road Interchange', coords: [38.262128, 21.750417], color: '#47a3c2' },
    { name: 'Dasyllio', coords: [38.248858, 21.745578], color: '#515660' },
    { name: 'Patras Centre', coords: [38.246877, 21.735854], color: '#5c52a0' },
    { name: 'Gounarh Road', coords: [38.245566, 21.730981], color: '#7687b7' },
    { name: 'South Park', coords: [38.237902, 21.725841], color: '#5a87a0' },
    { name: 'Leuka', coords: [38.2066,21.7271], color: '#805fa5' },
    { name: 'Demenika', coords: [38.2001,21.7438], color: '#566ba4' },
    { name: 'Paralia', coords: [38.1994,21.6992], color: '#2c6182' }
];

const locationWeatherInfo = document.getElementById('loc-info');
const locationTrafficInfo = document.getElementById('loc-info');

// Get the user's geolocation
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, handleError, {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
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

    
    // Clear weather and traffic info
    document.getElementById('temperature').textContent = "--";
    document.getElementById('humidity').textContent = "--";
    document.getElementById('wind-speed').textContent = "--";
    document.getElementById('wind-direction').textContent = "--";
    document.getElementById('rain').textContent = "--";
    document.getElementById('pressure').textContent = "--";
    
    document.getElementById('current-speed').textContent = "--";
    document.getElementById('free-flow-speed').textContent = "--";
    document.getElementById('traffic-percentage').textContent = "--";
}

// Call getLocation on page load
getLocation();

// Set up the section navigation
document.querySelectorAll('.nav-button').forEach(button => {
    button.addEventListener('click', () => {
        switchSection(button.dataset.section);
    });
});

// Switch the section navigation
function switchSection(sectionId) {
    document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    const button = document.querySelector(`[data-section="${sectionId}"]`);
    if (button) button.classList.add('active');
    
    const section = document.getElementById(sectionId);
    if (section) section.classList.add('active');
}

// Function to show City Points section
function showCityPointsSection() {
    document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    const cityPointsButton = document.querySelector('[data-section="city-points"]');
    cityPointsButton.classList.add('active');
    document.getElementById('city-points').classList.add('active');
}

// Update weather and traffic location info when a location point is clicked
document.querySelectorAll('.location-item').forEach(item => {
    item.addEventListener('click', () => {
        const locationName = item.getAttribute('data-location');
        if (locationName) {
            switchSection('city-points');
            selectedLocation = locationName; // Update selectedLocation
            updateWeatherLocationInfo(locationName);
            updateTrafficLocationInfo(locationName);
            if (selectedDate) {
                fetch('http://172.20.10.6:8080/api/city-data')
                    .then(response => response.json())
                    .then(data => {
                        updateForecastData(data, selectedLocation, selectedDate);
                    })
                    .catch(error => console.error('Error fetching forecast data:', error));
            }
        }
    });
});

// Custom marker icon definition
const createCustomMarker = (color) => {
    return L.divIcon({
        html: `<svg width="14" height="26" viewBox="0 0 24 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 8.4 12 20 12 20s12-11.6 12-20c0-6.63-5.37-12-12-12zm0 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z" 
            fill="${color}"/>
        </svg>`,
        className: 'custom-marker',
        iconSize: [14, 26],
        iconAnchor: [7, 26],
        popupAnchor: [0, -32]
    });
};

// Update weather and traffic location info when a marker in map is clicked
locations.forEach(loc => {
    const marker = L.marker(loc.coords, {
        icon: createCustomMarker(loc.color)
    })
    .bindPopup(`
        <div class="marker-popup">
            <h3>${loc.name}</h3>
        </div>
    `)
    .addTo(map)
    .on('click', () => {
        switchSection('city-points');
        selectedLocation = loc.name; // Update selectedLocation
        updateWeatherLocationInfo(loc.name);
        updateTrafficLocationInfo(loc.name);
        if (selectedDate) {
            fetch('http://172.20.10.6:8080/api/city-data')
                .then(response => response.json())
                .then(data => {
                    updateForecastData(data, selectedLocation, selectedDate);
                })
                .catch(error => console.error('Error fetching forecast data:', error));
        }
    });

    // Open popup on hover
    marker.on('mouseover', function (e) {
        this.openPopup();
    });

    // Close popup when mouse leaves
    marker.on('mouseout', function (e) {
        this.closePopup();
    });
});

// Update weather and traffic location info when infodropdown selection changes
document.querySelectorAll('.infodropdown-content button').forEach(button => {
    button.addEventListener('click', () => {
        const locationName = button.dataset.location;
        if (locationName) {
            updateWeatherLocationInfo(locationName);
            updateTrafficLocationInfo(locationName);
            updateinfodropdownButton(locationName);
        }
    });
});

const infodropdownButton = document.querySelector('.infodropdown button');

// Function to update the infodropdown button text
function updateinfodropdownButton(locationName) {
    if (infodropdownButton) {
        infodropdownButton.textContent = locationName;
    }
    document.querySelectorAll('.infodropdown-content button').forEach(button => {
        button.classList.remove('active');
        if (button.dataset.location === locationName) {
            button.classList.add('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', fetchCityData);
document.querySelector('.refresh-button').addEventListener('click', fetchCityData);

let currentSelectedLocation = '';

function fetchCityData() {
    /*fetch('http://192.168.1.6:8080/api/city-data') georgia*/
    /*fetch('http://192.168.1.144:8080/api/city-data') giorgos*/
    /*fetch('http://192.168.1.6:8080/api/city-data')*/
    fetch('http://172.20.10.6:8080/api/city-data') /*atout*/
        .then(response => response.json())
        .then(data => {
            if (currentSelectedLocation) {
                updateFrontend(data, currentSelectedLocation);
            }
        })
        .catch(error => console.error('Error fetching city data:', error));
}

// Update weather and traffic info
function updateFrontend(data, location) {
    const locationData = data[location];
    if (!locationData) return;

    const weather = locationData.weather || {};
    const traffic = locationData.traffic || {};

    // Helper function to handle display values with units
    const displayValue = (value, unit) => {
        if (value !== undefined && value !== null && value !== '') {
            return value + unit;
        }
        return '--';
    };

    // Weather information
    document.getElementById('temperature').textContent = displayValue(weather.Temperature, '°C');
    document.getElementById('humidity').textContent = displayValue(weather.Humidity, '%');
    document.getElementById('wind-speed').textContent = displayValue(weather['Wind Speed'], ' km/h');
    document.getElementById('wind-direction').textContent = displayValue(weather['Wind Direction'], '°');
    document.getElementById('rain').textContent = displayValue(weather.Rain, ' mm');
    document.getElementById('pressure').textContent = displayValue(weather.Pressure, ' hPa');

    // Traffic information
    document.getElementById('current-speed').textContent = displayValue(traffic['Current Speed'], ' km/h');
    document.getElementById('free-flow-speed').textContent = displayValue(traffic['Free Flow Speed'], ' km/h');
    document.getElementById('traffic-percentage').textContent = displayValue(((traffic['Traffic Percentage'])*100).toFixed(0), '%');
}

// Update weather info when location changes
function updateWeatherLocationInfo(location) {
    currentSelectedLocation = location;
    updateinfodropdownButton(location);
    fetchCityData(); // Fetch fresh data when location changes
}

// Update traffic info when location changes
function updateTrafficLocationInfo(location) {
}

// Add periodic data refresh (optional)
setInterval(fetchCityData, 30000);

// Reference the search input and form
const searchInput = document.querySelector('.search-container input[type="text"]');
const searchForm = document.querySelector('.search-container form');

// Event listener for the search form submission
searchForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the default form submission

    const searchTerm = searchInput.value.trim().toLowerCase();
    if (!searchTerm) return alert('Please enter a location name.');

    // Find the matching location
    const location = locations.find(loc => loc.name.toLowerCase().includes(searchTerm));
    if (!location) return alert('Location not found. Please try again.');

    // Navigate to the "City Points Info" section
    switchSection('city-points');

    // Update selectedLocation
    selectedLocation = location.name;

    // Update weather and traffic information
    updateWeatherLocationInfo(location.name);
    updateTrafficLocationInfo(location.name);

    if (selectedDate) {
        fetch('http://172.20.10.6:8080/api/city-data')
            .then(response => response.json())
            .then(data => {
                updateForecastData(data, selectedLocation, selectedDate);
            })
            .catch(error => console.error('Error fetching forecast data:', error));
    }

    // Highlight the matching location in the infodropdown (optional)
    document.querySelectorAll('.infodropdown-content button').forEach(button => {
        button.classList.remove('active');
        if (button.dataset.location === location.name) {
            button.classList.add('active');
        }
    });
});

// Function to format date as dd-MM-yyyy
function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
}

// Function to add days to a date
function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

// Get tomorrow's date
const tomorrow = addDays(new Date(), 1);

// Generate the next 3 dates
const dates = [
    tomorrow,
    addDays(tomorrow, 1),
    addDays(tomorrow, 2)
];

// Get the dropdown content container
const dateContent = document.getElementById('dateContent');

// Add the dates as buttons
dates.forEach(date => {
    const formattedDate = formatDate(date);
    const button = document.createElement('button');
    button.setAttribute('date', formattedDate);
    button.textContent = formattedDate;
    
    // Optional: Add click handler for the button
    button.addEventListener('click', () => {
        console.log('Selected date:', formattedDate);
        // You can handle the date selection here
    });
    
    dateContent.appendChild(button);
});





let selectedLocation = '';
let selectedDate = '';

// Function to convert date from DD-MM-YYYY to YYYY-MM-DD
function convertDateFormat(dateStr) {
    const [day, month, year] = dateStr.split('-');
    return `${year}-${month}-${day}`;
}

// Update forecast data based on selected location and date
function updateForecastData(data, location, buttonDate) {
    if (!data || !data[location] || !data[location].forecast) return;

    const forecasts = data[location].forecast;
    
    // Convert button date format (DD-MM-YYYY) to API date format (YYYY-MM-DD)
    const apiDateFormat = convertDateFormat(buttonDate);
    
    // Filter forecasts for the selected date
    const dayForecasts = forecasts.filter(forecast => 
        forecast.dt_txt.split(' ')[0] === apiDateFormat
    );

    // Update data for each time slot
    const times = ['09:00:00', '15:00:00', '21:00:00'];
    times.forEach(time => {
        const forecast = dayForecasts.find(f => f.dt_txt.split(' ')[1] === time) || {};
        const hour = time.split(':')[0];

        // Update all weather parameters for this time slot
        document.getElementById(`forecast-temperature-${hour}`).textContent = 
            forecast.temp !== undefined ? `${forecast.temp}°C` : '--';
        document.getElementById(`forecast-humidity-${hour}`).textContent = 
            forecast.humidity !== undefined ? `${forecast.humidity}%` : '--';
        document.getElementById(`forecast-wind-speed-${hour}`).textContent = 
            forecast.wind_speed !== undefined ? `${forecast.wind_speed} km/h` : '--';
        document.getElementById(`forecast-wind-direction-${hour}`).textContent = 
            forecast.wind_deg !== undefined ? `${forecast.wind_deg}°` : '--';
        document.getElementById(`forecast-rain-${hour}`).textContent = 
            forecast.rain_1h !== undefined ? `${forecast.rain_1h} mm` : '--';
        document.getElementById(`forecast-pressure-${hour}`).textContent = 
            forecast.pressure !== undefined ? `${forecast.pressure} hPa` : '--';
    });
}

// Modify the date button click handler
function setupDateButtons() {
    const dateButtons = document.querySelectorAll('#dateContent button');
    dateButtons.forEach(button => {
        button.addEventListener('click', () => {
            selectedDate = button.getAttribute('date');
            updateForecastDropdownButton(selectedDate); // Update dropdown button

            if (selectedLocation && selectedDate) {
                fetch('http://172.20.10.6:8080/api/city-data')
                    .then(response => response.json())
                    .then(data => {
                        updateForecastData(data, selectedLocation, selectedDate);
                    })
                    .catch(error => console.error('Error fetching forecast data:', error));
            }
        });
    });
}

const forecastdropdownButton = document.querySelector('.forecastdropdown button');

// Function to update the forecast dropdown button text and active state
function updateForecastDropdownButton(date) {
    const forecastDropdownButton = document.querySelector('.forecastdropdown button');
    if (forecastDropdownButton) {
        forecastDropdownButton.textContent = date;
    }
    document.querySelectorAll('.forecastdropdown-content button').forEach(button => {
        button.classList.remove('active');
        if (button.getAttribute('date') === date) {
            button.classList.add('active');
        }
    });
}



function setupLocationHandlers() {
    document.querySelectorAll('.infodropdown-content button').forEach(button => {
        button.addEventListener('click', () => {
            selectedLocation = button.dataset.location;
            updateinfodropdownButton(selectedLocation);
            
            if (!selectedDate) {
                clearForecastData();
            } else {
                fetch('http://172.20.10.6:8080/api/city-data')
                    .then(response => response.json())
                    .then(data => {
                        updateForecastData(data, selectedLocation, selectedDate);
                    })
                    .catch(error => console.error('Error fetching forecast data:', error));
            }
        });
    });
}

function clearForecastData() {
    const times = ['9', '15', '21'];
    const parameters = ['temperature', 'humidity', 'wind-speed', 'wind-direction', 'rain', 'pressure'];
    
    times.forEach(time => {
        parameters.forEach(param => {
            document.getElementById(`forecast-${param}-${time}`).textContent = '--';
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setupDateButtons();
    setupLocationHandlers();
    clearForecastData();
});


        

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.diagramsdropdown-content button').forEach(button => {
        button.addEventListener('click', function () {
            const location = this.getAttribute('data-location');
            const diagramContainer = document.getElementById('diagram-container-correlation');

            // Check if the container exists
            if (!diagramContainer) {
                console.error('Error: diagram-container-correlation not found in the DOM.');
                return;
            }

            // Update dropdown button text
            const diagramsdropdownButton = document.querySelector('.diagramsdropdown button');
            if (diagramsdropdownButton) {
                diagramsdropdownButton.textContent = location;
            }

            // Get the current date
            const today = new Date();

            // Generate the last 3 dates
            const dates = [];
            for (let i = 0; i < 3; i++) {
                const date = new Date(today);
                date.setDate(today.getDate() - i);
                const formattedDate = date.toISOString().split('T')[0];
                dates.push(formattedDate);
            }

            // Clear existing images
            diagramContainer.innerHTML = '';

            // Create a flex container for the images
            const flexContainer = document.createElement('div');
            flexContainer.style.display = 'flex';
            flexContainer.style.justifyContent = 'space-between';
            flexContainer.style.marginTop = '20px';

            // Load images
            dates.forEach(date => {
                const img = document.createElement('img');
                img.src = `correlation_diagrams/${location}/${date}.png`;
                img.alt = `${location} - ${date} Correlation Diagram`;
                img.style.width = '30%';
                img.style.border = '2px solid #ccc';
                img.style.borderRadius = '5px';

                // Add error handling
                img.onerror = () => {
                    img.style.display = 'none';
                    console.error(`Image not found: ${img.src}`);
                };

                flexContainer.appendChild(img);
            });

            diagramContainer.appendChild(flexContainer);

            // Update the dropdown button and active state
            document.querySelectorAll('.diagramsdropdown-content button').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
});

const diagramsdropdownButton = document.querySelector('.diagramsdropdown button');

// Function to update the diagramsdropdown button text
function updatediagramsdropdownButton(locationName) {
    if (diagramsdropdownButton) {
        diagramsdropdownButton.textContent = locationName;
    }
    document.querySelectorAll('.diagramsdropdown-content button').forEach(button => {
        button.classList.remove('active');
        if (button.dataset.location === locationName) {
            button.classList.add('active');
        }
    });
}

function handleError(error) {
    let errorMessage = "";
    switch(error.code) {
        case error.PERMISSION_DENIED:
            errorMessage = "Please enable location services to use this feature.";
            break;
        case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information is currently unavailable.";
            break;
        case error.TIMEOUT:
            errorMessage = "Location request timed out. Please try again.";
            break;
        default:
            errorMessage = "An unknown error occurred while getting location.";
            break;
    }
    console.log(errorMessage);
}