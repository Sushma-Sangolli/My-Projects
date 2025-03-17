import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import h5py
import json
import re

# Set page config to wide layout
st.set_page_config(layout="wide")

# Inject CSS directly into the script
st.markdown("""
    <style>
    body {
        background-color: #FC8EAC;
    }
    .stButton button {
        background-color: blush;
        color: white;
        border: none;
        padding: 10px 20px;
        margin: 5px;
        cursor: pointer;
    }
    .stButton button.selected {
        background-color: blush;
    }
    .main {
        background-color: #FC8EAC;
        border: 2px solid #000;
        padding: 10px;
    }
    .file-uploader-container .stFileUpload label {
        background-color: red;
        padding: 10px;
        border-radius: 5px;
    }
    .file-uploader-container .stFileUpload label:hover {
        background-color: white;
    }
    /* Style for the model buttons to be baby pink */
    .stButton button.baby-pink {
        background-color: #ffb6c1;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True
)

# Function to fix layer names
def fix_layer_names(config):
    if isinstance(config, dict):
        for key, value in config.items():
            if key == 'name' and isinstance(value, str):
                config[key] = re.sub(r'/', '_', value)
            else:
                fix_layer_names(value)
    elif isinstance(config, list):
        for item in config:
            fix_layer_names(item)

def load_model_with_fixed_names(h5_path):
    with h5py.File(h5_path, 'r') as f:
        model_config = f.attrs.get('model_config')
        if model_config:
            model_config = json.loads(model_config)
            fix_layer_names(model_config)
            model = load_model(h5_path)  # Load model directly from HDF5 file

            # Compile the model again to rebuild the optimizer state
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        else:
            raise ValueError("No model configuration found in HDF5 file.")

    return model

# Load models
model_paths = {
    "ResNet50V2": r'C:\UI\model_resnet50v2.h5',
    "InceptionV3": r'C:\UI\model_inceptionv3.h5',
    "MobileNetV3": r'C:\UI\model_mobilenetv3.h5'  # Added MobileNetV3 path
}
models = {}
for name, path in model_paths.items():
    try:
        models[name] = load_model_with_fixed_names(path)
    except Exception as e:
        st.error(f"Failed to load {name} model from {path}. Error: {e}")

def preprocess_image(image):
    image = image.convert('RGB')  # Ensures the image has 3 channels
    image = image.resize((224, 224))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize
    return image

# Update image display
st.image(image, caption='Uploaded Image', use_container_width=True)  # Replaces use_column_width

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'model' not in st.session_state:
    st.session_state.model = 'InceptionV3'

# Heading
st.markdown('<p style="background-color:#FC8EAC;color:black;font-size:50px;text-align:center;"><b>Water Bottle Image Classification With Water Level<b></p>', unsafe_allow_html=True)

# Horizontal buttons for navigation at the top
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    home_button = st.button('Home', key='home1', help="Go to Home page")
with col2:
    algorithm_button = st.button('Algorithm', key='algorithm1', help="Go to Algorithm page")
with col3:
    inceptionv3_button = st.button('InceptionV3', key='inceptionv3', help="InceptionV3 model details")
with col4:
    resnet50v2_button = st.button('ResNet50V2', key='resnet50v2', help="ResNet50V2 model details")
with col5:
    mobilenetv2_button = st.button('MobileNetV2', key='mobilenetv2', help="MobileNetV2 model details")


# Set session state based on button click
if home_button:
    st.session_state.page = 'Home'
elif algorithm_button:
    st.session_state.page = 'Algorithm'
elif inceptionv3_button:
    st.session_state.model = 'InceptionV3'
elif resnet50v2_button:
    st.session_state.model = 'ResNet50V2'
elif mobilenetv2_button:
    st.session_state.model = 'MobileNetV2'


# Highlight the selected button
if st.session_state.page == 'Home':
    st.markdown('<style>.stButton button[aria-pressed="true"] { background-color: darkblue; }</style>', unsafe_allow_html=True)
elif st.session_state.page == 'Algorithm':
    st.markdown('<style>.stButton button[aria-pressed="true"] { background-color: darkblue; }</style>', unsafe_allow_html=True)

# Display content based on the selected page
if st.session_state.page == 'Home':
    st.write("Upload Image")

    # Wrap the file uploader in a div with the new class
    st.markdown('<div class="file-uploader-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        resized_image = image.resize((200, 200))  # Resize to your desired size

        # Create three columns
        col1, col2, col3 = st.columns([1, 2, 1])

        # Display the image in the center column
        with col2:
            st.image(resized_image, caption='Uploaded Image.', width=600, use_column_width=False, output_format='JPEG')

        # Center align the image and classification button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Classify"):
                class_names = ['Full', 'Half', 'Overflow']
                for model_name, model in models.items():
                    if model:
                        image_processed = preprocess_image(image)
                        prediction = model.predict(image_processed)
                        predicted_class = class_names[np.argmax(prediction)]
                        st.markdown(f'<p style="background-color:green;color:white;font-size:18px;padding:10px;text-align:center;">{model_name} Prediction: {predicted_class}</p>', unsafe_allow_html=True)

                # Display model comparison graph with larger width and centered
                st.markdown('<p style="color:white;font-size:30px;text-align:center;">Model Comparison Graph</p>', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    comparison_image_path = "E:\\project\\model-comparison.png"
                    try:
                        with open(comparison_image_path, 'rb') as f:
                            image = Image.open(f)
                            st.image(image, caption='Model Comparison', width=800, use_column_width=False)
                    except FileNotFoundError:
                        st.error(f"Image not found at {comparison_image_path}. Please check the file path.")
                    except Exception as e:
                        st.error(f"Error loading image: {e}")


                    # Center align the image
                    st.write("")  # Empty line to push content to the centers

elif st.session_state.page == 'Algorithm':
    # Highlight the selected button
    st.markdown("""
        <style>
        .stButton button[aria-pressed="true"] {
            background-color: #ffb6c1 !important;
        }
        .stButton button.baby-pink {
            background-color: #ffb6c1;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display model-specific images based on selected model
    if st.session_state.model == 'InceptionV3':
        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Confusion Matrix</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\\project\\inception-testingmatrix.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Confusion Matrix for InceptionV3', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")

        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Loss and Accuracy Graph</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\project\INCEPTION-TRAINING.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Loss and Accuracy for InceptionV3', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")
            except Exception as e:
                st.error(f"Error loading image: {e}")

    elif st.session_state.model == 'ResNet50V2':
        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Confusion Matrix</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\\project\\resnet-testing-matrix.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Confusion Matrix for ResNet50V2', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")
            except Exception as e:
                st.error(f"Error loading image: {e}")

        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Loss and Accuracy Graph</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\\project\\resnet.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Loss and Accuracy for ResNet50V2', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")
            except Exception as e:
                st.error(f"Error loading image: {e}")

    elif st.session_state.model == 'MobileNetV2':
        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Confusion Matrix</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\\project\\mobilenettest.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Confusion Matrix for MobileNetV2', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")
            except Exception as e:
                st.error(f"Error loading image: {e}")

        st.markdown('<p style="color:white;font-size:30px;text-align:center;">Loss and Accuracy Graph</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image_path = "E:\\project\\mobilenet-loss.png"
            try:
                with open(image_path, 'rb') as f:
                    image = Image.open(f)
                    st.image(image, caption='Loss and Accuracy for MobileNetV2', use_column_width=True)
            except FileNotFoundError:
                st.error(f"Image not found at {image_path}. Please check the file path.")
            except Exception as e:
                st.error(f"Error loading image: {e}")
