# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install needed packages
RUN apt-get update
RUN apt-get install -y \
  build-essential \
  iputils-ping \
  curl \
  bc

# Set the working directory to /app
WORKDIR /app
COPY . /app

# master / worker port
EXPOSE 17011

# backend port
EXPOSE 5005

# Create worker user
RUN useradd -c "Worker" worker  -s /bin/bash
RUN chmod 700 /app
RUN chmod 1777 /tmp

# Add dev watch script
COPY ./scripts/watch.sh /app/watch.sh

RUN pip install -r /app/requirements.txt
RUN pip install -r /app/requirements-dev.txt
RUN pip install -r /app/docker/backend/requirements.txt
RUN pip install -r /app/plynx/cdp/requirements-cdp.txt