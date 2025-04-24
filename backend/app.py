from flask import Flask, request, jsonify
from flask_cors import CORS
from name_generator import generate_chinese_name

app = Flask(__name__)
CORS(app)

@app.route("/api/generate-name", methods=["POST"])
def generate_name():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    birthdate = data.get("birthdate")
    nationality = data.get("nationality")

    if not all([first_name, last_name, birthdate, nationality]):
        return jsonify({"error": "Missing required fields."}), 400

    result = generate_chinese_name(first_name, last_name, birthdate, nationality)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
