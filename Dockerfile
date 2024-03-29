FROM python:latest
RUN apt-get update -y
RUN apt-get upgrade -y
WORKDIR /src


COPY poetry.lock pyproject.toml /
RUN pip install poetry
RUN poetry export -f requirements.txt --output /src/requirements.txt
RUN pip uninstall poetry -y
RUN pip install -r /src/requirements.txt
COPY src/ ./src
