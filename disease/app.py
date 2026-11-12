import streamlit as st
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import base64
import io
import os
from groq import Groq

# Function to get base64 encoded image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
# Inject CSS with base64 background image, title styling, sidebar text color, and custom text color
background_image_path = 'image (6).jpeg'  # Update with your image path
green_eye1='OIP-removebg-preview.png'
base64_image = get_base64_encoded_image(background_image_path)
green_eye=get_base64_encoded_image(green_eye1)
st.markdown(
    f"""
<style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
    }}
    .back-arrow {{
        position: absolute;
        top: -45px;
        left: -260px;
        z-index: 1000;
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    .back-arrow img {{
        width: 45px;
        height: 45px;
    }}
    .title {{
        color: black;
        font-size: 44px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        font-family: Georgia;
    }}
    .custom-text {{
        color: white;
        font-size: 18px;
        text-align: center;
        margin-top:65px;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.2);
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: white;
    }}
    [data-testid="stSidebar"] .css-1b1w7xw, [data-testid="stSidebar"] .css-1b1w7xw input {{
        color: white;
    }}
    .st-emotion-cache-xwtqgq {{
    display: flex
;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    background-color: rgb(14 17 23 / 26%);
    border-radius: 0.5rem;
    color: rgb(250, 250, 250);
}}
.st-emotion-cache-1gwvy71 h2 {{
    font-size: 36px;
    font-weight: 600;
}}
.st-emotion-cache-qgowjl p {{
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 17px;
}}
.st-emotion-cache-lpgk4i {{
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
    background-color: rgb(43 44 54 / 38%);
    border: 1px solid rgba(250, 250, 250, 0.2);
}}
</style>
    """,
    unsafe_allow_html=True
)
# Function to encode image to base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
# Back arrow icon
back_arrow_image_path = 'AL4.png'
encoded_back_arrow = encode_image_to_base64(back_arrow_image_path)
st.markdown(f'''
<div class="back-arrow">
<a href="http://localhost:8501">
<img src="data:image/png;base64,{encoded_back_arrow}" alt="Back Arrow">
</a>
</div>
''', unsafe_allow_html=True)
@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained("Abhiram4/PlantDiseaseDetectorV2")
    model = AutoModelForImageClassification.from_pretrained("Abhiram4/PlantDiseaseDetectorV2")
    return processor, model
# Function to query Groq with LLaMA 3 for detailed disease information
def query_llama_3(disease_name):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Provide a detailed description, symptoms, causes, treatment, and suggested pesticides for {disease_name}.",
            }
        ],
        model="llama3-8b-8192",
    )
    response = chat_completion.choices[0].message.content
    return response
def handle_image(image_bytes):
    processor, model = load_model()
    image = Image.open(image_bytes).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_class = model.config.id2label[predicted_class_idx]
    # Fetch detailed information using Groq and LLaMA 3
    detailed_info = query_llama_3(predicted_class)
    return predicted_class, detailed_info
def main():
    st.markdown(f'''
    <style>
        .title {{
            color: white; /* Adjust title color */
            font-size: 50px; /* Adjust font size */
            font-weight: bold;
            text-align: center; /* Center the title */
            margin-bottom: 10px;
        }}
        
        .small-image {{
            width: 50px; /* Adjust image width */
            height: auto; /* Maintain aspect ratio */
        }}
                .image-container {{
                    text-align: center;
                    margin-right: -373px;
                    margin-top: -79px;
              }}
    </style>
    <h1 class='title'>Green EYE</h1>
    <div class="image-container">
        <img src="data:image/png;base64,{green_eye}" class="small-image" alt="Small Image">
    </div>
''', unsafe_allow_html=True)


    st.markdown("<p class='custom-text'>Upload an image of a plant leaf to identify potential diseases and receive treatment and pesticide suggestions.</p>", unsafe_allow_html=True)
    # Sidebar for image upload
    st.sidebar.header("Upload Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    # Sidebar for example images
    st.sidebar.header("Example Images")
    example_image_paths = ["spe.jpg", "might.jpg"]
    example_images = [Image.open(path) for path in example_image_paths]
    cols = st.sidebar.columns(len(example_images))
    example_image_selected = None
    for i, (col, example_image) in enumerate(zip(cols, example_images)):
        with col:
            st.image(example_image, caption=f"Example {i+1}")
            if st.button(f"Load Example {i+1}", key=f"example_{i+1}"):
                buffered = io.BytesIO()
                example_image.save(buffered, format="JPEG")
                example_image_selected = buffered.getvalue()
    image = None
    if uploaded_file is not None:
        image = uploaded_file.read()
    elif example_image_selected is not None:
        image = example_image_selected
    if image is not None:
        st.image(Image.open(io.BytesIO(image)), caption="Uploaded or Example Image")
        classification, detailed_info = handle_image(io.BytesIO(image))
        st.subheader("Results")
        st.write("Classification:", classification)
        st.write("Detailed Information:", detailed_info)
    else:
        pass
if __name__ == "__main__":
    main()

