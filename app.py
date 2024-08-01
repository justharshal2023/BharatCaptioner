import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
import base64
from BharatCaptioner import identify_landmark

# Set background color
page_bg_img = '''
<style>
body {
    background-color: #f0f2f6;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the Streamlit app
st.markdown("<h1 style='text-align: center; color: #4b4b4b;'>Indian Landmark Identifier and Describer</h1>", unsafe_allow_html=True)

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="file_uploader")
url = st.text_input("Or enter image URL...", key="url_input")

image = None

# Function to add border and padding to images
def add_border(image, border_color="#4b4b4b", padding=10):
    img_with_border = Image.new('RGB', 
                                (image.width + 2*padding, image.height + 2*padding), 
                                border_color)
    img_with_border.paste(image, (padding, padding))
    return img_with_border

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(add_border(image), caption="Uploaded Image", use_column_width=True)

if url:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    st.image(add_border(image), caption="Image from URL", use_column_width=True)

# If an image is uploaded or URL is provided
if image is not None:
    landmark = identify_landmark(image)
    summary = wikipedia.summary(landmark)

    st.markdown("<h2 style='color: #4b4b4b;'>Landmark:</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 18px; color: #4b4b4b;'>{landmark}</p>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #4b4b4b;'>Description:</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 16px; color: #4b4b4b;'>{summary}</p>", unsafe_allow_html=True)

    language_options = {
        "Hindi": "hi",
        "Bengali": "bn",
        "Telugu": "te",
        "Tamil": "ta",
        "Malayalam": "ml",
        "Gujarati": "gu",
        "Marathi": "mr",
        "Kannada": "kn",
        "Punjabi": "pa",
    }

    lang = st.selectbox(
        "Select language for translation:", list(language_options.keys())
    )
    target_language = language_options[lang]

    translated_summary = translator.translate(summary, target_language=target_language)
    st.markdown(f"<h2 style='color: #4b4b4b;'>Translated Description in {lang}:</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 16px; color: #4b4b4b;'>{translated_summary}</p>", unsafe_allow_html=True)
