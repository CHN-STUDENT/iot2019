


#Hardware Platform: FireBeetle-ESP32
#Result: input MQTTlibrary and remote controls LED by mqtt communication.

from umqttsimple import MQTTClient
from machine import Pin
from machine import I2C
from machine import I2C, Pin
import lcd
import network
import time
import utime
import machine
import dht
import lcd

temperature = 0.0
humidity = 0.0
last_message = 0
message_interval = 5
state = 0
led = Pin(2, Pin.OUT, value=0)
lcd = None

def sub_cb(topic, msg):
  global state
  print((topic, msg))
  lcd.move_to(12, 1)
  if msg == b"on":
    led.value(1)
    state = 0
    lcd.putstr("ON ")
    print("1")
  elif msg == b"off":
    led.value(0)
    state = 1
    lcd.putstr("OFF")
    print("0")
  elif msg == b"toggle":
    # LED is inversed, so setting it to current state
    # value will make it toggle
    led.value(state)
    state = 1 - state
  
def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  
def connect_and_subscribe():
  global SERVER,TOPIC
  server=SERVER
  # c = MQTTClient(CLIENT_ID, server,0,username,password)     #create a mqtt client
  c = MQTTClient(CLIENT_ID, server,0)     #create a mqtt client
  c.set_callback(sub_cb)                    #set callback
  c.connect()                               #connect mqtt
  c.subscribe(TOPIC)                        #client subscribes to a topic
  print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
  return c

def close_connect():
  global wlan,c
  if(c is not None):
    c.disconnect()
  wlan.disconnect()
  wlan.active(False)

def mqtt():
  try:
    global c,d,last_message,message_interval
    c = connect_and_subscribe()
    d = dht.DHT11(machine.Pin(0))
    # lcd.blink_cursor_off()
    while True:
      lcd.move_to(0, 0)
      lcd.putstr("Be Happy :)")
      time.sleep(1)
      c.check_msg()          #wait messageW
      if (time.time() - last_message) > message_interval:
        d.measure()
        temperature = d.temperature()
        lcd.clear()
        if(temperature > 29):
          topic_hub = TOPIC + "/auto"
          c.publish(topic_hub,str("on"))
          led.value(1)
          state = 0
        else:
          topic_hub = TOPIC + "/auto"
          c.publish(topic_hub,str("off"))
          led.value(0)
          state = 1
        # print("temperature",temperature)
        humidity = d.humidity()
        lcd.move_to(0, 1)
        show = "T:" + str(temperature) + "C "
        lcd.putstr(show)
        show = "H:" + str(humidity) + "% "
        lcd.putstr(show)
        if(state == 1):
          show = "OFF"
        else:
          show = "ON"
        lcd.putstr(show)
        #lcd.putstr("Humidity:%d",humidity)
        # print("humidity",humidity)
        temperature_topic_pub = TOPIC + "/temperature"
        humidity_topic_pub = TOPIC + "/humidity"
        c.publish(temperature_topic_pub, str(temperature))
        c.publish(humidity_topic_pub, str(humidity))
        last_message = time.time()
       
  except OSError as e:
    print(e)
    restart_and_reconnect()

  finally:
    close_connect()
    
mqtt()
