FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nmap

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-u", "main.py"]
