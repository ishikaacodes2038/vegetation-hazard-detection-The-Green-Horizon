import streamlit as st
from PIL import Image
import base64
import io
import requests
import re
from groq import Groq
import os
 
# Function to encode the image to base64
def encode_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")  # Ensure compatibility
    with io.BytesIO() as buffered:
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
# Title of the App


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    





st.markdown(
    f"""
    <style>
    .st-emotion-cache-qgowjl p {{
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 17px;
}}

    .st-emotion-cache-1v0mbdj {{
    display: flex;
    flex-direction: column;
    -webkit-box-align: stretch;
    align-items: stretch;
    width: 100%;
    -webkit-box-flex: 0;
    flex-grow: 0;
}}
.st-emotion-cache-1erivf3 {{
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    background-color: rgb(38 39 48 / 30%);
    border-radius: 0.5rem;
    color: rgb(250, 250, 250);
}}
.st-emotion-cache-1erivf3 {{
    display: flex
;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    background-color: rgb(255 255 255 / 30%);
    border-radius: 0.5rem;
    color: rgb(250, 250, 250);
}}
.st-emotion-cache-6rlrad {{
    vertical-align: middle;
    overflow: hidden;
    color: inherit;
    fill: white;
    display: inline-flex
;
    -webkit-box-align: center;
    align-items: center;
    font-size: 2.3rem;
    width: 2.3rem;
    height: 2.3rem;
    flex-shrink: 0;
}}
.st-cq {{
       background-color: rgb(246 246 246 / 56%);
}}
.st-d1 {{
    background-color: rgb(255 0 0 / 47%);
}}
.st-d0 {{
    color: rgb(255 255 255);
}}
  
.st-d3 {{
    background-color: rgb(61 213 109 / 45%);
}}

st-emotion-cache-15hul6a {{
    display: inline-flex
;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(95 95 95 / 59%);
    border: 1px solid rgba(250, 250, 250, 0.2);
}}
    </style>
 
    """,
    unsafe_allow_html=True
)
def encode_video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

# Encode your video file
video_path = "33212-395657672_small.mp4"  # Replace with your video file path
encoded_video = encode_video_to_base64(video_path)

# Inject CSS and HTML for the video background
video_background_html = f"""
<style>
.stApp {{
    background: none; /* Remove default background */
    position: relative;
    height: 100vh;
    overflow: hidden;
}}

.stApp::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2; /* Behind everything */
    background: black; /* Optional fallback */
}}

video {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1; /* Behaves as the background */
}}
</style>

<video autoplay loop muted>
    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
    Your browser does not support the video tag.
</video>
"""

# Add the HTML to Streamlit
st.markdown(video_background_html, unsafe_allow_html=True)



st.markdown('<div class="custom-heading">Hazard Detection ⚠️  </div>', unsafe_allow_html=True)
st.markdown("""

    <style>
    .custom-heading {
        # font-size: 36px; /* Adjust font size */
        # font-weight: bold;
        # color: black; /* Adjust text color */
        
        margin-bottom: 4px; /* Space below the heading */
         
        color: white; /* Change title color to white */
        font-weight: bold; /* Make title text bold */
        text-shadow: 2px 2px 4px black; /* Add black text shadow for better readability */
        font-size: 40px; /* Increase font size */
       
    }
  

</style>
""",unsafe_allow_html=True)
 
# Function to interact with Groq API and get prediction
def process_image_with_groq(base64_image):
    # Replace with your correct Groq API key
    api_key = os.getenv("GROQ_API_KEY", "")
 
    client = Groq(api_key=api_key)
 
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Does this image contain any of the following: powerline, forest, or grassland? Please strictly reply with 'Yes' or 'No'. If the image does not contain any of these categories, respond with 'Invalid Image'."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }],
        model="llama-3.2-11b-vision-preview",
    )
    return chat_completion.choices[0].message.content
 
# Function to get the weekly weather forecast using OpenWeather API
def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
    response = requests.get(complete_url, verify=False)
    return response.json()
 
# Function to convert DMS to Decimal Degrees
def dms_to_dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if direction in ['S', 'W']:
        dd = -dd
    return dd
 
# Function to parse DMS input
def parse_dms_input(dms_input):
    dms_pattern = r"(\d+)[°](\d+)'([\d.]+)\"([NSWE])"
    match = re.match(dms_pattern, dms_input.strip())
    if match:
        degrees, minutes, seconds, direction = match.groups()
        return dms_to_dd(degrees, minutes, seconds, direction)
    else:
        return None
 
# Main application
def main():
   
 
    # Define your OpenWeather API key
    weather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
 
    # Add background image
    
 
    
    
    image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
 
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=False)  # Updated parameter
 
        base64_image = encode_image(image)
 
        # Groq API analysis
        st.write("Processing with Groq API...")
 
        result = process_image_with_groq(base64_image)
 
        # Check for specific valid categories
        if any(keyword in result.lower() for keyword in ["powerline", "forest", "grassland"]):
            st.write("Valid Image detected! Proceeding with analysis...")
 
            # Process the vegetation or powerline analysis here
            # Proceed with vegetation or powerline hazard detection logic
 
            # Take Latitude and Longitude for Weather Prediction
            latitude_input = st.text_input("Enter Latitude (e.g., 12°58'39.3\"N):")
            longitude_input = st.text_input("Enter Longitude (e.g., 77°35'40.4\"E):")
 
            if latitude_input and longitude_input:
                latitude = parse_dms_input(latitude_input)
                longitude = parse_dms_input(longitude_input)
 
                if latitude is not None and longitude is not None:
                    st.write(f"Latitude: {latitude}, Longitude: {longitude}")
                    st.write("Fetching weather data...")
 
                    # Fetch weather data from OpenWeather API
                    weather_data = get_weekly_forecast(weather_api_key, latitude, longitude)
 
                    if weather_data:
                        st.subheader("🌦️ Weather Forecast")
                        hazardous = False
                        for entry in weather_data['list']:
                            if 'rain' in entry and entry['rain'].get('3h', 0) > 10:  # Moderate to high rain threshold
                                st.warning("🌧️ IT'S HAZARDOUS due to heavy rainfall!")
                                hazardous = True
                                break
                        if not hazardous:
                            st.success("🌤️ IT'S NON-HAZARDOUS!")
        else:
            st.error("Invalid Image!!")
 
if __name__ == "__main__":
    main()