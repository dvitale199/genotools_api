FROM python:3.11.3
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

RUN adduser --disabled-password --gecos "" gtuser

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/dvitale199/genotools_api.git

WORKDIR /app/genotools_api

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install .

# EXPOSE 8080

# CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
