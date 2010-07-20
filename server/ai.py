
from player import Player

class AI(Player):
	def __init__(self,pid):
		self.pid=pid

	def read(self):
		'''the ai goes here, and returns the actions it wants to do to the server.'''
		yield {}

	def send(self,d):
		'''receives info about the world.'''
		pass

	def send_string(self,d):
		'''receives info about the world.'''
		pass