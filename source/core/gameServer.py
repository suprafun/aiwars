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
		
		self.__onClientConnected = None
		self.__onMessageFromClient = {}
	#
	
	def setCallbackForMessageType(self, messageType, onMessageFromClient):
		if onMessageFromClient == None:
			del self.__onMessageFromClient[messageType]
		else:
			self.__onMessageFromClient[messageType] = onMessageFromClient
	#
	
	# A blocking call, which will call the onClientConnect callback whenever a new client connects.
	# The callback will be passed a GameServerClientData object.
	# Call stopListeningForConnections() from within the callback to make this function return.
	def listenForConnections(self, onClientConnected):
		self.__waitForConnections = True
		self.__onClientConnected = onClientConnected
		
		while self.__waitForConnections:
			(connection, address) = self.server.accept()
			
			clientData = ClientData(self.__getNextClientID(), connection, address)
			
			self.__clients.append(clientData)
			if self.__onClientConnected != None:
				self.__onClientConnected(clientData)
			
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
		if self.__onMessageFromClient.has_key(messageType):
			self.__onMessageFromClient[messageType](clientData, message)
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