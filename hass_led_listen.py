
import time
import random
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
#import paho.mqtt.publish as publish

#CONSTANTS
LED = 17
DOOR_INPUT = 26

USERNAME = "yourusername"
PASSWORD = " yourpassword"
state_topic = 'hass/mqtt_test/val'

def setup_gpio():
    """
    Initial setup of the GPIO
    """ 
    print("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.setup(DOOR_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
   
def mqtt_init():
    print("Launching Hass MQTT Sensor Client")
    broker = '192.168.1.120'
    client = mqtt.Client("Hass Sensor")
    #client.username_pw_set(username=USERNAME,password=PASSWORD)
    client.on_message = on_message	#register callback
    client.connect(broker)
    client.loop_start()
    client.subscribe(state_topic)
    return client

def on_message(client,userdata,message):
    # print "msg rcvd: %s"%message.payload.decode("utf-8")
    # print "msg topic: %s"%message.topic
    # print "msg qos: %s" %message.qos
    # print "mgs retain flag: %s" %message.retain
    # print "********************************************"
    parse_commands(message.payload.decode("utf-8"))

def parse_commands(command):
    if command == "LED_ON":
        print("Turning LED ON")
        GPIO.output(LED,GPIO.HIGH)
        time.sleep(3)
        client.publish(state_topic, 1)
    elif command == "LED_OFF":
        print("Turning LED OFF")
        GPIO.output(LED,GPIO.LOW)
        time.sleep(3)
        client.publish(state_topic, 0)        
        
     
        
        
setup_gpio()
client = mqtt_init()

delay = 5
val = 0
try:
    print("Entering Main Loop")
    while True:
        pass
        # if val > 20:
            # val = 0
            
        # client.publish(state_topic, val)
        # print("Publishing value: %d"%val)
        # val += 1
        # time.sleep(delay)

except KeyboardInterrupt:
    print("Stopping MQTT Client")
    client.loop_stop()
    GPIO.cleanup()
    

    
    
    
