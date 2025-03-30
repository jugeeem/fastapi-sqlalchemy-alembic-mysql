FROM python:3.13.2-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pymysql \
    && pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

FROM python:3.13.2-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    curl \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" appuser

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt . 

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
    && pip install --no-cache-dir pymysql \
    && rm -rf /wheels requirements.txt

COPY . . 

RUN mkdir -p /app/migrations/versions \
    && chmod -R 777 /app/migrations \
    && chown -R appuser:appuser /app/migrations

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

EXPOSE ${BACKEND_LOCAL_PORT}

CMD ["/app/entrypoint.sh"]
