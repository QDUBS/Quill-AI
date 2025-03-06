FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    gcc \
    libssl-dev \
    libsasl2-dev \
    libldap2-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
