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
import threading
import datetime
import random
import json
import sys
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import vts
from iotticket.models import datanodesvalue
from iotticket.client import Client
#main
data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
deviceId = data["deviceId"]
baseurl = data["baseurl"]
class test(object):	
	c = Client(baseurl, username, password)
	cr = criteria()
	cr.set_criterialist("age", "height", "weight", "hair color", "Eye Color", "finger no", "Speakers (Logitech USB Headset H340)")
	nv = datanodesvalue()
	nv.set_name("Finger No")
	nv.set_path("fingerno")
	nv.set_dataType("double")
	def autowrite(self):
		threading.Timer(2, self.autowrite).start()		
		self.nv.set_value(round(random.uniform(0.0, 100.0),2))
		self.nv.set_timestamp(self.c.dttots(datetime.datetime.now()))
		self.c.writedata("6f8af5b13ae04c1aad2dcabb612ec028", self.nv)
		print("v: " + str(self.nv.get_value()) +"\nts: " + str(self.nv.get_timstamp()) + "\n")
t = test()
t.autowrite()		