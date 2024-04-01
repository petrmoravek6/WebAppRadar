FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nmap

RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub \
  && gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub \
  && echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-u", "main.py"]
