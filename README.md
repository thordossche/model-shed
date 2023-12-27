# Model-Shed
Model-Shed is a tool designed for the management and utilization of machine learning models. It provides a structured and organized environment akin to a shed, where models are stored, managed, and deployed with ease.

## Purpose
Model-Shed offers a centralized solution for storing and accessing machine learning models, enabling their use across multiple projects. By facilitating model integration through API calls, it eliminates the need for heavy ML libraries in each project, reducing dependency overhead. This approach also keeps code repositories cleaner by not storing the models directly in them, making it ideal for projects that require only predictions.

## API Endpoints

- #### [`GET`] `/models`
    - **Description**: Retrieves a list of all available models from the database.
    - **Response**:
      - `200 OK`: Returns a JSON object containing an array of model names.

- #### [`GET`] `/<model_name>`
    - **Description**: Provides detailed information about a specific model.
    - **URL Parameters**:
      - `model_name`: The name of the model.
    - **Response**:
      - `200 OK`: Returns a JSON object with the model's name, type, and features.
      - `400 Bad Request`: Error message if the model is not found.

- #### [`PUT`]  `/<model_name>`
    - **Description**: Upload a model.
    - **URL Parameters**:
      - `model_name`: The intended name for the new model.
    - **Form Data**:
      - `model_type`: The type of the model (must be a valid type).
      - `file`: The binary file containing the model data.
    - **Response**:
      - `200 OK`: Confirmation message of successful upload.
      - `400 Bad Request`: Error message if the model type is invalid or the file part is missing.

- #### [`DELETE`] `/<model_name>`
    - **Description**: Delete the specified model.
    - **URL Parameters**:
      - `model_name`: The name of the model to be deleted.
    - **Response**:
      - `200 OK`: Confirmation message of successful deletion.

- #### [`POST`] `/<model_name>/predict`
    - **Description**: Performs a prediction using the specified model.
    - **URL Parameters**:
      - `model_name`: The name of the model.
    - **Request Body**:
      - `features`: JSON object containing the features required for prediction.
    - **Response**:
      - `200 OK`: Returns a JSON object containing the prediction results.
      - `400 Bad Request`: Error message if the model is not found or if an error occurs during prediction.

## CLI
The cli tool in `src/cli.py` implements some of the api methods. The cli is mainly ment for managing the available models.

- #### `list_models`
    - **Description**: Retrieves and displays a list of all machine learning models available on the server.

- #### `info <model_name>`
    - **Parameters**:
      - `model_name`: The name of the model to retrieve information about.
    - **Description**: Fetches and shows details about a specific model.

- #### `upload <model_name> <file_path> <model_type>`
    - **Parameters**:
      - `model_name`: Name for the model to be uploaded.
      - `file_path`: Path to the model file or directory. If a directory, it will be zipped before upload.
      - `model_type`: Type of the model, must be one of the predefined model types.
    - **Description**: Uploads a new model to the server. If the file path is a directory, it zips the directory before upload.

- #### `delete <model_name>`
    - **Parameters**:
      - `model_name`: The name of the model to be deleted.
    - **Description**: Deletes a model from the server.
