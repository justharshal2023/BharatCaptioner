import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
import matplotlib.pyplot as plt
from BharatCaptioner import identify_landmark


# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Title of the Streamlit app
st.title("BharatCaptioner")

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter image URL...")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

if url:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="Image from URL.", use_column_width=True)

# If an image is uploaded or URL is provided
if image is not None:
    landmark = identify_landmark(image)
    summary = wikipedia.summary(landmark)

    st.write("**Landmark:**", landmark)
    st.write("**Description:**", summary)

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
    st.write(f"**Translated Description in {lang}:**", translated_summary)
