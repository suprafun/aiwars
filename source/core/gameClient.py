import socket
import struct


class GameClient:
	def __init__(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.__listenForData = False
		self.__dataBuffer = ''
		self.__onMessageFromServer = {}
	#
	
	def setCallbackForMessageType(self, messageType, onMessageFromServer):
		if onMessageFromServer == None:
			del self.__onMessageFromServer[messageType]
		else:
			self.__onMessageFromServer[messageType] = onMessageFromServer
	#
	
	# Connect to the server at the specified host and port.
	def connectToServer(self, host, port, timeout):
		self.connection.settimeout(timeout)
		self.connection.connect((host, port))
	#
	
	# Start listening for data. This is a blocking call. If callbacks have been set for specific message types, they will be called whenever those message types come in.
	# Call stopListeningForData() from within the callback to make this function return (eventually...).
	def listenForData(self):
		if self.__listenForData:
			return
		
		self.__listenForData = True
		while self.__listenForData:
			try:
				data = self.connection.recv(4096)
			except socket.timeout:
				pass
			else:
				self.__dataBuffer += data
				
				# Check the incoming data for messages, call the type-specific callback for each individual message. If a message hasn't completely arrived yet,
				# continue waiting for the rest to come in.
				while len(self.__dataBuffer) >= 4:
					(messageSize,) = struct.unpack('>I', self.__dataBuffer[:4])
					if len(self.__dataBuffer) >= messageSize + 4:
						messageType = self.__dataBuffer[4]
						if self.__onMessageFromServer.has_key(messageType):
							self.__onMessageFromServer[messageType](self.__dataBuffer[5:4 + messageSize])
						
						self.__dataBuffer = self.__dataBuffer[4 + messageSize:]
					else:
						break
	#
	
	# Stops listening for data.
	def stopListeningForData(self):
		self.__listenForData = False
	#
	
	# Sends a message to the server. A sizeof unsigned integer will be prepended.
	def sendMessageToServer(self, messageType, message):
		self.connection.send(struct.pack('>I', len(messageType) + len(message)) + messageType + message)
	#
#