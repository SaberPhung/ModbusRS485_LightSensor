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
 
import unittest
import json
import sys
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

class testClient(unittest.TestCase):
	data = json.load(open(sys.argv[1]))
	username = data["username"]
	password = data["password"]
	deviceId = data["deviceId"]
	baseurl = data["baseurl"]
	c = client(baseurl, username, password)
	def testGetDevice(self):	
		d = self.c.getdevice(self.deviceId)
		self.assertIsNotNone(d)
		self.assertIsNotNone(d.get_name())
		self.assertIsNotNone(d.get_createdAt())
		self.assertIsNotNone(d.get_manufacturer())
		self.assertIsNotNone(d.get_href())
		self.assertEqual(d.get_deviceId(), self.deviceId)
	def testRegisterDevice(self):
		devicename = "Johan"
		manufacturer = "Wapice"
		type = "employee"
		d = device()
		d.set_name(devicename)
		d.set_manufacturer(manufacturer)
		d.set_type(type)
		d.set_attributes(deviceattribute("py","thon"), deviceattribute("iot","ticket"), deviceattribute("a","b"))
		
		d = self.c.registerdevice(d)
		self.assertIsInstance(d, device)
		self.assertIsNotNone(d)
		self.assertIsNotNone(d.get_name())
		self.assertIsNotNone(d.get_createdAt())
		self.assertIsNotNone(d.get_manufacturer())
		self.assertIsNotNone(d.get_deviceId())
		self.assertIsNotNone(d.get_href())
		self.assertEqual(3, len(d.get_attributes()))
	def testGetDevices(self):
		d = self.c.getdevices(10, 0)
		self.assertTrue(d.get_fullSize() >=1)
		self.assertEqual(d.get_limit(), 10)
		self.assertEqual(d.get_offset(), 0)
	def testGetAllQuota(self):
		d = self.c.getallquota()
		self.assertIsNotNone(d)
		self.assertIsNotNone(d.totalDevices)
		self.assertIsNotNone(d.maxNumberOfDevices)
		self.assertIsNotNone(d.maxDataNodePerDevice)
		self.assertIsNotNone(d.usedStorageSize)
		self.assertIsNotNone(d.maxStorageSize)
	def testDeviceQuota(self):
		d = self.c.getdevicequota(self.deviceId)
		self.assertIsNotNone(d)
		self.assertIsNotNone(d.totalRequestToday)
		self.assertIsNotNone(d.maxReadRequestPerDay)
		self.assertIsNotNone(d.numberOfDataNodes)
		self.assertIsNotNone(d.storageSize)
		self.assertEqual(d.deviceId, self.deviceId)
	def testWriteData(self):
		nv = datanodesvalue()
		nv.set_name("Arm No")
		nv.set_path("armno")
		nv.set_dataType("double")
		nv.set_value(2.0)
		nv1 = datanodesvalue()
		nv1.set_name("Leg No")
		nv1.set_path("legno")
		nv1.set_dataType("double")
		nv1.set_value(2.0)
		
		d = self.c.writedata(self.deviceId, nv, nv1)		
		self.assertIsNotNone(d)
		self.assertEqual(2, d.totalWritten)
		self.assertEqual(2, len(d.resultlist))
	def testReadData(self):
		cr = criteria()
		cr.set_criterialist("Speakers (Logitech USB Headset H340)")
		fd = "2016-03-22 17:22:30"
		td = "2016-03-22 17:22:40"
		
		d = self.c.readdata(self.deviceId, cr, fd, td)
		self.assertIsNotNone(d)
		self.assertEqual(1, len(d.datanodeslist))
if __name__ == "__main__":
	unittest.main()