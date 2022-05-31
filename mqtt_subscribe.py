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


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("\n on message: "+msg.topic+" "+str(msg.payload))

def on_log(client, userdata, level, buf):
    print("\n log:client = "+ str(client))
    print("\n log:level ="+str(level))
    print("\n log:buffer "+str(buf))

def on_subscribe(client, userdata, msg, qos_l):
    print("\n on_sub: client ="+str(client._client_id))
    print("\n on_sub: msg ="+str(msg))
    print("\n on_sub: qos level ="+str(qos_l))

try:
    client = mqtt.Client("UniSaIoT22Sub",True)
    client.on_subscribe = on_subscribe
    client.on_connect = on_connect
    client.on_message = on_message
#    client.on_log = on_log
#    client.connect("mqtttest1.duckdns.org", 1883, 60)
#    client.connect("79.22.108.147", 1883, 60)
    
    client.connect("test.mosquitto.org", 1883, 30)
    client.loop_start() # the loop() method periodically
                        # check the callback events
    
#    res=client.subscribe("$SYS/broker/clients/connected", 0)
#    print("\n res subscription - conn clients: ", res)
#    res=client.subscribe("$SYS/broker/clients/total", 0)
#    print("\n res subscription - tot clients: ", res)
#    res=client.subscribe("$SYS/broker/subscriptions/count", 2)
    res=client.subscribe("/IoT_unisa/test1", 2)

    print("\n res subscription counts: ", res)

    #client.loop_forever()

 ##   res=client.subscribe("temp/random", 1)
       
    while True:   
        print("running")    
        time.sleep(5)

        
except Exception as e:
    print('exception ', e)
finally:
    client.loop_stop()
    client.unsubscribe("/IoT_unisa/test1")
    client.disconnect()
    print("disconnected")