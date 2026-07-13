FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python backend/data/generate_dataset.py && python backend/train_model.py
EXPOSE 5001
CMD ["python", "backend/app.py"]
