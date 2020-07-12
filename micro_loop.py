import time
import json
from mqttroutines.routines import connect_mqtt, wsocket
import asyncio


global new_msg, wait_msg, disable_poll
poll_time = 120
ack_time = 5

###########

def on_message(client, userdata, message):
    print("got it")
    global wait_msg, new_msg, disable_poll
    msg = str(message.payload.decode("utf-8"))
    try:
        msg = json.loads(msg)
    except:
        pass
    topic = message.topic
    #    print(topic)
    if topic == "home/room/433Gateway/433toMQTT":
        new_msg = True
        val = msg['value']
        if val == 11110000:
            wait_msg = False
            client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 10001111}')
            time.sleep(2)
        elif (val - val % 1000000) // 1000000 == 2:
            wait_msg = False
            new_msg = False
            val = val % 2000000
            hum = val % 1000
            temp = val // 1000
            payload = {'value': temp}
            client.publish("home/room/temperature", payload=json.dumps(payload), qos=1, retain=True)
            payload = {'value': hum}
            client.publish("home/room/humidity", payload=json.dumps(payload), qos=1, retain=True)
            client.publish("home/room/microview/status", "on", qos=1, retained=True)

    elif topic == "home/room/persiana":
        if msg['value'] == "up":
            client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 9392466}')
        elif msg['value'] == 'down':
            client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 9392472}')
        elif msg['value'] == 'stop':
            print('stopping')
            client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 11100000}')

    elif topic == "home/room/temperature":
        client.publish('home/log', payload=json.dumps(dict(key='T', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "T"))

    elif topic == "home/room/humidity":
        client.publish('home/log', payload=json.dumps(dict(key='H', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "H"))

    elif topic == "home/room/microview/poll":
        print("Polling to microview..")
        client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 10000001}')
        time.sleep(0.5)


#######################################
client = connect_mqtt("micro", on_message)

try:
    while True:
        print('Polling...')
        wait_msg = True
        client.publish("home/room/microview/poll", 'poll')
        time.sleep(ack_time)
        if wait_msg == True:
            client.publish("home/room/microview/status", "off")
        else:
            client.publish("home/room/microview/status", "on")

        time.sleep(poll_time)
except KeyboardInterrupt:
    pass
print("Stopping")
client.loop_stop()  # stop the loop
