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
import urllib.request #import request
import json #import json
import time #import time to get the current timestamp
import urllib.error as err
from iotticket.stringbuilder import StringBuilder
from iotticket.validation import validate

#classes
#device attribute class"

class deviceattribute(object):
	""" Device Attribute class content attributes of a device """
	key = ""
	value = ""
	crit = [{"key": {"max_length":255, "nullable" : False, "dataType" : str}}, {"value": {"max_length": 255, "nullable":False, "dataType" : str}}]
	def __init__(self, key="", value=""):
		self.key = key
		self.value = value
	def get_key(self):
		return self.key
	def get_value(self):
		return self.value
	def parsedata(self,data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.key != None and self.key != ""):
			sb.Append("\tkey: " + self.key + "\n")
		if(self.value != None and self.value != ""):
			sb.Append("\tvalue: " + self.value + "\n")
		return str(sb)
# device class	

class device(object):
	""" Device Class contain infomation of a device. It has get-set methods to handle attributes of class"""
	crit = [{"name": {"max_length":100, "nullable" : False, "dataType" : str}}, {"manufacturer": {"max_length": 100, "nullable" : False, "dataType" : str}}, {"type": {"max_length": 100, "dataType" : str}}, {"description" : {"max_length" : 255, "dataType" : str}}, {"attributes":{"max_length" : 50}}]
	attributeslist = []			
	j_list = []	
	name = ""
	manufacturer = ""
	type = ""
	description = ""
	createdAt = ""
	deviceId = ""
	href = ""
	enterpriseId=""
	attributes = None
	def __init__(self, name = "", manufacturer = "", type = "", description = "", createdAt = "", deviceId = "", href = "", attributes = None,enterpriseId=""):
		self.name = name
		self.manufacturer = manufacturer
		self.type = type
		self.description = description
		self.createdAt = createdAt
		self.deviceId = deviceId
		self.href = href
		self.attributes = attributes
		self.enterpriseId=enterpriseId
	def parsedata(self, data):
		self.__dict__ = data	
		#check if device has attribute			
		if "attributes" not in data:
			self.attributes = None
			self.attributeslist = []	
		else:	
			if (len(self.attributeslist) > 0):
				self.attributeslist = []
			for n in data["attributes"]:
				da = deviceattribute()
				da.parsedata(n)
				self.attributeslist.append(da)
	def __str__(self):
		sb = StringBuilder()
		if(self.name != None and self.name != ""):
			sb.Append("name: ")
			sb.Append(self.name)
			sb.Append("\n")
		if(self.manufacturer != None and self.manufacturer != ""):
			sb.Append("manufacturer: ")
			sb.Append(self.manufacturer)
			sb.Append("\n")	
		if(self.type != None and self.type != ""):
			sb.Append("type: ")
			sb.Append(self.type)
			sb.Append("\n")	
		if(self.description != None and self.description != ""):
			sb.Append("description: ")
			sb.Append(self.description)
			sb.Append("\n")	
		if(self.createdAt != None and self.createdAt != ""):
			sb.Append("createdAt: ")
			sb.Append(self.createdAt)
			sb.Append("\n")	
		if(self.deviceId != None and self.deviceId != ""):
			sb.Append("deviceId: ")
			sb.Append(self.deviceId)
			sb.Append("\n")
		if (self.enterpriseId != None and self.enterpriseId != ""):
			sb.Append("EnterpriseId: ")
			sb.Append(self.enterpriseId)
			sb.Append("\n")
		if(self.href != None and self.href != ""):
			sb.Append("href: ")
			sb.Append(self.href)
			sb.Append("\n")	
		if(self.attributeslist != None and len(self.attributeslist) > 0):			
			sb.Append("attributes: \n")
			for da in self.attributeslist:
				sb.Append(str(da))
			sb.Append("\n")

		return str(sb)
	def set_name(self, new_name):
		self.name = new_name
	def get_name(self):
		return self.name
	def set_manufacturer(self, new_manufacturer):
		self.manufacturer = new_manufacturer
	def get_manufacturer(self):
		return self.manufacturer
	def set_type(self, new_type):
		self.type = new_type
	def get_type(self):
		return self.type
	def set_description(self, new_description):
		self.description = new_description
	def get_description(self):
		return self.description
	def get_createdAt(self):
		return self.createdAt
	def get_deviceId(self):
		return self.deviceId
	def get_href(self):
		return self.href
	def set_attributes(self, *new_deviceattribute):
		for a in new_deviceattribute:
			if(validate(a)):
				j_data = {"key":a.key,"value":a.value}
				self.j_list.append(j_data)
				self.attributes = self.j_list
			else:
				print("Attribute : ", a , " is not valid.")
	def get_attributes(self):
		return self.attributeslist
	def set_enterpriseId(self, new_enterpriseId):
		self.enterpriseId = new_enterpriseId
	def get_enterpriseId(self):
		return self.enterpriseId
