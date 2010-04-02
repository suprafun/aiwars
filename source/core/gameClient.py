import socket
import struct


class GameClient:
	def __init__(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.__listenForData = False
		self.__dataBuffer = ''
	#
	
	# Connect to the server at the specified host and port.
	def connectToServer(self, host, port):
		self.connection.connect((host, port))
	#
	
	# Start listening for data. This is a blocking call. The onMessageReceived callback will be called whenever a message comes in.
	# Call stopListeningForData() from within the callback to make this function return.
	def listenForData(self, onMessageReceived):
		if self.__listenForData:
			return
		
		self.__listenForData = True
		while self.__listenForData:
			data = self.connection.recv(4096)
			self.__dataBuffer += data
			
			# Check the incoming data for messages, call the callback for each individual message. If a message hasn't completely arrived yet,
			# continue waiting for the rest to come in.
			while len(self.__dataBuffer) >= 4:
				(messageSize,) = struct.unpack('>I', self.__dataBuffer[:4])
				if len(self.__dataBuffer) >= messageSize + 4:
					onMessageReceived(self.__dataBuffer[4:4 + messageSize])
					self.__dataBuffer = self.__dataBuffer[4 + messageSize:]
				else:
					break
	#
	
	# Stops listening for data.
	def stopListeningForData(self):
		self.__listenForData = False
	#
	
	# Sends a message to the server. A sizeof unsigned integer will be prepended.
	def sendMessageToServer(self, message):
		self.connection.send(struct.pack('>I', len(message)) + message)
	#
#