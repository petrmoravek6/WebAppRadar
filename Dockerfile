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

ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
