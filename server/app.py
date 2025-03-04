from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

# Define file paths
model_path = "./water_quality_model.pkl"
scaler_path = "./scaler.pkl"

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

# Function to determine water usability based on prediction and feature values
def get_usage_area(prediction, features):
    tds, turbidity, temp, conductivity = features[0]
    
    if prediction == 1:
        comment = "Water is potable. Meets safety standards for drinking and household use."
        usage = "Suitable for Residential and Drinking Purposes."
    else:
        comment = "Water is not potable. Contains impurities and is unsafe for direct consumption. Consider purification."
        if tds > 500 or turbidity > 5 or conductivity > 1000:
            usage = "Suitable for Industrial Use."
        else:
            usage = "Suitable for Agricultural Use."
    
    return {"comment": comment, "suggested_usage": usage}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input from the request
        data = request.get_json()
        
        # Ensure JSON input matches expected structure
        if "features" not in data or not isinstance(data["features"], list):
            return jsonify({"error": "Invalid JSON format. 'features' must be a list."}), 400
        
        # Convert input features into numpy array
        features = np.array([data["features"]])
        
        # Scale input features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get usage area and comments
        result = get_usage_area(prediction, features)
        
        return jsonify({"prediction": int(prediction), "comment": result["comment"], "suggested_usage": result["suggested_usage"]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
