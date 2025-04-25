# 中文名字生成器

## 启动方式（本地）

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

## 启动方式（Docker）

```bash
docker build -t name-generator .
docker run -p 5000:5000 name-generator
```

访问：http://localhost:5000/generate-name
