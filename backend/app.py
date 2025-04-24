from flask import Flask, request, jsonify
from flask_cors import CORS
from pinyin_engine import PhoneticEngine
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://name-generator-*.vercel.app",
            "http://localhost:*"
        ],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

# 初始化引擎
name_engine = PhoneticEngine()

def validate_birthdate(bdate_str):
    """验证日期格式"""
    try:
        datetime.strptime(bdate_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.route("/api/generate-name", methods=["POST"])
def generate_name():
    try:
        data = request.get_json()
        
        # 参数校验
        required_fields = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "birthdate": data.get("birthdate"),
            "nationality": data.get("nationality").upper() if data.get("nationality") else None
        }

        # 检查必填字段
        if not all(required_fields.values()):
            missing = [k for k, v in required_fields.items() if not v]
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # 验证日期格式
        if not validate_birthdate(required_fields["birthdate"]):
            return jsonify({"error": "Invalid birthdate format. Use YYYY-MM-DD"}), 400

        # 调用生成引擎
        results = name_engine.generate_chinese_name(
            first_name=required_fields["first_name"],
            last_name=required_fields["last_name"],
            gender=data.get("gender")  # 可选参数
        )

        # 格式化响应
        formatted_results = []
        for item in results:
            formatted = {
                "name": item["name"],
                "score": item["score"],
                "poetry_references": item["poetry"],
                "cultural_insights": {
                    "name_origin": "phonetic" if len(item["poetry"]) == 0 else "classic_poetry",
                    "gender_suitability": item["gender_suit"]
                }
            }
            formatted_results.append(formatted)

        return jsonify({"results": formatted_results})

    except Exception as e:
        logging.error(f"Generation error: {str(e)}")
        return jsonify({"error": "Name generation failed. Please try again."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
