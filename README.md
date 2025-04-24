# Chinese Name Generator Web App

这是一个基于 Flask 的前后端分离中文取名工具，旨在为外国人生成符合音译、美感与诗意的中文名字。

## 📁 项目结构

```
/project-root
│
├── backend/
│   ├── app.py
│   ├── name_generator.py
│   ├── pinyin_engine.py
│   └── poem_db.json
│
├── frontend/
│   ├── index.html
│   ├── result_modal.html
│   ├── style.css
│   └── script.js
│
├── Dockerfile
└── README.md
```

## 🚀 本地部署

### 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install flask flask-cors
```

### 启动服务

```bash
python app.py
```
服务运行在 `http://localhost:5000`

### 启动前端
用浏览器打开 `frontend/index.html`


## 🐳 Docker部署

### 构建镜像
```bash
docker build -t chinese-name-generator .
```

### 运行容器
```bash
docker run -d -p 5000:5000 chinese-name-generator
```

### 然后
将 `frontend/` 中内容部署到任意静态资源服务器或服务如 GitHub Pages / Netlify / Vercel。

## 📤 API说明

### `POST /api/generate-name`
**请求示例**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "birthdate": "1990-01-01",
  "nationality": "USA"
}
```

**返回示例**
```json
{
  "chinese_name": "李东",
  "pinyin": "Li Dong",
  "meaning": "东风破浪，行稳致远",
  "reference_poem": "白日依山尽，黄河入海流..."
}
```

## ✅ 待完善部分
- 音韵规则优化
- 接入真实诗词数据库并支持模糊标签匹配
- 实现农历换算逻辑
- 实现社交媒体 API 分享功能

欢迎贡献！
