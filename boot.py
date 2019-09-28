

# boot.py

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
#import mqtt

esp.osdebug(None)
import gc
gc.collect()

SSID="ZH's PI AP"
PASSWORD="66666666"
SERVER = "192.168.4.1"
c=None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
topic = "Node" + CLIENT_ID.decode()
print(topic)
TOPIC = topic.encode()

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)         #create a wlan object
  wlan.active(True)                         #Activate the network interface
  wlan.disconnect()                         #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                 #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  print('Connection successful')
  print(wlan.ifconfig())

connectWifi(SSID,PASSWORD)
exec(open('./mqtt.py').read(),globals())







