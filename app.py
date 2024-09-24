import os
import json
import streamlit as st
from PIL import Image, UnidentifiedImageError, ExifTags
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
from BharatCaptioner import identify_landmark
from groq import Groq
import hashlib

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Load configuration for Groq API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Title of the Streamlit app
st.title("BharatCaptioner with Conversational Chatbot")
st.write(
    "A tool to identify/describe Indian Landmarks in Indic Languages and chat about the image."
)

# Sidebar details
st.sidebar.title("Developed by Harshal and Harsh Pandey")
st.sidebar.write(
    "**For the Model that I trained**: [Mail me here](mailto:harshal19052003@gmail.com)"
)
st.sidebar.write(
    "**For the Code**: [GitHub Repo](https://github.com/justharshal2023/BharatCaptioner)"
)
st.sidebar.write(
    "**Connect with me**: [LinkedIn](https://www.linkedin.com/in/harshal-123a90250/)"
)

# Image upload or URL input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter a valid image URL...")

image = None
error_message = None
landmark = None
summary = None
caption = None


# Function to correct image orientation
def correct_image_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = img._getexif()
        if exif is not None:
            orientation = exif[orientation]
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img


# Function to get a unique hash for the image
def get_image_hash(image):
    img_bytes = image.tobytes()
    return hashlib.md5(img_bytes).hexdigest()


# Check if new image or URL is uploaded and reset the chat history
def reset_chat_if_new_image():
    if "last_uploaded_hash" not in st.session_state:
        st.session_state["last_uploaded_hash"] = None

    # Process the new image or URL
    if uploaded_file:
        image = Image.open(uploaded_file)
        image = correct_image_orientation(image)
        new_image_hash = get_image_hash(image)
    elif url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image = correct_image_orientation(image)
            new_image_hash = get_image_hash(image)
        except (requests.exceptions.RequestException, UnidentifiedImageError):
            image = None
            new_image_hash = None
            error_message = (
                "Error: The provided URL is invalid or the image could not be loaded."
            )
            st.error(error_message)
    else:
        image = None
        new_image_hash = None

    # If the image is new, reset the chat and session state
    if new_image_hash and new_image_hash != st.session_state["last_uploaded_hash"]:
        st.session_state.clear()
        st.session_state["last_uploaded_hash"] = new_image_hash
        st.experimental_rerun()

    return image


# Call the reset function to check for new images or URL
image = reset_chat_if_new_image()

# If an image is provided
if image is not None:
    # Resize image for processing
    image = image.resize((256, 256))

    # Identify the landmark using BharatCaptioner
    landmark, prob = identify_landmark(image)
    summary = wikipedia.summary(landmark, sentences=3)  # Shortened summary
    st.write(f"**Landmark Identified:** {landmark} (Confidence: {prob:.2f})")

    # Display image and landmark name in the sidebar
    with st.sidebar:
        st.image(image, caption="Current Image", use_column_width=True)
        st.write(f"**Landmark:** {landmark}")

    # Chatbot functionality
    st.write("### Chat with the Chatbot about the Image")
    caption = f"The landmark in the image is {landmark}. {summary}"

    # Initialize chat history in session state if not present
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Chatbot introduction message with bold text for landmark and question
    if not st.session_state.get("chatbot_started"):
        chatbot_intro = f"Hello! I see the image is of **{landmark}**. {summary} **Would you like to know more** about this landmark?"
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": chatbot_intro}
        )
        st.session_state["chatbot_started"] = True

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_prompt = st.chat_input("Ask the Chatbot about the image...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Send the user's message to the LLaMA chatbot
        messages = [
            {
                "role": "system",
                "content": "You are a helpful image conversational assistant. "
                + f"The caption of the image is: {caption}",
            },
            *st.session_state.chat_history,
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", messages=messages
        )

        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_response}
        )

        # Display chatbot response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
