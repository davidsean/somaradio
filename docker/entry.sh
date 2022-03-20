#!/bin/bash

# wait for rabbitmq container
./docker/wfi.sh -h rabbitmq -p 5672 -t 20

python3 -m somaradio