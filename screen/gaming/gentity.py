

class GEntity:
	instances={}
	def __init__(self,conf):
		#must have a model beforehands
		if not hasattr(self,'p3dobject'):
			raise Exception('must setup a p3dobject before calling Entity.__init__() !')
		self.p3dobject.setPythonTag('eid',conf['eid'])
		self.p3dobject.setPythonTag('ref',self)
		self.eid=conf['eid']
		self.instances[self.eid]=self
		
	def __del__(self):
		self.p3dobject.clearPythonTag('ref')
		self.p3dobject.destroy()
		del self.instances[self.eid]