from flask import Blueprint, jsonify
import json
from utils import load_dataframe
from config import TEST_IMAGES_PATH
import random

bp = Blueprint('images', __name__)


@bp.route('/images/all', methods=['GET'])
def get_images():
    try:
        test_images_path = TEST_IMAGES_PATH
        with open(test_images_path, 'r') as f:
            all_images = json.load(f)

        response = [{"id": image, "image_path": image,
                     "price": f"${random.uniform(50, 500):.0f}"} for image in all_images]
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/images/<image_id>', methods=['GET'])
def get_image_details(image_id):
    try:
        df = load_dataframe()
        row = df[df['id'].astype(str) == image_id]

        if row.empty:
            return jsonify({'error': f"No details found for image ID '{image_id}'"}), 404

        details = row.iloc[0][[
            'gender', 'masterCategory', 'subCategory', 'baseColour',
            'season', 'year', 'usage', 'productDisplayName'
        ]].to_dict()

        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
