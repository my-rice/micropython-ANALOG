import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a
# CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("Connected with result code "+str(rc))
    print("\n connected with client "+ str(client))
    print("\n connected with userdata "+str(userdata))
    print("\n connected with flags "+str(flags))
    loop_flag=0

def on_publish(client,userdata,result): #create function for callback
    print("data published \n")
    print("client = "+ str(client))
    print("\nresult in on_publish= ", result)

def on_log(client, userdata, level, buf):
    print("\n log:client = "+ str(client))
    print("\n log:level ="+str(level))
    print("\n log:buffer "+str(buf))
    
try:
    client = mqtt.Client("UniSaIoT22Pub")
    client.on_connect = on_connect
    client.on_publish = on_publish
    #client.on_log = on_log
    #client.connect("iot.eclipse.org", 1883, 60)
    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_start() # the loop() method periodically
                        # check the callback events

    i=0
    while i<10:
        res=client.publish("/IoT_unisa/dvd", "payload "+str(i), qos=1, retain=False)
        print("\n\n check publish =" + str(res))
        i+=1
        time.sleep(2)
    
except Exception as e:
    print('exception ', e)
finally:
    client.loop_stop()
    client.disconnect()