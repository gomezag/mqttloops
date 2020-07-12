#!/bin/bash
sleep $1
source mqttroutines/.env
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/hvac" -m '{"power":"off"}'


