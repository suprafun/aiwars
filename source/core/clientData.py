import socket
import threading
import struct


class ClientData:
	def __init__(self, id, connection, address):
		self.id = id
		self.connection = connection
		self.address = address
		print connection, address
		
		self.thread = None
		self.onMessageReceived = None
		
		self.__listenForData = False
		self.__dataBuffer = ''
		
		self.connection.setblocking(1)
	#
	
	# Start listening for data from this clients connection. Will call the onDataReceived callback when data comes in.
	# This function does not block.
	def listenForData(self, onMessageReceived):
		if self.__listenForData:
			return
		
		self.thread = threading.Thread(target = self.__listen)
		self.thread.setDaemon(True)
		self.onMessageReceived = onMessageReceived
		
		self.thread.start()
	#
	
	# Stop listening for data.
	def stopListeningForData(self):
		self.__listenForData = False
	#
	
	def __listen(self):
		self.__listenForData = True
		
		while self.__listenForData:
			try:
				data = self.connection.recv(4096)
			except socket.timeout:
				pass
			else:
				self.__dataBuffer += data
				
				# Check the incoming data for messages, call the callback for each individual message. If a message hasn't completely arrived yet,
				# continue waiting for the rest to come in.
				while len(self.__dataBuffer) >= 4:
					(messageSize,) = struct.unpack('>I', self.__dataBuffer[:4])
					if len(self.__dataBuffer) >= messageSize + 4:
						self.onMessageReceived(self, self.__dataBuffer[4], self.__dataBuffer[5:4 + messageSize])
						self.__dataBuffer = self.__dataBuffer[4 + messageSize:]
					else:
						break
	#
	
	# Sends a message to this client. A sizeof unsigned integer will be prepended.
	def sendMessage(self, messageType, message):
		self.connection.send(struct.pack('>I', len(messageType) + len(message)) + messageType + message)
	#
#