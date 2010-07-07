
import random as random_module

def random(a=0.,b=1.):
	if type(a)==type(int()) or type(a)==type(float()):
		return a+random_module.random()*(b-a)
	elif type(a)==type(list()):
		if len(a)==0:
			return None
		else:
			return a[int(random_module.random()*len(a))]

def dist2(a,b):
	'''dist for objects that have x and y attributes'''
	return ((b.x-a.x)**2+(b.y-a.y)**2)**.5

def dist3(a,b):
	'''dist for p3dobjects (getX,getY,getZ)'''
	return ((b.getX()-a.getX())**2+(b.getY()-a.getY())**2+(b.getZ()-a.getZ())**2)**.5 

class Rectangle:
	def __init__(self,x,y,w,h):
		self.x,self.y,self.w,self.h=x,y,w,h

	def __repr__(self):
		return '<Rectangle x=%f, y=%f, w=%f, h=%f>'%(self.x,self.y,self.w,self.h)

	def hit_test(self,x,y=None):
		ret=self.x<x<self.x+self.w and self.y<y<self.y+self.h
		out(str(self)+'.hit_test('+str(x)+','+str(y)+')->'+str(ret))
		return ret
	
def pstat(func):
	try:
		from pandac.PandaModules import PStatCollector
		collectorName = "Debug:%s" % func.__name__
		if hasattr(base, 'custom_collectors'):
			if collectorName in base.custom_collectors.keys():
				pstat = base.custom_collectors[collectorName]
			else:
				base.custom_collectors[collectorName] = PStatCollector(collectorName)
				pstat = base.custom_collectors[collectorName]
		else:
			base.custom_collectors = {}
			base.custom_collectors[collectorName] = PStatCollector(collectorName)
			pstat = base.custom_collectors[collectorName]
		def doPstat(*args, **kargs):
			pstat.start()
			returned = func(*args, **kargs)
			pstat.stop()
			return returned
		doPstat.__name__ = func.__name__
		doPstat.__dict__ = func.__dict__
		doPstat.__doc__ = func.__doc__
		return doPstat
	except:
		return func