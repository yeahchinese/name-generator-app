# backend/app.py
import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from name_generator import NameGenerator
from surname_translator import SurnameTranslator
from poetry_db import PoetryDatabase

# 初始化应用
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NameGenerator")

# 全局实例初始化
try:
    surname_translator = SurnameTranslator()
    poetry_db = PoetryDatabase()
    name_generator = NameGenerator(surname_translator, poetry_db)
    logger.info("Application components initialized successfully")
except Exception as e:
    logger.error(f"Initialization failed: {str(e)}")
    raise RuntimeError("Critical initialization failure")

# 缓存预热
@app.before_first_request
def warmup():
    logger.info("Running warmup tasks...")
    # 预加载必要资源
    surname_translator.translate("Smith")
    poetry_db.get_poetry_by_pinyin("li")
    logger.info("Warmup completed")

@app.route("/api/generate-name", methods=["POST"])
def generate_name():
    """核心生成端点"""
    try:
        # 输入验证
        data = request.get_json()
        required_fields = ["first_name", "last_name", "birthdate", "nationality"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # 日期格式验证
        try:
            birth_date = datetime.strptime(data["birthdate"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format (YYYY-MM-DD)"}), 400

        # 生成逻辑
        results = name_generator.generate(
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=birth_date,
            nationality=data["nationality"],
            gender=data.get("gender")
        )

        return jsonify({"results": results})

    except Exception as e:
        logger.error(f"Generation error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Name generation failed",
            "detail": str(e),
            "retry_url": "/api/generate-name"
        }), 500

@app.route("/api/health")
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "ready",
        "components": {
            "surname_translator": surname_translator.is_ready(),
            "poetry_database": poetry_db.count_poems() > 0
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
