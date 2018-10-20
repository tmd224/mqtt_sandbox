
import time
import random
import logging
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


#Documentation https://pypi.org/project/paho-mqtt/#usage-and-api

#CONSTANTS
LED = 17
DOOR_INPUT = 26

#MQTT CONSTANTS
USERNAME = "JarvisMQTT"
PASSWORD = "kittyWhispers"

LOG_FILE_PATH = "test.log"

def init_logger(fullpath):
    """
    Setup the logger object
    
    Args: 
        fullpath (str): full path to the log file 
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d-%y %H:%M:%S',
                        filename=fullpath,
                        filemode='w')
                        
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logging.debug("Creating log file")

    
    


CONNECT_RESPONSE = {0: 'Connection successful',
                    1: 'Connection refused - incorrect protocol version',
                    2: 'Connection refused - invalid client identifier',
                    3: 'Connection refused - server unavailable',
                    4: 'Connection refused - bad username or password',
                    5: 'Connection refused - not authorised',
                   }



state_topic = 'hass/mqtt_test/val'

def setup_gpio():
    """
    Initial setup of the GPIO
    """ 
    main_log.info("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.setup(DOOR_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
   
def mqtt_init():
    main_log.info("Launching Hass MQTT Sensor Client")
    broker = '192.168.1.120'
    client = mqtt.Client("Hass Sensor")
    client.username_pw_set(USERNAME,PASSWORD)
    #register callbacks
    client.on_message = on_message_callback
    client.on_connect = on_connect_callback
    client.on_log=on_log
    client.connect(broker)
    client.loop_start()
    client.subscribe(state_topic)
    return client

def on_connect_callback(client, userdata, flags, rc):
    """
    This callback gets called during a client connection
    """
    if rc > 5:
        main_log.info("Unsuccessful client connection - Error code unknown (%d)"%rc)
        client.bad_connection_flag=True
    else:
        main_log.info("MQTT Client Connection Response: %s (%d)"%(CONNECT_RESPONSE[rc],rc))
        client.connected_flag=True #Flag to indicate success        
        
def on_message_callback(client,userdata,message):
    """
    Callback to handle all incoming messages
    """
    # main_log.info "msg rcvd: %s"%message.payload.decode("utf-8")
    # main_log.info "msg topic: %s"%message.topic
    # main_log.info "msg qos: %s" %message.qos
    # main_log.info "mgs retain flag: %s" %message.retain
    # main_log.info "********************************************"
    parse_commands(message.payload.decode("utf-8"))

def on_log(client, userdata, level, buf):
    """
    Logging callback from client.  Push to log file as debug
    """
    paho_log.debug(buf)

    
def parse_commands(command):
    """
    Function to parse all incoming commands
    """
    if command == "LED_ON":
        main_log.info("Turning LED ON")
        GPIO.output(LED,GPIO.HIGH)
        time.sleep(3)
        client.publish(state_topic, 1)
    elif command == "LED_OFF":
        main_log.info("Turning LED OFF")
        GPIO.output(LED,GPIO.LOW)
        time.sleep(3)
        client.publish(state_topic, 0)        
        
     
        
init_logger(LOG_FILE_PATH)    
#add logger devices
main_log = logging.getLogger('MAIN')
paho_log = logging.getLogger('PAHO')
    
setup_gpio()
client = mqtt_init()

delay = 5
val = 0
try:
    main_log.info("Entering Main Loop")
    while True:
        pass
        # if val > 20:
            # val = 0
            
        # client.publish(state_topic, val)
        # main_log.info("Publishing value: %d"%val)
        # val += 1
        # time.sleep(delay)

except KeyboardInterrupt:
    main_log.info("Stopping MQTT Client")
    client.loop_stop()
    client.disconnect()
    GPIO.cleanup()
    

    
    
    
