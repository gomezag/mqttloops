import json
import ssl
import websockets
import asyncio
import paho.mqtt.client as mqtt
import os

def connect_mqtt(clientname, function):
    broker_address = os.getenv("MQTTHOST")

    client = mqtt.Client(clientname)  # create new instance

    client.on_message = function  # attach function to callback
    client.username_pw_set(username=os.getenv("MQTTUSER"), password=os.getenv("MQTTPASS"))
    client.connect(broker_address)  # connect to broker
    print("Connected")
    client.loop_start()  # start the loop
    print('Loop started')
    gateway = "+/#"
    client.subscribe(gateway)

    return client


async def wsocket(data, channel):
    uri = "wss://"+os.getenv('DASHIP')+":8000/ws/room/"+channel+"/"
    print('sending to '+uri)
    print('sending ', data, ' to ', channel)
    data = {
        'type': 'data_update',
        'message': data
    }

    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
#    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(data))
        print(f"> {data}")
