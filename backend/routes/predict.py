from flask import Blueprint, request, jsonify
import os
from config import IMAGES_PATH
from utils import predict_image

bp = Blueprint('predict', __name__)


@bp.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()

    if not data or 'imagePath' not in data:
        return jsonify({'error': 'No imagePath provided'}), 400

    image_path = os.path.join(IMAGES_PATH, data['imagePath'])

    if not os.path.isfile(image_path):
        return jsonify({'error': f"Image '{data['imagePath']}' not found"}), 404

    predictions = predict_image(image_path)

    return jsonify(predictions)
