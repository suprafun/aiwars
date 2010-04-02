import socket
from clientData import *


class GameServer:
	def __init__(self, host, port):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((host, port))
		self.server.listen(5)
		
		self.__waitForConnections = False
		self.__clients = []
		self.__nextClientID = 0
		
		# Callbacks - these can be set by the calling code.
		self.onClientConnected = None
		self.onMessageReceivedFromClient = None
	#
	
	# A blocking call, which will call the onClientConnect callback whenever a new client connects.
	# The callback will be passed a GameServerClientData object.
	# Call stopListeningForConnections() from within the callback to make this function return.
	def listenForConnections(self):
		self.__waitForConnections = True
		
		while self.__waitForConnections:
			(connection, address) = self.server.accept()
			
			clientData = ClientData(self.__getNextClientID(), connection, address)
			
			self.__clients.append(clientData)
			if self.onClientConnected != None:
				self.onClientConnected(clientData)
			
			clientData.listenForData(self.__onMessageReceivedFromClient)
	#
	
	def __getNextClientID(self):
		self.__nextClientID += 1
		return self.__nextClientID - 1
	#
	
	# Stop listening for connections. This will make the call to listenForConnections return.
	def stopListeningForConnections(self):
		self.__waitForConnections = False
	#
	
	def __onMessageReceivedFromClient(self, clientData, messageType, message):
		if self.onMessageReceivedFromClient != None:
			self.onMessageReceivedFromClient(clientData, messageType, message)
	#
	
	
	# Sends a message to the client with the specified ID.
	def sendMessageToClient(self, clientID, message):
		client = self.__getClientByID
		if client != None:
			client.sendMessage(message)
	#
	
	def __getClientByID(self, id):
		for clientData in self.__clients:
			if clientData.id == id:
				return clientData
		return None
	#
#