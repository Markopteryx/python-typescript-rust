FROM nikolaik/python-nodejs:python3.12-nodejs21-bullseye

RUN apt update -y

RUN curl https://sh.rustup.rs/ -sSf | sh -s -- -y

RUN pip install poetry

COPY python/pyproject.toml .

COPY python/poetry.loc[k] .

RUN poetry config virtualenvs.create false && poetry install --no-interaction
