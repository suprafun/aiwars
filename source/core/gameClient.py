import socket


class GameClient:
	def __init__(self):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.__listenForData = False
	#
	
	# Connect to the server at the specified host and port.
	def connectToServer(self, host, port):
		self.connection.connect((host, port))
	#
	
	# Start listening for data. This is a blocking call. The onDataReceived callback will be called whenever data comes in.
	# Call stopListeningForData() from within the callback to make this function return.
	def listenForData(self, onDataReceived):
		if self.__listenForData:
			return
		
		self.__listenForData = True
		while self.__listenForData:
			data = self.connection.recv(4096)
			onDataReceived(data)
	#
	
	# Stops listening for data.
	def stopListeningForData(self):
		self.__listenForData = False
	#
	
	# Sends a message to the server. The message is assumed to be properly formatted - this function will not alter the message in any way.
	def sendMessageToServer(self, message):
		self.connection.send(message)
	#
#