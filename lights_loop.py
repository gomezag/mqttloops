import time
import json
from mqttroutines.routines import connect_mqtt



global new_msg, wait_msg, disable_poll, wait_msg2, lights
log_file = "./mqtt.log"
poll_time = 120
ack_time = 5
lights=False

###########

def on_message(client, userdata, message):
    global wait_msg, new_msg, disable_poll, wait_msg2, lights
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
        if val==10295236:
            if lights==True:
                 payload="OFF"
            elif lights==False:
                 payload="ON"
            client.publish("home/room/lights/main-light/cmnd/POWER", payload=payload)
        else:
            print(val)

    elif topic == "home/room/lights/main-light/STATE":
         if msg["POWER"].lower()=="on":
              lights=True
         elif msg["POWER"].lower()=="off":
              lights=False
         else:
              print(msg)
    elif topic=="home/room/lights/main-light/RESULT":
         if msg["POWER"].lower() == "off":
            lights=False
         elif msg["POWER"].lower()=="on":
            lights=True


#######################################
client = connect_mqtt("lights", on_message)

try:
    while True:
        time.sleep(poll_time)
except KeyboardInterrupt:
    pass
print("Stopping")
client.loop_stop()  # stop the loop
