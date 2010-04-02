from core.messageTypes import *


# This class emulates a function - it wraps a check around the various client command callbacks.
# If the clients player is not the active player, the command is ignored and the client is sent a
# SERVER_RESULT_NOT_YOUR_TURN message.
class ClientPlayerCheck(object):
	def __init__(self, main, callback):
		self.main = main
		self.callback = callback
	#
	
	def __call__(self, client, message):
		if self.main.controllers[client].player is self.main.game.activePlayer:
			self.callback(client, message)
		else:
			client.sendMessage(STC_RESULT, SERVER_RESULT_NOT_YOUR_TURN)
	#
#