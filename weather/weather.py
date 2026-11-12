import streamlit as st
import requests
import groq
from datetime import datetime
import base64
import html  # Import html module
import os
 
# Function to encode images to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
 
# Back Arrow Image
back_arrow_image_path = "backward.png"  # Path to your back arrow image
encoded_back_arrow = encode_image_to_base64(back_arrow_image_path)
st.markdown(f'''
<div class="back-arrow">
    <a href="http://localhost:8501">
    <img src="data:image/png;base64,{encoded_back_arrow}" alt="Back Arrow">
    </a>
</div>
''', unsafe_allow_html=True)
 
# Custom CSS for the app theme
st.markdown(
    """
    <style>
    /* Ensure the entire page background */
    html, body {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
        background-image: url(https://cdn.pixabay.com/photo/2021/05/22/20/31/thunderstorm-6274575_1280.jpg) !important;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4);
    }
    .st-b7 {
    background-color: rgb(168 174 186 / 19%);
}
 
    /* Override the header background by targeting the generated class name */
    .st-emotion-cache-12fmjuu {
        background-image: url(https://cdn.pixabay.com/photo/2021/05/22/20/31/thunderstorm-6274575_1280.jpg) !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }
 
    /* Ensure the header remains visible with a higher z-index */
    .st-emotion-cache-12fmjuu {
        z-index: 999990 !important;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 3.75rem;
        outline: none;
        display: block;
    }
 
    /* Ensure the back arrow image has the correct size */
    .back-arrow img {
        width: 45px !important;  /* Enforce the original size */
        height: 45px !important;
    }
 
    /* Ensure the weather icon images have the correct size */
    .weather-container img {
        width: 80px !important;  /* Enforce the original size */
        height: 80px !important;
    }
 
    /* Custom header text color */
    .st-emotion-cache-12fmjuu h1, .st-emotion-cache-12fmjuu h2, .st-emotion-cache-12fmjuu p {
        color: white !important;
    }
 
    /* Ensure the main app container spans the entire viewport */
    .stApp {
        height: 100vh;
        width: 100%;
        overflow: hidden;
        background: transparent !important;  /* Allow background to show */
    }
 
    /* Ensure sidebar background is slightly transparent */
    .css-1d391kg {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white;
        backdrop-filter: blur(5px);
    }
 
   /* Weather description container with transparent gray background */
.weather-container {
    background-color: rgba(0, 0, 0, 0.5) !important;  /* Transparent gray color */
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    border-radius: 10px !important;
    padding: 20px !important;
    color: khaki !important;
    margin-bottom: 20px !important;
    text-align: center !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5) !important;
    z-index: 99999 !important; /* Ensure it is not hidden */
}
 
 
    .weather-container h4 {
        font-size: 24px !important;
        font-weight: bold !important;
        text-shadow: none !important;
        color: white !important;
    }
 
    .weather-container p {
        font-size: 16px !important;
        color: white !important;
    }
 
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;  /* Green */
        color: orange;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
 
    /* Header and sidebar styling */
    .stHeader {
        background-image: url('https://your-image-url.jpg');
        background-size: cover;
        background-position: center;
        height: 100px;
        color: white;
    }
 
    .stHeader h1, .stHeader h2 {
        color: white !important;
    }
 
    .stHeader .stButton>button {
        font-size: 20px !important;
        padding: 10px !important;
        color: white !important;
    }
 
    .stHeader .stButton>button i {
        font-size: 24px !important;
        padding: 5px !important;
    }
 
    .stSidebar {
        background-color: rgba(38, 39, 48, 0.4) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5) !important;
    }
 
    .stSidebar h1, .stSidebar h2, .stSidebar p {
        color: white !important;
    }
 
    .stSidebar .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        border: none !important;
        transition: background-color 0.3s;
    }
 
    .stSidebar .stButton>button:hover {
        background-color: #45a049 !important;
    }
    .stButton>button {
    background-color: #4CAF50;
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
}
    </style>
    """,
    unsafe_allow_html=True
)
# Function to get weather data from the OpenWeather API
def get_weather_data(city, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()
 
# Function to get weather data by latitude and longitude
def get_weather_data_by_coordinates(lat, lon, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={weather_api_key}&lat={lat}&lon={lon}"
    response = requests.get(complete_url)
    return response.json()
 
# Function to get weather data from the OpenWeather API
def get_weather_data(city, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()
 
# Function to generate a weather description using Groq API
def generate_weather_description(data, groq_api_key):
    groq.api_key = groq_api_key
    try:
        temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        description = data['weather'][0]['description']
        icon_url = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-1024.png" # Weather Icon URL
        wind_speed = data['wind']['speed']  # Wind speed in meters per second
        humidity = data['main']['humidity']  # Humidity in percentage
 
        # Determine the wind quality description based on wind speed
        if wind_speed < 1:
            wind_quality = "Calm"
        elif 1 <= wind_speed <= 5:
            wind_quality = "Breezy"
        else:
            wind_quality = "Windy"
       
        # Prepare the prompt for Groq API to generate a description
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}℃. The wind speed is {wind_speed} m/s ({wind_quality}), and the humidity is {humidity}%. Explain this in terms of nature and plant growth."
 
        client = groq.Client(api_key=groq_api_key)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=550
        )
 
        if response.choices:
            message = response.choices[0].message
            description_content = message.content if hasattr(message, 'content') else "No content available."
        else:
            description_content = "The weather conditions are favorable for plant growth, with moderate temperature and humidity."
 
        # Escape any special HTML characters
        description_content = html.escape(description_content)
 
        # Use st.markdown to render the content in bullet points
        st.markdown(f"""
        <div class="weather-container">
            <img src="{icon_url}" alt="Weather Icon"/>
            <div>
                <h4>Weather Overview</h4>
                <ul style="text-align: left;">
                    <li><strong>Temperature:</strong> {temperature:.1f}℃</li>
                    <li><strong>Wind Speed:</strong> {wind_speed} m/s (<strong>{wind_quality}</strong>)</li>
                    <li><strong>Humidity:</strong> {humidity}%</li>
                    <li><strong>Weather Description:</strong> {description.capitalize()}</li>
                    <li><strong>Detailed Explanation:</strong> {description_content}</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"<p style='color: red;'>Error: {str(e)}</p>", unsafe_allow_html=True)
 
# Function to get weekly forecast data from OpenWeather API
def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()
 
# Function to display the weekly weather forecast in a single box
def display_weekly_forecast(data, city_name):
    try:
        if "list" not in data:
            st.error("No forecast data available.")
            return
       
        # Custom background for the entire forecast section
        st.markdown(
            f"""
            <div style="background: rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 20px; color: orange; text-align: center;">
                <!-- Custom box for the header with transparent black background -->
                <div style="background-color: rgba(50, 205, 50, 0.4); padding: 20px; border-radius: 10px; color: orange; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);">
            <h3>Weekly Weather Forecast for {city_name} 🌿</h3>
        </div>
    </div>
 
<!--<div style="background-image: url('https://th.bing.com/th/id/R.517f585434aac6f6bd29f19a1b8ce9c6?rik=HbYacb1tCyiCzg&riu=http%3a%2f%2fwww.donzonpower.com%2fimg%2fipart5-pic1.jpg&ehk=%2b7Nqb5wJkVbxJXc9BUBnOY0ZcHI5afnPHwJqcu2M8Zs%3d&risl=&pid=ImgRaw&r=0'); background-size: cover; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);">
    <div style="display: flex; flex-direction: column; text-align: center; color: black;">
    </div></div>-->
            """, unsafe_allow_html=True
        )
 
        displayed_dates = set()
        weekly_report = ""  # String to hold the content for the week
       
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            if date not in displayed_dates:
                displayed_dates.add(date)
 
                min_temp = day['main']['temp_min'] - 273.15
                max_temp = day['main']['temp_max'] - 273.15
                description = day['weather'][0]['description']
 
                # Add each day's data to the weekly report string
                weekly_report += f"""
                    <div style="padding: 15px; margin-bottom: 15px; background: rgba(50, 50, 50, 0.4); border-radius: 10px; background-color: rgba(0, 0, 0, 0.6); color: white; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);">
                      <h4>{date}</h4>
                      <p><strong>Weather:</strong> {description.capitalize()}</p>
                      <p><strong>Min Temp:</strong> {min_temp:.1f}℃ | <strong>Max Temp:</strong> {max_temp:.1f}℃</p>
                    </div>
                """
 
        # Render the full weekly report inside a single box
        st.markdown(weekly_report, unsafe_allow_html=True)
       
        st.markdown("</div></div></div>", unsafe_allow_html=True)
    except Exception as e:
        st.error("Error displaying weekly forecast: " + str(e))
 
 
# Function to get latitude and longitude from city name
def get_lat_lon_from_city(city, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={weather_api_key}&q={city}"
    response = requests.get(complete_url)
    data = response.json()
    if 'coord' in data:
        return data['coord']['lat'], data['coord']['lon'], data['name']
    else:
        return None, None, None
 
# Main function to run the Streamlit app
def main():
    # Sidebar configuration
    st.sidebar.title("Weather Forecasting 🌿")
   
    # Input fields for City, State, and Country
    st.sidebar.markdown("Option 1: Enter City, State, and Country Code \n")
    st.sidebar.markdown("Option 2: Enter Latitude and Longitude")
    city = st.sidebar.text_input("City Name")
    state_code = st.sidebar.text_input("State Code (optional)")
    country_code = st.sidebar.text_input("Country Code", "IN")
   
    # OR Label
    st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 15px; color: orange;">
        "OR"
    </div>
    """,
    unsafe_allow_html=True
)
 
   
    # Input fields for Latitude and Longitude
    lat = st.sidebar.text_input("Latitude", "")
    lon = st.sidebar.text_input("Longitude", "")
   
    st.sidebar.markdown("###")
   
    # Description about the inputs
    st.sidebar.markdown("""
    Please provide either **City, State, and Country Code** (Option 1)
    or **Latitude and Longitude** (Option 2) to get the weather updates.
    """)
   
    # API Keys
    weather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
    groq_api_key = os.getenv("GROQ_API_KEY", "")
   
    # Submit buttons
    submit_weather = st.sidebar.button("Get Current Weather")
    submit_forecast = st.sidebar.button("Show Weekly Forecast")
   
    # Get Current Weather or Weekly Forecast
    if submit_weather:
        st.markdown(f"<h1 style='color: white;'>Weather Updates</h1>", unsafe_allow_html=True)
        with st.spinner('Fetching weather data...'):
            if city:  # If city is provided
                weather_data = get_weather_data(f"{city},{state_code},{country_code}", weather_api_key)
                if 'main' in weather_data:
                    city_name = weather_data.get('name', city)
                    st.markdown(f"<h3 style='color: black;'>Weather Overview for {city_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style="background: rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 20px; color: white; text-align: center;">
                            {generate_weather_description(weather_data, groq_api_key)}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("City not found. Please check the city name.")
            elif lat and lon:  # If lat and lon are provided
                # Ensure the lat and lon are numbers
                try:
                    lat = float(lat)
                    lon = float(lon)
                    weather_data = get_weather_data_by_coordinates(lat, lon, weather_api_key)
                    if 'main' in weather_data:
                        st.markdown(f"<h3 style='color: yellow;'>Weather Overview for Coordinates: {lat}, {lon}</h3>", unsafe_allow_html=True)
                        st.markdown(f"""
                            <div style="background: rgba(0, 0, 0, 0.5); border-radius: 10px; padding: 20px; color: white; text-align: center;">
                                {generate_weather_description(weather_data, groq_api_key)}
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Location not found. Please check the coordinates.")
                except ValueError:
                    st.error("Please enter valid latitude and longitude values.")
   
    if submit_forecast:
        st.markdown(f"<h1 style='color: white;'>Weekly Weather Forecast</h1>", unsafe_allow_html=True)
        with st.spinner('Fetching weekly forecast...'):
            if city:  # If city is provided
                lat, lon, city_name = get_lat_lon_from_city(city, weather_api_key)
                if lat and lon:
                    weekly_data = get_weekly_forecast(weather_api_key, lat, lon)
                    display_weekly_forecast(weekly_data, city_name)
                else:
                    st.error("Location not found. Please check the city or coordinates.")
            elif lat and lon:  # If lat and lon are provided
                try:
                    lat = float(lat)
                    lon = float(lon)
                    weekly_data = get_weekly_forecast(weather_api_key, lat, lon)
                    display_weekly_forecast(weekly_data, f"Coordinates: {lat}, {lon}")
                except ValueError:
                    st.error("Please enter valid latitude and longitude values.")
 
# Run the Streamlit app
if __name__ == "__main__":
    main()