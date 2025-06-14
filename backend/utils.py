import os
from config import ALLOWED_EXTENSIONS, IMAGES_PATH, LABEL_MAPPING_PATH, DATA_FRAME_PATH
import json

from tensorflow.keras.models import load_model
import numpy as np
from config import MODEL_PATH
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import pandas as pd
from sklearn.metrics import mean_squared_error

model = load_model(MODEL_PATH)


def load_dataframe():
    df = pd.read_csv(DATA_FRAME_PATH)
    df['image_path'] = df['image_path'].apply(lambda x: f"../{x}")
    return df


def mse(img1, img2):
    return mean_squared_error(img1.flatten(), img2.flatten())


def find_similar_images(input_image_path, top_n=10):
    df = load_dataframe()

    input_img = preprocess_image(input_image_path)
    input_img_batch = np.expand_dims(input_img, axis=0)

    predicted_probs = model.predict(input_img_batch)
    predicted_class_index = np.argmax(predicted_probs)
    predicted_class_label = predicted_class_index

    df['label'] = df['articleType'].astype('category').cat.codes
    same_class_rows = df[df['label'] == predicted_class_label]

    mse_scores = []
    for _, row in same_class_rows.iterrows():
        img = preprocess_image(os.path.join(IMAGES_PATH, f"{row['id']}.jpg"))
        score = mse(input_img, img)
        mse_scores.append((row['id'], score))

    top_matches = sorted(mse_scores, key=lambda x: x[1])[:top_n]

    return [image_id for image_id, _ in top_matches]


def preprocess_image(image_path, target_size=(128, 128)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    return img_array


def load_class_mapping():
    try:
        with open(LABEL_MAPPING_PATH, 'r') as f:
            class_mapping = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Cannot load file {LABEL_MAPPING_PATH}: {e}")
    return class_mapping


class_mapping = load_class_mapping()


def predict_image(image_path):
    image = preprocess_image(image_path)
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)[0]

    results = [
        {"class_name": class_mapping.get(str(idx), "Unknown"), "probability": round(float(pred), 4)}
        for idx, pred in enumerate(predictions)
    ]

    results = sorted(results, key=lambda x: x["probability"], reverse=True)[:5]

    return {"predicted_classes": results}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
