FROM python:3.11.3
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/* # clean up to reduce image size

RUN git clone https://github.com/dvitale199/genotools_api.git

WORKDIR /app/genotools_api

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install uvicorn==0.29.0 fastapi==0.111.0 && \
    pip install .

# RUN adduser --disabled-password --gecos "" gtuser && \
#     chown -R gtuser:gtuser /app

# USER gtuser
# ENV PATH="/home/gtuser/.local/bin:${PATH}"
EXPOSE 8080

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 8080