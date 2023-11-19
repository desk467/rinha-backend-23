FROM python:3.12-bookworm

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false

WORKDIR /opt/app

COPY pyproject.toml poetry.lock /opt/app/

RUN poetry install --without dev

COPY . .

CMD ["./run.sh"]
