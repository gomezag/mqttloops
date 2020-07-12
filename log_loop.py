import time
import json
import csv
import datetime
from mqttroutines.routines import connect_mqtt
import os


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))

    try:
        msg = json.loads(msg)
    except:
        pass
    topic = message.topic

    if topic == 'home/log':
        print("logging")
        row = (datetime.datetime.now(), msg['key'], msg['value'])
        with open(os.getenv("LOGFILE"), 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(row)


#######################################
client = connect_mqtt("log", on_message)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass
print("Stopping")
client.loop_stop()  # stop the loop
