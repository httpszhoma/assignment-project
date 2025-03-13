FROM python:3.12.4-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    python3-gdal \
    build-essential \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000

COPY ./start.sh /start
RUN chmod +x /start
