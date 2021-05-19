FROM tiangolo/uvicorn-gunicorn-fastapi

RUN /usr/local/bin/python3 -m pip install --upgrade pip

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root --no-dev

RUN mkdir /meiweb/

COPY *.py /app
WORKDIR /app

EXPOSE 80