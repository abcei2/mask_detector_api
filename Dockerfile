###########################################
# General Dockerfile for Tucano detectors
# TucanoRobotics 2020
###########################################

FROM python:3.7
# FROM fbcotter/docker-tensorflow-opencv:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade

WORKDIR /opt/detector

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/api.py"]