#devices class
class devices(object):	
	""" Devices class content list of device. It will return list of device object."""
	fullSize = 0
	limit = 0
	offset = 0
	items = None
	deviceslist = []
	def __init__(self, fullSize = 0, limit = 0, offset = 0, items = None):
		self.fullSize = fullSize
		self.limit = limit
		self.offset = offset
		self.items = items
	def parsedata(self, data):
		self.__dict__ = data
		if "items" not in data:
			self.items = None
			self.deviceslist = []
		else:	
			for n in data["items"]:
				d = device()
				d.parsedata(n)
				self.deviceslist.append(d)	
	def __str__(self):
		sb = StringBuilder()
		if(self.fullSize != None and self.fullSize != 0):
			sb.Append("fullSize: ")
			sb.Append(str(self.fullSize))
			sb.Append("\n")	
		if(self.limit != None and self.limit != 0):
			sb.Append("limit: ")
			sb.Append(str(self.limit))
			sb.Append("\n")			
		if(self.offset != None and self.offset != 0):
			sb.Append("offset: ")
			sb.Append(str(self.offset))
			sb.Append("\n")
		if(self.deviceslist != None and len(self.deviceslist) > 0):			
			sb.Append("deviceslist: \n")
			for d in self.deviceslist:
				sb.Append(str(d))
				sb.Append("\n")	
		return str(sb)
	def get_fullSize(self):
		return self.fullSize
	def get_limit(self):
		return self.limit
	def get_offset(self):
		return self.offset
#datanode class
class datanode(object):	
	""" Contain datanode information."""
	unit = ""
	dataType = ""
	href = ""
	name = ""
	path = ""
	def __init__(self, unit = "", dataType = "", href = "", name = "", path = ""):
		self.unit = unit
		self.dataType = dataType
		self.href = href
		self.name = name
		self.path = path
	def parsedata(self, data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.name != None and self.name != ""):
			sb.Append("\tname: " + self.name + "\n")
		if(self.unit != None and self.unit != ""):
			sb.Append("\tunit: " + self.unit + "\n")
		if(self.dataType != None and self.dataType != ""):
			sb.Append("\tdataType: " + self.dataType + "\n")
		if(self.href != None and self.href != ""):
			sb.Append("\thref: " + self.href + "\n")		
		if(self.path != None and self.path != ""):
			sb.Append("\tpath: " + self.path + "\n")
		return str(sb)
