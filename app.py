import random
import streamlit as st
from PIL import Image
from groq import Groq
import base64
import tempfile
import cv2
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import http.client
import json
import base64
import cv2
import numpy as np
import os
import requests
from docx import Document
from docx.shared import Pt, RGBColor  # For font size and color
from io import BytesIO
from datetime import datetime, timedelta

from fpdf import FPDF
import os
import subprocess
import platform
from datetime import datetime, timedelta
 

import re

def encode_image(image_path):
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


weather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
cropped_dense="dense_green_region.jpg"


 
# Local fallback detection using OpenCV
def local_grassland_detection(image):
    image_np = np.array(image)
    hsv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
 
    # Define range for "green" in HSV
    lower_green = np.array([25, 40, 20])
    upper_green = np.array([85, 255, 255])
 
    # Create a mask
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
 
    # Calculate the percentage of green in the image
    green_percentage = (cv2.countNonZero(mask) / mask.size) * 100
    return green_percentage > 20  # Consider grassland if more than 20% is green
 
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
def get_lat_lon(api_key, lat, lon):
    """
    Fetches weather data using latitude and longitude.
 
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        api_key (str): OpenWeatherMap API key.
 
    Returns:
        dict: Weather data for the location.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data
# Function to get weekly weather forecast


# Function to fetch the 7-day weather forecast (avg temp, humidity, description)
def get_seven_day_forecast(api_key, lat, lon):
    """
    Fetches the 7-day weather forecast for a given location.
 
    Args:
        api_key (str): OpenWeatherMap API key.
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
 
    Returns:
        list: 7-day weather forecast.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
 
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
 
        weekly_forecast = []
        today = datetime.now().date()
 
        for i in range(7):
            day_date = today + timedelta(days=i)
            daily_data = [
                entry for entry in data["list"]
                if datetime.fromtimestamp(entry["dt"]).date() == day_date
            ]
 
            if daily_data:
                avg_temp = sum(entry["main"]["temp"] for entry in daily_data) / len(daily_data)
                avg_humidity = sum(entry["main"]["humidity"] for entry in daily_data) / len(daily_data)
                description = daily_data[0]["weather"][0]["description"]
 
                weekly_forecast.append({
                    "date": day_date.strftime('%A, %d %B %Y'),
                    "description": description,
                    "temp": round(avg_temp, 1),
                    "humidity": round(avg_humidity, 1),
                })
 
        return weekly_forecast
    except Exception as e:
        print("Error fetching or processing data:", e)
        return []
