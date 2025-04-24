# backend/app.py
from flask import Flask, request, jsonify
from name_generator import generate_chinese_name
from lunar_converter import convert_to_lunar

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    name = generate_chinese_name(data['first_name'], data['last_name'], data['dob'], data['nationality'])
    lunar_info = convert_to_lunar(data['dob'])
    return jsonify({
        "chinese_name": name['name'],
        "meaning": name['meaning'],
        "poem_reference": name['poem'],
        "lunar_date": lunar_info
    })

if __name__ == '__main__':
    app.run(debug=True)
