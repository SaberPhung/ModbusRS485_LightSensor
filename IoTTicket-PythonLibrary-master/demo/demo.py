 # The MIT License (MIT)
 #
 # Copyright (c) 2016 Wapice Ltd.
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy of this
 # software and associated documentation files (the "Software"), to deal in the Software
 # without restriction, including without limitation the rights to use, copy, modify, merge,
 # publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
 # to whom the Software is furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in all copies or
 # substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
 # PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
 # FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 # OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 # DEALINGS IN THE SOFTWARE.
 
#lib
import json
import sys
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
#main

data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]

c = Client(baseurl, username, password)

#get device function demo
print("GET DEVICE FUNTION.")
print(c.getdevice(deviceId))
print("END GET DEVICE FUNCTION")
print("-------------------------------------------------------\n")
#get all device function demo
print("GET ALL DEVICES FUNTION.")
print("Get list of devices:\n" , c.getdevices(5,0))
print("END GET ALL DEVICES FUNCTION")
print("-------------------------------------------------------\n")
#get device datanode demo
print("GET DEVICE DATANODES FUNTION.")
print("Datanodes:\n" , c.getdatanodeslist(deviceId, 10, 0))
print("END GET DEVICE DATANODES FUNCTION")
print("-------------------------------------------------------\n")
#get all quota demo
print("GET ALL QUOTA FUNTION.")
print("Get all quota:\n" , c.getallquota())
print("END GET ALL QUOTA FUNCTION")
print("-------------------------------------------------------\n")
#get device quota demo
print("GET DEVICE QUOTA FUNTION.")
print(c.getdevicequota(deviceId))
print("END GET DEVICE QUOTA FUNCTION")
print("-------------------------------------------------------\n")
#create a device
d = device()
d.set_name("Johan") #needed for register
d.set_manufacturer("Wapice") #needed for register
d.set_type("employee")
d.set_description("Im trainee")
d.set_enterpriseId("E0000") #if enterprise id is not given, iotticket use default enterprise id.
d.set_attributes(deviceattribute("a","b"), deviceattribute("c","d"), deviceattribute("key","value"))
#register device demo
print("REGISTER DEVICE FUNTION.")
print(c.registerdevice(d))
print("END REGISTER DEVICE FUNCTION")
print("-------------------------------------------------------\n")
#move device demo
print("MOVE DEVICE FUNTION.")
print(c.movedevice(deviceId,"E0001")) # E0001=enterprise id of destination enterprise.
print("END MOVE DEVICE FUNCTION")
print("-------------------------------------------------------\n")
#read datanode demo
print("READ DEVICE DATANODES FUNTION.")
cr = criteria()
cr.set_criterialist("Latitude", "Longitude", "Finger No")
fd = "2016-03-22 17:22:00"
td = "2016-03-22 17:25:00"
print(c.readdata(deviceId, cr, fd, td))
print("END READ DEVICE DATANODES FUNCTION")
print("-------------------------------------------------------\n")
#write datanode demo
print("WRITE DEVICE DATANODES FUNTION.")
listofvalues=[]
nv = datanodesvalue()
nv.set_name("Arm No") #needed for writing datanode
nv.set_path("armno")
nv.set_dataType("double")
nv.set_value(2.0) #needed for writing datanode
nv1 = datanodesvalue()
nv1.set_name("Leg No") #needed for writing datanode
nv1.set_path("legno")
nv1.set_dataType("double")
nv1.set_value(2.0) #needed for writing datanode
listofvalues.append(nv)
listofvalues.append(nv1)
print(c.writedata(deviceId, *listofvalues)) # another way to make this would be c.writedata(deviceId, nv, nv1)
print("END WRITE DEVICE DATANODES FUNCTION")
print("-------------------------------------------------------\n")

	