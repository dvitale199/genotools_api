FROM python:3.11-slim
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" gtuser

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev --verbose \
    && apt-get remove -y gcc build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN chown -R gtuser:gtuser /app

USER gtuser

CMD ["uvicorn", "genotools_api.main:app", "--host", "0.0.0.0", "--port", "8080"]