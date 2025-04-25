from flask import Flask, request, jsonify
from name_generator import generate_name
from pinyin_engine import get_initial_letter

app = Flask(__name__)

@app.route("/generate-name", methods=["POST"])
def api_generate_name():
    data = request.get_json()
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    gender = data.get("gender", "unisex")
    result = generate_name(first_name, last_name, gender)
    return jsonify(result)
