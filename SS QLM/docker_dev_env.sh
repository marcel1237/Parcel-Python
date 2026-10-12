#!/bin/bash
# Quick Docker environment setup for development
# Generates a Dockerfile and docker-compose.yml

cat << 'DOCKER' > Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y build-essential cmake g++ gdb git
WORKDIR /app
DOCKER

cat << 'COMPOSE' > docker-compose.yml
version: '3'
services:
  dev:
    build: .
    volumes:
      - .:/app
    stdin_open: true
    tty: true
COMPOSE

echo "Docker environment files generated. Run 'docker-compose up -d' to start."
