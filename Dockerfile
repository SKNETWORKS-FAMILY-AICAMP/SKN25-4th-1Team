FROM python:3.12.12-slim

RUN apt-get update && apt-get install -y \
    redis-server \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run_scripts.sh

EXPOSE 8000 8501 6379

CMD ["./run_scripts.sh"]
