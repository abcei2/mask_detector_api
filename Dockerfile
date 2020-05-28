###########################################
# General Dockerfile for Tucano detectors
# TucanoRobotics 2020
###########################################

FROM python:3.7
# FROM fbcotter/docker-tensorflow-opencv:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade

ADD requirements.txt /opt/detector/

WORKDIR /opt/detector
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /opt/detector

CMD ["python", "./src/api.py"]
