FROM python:3.13-slim

RUN apt -f install -y && \
    apt-get update && \
    apt-get install -y nmap \
                       wget

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN apt-get install ./google-chrome-stable_current_amd64.deb -y --fix-missing

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "app:app"]
