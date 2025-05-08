FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install numpy fastapi uvicorn pydicom python-multipart

CMD ["uvicorn", "main:dicomCalculator", "--host", "0.0.0.0", "--port", "5000"]