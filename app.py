import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
from BharatCaptioner import identify_landmark

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Title of the Streamlit app
st.title("BharatCaptioner")

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'landmark' not in st.session_state:
    st.session_state.landmark = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'error' not in st.session_state:
    st.session_state.error = None

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter image URL...")

if uploaded_file is not None:
    st.session_state.image = Image.open(uploaded_file)
    st.image(st.session_state.image, caption="Uploaded Image.", use_column_width=True)
    st.session_state.landmark = None
    st.session_state.summary = None
    st.session_state.error = None

if url:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        st.session_state.image = Image.open(BytesIO(response.content))
        st.image(st.session_state.image, caption="Image from URL.", use_column_width=True)
        st.session_state.landmark = None
        st.session_state.summary = None
        st.session_state.error = None
    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        st.session_state.image = None
        st.session_state.landmark = None
        st.session_state.summary = None
        st.session_state.error = "Error: The provided URL is invalid or the image could not be loaded. Sometimes some image URLs don't work. We suggest you upload the downloaded image instead ;)"

# Display error message if any
if st.session_state.error:
    st.error(st.session_state.error)

# Process the image if available and no error
if st.session_state.image is not None:
    if st.session_state.landmark is None or st.session_state.summary is None:
        st.session_state.landmark = identify_landmark(st.session_state.image)
        st.session_state.summary = wikipedia.summary(st.session_state.landmark)

    st.write("**Landmark:**", st.session_state.landmark)
    st.write("**Description:**", st.session_state.summary)

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
        "Assamesse": "as",
        "Nepali": "ne",
        "Tibetan": "bo",
        "Odiya": "or",
        "Sanskrit": "sa",
        "Sindhi": "sd",
        "Urdu": "ur",
    }

    lang = st.selectbox(
        "Select language for translation:", list(language_options.keys())
    )
    target_language = language_options[lang]

    translated_summary = translator.translate(st.session_state.summary, target_language=target_language)
    st.write(f"**Translated Description in {lang}:**", translated_summary)

# Add a reset button
if st.button("Reset"):
    st.session_state.image = None
    st.session_state.landmark = None
    st.session_state.summary = None
    st.session_state.error = None
    st.experimental_rerun()