#datanodes class
class datanodes(object):
	""" Contain list of datanode value. It will be used when getdatanodelist function is called."""
	fullSize = 0
	limit = 0
	offset = 0
	items = None
	datanodelist = []
	def __init__(self, fullSize = 0, limit = 0, offset = 0, items = None):
		self.fullSize = fullSize
		self.limit = limit
		self.offset = offset
		self.items = items
	def parsedata(self, data):
		self.__dict__ = data
		if "items" not in data:
			self.items = None
			self.datanodelist = []
		else:	
			for n in data["items"]:
				dn = datanode()
				dn.parsedata(n)
				self.datanodelist.append(dn)
	def __str__(self):
		sb = StringBuilder()
		if(self.fullSize != None and self.fullSize != 0):
			sb.Append("fullSize: ")
			sb.Append(str(self.fullSize))
			sb.Append("\n")	
		if(self.limit != None and self.limit != 0):
			sb.Append("limit: ")
			sb.Append(str(self.limit))
			sb.Append("\n")			
		if(self.offset != None and self.offset != 0):
			sb.Append("offset: ")
			sb.Append(str(self.offset))
			sb.Append("\n")
		if(self.datanodelist != None and len(self.datanodelist) > 0):			
			sb.Append("datanodelist: \n")
			for dn in self.datanodelist:
				sb.Append(str(dn))
				sb.Append("\n")
		sb.Append("\n")			
		return str(sb)	
#datanodes value and timestamp class
class vts(object):
	""" Contain the actual value of the datanode. It's used to read datanode value."""
	crit = [{"v": {"nullable" : False, "dataType" : float}}]
	v = 0
	ts = 0
	def __init__(self, v=0, ts=0):
		self.v = v
		self.ts = ts
	def get_value(self):
		return self.v
	def get_timestamp(self):
		return self.ts
	def parsedata(self,data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.v != None and self.v != 0):
			sb.Append("\tv: " + str(self.v) + "\n")
		if(self.ts != None and self.ts != 0):
			sb.Append("\tts: " + str(self.ts) + "\n")
		return str(sb)
#datanodes value class
class datanodesvalue(object):
	""" Contain datanode infomation and list of datanode value depends on how the url is passed."""
	crit = [{"name": {"max_length":100, "nullable" : False, "dataType" : str}}, {"unit": {"max_length": 10, "dataType" : str}}, {"path": {"max_length": 1000, "regex" : "(\\/[a-zA-Z0-9_]+){0,10}$", "dataType" : str}},{"v": {"nullable" : False, "dataType" : "multi"}}]
	unit = ""
	dataType = ""
	href = ""
	name = ""
	path = ""
	v = 0
	ts = 0
	values = None
	valueslist = []			
	j_list = []	
	def __init__(self, unit = "", dataType = "", name = "", path = "", values = None, v= 0, ts= int(round(time.time() * 1000))):
		self.unit = unit
		self.dataType = dataType
		self.name = name
		self.path = path
		self.values = values
		self.v = v
		self.ts = ts		
	def parsedata(self, data):
		self.__dict__ = data
		if "values" not in data:
			self.values = None
			self.valueslist = []
		else:	
			if (len(self.valueslist) > 0):
				self.valueslist = []
			for n in data["values"]:
				da = vts()
				da.parsedata(n)
				self.valueslist.append(da)		
	def set_name(self, new_name):
		self.name = new_name
	def get_name(self):
		return self.name
	def set_unit(self, new_unit):
		self.unit = new_unit
	def get_unit(self):
		return self.unit
	def set_dataType(self, new_dataType):
		self.dataType = new_dataType
	def get_dataType(self):
		return self.dataType
	def set_path(self, new_path):
		if( new_path.startswith("/")):
			self.path = new_path
		elif new_path == "": 
			self.path = ""
		else:
			self.path = "/" + new_path
	def get_path(self):
		return self.path
	def set_values(self, *new_value):
		for a in new_value:
			j_data = {"v":a.v,"ts":a.ts}
			self.j_list.append(j_data)
			self.values = self.j_list
	def get_values(self):
		return self.valueslist	
	def set_value(self, v):
		self.v = v
	def get_value(self):
		return self.v
	def set_timestamp(self, ts):
		self.ts = ts
	def get_timstamp(self):
		return self.ts
	def __str__(self):
		sb = StringBuilder()
		if(self.name != None and self.name != ""):
			sb.Append("\tname: " + self.name + "\n")
		if(self.unit != None and self.unit != ""):
			sb.Append("\tunit: " + self.unit + "\n")
		if(self.dataType != None and self.dataType != ""):
			sb.Append("\tdataType: " + self.dataType + "\n")	
		if(self.href != None and self.href != ""):
			sb.Append("\thref: " + self.href + "\n")		
		if(self.path != None and self.path != ""):
			sb.Append("\tpath: " + self.path + "\n")
		if(self.valueslist != None and len(self.valueslist) > 0):			
			sb.Append("values: \n")
			for da in self.valueslist:
				sb.Append(str(da))
				sb.Append("\n")	
		return str(sb)
