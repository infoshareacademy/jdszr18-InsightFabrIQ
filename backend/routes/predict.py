from flask import Blueprint, request, jsonify, send_from_directory
import os
from config import IMAGES_PATH, UPLOAD_FOLDER
from utils import allowed_file, find_similar_images, predict_image
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('predict', __name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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


@bp.route('/predict/similar', methods=['POST'])
def get_similar_images():
    try:
        data = request.get_json()

        if not data or 'imagePath' not in data:
            return jsonify({'error': 'No image_path provided'}), 400

        image_path = os.path.join(IMAGES_PATH, data['imagePath'])
        similar_images = find_similar_images(image_path)

        return jsonify({'similar_images_ids': similar_images})
    except Exception as e:

        return jsonify({'error': str(e)}), 500


@bp.route('/predict/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)

        try:
            predictions = predict_image(file_path)
            similar_images = find_similar_images(file_path)

            return jsonify({
                'predictions': predictions,
                'similar_images_ids': similar_images,
                'image_id': unique_filename
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploaded_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404
