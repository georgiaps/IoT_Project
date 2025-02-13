# City Microclimate and Traffic Analysis

A web-based platform for analyzing and visualizing correlations between urban microclimate conditions and traffic patterns.

## Description

This project provides an interactive web interface to explore the relationships between various urban environmental factors and traffic flow. The system processes environmental and traffic data to generate correlation diagrams and presents the findings through an intuitive web interface.

## Prerequisites

- Python 3.8 or higher
- Flask
- Required Python packages (install using `pip install -r requirements.txt`):
  - pandas
  - numpy
  - matplotlib
  - flask
  - flask-cors
  - influxdb_client
  - requests
  - scipy
  - paho-mqtt

## Installation

1. Clone this repository:
```bash
git clone https://github.com/georgiaps/IoT_Project
cd IoT_Project/code/backend
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the application, you need to configure the frontend to communicate with the backend server:

1. Navigate to the static folder
2. Open `script.js`
3. Locate the `backend_ip` constant
4. Replace its value with your localhost address:
```javascript
const backend_ip = "http://localhost:8080";
```

## Running the Application

1. First, generate the correlation diagrams:
```bash
python correlation_diagrams.py
```

2. Start the Flask backend server:
```bash
python flask_backend.py
```

3. Access the application:
   - Main website: [http://localhost:8080/](http://localhost:8080/)
   - API endpoint for city data: [http://localhost:8080/api/city-data](http://localhost:8080/api/city-data)

## Project Structure

```
backend/
├── correlation_diagrams.py   # Generates correlation analysis visualizations
├── flask_backend.py          # Flask server implementation
├── static/                   # Static assets
│   ├── script.js             # Frontend JavaScript
│   ├── styles.css            # CSS styles
│   ├── images/               # Images needed in frontend
│   ├── weather icons/        # Weather icons images
│   └── correlation diagrams/ # Correlation diagrams images
├── templates/                # HTML templates
│   └── index.html            # HTML file
```

## API Endpoints

- `GET /api/city-data`: Returns the processed city environmental and traffic data
- `GET /`: Serves the main web interface

## Troubleshooting

- Ensure all dependencies are installed.
- Make sure the backend is running before accessing the website.
- Check your firewall settings if you encounter connectivity issues.

## Contributions

Feel free to submit issues or pull requests for improvements.

## Contact
For questions or suggestions, reach out to the project maintainers.

- Fyrogeni Ariadne
- Psychogiou Georgia

Project Link: [https://github.com/georgiaps/IoT_Project](https://github.com/georgiaps/IoT_Project)
