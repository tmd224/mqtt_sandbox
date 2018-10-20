
import time
import random
import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish

USERNAME = "MyUserName"
PASSWORD = " MyPassword"

print("Launching Hass MQTT Sensor Client")
broker = '192.168.1.120'
client = mqtt.Client("Hass Sensor")
client.username_pw_set(username=USERNAME,password=PASSWORD)
client.connect(broker)
client.loop_start()
state_topic = 'hass/mqtt_test/val'
delay = 5
val = 0
try:
    print("Entering Main Loop")
    while True:
        if val > 20:
            val = 0
            
        client.publish(state_topic, val)
        print("Publishing value: %d"%val)
        val += 1
        time.sleep(delay)

except KeyboardInterrupt:
    print("Stopping MQTT Client")
    client.loop_stop()
    

    
    
    
