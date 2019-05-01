import paho.mqtt.client as mqtt
import time
from pyfirmata import Arduino, util

SECRET_KEY = ''

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(("dev/#", 1))

# callback for when client is disconnected
def on_disconnect(client, userdata, rc):
    print("Connection returned result:"+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(SECRET_KEY)
    client.connect("mqtt.beebotte.com", 1883, 60)
    print("Starting the loop..")
    client.loop_forever(timeout=1.0)

if __name__ == "__main__":
    main()

