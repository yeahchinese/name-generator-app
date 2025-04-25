FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
