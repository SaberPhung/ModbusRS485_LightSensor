#lib
import json
import sys
import time
import random
import serial
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

port = serial.Serial('COM7', baudrate = 9600, timeout=1);
global received;
port.close();

#main

#data = json.load(open(sys.argv[1]))
data = json.load(open("demo/config.json"))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]

c = Client(baseurl, username, password)

def send_data_to_iot_ticket(value):
    print("WRITE DEVICE DATANODES FUNTION.")
    listofvalues=[]
    nv = datanodesvalue()
    nv.set_name("LUX") #needed for writing datanode
    nv.set_path("lux")
    nv.set_dataType("double")
    nv.set_unit("lx")
    nv.set_value(value) #needed for writing datanode
    nv.set_timestamp(time.time()*1000)
    listofvalues.append(nv)
    print(c.writedata(deviceId, *listofvalues)) # another way to make this would be c.writedata(deviceId, nv, nv1)
    print("END WRITE DEVICE DATANODES FUNCTION")
    print("-------------------------------------------------------\n")

def modbus_request(hexadecimal_string):
        #01 04 00 01 00 01 60 0A
        #https://rapidscada.net/modbus/ModbusParser.aspx
    print("request",hexadecimal_string);
    port.open();
    port.write(hexadecimal_string);
    received=port.read(8);
    print("respond",received);
    value=((received[3]<<8)|received[4])&0xffff; #adc value to real value
    time.sleep(1);
    port.close();
    return value;

while True:
    hexadecimal_string=[0x0b,0x04,0x00,0x01,0x00,0x01,0x60,0xA0]
    value=modbus_request(hexadecimal_string)*10/10
    print(value,"LUX")
    send_data_to_iot_ticket(value); 
    time.sleep(10);
