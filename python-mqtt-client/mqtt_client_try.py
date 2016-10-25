import paho.mqtt.client as mqtt
import threading
import time
import numpy as np

# for plot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

is_connected_to_broker = False
temperature = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global is_connected_to_broker
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(("mydome/#", 2))
    client.subscribe(("dcsquare/#", 0))
    client.subscribe(("lotik/test", 0))

    if rc == 0:
        is_connected_to_broker = True
        timer_callback()

# callback for when client is disconnected
def on_disconnect(client, userdata, rc):
    print("Connection returned result:"+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global temperature
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == "mydome/temp/value":
        temperature = msg.payload

# 1 second timer callback
def timer_callback():
    threading.Timer(1.0, timer_callback).start()

    if is_connected_to_broker == True:
        client.publish("lotik/test", time.time())

    # for plot
    for i in range(10):
        y = np.random.random()
        plt.scatter(i, y)
        plt.pause(0.05)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("broker.mqttdashboard.com", 1883, 60)

# for plots
plt.axis([0, 10, 0, 1])
plt.ion()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
print("Starting the loop..")
client.loop_forever(timeout=1.0)
