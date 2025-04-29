from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)

saved_destinations = []

# Route to serve the HTML frontend
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/save-destination', methods=['POST'])
def save_destination():
    data = request.get_json()
    destination = data.get('destination')

    if destination:
        saved_destinations.append(destination)
        print(f"Destination saved: {destination}")
        return jsonify({"message": "Destination saved successfully"}), 200
    else:
        return jsonify({"error": "No destination provided"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
