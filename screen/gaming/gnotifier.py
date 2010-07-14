
from screen.layout import HLayout
from screen.widgetwrapper import Frame

class GNotifier(Frame):
	def __init__(self,*args,**kwargs):
		kwargs['fill']=160,160,160
		kwargs['layout']=HLayout
		Frame.__init__(self,*args,**kwargs)