FROM python:3.10-slim

RUN apt -f install -y && \
    apt-get update && \
    apt-get install -y nmap \
                       wget

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y --fix-missing

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-u", "main.py"]
