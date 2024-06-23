FROM nikolaik/python-nodejs:python3.12-nodejs21-bullseye

# AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

# Terraform
RUN echo "deb https://apt.releases.hashicorp.com bullseye main" > /etc/apt/sources.list.d/hashicorp.list && \
    wget -qO- https://apt.releases.hashicorp.com/gpg | apt-key add -

RUN apt-get update && \
    apt-get upgrade -yqq

# Terraform
RUN apt-get install -yqq terraform

RUN apt install -yqq zip

# Python Package Manager
RUN pip install poetry

# Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /bin/bash -c "source $HOME/.cargo/env && rustup component add rust-src"

COPY python/pyproject.toml .

COPY python/poetry.loc[k] .

RUN pip3 install cargo-lambda

RUN npm install --global tsx

RUN poetry config virtualenvs.create false && poetry install --no-interaction