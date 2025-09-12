# Real-Time Weather Data Visualization Art

This project visualizes real-time or historical weather data as dynamic visual art. Weather parameters such as temperature, humidity, wind speed, precipitation, and pressure are mapped to visual elements like color, transparency, particle motion, and size.


## Data-Visualization Mapping

| Weather Data Field      | Visual Element                | Mapping Description |
|------------------------|-------------------------------|---------------------|
| temp_min, temp_max     | Color (background & balls)    | Average temperature maps to color: low temp = cyan/blue, high temp = orange/red |
| humidity_min, humidity_max | Number of balls            | Higher average humidity = more balls |
| wind_speed             | Ball movement & line count    | Higher wind = more pronounced ball movement and more connecting lines |
| description            | Ball size                     | If description contains 'shower' or 'thunderstorm', balls are larger |
| date                   | Date label                    | Displayed at top left |

Other features:
- The visualization automatically cycles through daily weather data every 2 seconds.
- All visual elements update in real time according to the current day's weather data.


## Data Source

Weather data is sourced from the official Hong Kong Observatory 9-day Weather Forecast:
https://www.hko.gov.hk/en/wxinfo/currwx/fnd.htm

These mappings help users intuitively understand the relationship between weather data and visual effects.
