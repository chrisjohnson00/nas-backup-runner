FROM python:3.9.5-slim

WORKDIR /usr/src/app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y rsync openssh-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]
