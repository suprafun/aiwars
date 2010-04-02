import socket
import threading
import struct


class ClientData:
	def __init__(self, id, connection, address):
		self.id = id
		self.connection = connection
		self.address = address
		
		self.thread = None
		self.onDataReceived = None
		
		self.__listenForData = False
	#
	
	# Start listening for data from this clients connection. Will call the onDataReceived callback when data comes in.
	# This function does not block.
	def listenForData(self, onDataReceived):
		if self.__listenForData:
			return
		
		self.thread = threading.Thread(target = self.__listen)
		self.onDataReceived = onDataReceived
		
		self.thread.start()
	#
	
	# Stop listening for data.
	def stopListeningForData(self):
		self.__listenForData = False
	#
	
	def __listen(self):
		self.__listenForData = True
		
		while self.__listenForData:
			data = self.connection.recv(4096)
			self.onDataReceived(self, data)
	#
	
	# Sends a message to this client. A sizeof unsigned integer will be prepended.
	def sendMessage(self, message):
		self.connection.send(struct.pack('>I', len(message)) + message)
	#
#