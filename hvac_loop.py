import time
import json
import datetime
from mqttroutines.routines import connect_mqtt
from hvac_ircontrol.ir_sender import LogLevel
from hvac_ircontrol.mitsubishi import Mitsubishi, ClimateMode, FanMode, VanneVerticalMode, VanneHorizontalMode, \
    ISeeMode, AreaMode, PowerfulMode


poll_time = 120

###########

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    try:
        msg = json.loads(msg)
    except:
        pass
    topic = message.topic

    if topic == "home/room/hvac":
        print('tocando el aire')
        if msg['power'] == 'off':
            print('apagando')
            HVAC.power_off()
        elif msg['power'] == 'cold':
            try:
                msg['temp']=int(msg['temp'])
                HVAC.send_command(
                      climate_mode=ClimateMode.Cold,
                      temperature=msg['temp'],
                      fan_mode=FanMode.Auto,
                      vanne_vertical_mode=VanneVerticalMode.Auto,
                      vanne_horizontal_mode=VanneHorizontalMode.NotSet,
                      isee_mode=ISeeMode.ISeeOn,
                      area_mode=AreaMode.Full,
                      end_time=datetime.datetime(2020,1,1,1,0,0),
                      powerful=PowerfulMode.PowerfulOn
                    )
            except Exception as e:
                print(repr(e))

        elif msg['temp']:
            print('solo temp')

#######################################
client = connect_mqtt("hvac", on_message)

gpio = 23
HVAC=Mitsubishi(gpio, LogLevel.ErrorsOnly)
print('HVAC Defined on GPIO ', gpio)
try:
    while True:
        time.sleep(poll_time)
except KeyboardInterrupt:
    pass
print("Stopping")
client.loop_stop()  # stop the loop