def get_weekly_forecast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weather_api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def calculate_vegetation_percentage(image_path: str):
    # Define HSV ranges for dark green, light green, and yellow
    # Dark Green
    dark_green_lower = np.array([35, 50, 20])  # Lower brightness and higher saturation
    dark_green_upper = np.array([85, 255, 150])
    
    # Light Green
    light_green_lower = np.array([35, 20, 150])  # Higher brightness, lower saturation
    light_green_upper = np.array([85, 100, 255])
    
    # Yellow
    yellow_lower = np.array([20, 50, 130])  # Broad S and V ranges for yellow
    yellow_upper = np.array([35, 255, 255])
    
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image not found")
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create masks for each vegetation type
    dark_green_mask = cv2.inRange(hsv, dark_green_lower, dark_green_upper)
    light_green_mask = cv2.inRange(hsv, light_green_lower, light_green_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    
    # Combine all masks
    combined_mask = cv2.bitwise_or(dark_green_mask, light_green_mask)
    combined_mask = cv2.bitwise_or(combined_mask, yellow_mask)
    
    # Calculate vegetation percentage
    total_pixels = combined_mask.size
    vegetation_pixels = cv2.countNonZero(combined_mask)
    vegetation_percentage = (vegetation_pixels / total_pixels) * 100
    print(vegetation_percentage)

    if vegetation_percentage >= 26:
        return "Forest or Dense Vegetation",combined_mask
    elif vegetation_percentage >10:
        return "Grassland",combined_mask
    else:
        return "Irrelevent",combined_mask



def get_grassland_info():
    # List of possible content for grassland
    grassland_info = [
        "The grassland is in good condition with no immediate hazards detected. Routine checks are recommended to monitor changes in vegetation density or potential risks due to seasonal variations. Ensure proper maintenance to prevent overgrowth and maintain field accessibility.",
        
        "The grassland is stable and free from any hazardous vegetation. Periodic assessments are advised to ensure that the area remains safe and suitable for its intended purpose. Seasonal changes may require adjustments in maintenance schedules.",
        
        "No threats detected in the grassland. Regular monitoring is encouraged to identify any unexpected growth or environmental changes. Maintaining clear boundaries and controlled vegetation will support long-term safety and usability.",
        
        "The grassland poses no immediate safety concerns. Ensure routine mowing and inspection to manage potential overgrowth. Consider seasonal maintenance strategies to address any changes in growth patterns."
    ]
    
    # Randomly select one of the entries
    return random.choice(grassland_info)



# Function to load the template and replace placeholders
def load_template_and_generate_grassland(status, info,today_date,maintenance_due_date):
    # Load the template (template.docx should be in the same directory)
    doc = Document("Hazard_Report.docx")
    
    # Replace the placeholders in the template
    for para in doc.paragraphs:
        if "{{status}}" in para.text:
            # Replace placeholder with status
            para.text = para.text.replace("{{status}}", status)
            
            # Apply color customization to status
            for run in para.runs:
                if status in run.text:
                    run.font.color.rgb = RGBColor(0, 100, 0)  # Set color to red
            
        if "{{report_date}}" in para.text:
            # Replace placeholder with info
            para.text = para.text.replace("{{report_date}}", today_date)
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
            
            
        if "{{maintenance_date}}" in para.text:
            # Replace placeholder with status
            para.text = para.text.replace("{{maintenance_date}}", maintenance_due_date)
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
        if "{{info}}" in para.text:
            # Replace placeholder with info
            para.text = para.text.replace("{{info}}", info)
            
            # Apply font customization to info
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
            
         
    settings = doc.settings
    protection = parse_xml(f'<w:documentProtection {nsdecls("w")} w:edit="readOnly" w:enforcement="1"/>')
    settings.element.append(protection)
    # Save the modified document to a BytesIO object
    output = BytesIO()
    doc.save(output)
    output.seek(0)  # Rewind the file pointer to the beginning
    
    return output
  


# Function to load the template and replace placeholders
def load_template_and_generate(status, info,today_date,maintenance_due_date):
    # Load the template (template.docx should be in the same directory)
    doc = Document("Hazard_Report.docx")
    
    # Replace the placeholders in the template
    for para in doc.paragraphs:
        if "{{status}}" in para.text:
            # Replace placeholder with status
            para.text = para.text.replace("{{status}}", status)
            
            # Apply color customization to status
            for run in para.runs:
                if status in run.text:
                    run.font.color.rgb = RGBColor(255, 0, 0)  # Set color to red
            
        if "{{report_date}}" in para.text:
            # Replace placeholder with info
            para.text = para.text.replace("{{report_date}}", today_date)
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
            
            
        if "{{maintenance_date}}" in para.text:
            # Replace placeholder with status
            para.text = para.text.replace("{{maintenance_date}}", maintenance_due_date)
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
        if "{{info}}" in para.text:
            # Replace placeholder with info
            para.text = para.text.replace("{{info}}", info)
            
            # Apply font customization to info
            for run in para.runs:
                run.font.size = Pt(10)  # Set font size to 10 pt
                run.font.bold = False  # Remove bold formatting
            
         
    settings = doc.settings
    protection = parse_xml(f'<w:documentProtection {nsdecls("w")} w:edit="readOnly" w:enforcement="1"/>')
    settings.element.append(protection)
    # Save the modified document to a BytesIO object
    output = BytesIO()
    doc.save(output)
    output.seek(0)  # Rewind the file pointer to the beginning
    
    return output
def display_normal_image(base64_image):
    image_data = base64.b64decode(base64_image)
    np_image = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    
    # Convert the image to RGB (OpenCV loads images in BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert the image to grayscale for thresholding
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to create binary masks for tree and powerlines
    # We assume that trees are darker (below threshold) and powerlines are detected by edge detection
    
    # Create tree mask: Dark regions (trees)
    _, tree_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    # Detect powerlines using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)  # Experiment with thresholds for better results
    
    # Dilation to make edges thicker (helpful for powerlines)
    dilated_edges = cv2.dilate(edges, None, iterations=1)
    
    # Apply morphological closing to remove small gaps and noise
    kernel = np.ones((5, 5), np.uint8)
    dilated_edges = cv2.morphologyEx(dilated_edges, cv2.MORPH_CLOSE, kernel)
    
    # Create a mask for powerlines (binary mask for the detected powerlines)
    _, powerline_mask = cv2.threshold(dilated_edges, 50, 255, cv2.THRESH_BINARY)
    
    # Display the tree and powerline masks in separate subplots with axes
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    
    # Tree mask (Left subplot)
    axes[0].imshow(tree_mask, cmap='gray')
    axes[0].set_title('Tree Mask')
    axes[0].set_xlabel('X-axis')
    axes[0].set_ylabel('Y-axis')
    axes[0].axis('on')  # Show axes
    
    # Powerline mask (Right subplot)
    axes[1].imshow(powerline_mask, cmap='gray')
    axes[1].set_title('Powerline Mask')
    axes[1].set_xlabel('X-axis')
    axes[1].set_ylabel('Y-axis')
    axes[1].axis('on')  # Show axes
    
    # Show the plot in Streamlit using st.pyplot
    st.pyplot(fig)
    

def detect_and_crop_dense_green_region(base64_image):
    # Decode the base64 image
    try:
        image_data = base64.b64decode(base64_image)
        np_image = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
        
        if image is None:
            st.error("Failed to decode the image.")
            return None
        print("Image successfully loaded")
    except Exception as e:
        st.error(f"Error decoding image: {str(e)}")
        return None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize the image for faster processing
    resized_image = cv2.resize(image_rgb, (400, 400))
    print(f"Resized image shape: {resized_image.shape}")

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2HSV)

    # Reshape the image for clustering
    pixel_values = hsv_image.reshape((-1, 3)).astype(np.float32)

    # Apply KMeans clustering
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(pixel_values)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Identify the green cluster
    green_cluster_index = np.argmin([np.abs(center[0] - 60) for center in centers])
    mask = (labels == green_cluster_index).reshape(hsv_image.shape[:2])

    # Create and refine mask
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_OPEN, kernel)

    # Find contours from the cleaned binary mask
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        st.warning("No green regions detected.")
        return None

    dense_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        region = mask_cleaned[y:y+h, x:x+w]
        green_density = np.sum(region) / (w * h)
        if green_density > 0.5:  # Adaptive threshold
            dense_contours.append(contour)

    if not dense_contours:
        st.warning("No dense green regions detected.")
        return None

    # Find and crop the largest dense green region
    largest_dense_contour = max(dense_contours, key=cv2.contourArea)

    # Get bounding box for the largest dense green region
    x, y, w, h = cv2.boundingRect(largest_dense_contour)

    print(f"Bounding box: x={x}, y={y}, w={w}, h={h}")

    # Scale back to the original image size
    original_height, original_width = image.shape[:2]
    scale_x = original_width / 400
    scale_y = original_height / 400

    x = int(x * scale_x)
    y = int(y * scale_y)
    w = int(w * scale_x)
    h = int(h * scale_y)

    print(f"Scaled bounding box: x={x}, y={y}, w={w}, h={h}")

    # Crop the largest dense green region
    largest_crop = image[y:y+h, x:x+w]

    # Ensure the crop is valid
    if largest_crop.size == 0:
        st.warning("The cropped image is empty.")
        return None

    # Ensure directory exists
    cropped_dense_path = 'dense_green_region.jpg'
    if os.path.exists(cropped_dense_path):
        os.remove(cropped_dense_path)

    # Save the cropped image
    success = cv2.imwrite(cropped_dense_path, largest_crop)
    if not success:
        st.error("Failed to save the cropped image.")
        return None
    print("Cropped image saved successfully")

    # Plot results
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image with Bounding Box')
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(largest_crop, cv2.COLOR_BGR2RGB))
    plt.title('Cropped Dense Green Region')
    st.pyplot(plt)

    return cropped_dense_path