#datanodes value list class
class datanodesvaluelist(object):
	""" Contain a list of datanode. Usually it will return only one datanodevalue object, but it can also return a list of datanodevalue object if you have the same datanode name with different path."""	
	href = ""
	datanodeslist = []
	j_list = []
	def __init__(self, href="", datanodeReads = None):
		self.href = href
		self.datanodeReads = datanodeReads
	def parsedata(self, data):
		self.__dict__ = data
		if "datanodeReads" not in data:
			self.datanodeReads = None
			self.datanodeslist = []	
		else:	
			if (len(self.datanodeslist) > 0):
				self.datanodeslist = []
			for n in data["datanodeReads"]:
				da = datanodesvalue()
				da.parsedata(n)
				self.datanodeslist.append(da)
	def __str__(self):
		sb = StringBuilder()
		if(self.href != None and self.href != ""):
			sb.Append("href: ")
			sb.Append(self.href)
			sb.Append("\n")		
		if(self.datanodeslist != None and len(self.datanodeslist) > 0):			
			sb.Append("datanodeslist: \n")
			for da in self.datanodeslist:
				sb.Append(str(da))
				sb.Append("\n")	
		return str(sb)
	def set_href(self, new_href):
		self.href = new_href
	def get_href(self):
		return self.href	
	def set_datanodereads(self, *new_datanoderead):
		for a in new_datanoderead:
			j_data = {"dataType":a.dataType,"unit":a.unit, "name":a.name, "path":a.path, "v":a.v, "ts":a.ts}
			self.j_list.append(j_data)
			self.datanodeReads = self.j_list
	def get_attributes(self):
		return self.datanodeslist
#criteria class
class criteria(object):
	""" Contain the criteria to pass to the url as argument to get datanode value."""
	criterialist = []
	def set_criterialist(self, *criterialist):
		for cr in criterialist:
			if(type(cr)==str):
				self.criterialist.append(cr)
			else:
				self.criterialist.append(str(cr))
	def get_criterialist(self):
		return self.criterialist
#quota class
class quota(object):
	""" Contain quota infomation."""
	totalDevices = None
	maxNumberOfDevices = None
	maxDataNodePerDevice = None
	usedStorageSize = None
	maxStorageSize = None
	def parsedata(self, data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.totalDevices != None):
			sb.Append("totalDevices: " + str(self.totalDevices) + "\n")
		if(self.maxNumberOfDevices != None):
			if(self.maxNumberOfDevices > 0):
				sb.Append("maxNumberOfDevices: " + str(self.maxNumberOfDevices) + "\n")
			else:
				sb.Append("maxNumberOfDevices: " + "Unlimit" + "\n")
		if(self.maxDataNodePerDevice != None):
			if(self.maxDataNodePerDevice > 0):			
				sb.Append("maxDataNodePerDevice: " + str(self.maxDataNodePerDevice) + "\n")
			else:
				sb.Append("maxDataNodePerDevice: " + "Unlimit" + "\n")
		if(self.usedStorageSize != None):
			sb.Append("usedStorageSize: " + str(self.usedStorageSize) + "\n")
		if(self.maxStorageSize != None):
			if(self.maxStorageSize > 0):
				sb.Append("maxStorageSize: " + str(self.maxStorageSize) + "\n")
			else:
				sb.Append("maxStorageSize: " + "Unlimit" + "\n")
		return str(sb)
