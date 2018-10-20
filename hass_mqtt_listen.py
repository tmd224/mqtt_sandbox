import paho.mqtt.client as mqtt
import time

def on_message(client,userdata,message):
    print "msg rcvd: %s"%message.payload.decode("utf-8")
    print "msg topic: %s"%message.topic
    print "msg qos: %s" %message.qos
    print "mgs retain flag: %s" %message.retain
    print "********************************************"


broker_address = '192.168.1.120'
state_topic = "/hass/test"
client = mqtt.Client("Rpi")
client.on_message = on_message	#register callback
client.connect(broker_address)
client.loop_start()

client.subscribe(state_topic)
print "Client subscribing to topic: %s"%state_topic

#client.publish("test","Raspberry Pi Client Online!!!")

try:
    while True:
	time.sleep(1)
except KeyboardInterrupt:
    #client.publish("test","Raspberry Pi Client going offline in 5 seconds")
    print "Disconnecting in 5 seconds..."
    time.sleep(5)

    client.loop_stop()

