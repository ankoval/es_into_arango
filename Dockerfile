FROM python:3.8-slim-buster AS builder

ENV PYTHONUSERBASE /var/python/dist
# ARG GIT_PAT

RUN apt-get update \
    && apt-get -y install --no-install-recommends gcc build-essential curl apt-utils dialog 2>&1 \
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git iproute2 procps lsb-release \
    && pip install --upgrade pip \
    && pip install pipenv \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

#Set our working directory install dependencies and start the application
WORKDIR /app

# RUN git config --global url."https://${GIT_PAT}:x-oauth-basic@github.com/".insteadOf "https://github.com/"

RUN PIP_USER=1 pipenv install --system --deploy --ignore-pipfile

FROM builder AS production

CMD ["python"]