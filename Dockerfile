FROM python:3.10-slim

WORKDIR /app

COPY backend/ ./backend/

RUN pip install flask flask-cors

EXPOSE 5000

CMD ["python", "backend/app.py"]
