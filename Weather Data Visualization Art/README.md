# Real-Time Weather Data Visualization Art

This project visualizes real-time or historical weather data as dynamic visual art. Weather parameters such as temperature, humidity, wind speed, precipitation, and pressure are mapped to visual elements like color, transparency, particle motion, and size.

## Available Versions

### 🌐 HTML/JavaScript Version
- **File**: `assets/weather_art.html`
- **Platform**: Web browsers
- **Features**: Interactive visualization using p5.js
- **Usage**: Open the HTML file in any web browser

### 🖥️ Python Desktop Version
- **File**: `weather_art_python.py`
- **Platform**: Desktop application (Windows, macOS, Linux)
- **Features**: Native desktop app using Pygame
- **Usage**: Run `python weather_art_python.py`

Both versions provide identical visual effects and data mapping.


## Data-Visualization Mapping

| Weather Data Field      | Visual Element                | Mapping Description |
|------------------------|-------------------------------|---------------------|
| temp_min, temp_max     | Color (background & balls)    | Average temperature maps to color: low temp = cyan/blue, high temp = orange/red |
| humidity_min, humidity_max | Number of balls            | Higher average humidity = more balls |
| wind_speed             | Ball movement & line count    | Higher wind = more pronounced ball movement and more connecting lines |
| description            | Ball size                     | If description contains 'shower' or 'thunderstorm', balls are larger |
| date                   | Date label                    | Displayed at top left |

Other features:
- The visualization automatically cycles through daily weather data every 1.5 seconds.
- All visual elements update in real time according to the current day's weather data.
- Interactive controls: Use left/right arrow keys to manually navigate between dates (Python version only).

## Installation & Setup

### HTML Version
1. Open `assets/weather_art.html` in any modern web browser
2. No additional installation required

### Python Version
1. Install required dependencies:
   ```bash
   pip install pygame
   ```
2. Run the application:
   ```bash
   python weather_art_python.py
   ```


## Data Source

Weather data is sourced from the official Hong Kong Observatory 9-day Weather Forecast:
https://www.hko.gov.hk/en/wxinfo/currwx/fnd.htm

These mappings help users intuitively understand the relationship between weather data and visual effects.
