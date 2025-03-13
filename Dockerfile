
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY static /app/static
COPY templates /app/templates

EXPOSE 8000

CMD ["sh", "/wait-for-db.sh", "db", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

COPY wait-for-db.sh /wait-for-db.sh