from config import LABEL_MAPPING_PATH, DATA_FRAME_PATH
import json

from tensorflow.keras.models import load_model
import numpy as np
from config import MODEL_PATH
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pandas as pd

model = load_model(MODEL_PATH)


def preprocess_image(image_path, target_size=(128, 128)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img) / 255.0
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

    return {"predicted_classes": results, "similar_products": []}


def load_dataframe():
    df = pd.read_csv(DATA_FRAME_PATH)
    df['image_path'] = df['image_path'].apply(lambda x: f"../{x}")
    return df
