import traceback
import pandas as pd
from flask import Flask, request, jsonify
from predictor_utils import ModelType, load_predictor
from database_layer import DatabaseLayer

app = Flask(__name__)

@app.route('/models', methods=['GET'])
def models():
    models = DatabaseLayer().get_models()
    return jsonify({ 'models': models })


@app.route('/<model_name>', methods=['GET'])
def model_info(model_name):
    model_type, model_data = DatabaseLayer().get_model(model_name)
    if model_type is None or model_data is None:
        return jsonify({'error': f"Model '{model_name}' not found."}), 400

    predictor = load_predictor(model_type, model_data)
    features = predictor.features()
   
    return jsonify({
        'name': model_name,
        'type': model_type.model_name,
        'features': features
    })
    

@app.route('/<model_name>/predict', methods=['POST'])
def predict(model_name):
    model_type, model_data = DatabaseLayer().get_model(model_name)
    if model_type is None or model_data is None:
        return jsonify({'error': f"Model '{model_name}' not found."}), 400

    predictor = load_predictor(model_type, model_data)
    features = pd.DataFrame(request.json['features'])
    try:
        predictions = predictor.predict(features)
        return jsonify({'predictions': list(predictions)}), 200
    except Exception as _:
        return jsonify({'error': traceback.format_exc()}), 400


@app.route('/<model_name>', methods=['PUT'])
def upload_model(model_name):
    model_type = request.form.get('model_type')

    if model_type not in [e.model_name for e in ModelType]:
        return jsonify({'error': 'Invalid model type', 'valid_types': [e.model_name for e in ModelType]}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    DatabaseLayer().add_model(model_name, ModelType.from_name(model_type), request.files['file'].read())

    return jsonify({'message': f"'{model_name}' uploaded successfully"}), 200

@app.route('/<model_name>', methods=['DELETE'])
def delete_model(model_name):
    DatabaseLayer().delete_model(model_name)
    return jsonify({'message': f"'{model_name}' was successfully deleted"}), 200


@app.errorhandler(ValueError)
def value_error_handler(value_error: ValueError):
    return f'{value_error}\n', 400

if __name__ == '__main__':
    app.run(debug=True)