def get_plant_name(image_path):
       
    conn = http.client.HTTPSConnection("plant.id")
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    payload = json.dumps({
    "images": [
        f"data:image/jpg;base64,{base64_image}"
    ],
    "similar_images": True
    })
    headers = {
    'Api-Key': 'UlSwpQB3QsUaXwSeVEkZXMDh0QzYPfBjLxPF3kxZR9yM8UaTrA',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/v3/identification", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decoded_data = json.loads(data.decode('utf-8'))
    suggestions = decoded_data["result"]["classification"]["suggestions"]
    pn = suggestions[0]["name"] 
    return pn


def assess_powerline_outage_risk(image,plant_name):
        prompt = f"""
Study the provided high-resolution image and deliver a comprehensive Powerline Outage Risk Assessment for {plant_name}. Base your assessment on the specific characteristics of the plant and its proximity to powerlines:

CRITICAL ANALYSIS PARAMETERS:
1. Plant Characteristics Risk Evaluation:
   - Specific growth patterns of {plant_name}
   - Typical mature height
   - Branch flexibility and brittleness
   - Root system characteristics
   - Seasonal growth behavior

2. Powerline Proximity Risk Factors:
   - Distance from powerlines
   - Potential for branch contact
   - Likelihood of vegetation-caused electrical interference
   - Seasonal impact on plant structure

3. Outage Risk Determination:
   - Probability of direct line contact
   - Potential for:
     * Branch breakage
     * Electrical arcing
     * Vegetation-induced short circuits
   - Seasonal vulnerability assessment

RISK CLASSIFICATION CRITERIA:
- Extreme Risk: High probability of power interruption
- Significant Risk: Moderate potential for outages
- Moderate Risk: Potential for intermittent interference
- Low Risk: Minimal threat to power infrastructure

Provide a definitive risk assessment with specific outage potential for {plant_name} near powerlines. 

RESPONSE FORMAT:
1. Risk Level: [Extreme/Significant/Moderate/Low]
2. Key Risk Factors: [Detailed list of specific risks]
3. Mitigation Recommendations: [Specific actions to reduce risk]

As an AI model, I don't have the capability to visualize an image, and I don't have access to any image of the plant Pieces. However, I can provide general guidelines for a Powerline Outage Risk Assessment, which can be universally applied.Dont tell these kind of lines in response, just give the response in the above response format given.
"""


        api_key = os.getenv("GROQ_API_KEY", "")
        client = Groq(api_key=api_key)

        # Prompt to detect the presence of grassland or small vegetation
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-90b-vision-preview",
        )
        return chat_completion.choices[0].message.content

