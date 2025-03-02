from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

# Define file paths
model_path = "../water_quality_model.pkl"
scaler_path = "../scaler.pkl"

# Load the trained model and scaler
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    exit(1)

# Initialize Flask app
app = Flask(__name__)

CORS(app, supports_credentials=True)

@app.route("/", methods=["GET"])
def home():
    return "Water Quality Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input from the request
        data = request.get_json()
        
        # Convert input features into numpy array
        features = np.array(data["features"]).reshape(1, -1)

        # Scale input features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)

        # Return prediction as JSON response
        return jsonify({"prediction": prediction.tolist()[0]})

    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
