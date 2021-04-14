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
 
import re
def validate(obj):
	""" Validate function is used to check the max length, nullable and datatype of an object attribute."""
	isValid = True
	for n in obj.crit:
		for key in n:
			critlist = n[key]
			for critlistkey in critlist:
				if critlistkey == "max_length":
					if getattr(obj,key) != None:
						if len(getattr(obj,key)) > critlist[critlistkey]:
							isValid = False
				if critlistkey == "nullable":
					if critlist[critlistkey] is False:
						if(getattr(obj,key) == "" or getattr(obj,key) == None):
							isValid = False
				if critlistkey == "regex":
					if( not re.match(critlist[critlistkey], getattr(obj,key), flags = 0)):	
						isValid = False
				if critlistkey == "dataType":
					if critlist[critlistkey] == "multi":
						if obj.dataType == "string" or obj.dataType == "String":
							if not isinstance(getattr(obj,key), str):
								isValid = False
						elif obj.dataType == "Double" or obj.dataType == "double":
							if not isinstance(getattr(obj,key), float):
								isValid = False
						elif obj.dataType == "Boolean" or obj.dataType == "boolean":
							if not isinstance(getattr(obj,key), bool):
								isValid = False
						elif obj.dataType == "Long" or obj.dataType == "long":
							if not isinstance(getattr(obj,key), int):
								isValid = False
						else:
							isValid = False
					else:		
						if not isinstance(getattr(obj,key), critlist[critlistkey]):
							isValid = False
	return isValid						
				