import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import wikipedia
from easygoogletranslate import EasyGoogleTranslate
from BharatCaptioner import identify_landmark
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration

# Initialize EasyGoogleTranslate
translator = EasyGoogleTranslate(source_language="en", target_language="hi", timeout=10)

# Load the Llava model and processor
model_id = "llava-hf/llava-1.5-7b-hf"

@st.cache_resource
def load_llava_model():
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True
    ).to("cuda" if torch.cuda.is_available() else "cpu")
    processor = AutoProcessor.from_pretrained(model_id)
    return model, processor

model, processor = load_llava_model()

# Title of the Streamlit app
st.title("BharatCaptioner")

# Upload image or URL
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
url = st.text_input("Or enter image URL...")

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
    
    # Use Llava model for captioning
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What are these?"},
                {"type": "image"},
            ],
        },
    ]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(prompt, image, return_tensors='pt').to("cuda" if torch.cuda.is_available() else "cpu", torch.float16)
    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    caption = processor.decode(output[0][2:], skip_special_tokens=True)
    st.write("**Caption:**", caption)

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

    translated_caption = translator.translate(caption, target_language=target_language)
    translated_summary = translator.translate(summary, target_language=target_language)
    st.write(f"**Translated Caption in {lang}:**", translated_caption)
    st.write(f"**Translated Description in {lang}:**", translated_summary)

# Add a reset button
if st.button("Reset"):
    st.experimental_rerun()
