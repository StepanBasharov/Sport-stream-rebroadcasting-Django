FROM ubuntu:20.04

WORKDIR /app
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
COPY requirements.txt /app/
COPY . /app/
RUN apt-get update && apt-get install -y \
ffmpeg \
screen \
python3.9 \
python3-pip 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
