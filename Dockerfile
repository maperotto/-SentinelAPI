FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

COPY app/ ./app/
COPY endpoints.json ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.main"]
