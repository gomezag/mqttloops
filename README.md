# MQTTLoops
This are python control loops for connecting messages between different clients.
It works on a 
It works in conjunction with [MQTTdash](https://github.com/gomezag/mqttdash) and [MQTTarduino](https://github.com/gomezag/mqttarduino)

[hvac_ir_control](https://github.com/gomezag/mqttloops/tree/master/hvac_ircontrol) library is taken from [this awesome project](https://github.com/Ericmas001/HVAC-IR-Control) which happened to work with my Mitsubish HVAC.
For this service to work you need permissions for the GPIO port in the RPi and an IR transmitter connected to pin 23.

#### Next upgrades:
- Create class that mimics the different scripts and a worker that creates different instances dynamically or via .yaml files.
- Create centralized worker that creates different services via threads.
- The point of splitting services is because a long if/elif comparator caused messages to be lost during the processing of previous messages meant for different services (the same service is usually not updated that fast since they have to communicate with something which brings delay)
