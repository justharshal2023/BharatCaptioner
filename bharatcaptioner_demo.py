import os
import tensorflow as tf

class_labels = [
    "Ajanta Caves",
    "Alai Darwaza",
    "Basilica of Bom Jesus",
    "Brihadisvara Temple",
    "Charar-e-Sharief shrine",
    "Charminar",
    "Chhatrapati Shivaji Terminus",
    "Chota Imambara",
    "Ellora Caves",
    "Fatehpur Sikri",
    "Gateway of India",
    "Ghats in Varanasi",
    "Golden Temple",
    "Hampi",
    "Hawa Mahal",
    "Humayun's Tomb",
    "The India gate",
    "Iron Pillar",
    "Jageshwar",
    "Jama Masjid",
    "Jamali Kamali Tomb",
    "Khajuraho Temple",
    "Konark Sun Temple",
    "Mahabodhi Temple",
    "Meenakshi Temple",
    "Qutb Minar",
    "Qutb Minar Complex",
    "The Red Fort",
    "Sanchi",
    "The Lotus Temple",
    "The Mysore Palace",
    "The Statue of Unity",
    "The Taj Mahal",
    "Vaishno Devi Temple",
    "Victoria Memorial, Kolkata",
]

import gdown
import os

# URL with the file ID
file_id = '1-c2ly8k-mHuYo4Tjx3Kq_EU2CytAe95-'  # Replace with your file ID
url = 'https://drive.google.com/file/d/1-c2ly8k-mHuYo4Tjx3Kq_EU2CytAe95-/view?usp=drive_link'

# Output path to save the model
output = 'indian_monument_classifier35.h5'  # Replace with your model file name

# Download the file if it doesn't exist
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load your model (example using a dummy function)
def load_model():
    # Replace with code to load your actual model
    loaded_model = tf.keras.models.load_model("indian_monument_classifier35.h5")
    return "Model loaded"

loaded_model = load_model()
# Predict on a new image
from tensorflow.keras.preprocessing import image
import numpy as np

import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt


def identify_landmark(img):
    img1 = img.copy()

    # Preprocess the image
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Get predictions
    predictions = loaded_model.predict(img_array)

    # Get the index of the class with the highest probability
    predicted_class_index = np.argmax(predictions[0])

    # Map the predicted class index to the class label
    return class_labels[predicted_class_index]


def generate_landmark_path(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img1 = img.copy()

    # Preprocess the image
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    # Get predictions
    predictions = loaded_model.predict(img_array)

    # Get the index of the class with the highest probability
    predicted_class_index = np.argmax(predictions[0])

    # Map the predicted class index to the class label
    plt.imshow(img1)
    plt.axis("off")
    plt.title(class_labels[predicted_class_index])
    plt.show()
    return wikipedia.summary(class_labels[predicted_class_index])


def generate_landmark_url(img_url):
    try:
        # Download the image from the URL
        response = requests.get(img_url)
        response.raise_for_status()  # Check if the request was successful

        # Open the image
        img = Image.open(BytesIO(response.content))
        img1 = img.copy()

        # Preprocess the image
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        # Get predictions
        predictions = loaded_model.predict(img_array)

        # Get the index of the class with the highest probability
        predicted_class_index = np.argmax(predictions[0])

        # Map the predicted class index to the class label
        plt.imshow(img1)
        plt.axis("off")
        plt.title(class_labels[predicted_class_index])
        plt.show()

        return wikipedia.summary(class_labels[predicted_class_index])

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")
        return "Invalid image URL."
    except IOError as e:
        print(f"Error opening the image: {e}")
        return "Invalid image file."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing the image."
