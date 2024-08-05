import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
from BharatCaptioner import identify_landmark
import torch
# from transformers import pipeline

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# # # Load the BLIP model and processor
# pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")

# Title of the Streamlit app
st.title("BharatCaptioner")
st.write('A simple tool to identify/describe Indian Landmarks in Indic Languages')

# Add your information to the sidebar
st.sidebar.title("Developed by Harshal")
st.sidebar.write("**For the Model that i trained**: [Mail me here](harshal19052003@gmail.com)")
st.sidebar.write("**For the Code**: [My GitHub](https://github.com/justharshal2023)")
st.sidebar.write("**Connect with me here**: [My LinkedIn](https://www.linkedin.com/in/harshal-123a90250/)")

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter a valid image URL...")

image = None
error_message = None
landmark = None
summary = None
caption = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

if url:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="Image from URL.", use_column_width=True)
    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        image = None
        error_message = "Error: The provided URL is invalid or the image could not be loaded. Sometimes some image URLs don't work. We suggest you upload the downloaded image instead ;)"

# Display error message if any
if error_message:
    st.error(error_message)

# Process the image if available and no error
if image is not None:
    # Optimize image size
    image = image.resize((256, 256))  # Resize to 256x256 pixels
    # caption = pipe(image)[0]['generated_text']
    # cap_list = list(caption.split(" "))
    # if cap_list[0] == 'araffes':
    #     cap_list.pop(0)
    #     cap_list.insert(0,'people')
    # elif cap_list[0] == 'araffed':
    #     cap_list.pop(0)
    #     cap_list.insert(0,'an image of')
    # elif cap_list[0] == 'arafed':
    #     cap_list.pop(0)
    # caption = ' '.join([str(elem) for elem in cap_list])
    # st.write("**Caption:**", caption)

    landmark,prob = identify_landmark(image)
    summary = wikipedia.summary(landmark)
    st.write("**Landmark:**", landmark)
    st.write("Probability:",prob)
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
        "Assamese": "as",
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

    #translated_caption = translator.translate(caption, target_language=target_language)
    translated_summary = translator.translate(summary, target_language=target_language)
    #st.write(f"**Translated Caption in {lang}:**", translated_caption)
    st.write(f"**Translated Description in {lang}:**", translated_summary)

# Add a reset button
st.write('')
if st.button("Reset"):
    st.experimental_rerun()
