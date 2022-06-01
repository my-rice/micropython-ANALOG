#OMNISCIENT
from umqttsimple import MQTTClient
from machine import Pin
import utime
from machine import Timer


#TODO: Da definire il pin adc
#pin_adc = 

i=0
value=30
def adc_read():
    global i
    global value
    current_value = value #= pin_adc.value() #Devo inserire il valore corrente del sensore adc
    if station.isconnected() == True:
        led_pin.value(1)
        i=i+1
        #value=30  #DA LEGGERE IL VALORE VERO
        print(i, 'Reading value',value,', publishing to topic',topic_value)
        payload={"session-id": session_id, "value": value}
        c.publish(topic_value,json.dumps(payload)) #converte qualsiasi oggetto in una stringa in formatoJSON 
        utime.sleep_ms(led_on_time_ms)
        led_pin.value(0)
    last_value=current_value
    

# tim = Timer(-1)
# tim.init(period=period_edge_control_ms, mode=Timer.PERIODIC, callback=on_click)

while True:
    adc_read()
    utime.sleep_ms(period_ms)
    if station.isconnected() == False:
        led_pin = machine.PWM(machine.Pin(0), freq=4)
        led_pin.duty(512)
        print('connection problem, trying to reconnect')
        station.connect(ssid, password)
        i = 0
        while station.isconnected() == False:
            print('trying to reconnect')
            i = i + 1

            utime.sleep_ms(1000)
            if i >= 300:
                led_pin.deinit()
                raise Exception

        print('Connection successful')
        print(station.ifconfig())

        try:
            f = open('session_id', 'r')
            session_id = int(f.read())
            f.close()
        except OSError:
            print('file non aperto')

        print ('old session id:', session_id)
        session_id = (session_id + 1) % 100

        try:
            f = open('session_id', 'w')
            f.write(str(session_id))
            f.close()
        except OSError:
            print('non riesco a scrivere')

        print ('new session id:', session_id)

        value = 'DISCONNECTED'
        payload = {'session-id': session_id, 'value': value}
        c.set_last_will(topic_disconnect, json.dumps(payload))

        c.connect()
        value = 'CONNECTED'
        payload = {'session-id': session_id, 'value': value}
        c.publish(topic_connect, json.dumps(payload))  # converte qualsiasi oggetto in una stringa in formatoJSON

        led_pin.deinit()
        led_pin = Pin(0, Pin.OUT)
    else:

        utime.sleep_ms(1000)
        try:
            c.ping()
            c.check_msg()
        except OSError:
            print ('errore dal check message PING o dal PING con il server')
