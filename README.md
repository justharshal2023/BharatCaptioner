# BharatCaptioner

BharatCaptioner is an AI-powered application designed to identify Indian landmarks and provide descriptions in multiple languages. The app is deployed on Streamlit, allowing users to upload an image or provide a URL to receive a detailed description of the landmark in various Indian languages.

## Live Link

You can try out BharatCaptioner [here](https://btjk5ajztxtrzxo9unbdko.streamlit.app/).

## Features

- **Image Captioning:** Uses the BLIP model to generate captions for uploaded images. - Currently the captioning feature is put down due to limited resources availablity.
- **Landmark Identification:** Utilizes a custom-trained ResNet model to identify Indian landmarks.
- **Multilingual Descriptions:** Provides descriptions in multiple Indian languages using EasyGoogleTranslate.
- **Error Handling:** Robust error handling for invalid URLs or unsupported image formats.

## Technologies Used

- **BLIP Model:** For image captioning.
- **ResNet Model:** Custom-trained for landmark identification.
- **EasyGoogleTranslate:** For translating descriptions into various Indian languages.
- **Streamlit:** For deploying the web application.

## How It Works

1. **Image Upload/URL Input:** Users can upload an image or provide a URL.
2. **Caption Generation:** The app generates a caption for the image using the LLava model.
3. **Landmark Identification:** The image is processed to identify the landmark.
4. **Description Retrieval:** A description of the landmark is retrieved from Wikipedia.
5. **Multilingual Translation:** The description is translated into multiple Indian languages.

## Future Progress

- **Expand Landmark Database:** Include more landmarks from across India.
- **Enhance Translation Accuracy:** Improve the quality and accuracy of translations.
- **Add More Features:** Incorporate additional features such as historical information, tourist tips, etc.

## Contact

For any queries or feedback, feel free to reach out to me at [harshal8587943524@gmail.com](mailto:harshal19052003@gmail.com).

## Acknowledgments

Special thanks to [Aishala](https://ai-shala.com/) for providing the platform to convert my ideas into a real-world project.