def generate_report(dense_vegetation, hazardous_weather, weather_details):
    report = ""
    if dense_vegetation:
        report += "⚠️ Hazardous dense vegetation detected! High vegetation or trees found.\n"
    else:
        report += "✅ No hazardous dense vegetation detected.\n"
 
    if hazardous_weather:
        report += "🌧️ Hazardous weather detected due to heavy rainfall!\n"
    else:
        report += "🌤️ Weather is non-hazardous.\n"
 
    report += "\n### Weather Forecast Details:\n"
    
 
    return report


def sanitize_text(text):
    """Sanitize text to be compatible with latin-1 encoding."""
    return text.encode("latin-1", errors="replace").decode("latin-1")

def generate_pdf_report(forecast_data, location, report_type="7-day", report=None, output_file="weather_report.pdf"):
    """
    Generates a PDF report for the weather forecast and includes a hazardous/non-hazardous report section.

    Args:
        forecast_data (list): List of daily weather forecast data.
        location (str): Name of the location.
        report_type (str): Type of the report (7-day or 5-day).
        report (str): Hazardous or non-hazardous information.
        output_file (str): The name of the PDF file to save.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    # Title Area
    pdf.set_fill_color(0, 102, 0)  # Dark green background
    pdf.rect(0, 0, pdf.w, 20, 'F')  # Header rectangle
    pdf.set_text_color(255, 255, 255)  # White text
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Weather Forecast for {sanitize_text(location)}", ln=True, align="C")
    pdf.ln(10)

    # Hazardous/Non-Hazardous Section
    pdf.set_text_color(0, 0, 0)  # Reset text color to black
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "Hazard Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    if report:
        pdf.multi_cell(0, 10, sanitize_text(report))  # Include the report about hazardous/non-hazardous information
    else:
        pdf.multi_cell(0, 10, "No additional information about hazards is available.")
    pdf.ln(5)

    # Add Forecast Table
    pdf.set_font("Arial", size=10)
    headers = ["Date", "Description", "Temperature (°C)", "Humidity (%)"] if report_type == "7-day" else \
              ["Date", "Max Temp (°C)", "Min Temp (°C)", "Description", "Wind Speed (m/s)"]
    col_widths = [60, 60, 40, 30] if report_type == "7-day" else [40, 30, 30, 50, 30]

    # Header Row
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()

    # Add forecast data rows
    for day in forecast_data:
        if report_type == "7-day":
            pdf.cell(col_widths[0], 8, sanitize_text(day["date"]), border=1, align="C")
            pdf.cell(col_widths[1], 8, sanitize_text(day["description"].capitalize()), border=1, align="C")
            pdf.cell(col_widths[2], 8, str(day["temp"]), border=1, align="C")
            pdf.cell(col_widths[3], 8, str(day["humidity"]), border=1, align="C")
        else:
            pdf.cell(col_widths[0], 8, sanitize_text(day["date"]), border=1, align="C")
            pdf.cell(col_widths[1], 8, str(day["temp_max"]), border=1, align="C")
            pdf.cell(col_widths[2], 8, str(day["temp_min"]), border=1, align="C")
            pdf.cell(col_widths[3], 8, sanitize_text(day["description"].capitalize()), border=1, align="L")
            pdf.cell(col_widths[4], 8, f"{day['wind_speed']} m/s", border=1, align="C")
        pdf.ln()

    # Footer with current date
    pdf.set_y(-15)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%d %b %Y')}", 0, 0, 'C')

    # Save the PDF
    pdf.output(output_file)

    full_path = os.path.abspath(output_file)
    print(f"Report generated and saved at: {full_path}")

    # Open the PDF automatically (platform-dependent)
    if platform.system() == "Darwin":
        subprocess.run(["open", full_path])
    elif platform.system() == "Windows":
        os.startfile(full_path)
    else:
        subprocess.run(["xdg-open", full_path])

    return full_path








# Step 1: Radio button to choose the type of image
image_type = st.radio(
    "Select the type of image you want to upload:",
    ("Satellite Image", "Normal Image")
)

# Step 2: File uploader based on the selected image type
uploaded_file = st.file_uploader(
    f"Upload a {image_type.lower()} file:", type=["jpg", "jpeg", "png"]
)

# Step 3: Process uploaded file based on the type
if uploaded_file is not None:
    try:
        # Use tempfile to save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Open the image using PIL
        image = Image.open(temp_file_path)
        st.image(image, caption=f"Uploaded {image_type}", use_column_width=False)
        st.write(f"{image_type} uploaded successfully!")

        # Step 4: Encode image and perform specific steps
        base64_image = encode_image(temp_file_path)

        if image_type == "Satellite Image":
            st.subheader("Processing Satellite Image...")
            st.write("Running local vegetation analysis...")
            dense_vegetation = local_grassland_detection(image)
    
            if dense_vegetation:
                st.warning("HAZARDOUS: Dense trees or high vegetation detected!")
                # Take Latitude and Longitude for Weather Prediction
                latitude_input = st.text_input("Enter Latitude (e.g., 12°58'39.3\"N):")
                longitude_input = st.text_input("Enter Longitude (e.g., 77°35'40.4\"E):")
    
                if latitude_input and longitude_input:
                    latitude = parse_dms_input(latitude_input)
                    longitude = parse_dms_input(longitude_input)
    
                    if latitude is not None and longitude is not None:
                        st.write(f"Latitude: {latitude}, Longitude: {longitude}")
                        st.write("Fetching weather data...")
    
                        weather_data = get_weekly_forecast(weather_api_key, latitude, longitude)
    
                        if weather_data:
                            st.subheader("🌦️ Weather Forecast")
                            hazardous = False
                            weather_details = []
                            for entry in weather_data['list']:
                                weather_details.append(entry)
                        
                               
                                if any(desc in item['description'].lower() for item in entry.get('weather', []) for desc in ["rain"]):  # Moderate to high rain threshold
                                    st.warning("🌧️ IT'S HAZARDOUS due to heavy rainfall!")
                                    st.warning("Diffrent Weather Conditions may cause the change in results.")
                                    hazardous = True
                                    break
                            if not hazardous:
                                st.success("🌤️ According to the Current Weather Condition, IT'S NON-HAZARDOUS!")
                                st.success("Diffrent Weather Conditions may cause the change in results.")
    
                            # Generate report button
                            if st.button("Generate Report"):
                                report = generate_report(dense_vegetation, hazardous, weather_details)
                                if latitude and longitude:  # Check if latitude and longitude are not empty
                                        # Fetch the weather data for the provided latitude and longitude
                                        weather_data = get_lat_lon(weather_api_key, latitude, longitude)
                                        if weather_data:
                                            city_name = weather_data.get("name", "Unknown Location")
                            
                                            
                                            forecast_data = get_seven_day_forecast(weather_api_key, latitude, longitude)
                                            report_type = "7-day"
                                            
                            
                                            if forecast_data:
                                                report_path = generate_pdf_report(forecast_data, city_name, report_type,report)
                            
                                                # Display success message with download link
                                                if os.path.exists(report_path):
                                                    with open(report_path, "rb") as file:
                                                        st.download_button(
                                                            label="Download Weather Report",
                                                            data=file,
                                                            file_name=os.path.basename(report_path),
                                                            mime="application/pdf",
                                                        )


                                
            else:
                st.success("No hazardous dense vegetation detected.")

        elif image_type == "Normal Image":
            # display_normal_image(base64_image)

            grassland_info,combined_mask = calculate_vegetation_percentage(temp_file_path)
            st.write(grassland_info)
            if grassland_info is "Grassland":
                display_normal_image(base64_image)
                st.success("✅ Non-Hazardous: Vegetation levels near power lines are within safe limits.")
                today_date = datetime.now().strftime("%B %d, %Y")
                maintenance_due_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")

                status = "No HAZARDOUS vegetation detected: The area is clear of any immediate risks."
                info = get_grassland_info()
                if st.button("Generate Report"):
    # Generate the report
                    file = load_template_and_generate_grassland(status, info,today_date,maintenance_due_date)
    
    # Provide download link for the generated report
                    st.download_button(
                        label="Download Hazard Report",
                        data=file,
                        file_name="hazard_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                    st.success("Normal image processed successfully!")

            elif grassland_info is "Forest or Dense Vegetation":
                display_normal_image(base64_image)
                cropped_image_path = detect_and_crop_dense_green_region(base64_image)
                if cropped_image_path:
                        # Get plant name
                        plant_name = get_plant_name(cropped_image_path)
                         
                        st.markdown(f"""
                            <style>
                                .custom-heading {{
                                    margin-bottom: 4px;
                                    text-align:center;
                                    color: white; /* Change title color to white */
                                    font-weight: bold; /* Make title text bold */
                                    text-shadow: 2px 2px 4px black; /* Add black text shadow for better readability */
                                    font-size: 32px; /* Increase font size */
                                }}
                            </style>
                            <div class="custom-heading">Identified Plant :-{plant_name}</div>
                        """, unsafe_allow_html=True)
                        infom=assess_powerline_outage_risk(base64_image,plant_name)
                        st.warning("HAZARDOUS: Dense trees or high vegetation detected! ")
                        ##st.write(infom)
                        today_date = datetime.now().strftime("%B %d, %Y")
                        maintenance_due_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")

                        status = "⚠️ Hazardous Alert: High vegetation detected near power lines"
                        info =infom
                        if st.button("Generate Report"):
                            file = load_template_and_generate(status, info,today_date,maintenance_due_date)
                            st.download_button(
                                label="Download Hazard Report",
                                data=file,
                                file_name="hazard_report.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

                            st.success("Normal image processed successfully!")


            
            elif grassland_info is "Irrelevent":
                st.warning("Please upload a relevent image containing powerlines with vegetation")
            
    
                
                        
                

        

    except Exception as e:
        st.error(f"Error loading or processing the image: {e}")

    finally:
        # Clean up the temporary file
        if 'temp_file_path' in locals():
            import os
            os.remove(temp_file_path)
else:
    st.info(f"Please upload a {image_type.lower()} to proceed.")