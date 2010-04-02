import struct


# This method makes it convenient to pack multiple objects into a struct.
# It can handle booleans, integers, strings and integer lists.
def toStream(*variables):
	format = ''
	content = []
	
	for variable in variables:
		variableType = type(variable)
		
		if variableType == bool:
			format += 'B'
			content.append(variable)
		elif variableType == int:
			format += 'i'
			content.append(variable)
		elif variableType == str:
			variableLength = len(variable)
			format += 'I' + str(variableLength) + 's'
			content.append(variableLength)
			content.append(variable)
		elif variableType == list:
			variableLength = len(variable)
			format += 'I' + str(variableLength) + 'i'
			content.append(variableLength)
			content.extend(variable)
		else:
			print 'Unsupported type, can\'t write to stream!'
	
	return struct.pack(format, *content)
#

# This method reads the stream according to the expected types, in their respective order.
# For example, when called with (stream, str, int, list), it will return a tuple that contains a string, an int and a list containing integers.
def fromStream(stream, *types):
	content = []
	
	streamPos = 0
	for _type in types:
		if _type == bool:
			if struct.unpack('B', stream[streamPos:streamPos + 1])[0] == 0:
				content.append(False)
			else:
				content.append(True)
			streamPos += 1
		elif _type == int:
			streamPos = __streamPosAccountedForPadding(streamPos)
			content.append(struct.unpack('i', stream[streamPos:streamPos + 4])[0])
			streamPos += 4
		elif _type == str:
			strLength = struct.unpack('I', stream[streamPos:streamPos + 4])[0]
			streamPos += 4
			content.append(struct.unpack(str(strLength) + 's', stream[streamPos:streamPos + strLength])[0])
			streamPos += strLength
		elif _type == list:
			streamPos = __streamPosAccountedForPadding(streamPos)
			listLength = struct.unpack('I', stream[streamPos:streamPos + 4])[0]
			streamPos += 4
			content.append([])
			if listLength > 0:
				content[-1].extend(struct.unpack(str(listLength) + 'i', stream[streamPos:streamPos + listLength * 4]))
			streamPos += listLength * 4
		else:
			print 'Unsupported type, can\'t read from stream!'
	
	return content
#

def __streamPosAccountedForPadding(streamPos):
	if streamPos & 3 > 0:
		return streamPos + (4 - streamPos & 3)
	else:
		return streamPos
#