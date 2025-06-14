import os

MODEL_PATH = 'best_model.keras'
IMAGES_PATH = '../images/'
STYLES_PATH = '../styles.csv'
TEST_IMAGES_PATH = './test_images.json'
LABEL_MAPPING_PATH = './label_mapping.json'
DATA_FRAME_PATH = 'dataframe.csv'
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(IMAGES_PATH):
    raise FileNotFoundError(f"Directory {IMAGES_PATH} does not exist.")
