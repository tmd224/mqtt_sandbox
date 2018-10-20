import time
import RPi.GPIO as GPIO

#CONSTANTS
LED = 17
DOOR_INPUT = 26



def door_open_callback(channel):
    """
    Door input callback
    """
    print("Door Sensor Event Detected (%s)" %channel)
    
def flash_led():
    """
    Function to flash LED
    """
    GPIO.output(LED,GPIO.HIGH)
    time.sleep(1)
    print("LED is now on")
    time.sleep(1)
    print("Turning LED off")
    GPIO.output(LED,GPIO.LOW)
    
def setup():
    """
    Initial setup of the GPIO
    """ 
    print("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.setup(DOOR_INPUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.add_event_detect(DOOR_INPUT, GPIO.RISING, callback=door_open_callback) 
    
    
print("Loading Garage Door Simulator...")

try:
    setup()
    for x in range(0,10):
        flash_led()
        time.sleep(1)
    
except Exception as e:
    print("An error occured: %s"%e)

finally:
    print("Cleaning up...")
    GPIO.cleanup()