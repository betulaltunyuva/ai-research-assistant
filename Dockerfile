FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p \
    /app/documents/uploads \
    /app/outputs/reports \
    /app/outputs/exports

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000"]