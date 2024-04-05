FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
COPY ./requirements/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
COPY . /app
WORKDIR /app