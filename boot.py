#OMNISCIENT
import utime
from umqttsimple import MQTTClient
import ubinascii
import machine
from machine import Pin
import network
import json


session_id=0

try:
  f=open('session_id','r')
  session_id=int(f.read())
  f.close()
except OSError:
  print("file non aperto")

print("old session id:", session_id)      
session_id=(session_id + 1)%100

try:
  f= open('session_id', 'w')
  f.write(str(session_id))
  f.close()
except OSError:
  print("non riesco a scrivere")

print("new session id:", session_id)
    
    #


#led_pin=Pin(0,Pin.OUT)
led_pin = machine.PWM(machine.Pin(0), freq=4)

#aperture file json
with open('config.json') as file:
  CONFIG = json.load(file)
#print(CONFIG,CONFIG["ssid"])

#INPUT FEATURES SENSOR
type_IN= CONFIG["type_IN"] #PULL_UP or IN
type_EDGE =CONFIG["type_EDGE"] #'RISING' or 'FALLING' or ['RISING','FALLING'] 
period_edge_control_ms= CONFIG["period_edge_control_ms"] #ogni quanto verifico fronte
led_on_time_ms= CONFIG["led_on_time_ms"] #durata accensione led'''

with open('config.json') as file:
  CONFIG = json.load(file)
#print(CONFIG,CONFIG["ssid"])

#CONNECT WI-FI
ssid = CONFIG["ssid"]
password = CONFIG["password"]
mqtt_server = CONFIG["mqtt_server"]
#EXAMPLE IP ADDRESS
client_id = ubinascii.hexlify(machine.unique_id())
#mqtt_user=b'admin'
mqtt_user= CONFIG["mqtt_user"]
mqtt_password= CONFIG["mqtt_password"]
topic_pub= CONFIG["topic_pub"]
type_SENSOR= CONFIG["type_SENSOR"]
#message value
value_0_stato_attuale=CONFIG["value_0_stato_attuale"]
value_1_stato_attuale=CONFIG["value_1_stato_attuale"]

topic_connect= str(topic_pub) + "/" + str(type_SENSOR) + "/" + client_id.decode('ascii') + "/CONNECTED"
topic_disconnect= str(topic_pub) + "/" + str(type_SENSOR) + "/" + client_id.decode('ascii') + "/DISCONNECTED"
topic_value= str(topic_pub) + "/" + str(type_SENSOR) + "/" + client_id.decode('ascii') + "/VALUE"

last_value=-1

def broadcast(topic,msg):
  if topic == b'NOCTUA/BROADCAST' and msg == b'PING':
    print("rispondo al ping, con session_id:", session_id, "e stato attuale:", last_value)
    value="CONNECTED"
    payload={"session-id": session_id, "value": value}
    c.publish(topic_connect,json.dumps(payload)) #converte qualsiasi oggetto in una stringa in formatoJSON
    if last_value==0:
      value=value_0_stato_attuale
      payload={"session-id": session_id, "value": value}
      c.publish(topic_value,json.dumps(payload)) #converte qualsiasi oggetto in una stringa in formatoJSON 
    elif last_value==1:
      value=value_1_stato_attuale
      payload={"session-id": session_id, "value": value}
      c.publish(topic_value,json.dumps(payload)) #converte qualsiasi oggetto in una stringa in formatoJSON




last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

i=0
led_pin.duty(512)
while station.isconnected() == False:
  utime.sleep_ms(1000)

  print("trying to connect")
  i=i+1
  if i>=30:
    led_pin.deinit()
    led_pin=Pin(0,Pin.OUT)
    raise Exception

led_pin.deinit()
led_pin=Pin(0,Pin.OUT)
print('Connection successful')
print(station.ifconfig())

#definizione client
c = MQTTClient(client_id, mqtt_server,user=mqtt_user,password=mqtt_password,keepalive=5) #keep live in sec
value="DISCONNECTED"
payload={"session-id": session_id, "value": value}

c.set_last_will(topic_disconnect,json.dumps(payload))
c.set_callback(broadcast)
c.connect()

value="CONNECTED"
payload={"session-id": session_id, "value": value}
c.publish(topic_connect,json.dumps(payload)) #converte qualsiasi oggetto in una stringa in formatoJSON 
c.subscribe("NOCTUA/BROADCAST")