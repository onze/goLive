
from player import Player

class AI(Player):
	'''
	the AI part is a mess that will be taken care of later.
	everything has to be coded, nothing has been done, not even a proper constructor.
	'''
	def __init__(self,pid):
		self.pid=pid

	def read(self):
		'''the ai goes here, and returns the actions it wants to do to the server.'''
		yield {}

	def send(self,d):
		'''receives info about the world.'''
		pass

	def send_string(self,s):
		'''receives info about the world.'''
		pass