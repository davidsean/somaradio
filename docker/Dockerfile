FROM ubuntu:latest

LABEL version="0.1"
LABEL David Sean "https://github.com/davidsean"

RUN apt update && apt upgrade -y && apt install -y locales && locale-gen en_US.UTF-8
RUN apt install -y python3 pip vlc


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "./docker/entry.sh" ]