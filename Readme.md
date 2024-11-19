# Personal Color Analysis Web Application

This is a Flask-based web application that allows users to upload an image and receive a detailed personal color analysis based on the colors of their hair, skin, and eyes. The analysis determines the user's personal color type out of 20 defined types, as well as overall color classification.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [How It Works](#how-it-works)
- [License](#license)

## Features
- **Image Upload**: Users can upload their image to analyze their personal color type.
- **Color Analysis**: The app extracts and processes color data from the hair, skin, and eyes.
- **20 Types of Personal Color**: The app determines the user's type from 20 defined personal color types.
- **Detailed Result Page**: Displays analysis results including hair, skin, and eye types along with an overall personal color type.

## Installation
To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ImageProcessing-team12/personalcolor_model.git
    cd personalcolor_model
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask app**:
    ```bash
    python main.py
    ```

6. **Access the app in your browser**:
   Navigate to `http://127.0.0.1:5000/` to use the web application.

## Usage
1. Open your web browser and go to `http://127.0.0.1:5000/`.
2. Upload an image file by clicking the "Select Image" button.
3. Click the "Analyze" button to process the image.
4. View the detailed analysis results, including the hair, skin, and eye color types, as well as the overall personal color type.

## File Structure
```
personalcolor_model/
│
├── static/
│   └── uploads/                 # Uploaded images are stored here
│   └── styles.css               # Custom styling for the web application
│
├── templates/
│   ├── index.html               # Main page template for image upload
│   └── result.html              # Result page template for analysis output
│
├── main.py                      # Main Flask application script
├── extract_features.py          # Utility for extracting features from the image
├── model_utils.py               # Utility functions for model operations
├── personal_color_diagnosis.py  # Color analysis logic and diagnosis functions
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation (this file)
```

## How It Works
1. **Image Upload**: Users can upload an image file on the main page (`index.html`).
2. **Feature Extraction**: The application uses image processing techniques to identify and extract the color properties of the hair, skin, and eyes from the uploaded image.
3. **Color Conversion and Analysis**:
    - Converts the color data to HSV format for detailed analysis.
    - Determines whether the color is clear or dull.
    - Calculates an overall color type based on average hue, lightness, saturation, and clarity.
4. **Result Display**: The results are shown on the `result.html` page, including the hair, skin, and eye types, and the overall personal color type.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
