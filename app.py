import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
from bharatcaptioner_demo import identify_landmark

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Title of the Streamlit app
st.title("Indian Landmark Identifier and Describer")

# Initialize session state
if 'image' not in st.session_state:
    st.session_state.image = None
if 'landmark' not in st.session_state:
    st.session_state.landmark = None
if 'summary' not in st.session_state:
    st.session_state.summary = None

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter image URL...")

if uploaded_file is not None:
    st.session_state.image = Image.open(uploaded_file)
    st.image(st.session_state.image, caption="Uploaded Image.", use_column_width=True)
    st.session_state.landmark = None
    st.session_state.summary = None

if url:
    response = requests.get(url)
    st.session_state.image = Image.open(BytesIO(response.content))
    st.image(st.session_state.image, caption="Image from URL.", use_column_width=True)
    st.session_state.landmark = None
    st.session_state.summary = None

# Process the image if available
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
        "Assamesse":"as",
        "Nepali":"ne",
        "Tibetan":"bo",
        "Odiya":"or",
        "Sanskrit":"sa",
        "Sindhi":"sd",
        "Urdu":"ur",
    }

    lang = st.selectbox(
        "Select language for translation:", list(language_options.keys())
    )
    target_language = language_options[lang]

    translated_summary = translator.translate(st.session_state.summary, target_language=target_language)
    st.write(f"**Translated Description in {lang}:**", translated_summary)
