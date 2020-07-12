import time
import json

from mqttroutines.routines import connect_mqtt, wsocket
import asyncio


poll_time = 120


###########

def on_message(client, userdata, message):
    print("got it")
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
        if (val - val % 1000000) // 1000000 == 3:
            wait_msg2 = False
            val = val % 3000000
            val1 = val % 100
            val = val // 100
            val2 = val % 100
            val3 = val // 100
            payload = {'value': val1}
            client.publish("home/room/balcony/pot1", payload=json.dumps(payload), qos=1, retain=True)
            payload = {'value': val2}
            client.publish("home/room/balcony/pot2", payload=json.dumps(payload), qos=1, retain=True)
            payload = {'value': val3}
            client.publish("home/room/balcony/pot3", payload=json.dumps(payload), qos=1, retain=True)
            client.publish("home/room/nano/status", "on", qos=1)
        elif (val - val % 1000000) // 1000000 == 4:
            wait_msg2 = False
            val = val % 4000000
            t = val % 100
            val = val // 100
            h = val % 100
            payload = {'value': t}
            client.publish("home/room/balcony/temp", payload=json.dumps(payload), qos=1, retain=True)
            payload = {'value': h}
            client.publish("home/room/balcony/hum", payload=json.dumps(payload), qos=1, retain=True)
            client.publish("home/room/nano/status", "on", retained=True)
        elif (val - val % 1000000) // 1000000 == 5:
            val = val % 5000000
            payload = {'value': val}
            client.publish("home/room/nano/bat", payload=json.dumps(payload), qos=1, retain=True)

    elif topic == "home/room/balcony/pot1":
        client.publish('home/log', payload=json.dumps(dict(key='P1', value=msg['value'])), qos=1)
        asyncio.run(wsocket(str(msg['value']), "P1"))

    elif topic == "home/room/balcony/pot2":
        client.publish('home/log', payload=json.dumps(dict(key='P2', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "P2"))

    elif topic == "home/room/balcony/pot3":
        client.publish('home/log', payload=json.dumps(dict(key='P3', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "P3"))

    elif topic == "home/room/balcony/temp":
        client.publish('home/log', payload=json.dumps(dict(key='TO', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "TO"))

    elif topic == "home/room/balcony/hum":
        client.publish('home/log', payload=json.dumps(dict(key='HO', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "HO"))

    elif topic == "home/room/nano/bat":
        client.publish('home/log', payload=json.dumps(dict(key='NB', value=msg['value'])))
        asyncio.run(wsocket(str(msg['value']), "NB"))

    elif topic == "home/room/nano/poll":
        print("Polling to nano..")
        client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 10000002}')
        time.sleep(0.5)
    elif topic == "home/room/nano/poll2":
        client.publish("home/room/433Gateway/commands/MQTTto433", '{"value": 10000003}')
        time.sleep(0.5)


#######################################
client = connect_mqtt("nano", on_message)

try:
    while True:
        time.sleep(poll_time)
except KeyboardInterrupt:
    pass
print("Stopping")
client.loop_stop()  # stop the loop