#device quota class
class devicequota(object):
	""" Contain device quota information."""
	totalRequestToday = None
	maxReadRequestPerDay = None
	deviceId = None
	numberOfDataNodes = None
	storageSize = None
	def parsedata(self, data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.totalRequestToday != None):
			sb.Append("totalRequestToday: " + str(self.totalRequestToday) + "\n")
		if(self.maxReadRequestPerDay != None):
			if(self.maxReadRequestPerDay > 0):
				sb.Append("maxReadRequestPerDay: " + str(self.maxReadRequestPerDay) + "\n")
			else:
				sb.Append("maxReadRequestPerDay: " + "Unlimit" + "\n")
		if(self.deviceId != None):
			sb.Append("deviceId: " + self.deviceId + "\n")
		if(self.numberOfDataNodes != None):
			sb.Append("numberOfDataNodes: " + str(self.numberOfDataNodes) + "\n")
		if(self.storageSize != None):
			sb.Append("storageSize: " + str(self.storageSize) + "\n")	
		return str(sb)
#error info class
class errorinfo(Exception):
	""" Contain the error response returned by the Server. When it is 404, the description and code will be stored with the value get from the header error response. Usually description: Not found, code: 404"""
	description = ""
	code = 0
	moreInfo = ""
	apiver = 0
	__httpstatus = None
	def __init__(self, description = "", code = 0, moreInfo = "https://my.iot-ticket.com/api/v1/errorcodes", apiver = 1):
		self.description = description
		self.code = code
		self.moreInfo = moreInfo
		self.apiver = apiver
	def parsedata(self, data):
		self.__dict__ = data
	def get_httpstatus(self):
		return self.__httpstatus
	def set_httpstatus(self, new_httpstatus):
		self.__httpstatus = new_httpstatus
	def __str__(self):
		sb = StringBuilder()
		if(self.description != None and self.description != ""):
			sb.Append("ERROR:\n")
			sb.Append("\tdescription: ")
			sb.Append(self.description)
			sb.Append("\n")	
		if(self.code != None and self.code != 0):
			sb.Append("\tcode: ")
			sb.Append(str(self.code))
			sb.Append("\n")			
		if(self.moreInfo != None and self.moreInfo != ""):
			sb.Append("\tmoreInfo: ")
			sb.Append(self.moreInfo)
			sb.Append("\n")
		if(self.apiver != None and self.apiver != 0):
			sb.Append("\tapiver: ")
			sb.Append(str(self.apiver))
			sb.Append("\n")	
		return str(sb)			
#class write result
class writeresult(object):
	""" Contain the result returned by the server when write datanode to server."""
	href = None
	writtenCount = None
	def __init__(self, href=None, writtenCount=None):
		self.href = href
		self.writtenCount = writtenCount
	def parsedata(self,data):
		self.__dict__ = data
	def __str__(self):
		sb = StringBuilder()
		if(self.href != None):
			sb.Append("\thref: " + self.href + "\n")
		if(self.writtenCount != None):
			sb.Append("\twrittenCount: " + str(self.writtenCount) + "\n")
		return str(sb)
#class datanode write result
class writeresults(object):
	""" Contain list of result returned by the server."""
	totalWritten = None
	writeResults = None
	resultlist = []		
	j_list = []		
	def parsedata(self, data):
		self.__dict__ = data	
		#check if device has attribute			
		if "writeResults" not in data:
			self.writeResults = None
			self.resultlist = []	
		else:	
			if (len(self.resultlist) > 0):
				self.resultlist = []
			for n in data["writeResults"]:
				da = writeresult()
				da.parsedata(n)
				self.resultlist.append(da)
	def __str__(self):
		sb = StringBuilder()	
		if(self.totalWritten != None):
			sb.Append("totalWritten: ")
			sb.Append(str(self.totalWritten))
			sb.Append("\n")	
		if(self.resultlist != None and len(self.resultlist) > 0):			
			sb.Append("writeResults: \n")
			for da in self.resultlist:
				sb.Append(str(da))
			sb.Append("\n")	
		return str(sb)			