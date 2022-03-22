
# docker stack
```bash
docker compose -f docker/docker-compose.yaml build
docker compose -f docker/docker-compose.yaml up
```
# dev on osx
Install pulseaudio server on host

```bash
brew install pulseaudio
```

Let image connect to host audio
```yaml
    environment:
      - PULSE_SERVER=docker.for.mac.localhost
```

Edit the file: `/usr/local/Cellar/pulseaudio/14.2/etc/pulse/default.pa`
and  uncomment
```
load-module module-esound-protocol-tcp
load-module module-native-protocol-tcp
```

Kill a restart the daemon with the `module-native-protocol-tcp` module:
```
pulseaudio -k
pulseaudio --load=module-native-protocol-tcp --start -v
```

Copy the coockie file into the docker container
```bash
cp ~/.config/pulse/cookie .
```

