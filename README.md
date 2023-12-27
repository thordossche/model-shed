# Model Prediction API Documentation

This document provides detailed information about the Model Prediction API, which allows for managing and utilizing machine learning models for prediction. The API is implemented using Flask and interacts with a database for storing and retrieving model data.

## API Endpoints

### 1. List Available Models

- **Endpoint**: `/models`
- **Method**: `GET`
- **Description**: Retrieves a list of all available models from the database.
- **Response**:
  - `200 OK`: Returns a JSON object containing an array of model names.

### 2. Get Model Information

- **Endpoint**: `/<model_name>`
- **Method**: `GET`
- **Description**: Provides detailed information about a specific model.
- **URL Parameters**:
  - `model_name`: The name of the model.
- **Response**:
  - `200 OK`: Returns a JSON object with the model's name, type, and features.
  - `400 Bad Request`: Error message if the model is not found.

### 3. Predict with a Model

- **Endpoint**: `/<model_name>/predict`
- **Method**: `POST`
- **Description**: Performs a prediction using the specified model.
- **URL Parameters**:
  - `model_name`: The name of the model.
- **Request Body**:
  - `features`: JSON object containing the features required for prediction.
- **Response**:
  - `200 OK`: Returns a JSON object containing the prediction results.
  - `400 Bad Request`: Error message if the model is not found or if an error occurs during prediction.

### 4. Upload a New Model

- **Endpoint**: `/<model_name>`
- **Method**: `PUT`
- **URL Parameters**:
  - `model_name`: The intended name for the new model.
- **Form Data**:
  - `model_type`: The type of the model (must be a valid type).
  - `file`: The binary file containing the model data.
- **Response**:
  - `200 OK`: Confirmation message of successful upload.
  - `400 Bad Request`: Error message if the model type is invalid or the file part is missing.

### 5. Delete a Model

- **Endpoint**: `/<model_name>`
- **Method**: `DELETE`
- **URL Parameters**:
  - `model_name`: The name of the model to be deleted.
- **Response**:
  - `200 OK`: Confirmation message of successful deletion.
