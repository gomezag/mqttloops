#!/bin/bash
source ./mqttroutines/.env
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/persiana" -m '{"value":"up"}'
sleep 9
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/persiana" -m '{"value":"stop"}'
sleep 180
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/persiana" -m '{"value":"up"}'
sleep 9
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/persiana" -m '{"value":"stop"}'
sleep 120
mosquitto_pub -h $MQTTHOST -u $MQTTUSER -P $MQTTPASS -t "home/room/lights/main-light/POWER" -m 'ON'
