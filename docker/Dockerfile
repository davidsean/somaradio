FROM ubuntu:latest

LABEL version="0.1"
LABEL David Sean "https://github.com/davidsean"


RUN apt update && apt upgrade -y 
RUN apt install -y locales && locale-gen en_US.UTF-8

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y python3 pip vlc --no-install-recommends

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    apt install -y pulseaudio pulseaudio-utils  --no-install-recommends


ENV HOME /home/vlcuser
RUN useradd --create-home --home-dir $HOME vlcuser \
	&& usermod -aG audio,pulse,pulse-access vlcuser \
	&& chown -R vlcuser:vlcuser $HOME



WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m pip install -r requirements.txt


USER vlcuser

ENTRYPOINT [ "./docker/entry.sh" ]