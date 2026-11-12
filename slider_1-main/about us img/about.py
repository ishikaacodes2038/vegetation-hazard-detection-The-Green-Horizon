import streamlit as st
import base64
 
# Setting up the page configuration
st.set_page_config(
    page_title="About Us - Vegetation Hazard Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# Function to encode the image to base64
def get_base64_of_bin_file(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()
 
# Encoding the background image
bg_image_path = r"C:\Users\SAKVINAY\Desktop\vegetation front\slider_1-main\about us img\bg.jpg"  # Replace with your local image filename
try:
    bg_image_base64 = get_base64_of_bin_file(bg_image_path)
    bg_image_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """
    st.markdown(bg_image_style, unsafe_allow_html=True)
except FileNotFoundError:
    st.error("Background image not found! Please ensure 'bg.jpg' is in the script's directory.")
 
# Adding custom CSS for hover effects and animations
st.markdown("""
    <style>
        /* Page title and subtitle styling with animation */
        .title {
            text-align: center;
            color: #54ab7a;
            font-size: 3em;
            font-weight: bold;
            margin-top: 20px;
            animation: fadeIn 2s ease-in-out;
        }
        .subtitle {
            text-align: center;
            color: #54ab7a;
            font-size: 1.5em;
            margin-bottom: 40px;
            animation: slideIn 2s ease-in-out;
        }
 
        /* About section styling with hover effect */
        .about-section {
            background-color: rgba(244, 244, 244, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 40px;
            transition: transform 0.3s ease;
        }
        .about-section:hover {
            transform: scale(1.03);
        }
 
        /* Team member styling with hover effect */
        .team-card {
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .team-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .team-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #54ab7a;
            margin-top: 10px;
        }
        .team-role {
            color: #54ab7a;
            font-size: 1em;
            margin-bottom: 20px;
        }
 
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)
 
# Header Section
st.markdown('<div class="title">About Us</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Innovation at the Intersection of Technology and Nature</div>', unsafe_allow_html=True)
 
# About Project Section
st.markdown("""
<div class="about-section">
    <h3>About Our Project</h3>
    <p>
        Welcome to our "Vegetation Hazard Detection and Management" initiative!
        We are a passionate team of technologists participating in a GenAI Hackathon, aiming to revolutionize
        vegetation management using cutting-edge artificial intelligence.
    </p>
    <p>
        Our solution leverages machine learning and advanced analytics to detect potential vegetation hazards
        such as overgrown trees near power lines, invasive plant species, and other ecological concerns.
        By providing actionable insights, we empower stakeholders to take proactive measures to
        ensure safety, sustainability, and environmental harmony.
    </p>
</div>
""", unsafe_allow_html=True)
 
# Team Section
st.markdown('<div class="title">Meet Our Team</div>', unsafe_allow_html=True)
 
# Team Data
team_data = [
    {"name": "Ishika Mittal", "role": "Project Lead", "photo": "ishikam.jpg"},
    {"name": "Sakshi Supe", "role": "AI Developer", "photo": "sakshi.jpg"},
    {"name": "Sonal Singh Suppahia", "role": "AI Developer", "photo": "Sonal.jpg"},
    {"name": "Madhushree", "role": "AI Developer", "photo": "madhu.jpg"},
    {"name": "Aradhana  Surankar", "role": "AI Developer", "photo": "aradhana.jpg"},
]
 
# Display Team Members with Hover Effects
col1, col2, col3 = st.columns(3)
 
with col1:
    for i in [0, 3]:  # Show 1st and 4th team member in column 1
        st.markdown("<div class='team-card'>", unsafe_allow_html=True)
        st.image(team_data[i]['photo'], caption=None, width=150)
        st.markdown(f"<div class='team-name'>{team_data[i]['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='team-role'>{team_data[i]['role']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
 
with col2:
    for i in [1, 4]:  # Show 2nd and 5th team member in column 2
        st.markdown("<div class='team-card'>", unsafe_allow_html=True)
        st.image(team_data[i]['photo'], caption=None, width=150)
        st.markdown(f"<div class='team-name'>{team_data[i]['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='team-role'>{team_data[i]['role']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
 
with col3:
    for i in [2]:  # Show 3rd team member in column 3
        st.markdown("<div class='team-card'>", unsafe_allow_html=True)
        st.image(team_data[i]['photo'], caption=None, width=150)
        st.markdown(f"<div class='team-name'>{team_data[i]['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='team-role'>{team_data[i]['role']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
 
# Footer Section
st.markdown("""
<hr>
<div style="text-align: center;
            color: rgb(255 255 255">
    <p>© 2024 Vegetation Hazard Detection & Management Team | Powered by GenAI Hackathon 2.0</p>
</div>
""", unsafe_allow_html=True)
 