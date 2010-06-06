from direct.fsm import FSM
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from panda3d.core import ConfigVariableInt,ConfigVariableDouble,ConfigVariableString,ConfigVariableBool

class Console(FSM.FSM):
	def __init__(self,print_messenger_events=False):
		FSM.FSM.__init__(self,'console.fsm')
		self.defaultTransitions={'Closed':['Open'],'Open':['Closed']}
		self.lines=[]
		#
		self.textObject=OnscreenText(text='',pos=(-1.55,.85),scale=0.04,align=TextNode.ALeft)
		self.textObject.setFg((.95,.95,.95,.6))
		self.textObject.setBg((.50,.50,.50,.5))
		self.max_rows=15
		#when true, prints panda messenger events traffic
		self.print_messenger=print_messenger_events
		self.out('console ready.')

	def enterClosed(self):
		self.accept(ConfigVariableString('console-trigger').getValue(),self.demand,extraArgs=['Open'])
		self.textObject.textNode.setOverallHidden(True)

	def enterOpen(self):
		self.accept(ConfigVariableString('console-trigger').getValue(),self.demand,extraArgs=['Closed'])
		self.textObject.textNode.setOverallHidden(False)

	def exitClosed(self):
		self.ignoreAll()

	def exitOpen(self):
		self.ignoreAll()

	def out(self,*args,**kwargs):
		line=[]
		if len(args)>0:
			line.extend([str(a)+' ' for a in args])
		if len(kwargs.keys())>0:
			line.extend([' {']+[str(k)+':'+str(kwargs[k]) for k in kwargs]+['}'])
		line=''.join(line)
		print line
		self.lines.append(line)
		self.lines=self.lines[-self.max_rows:]
		self.textObject.setText('\n'.join(self.lines))

	def get_print_messenger(self):
		return self._print_messenger

	def set_print_messenger(self,b):
		self._print_messenger=b
		if b and messenger.quiet:
			messenger.toggleVerbose()
			self.task_watch_messenger=taskmgr.add(self.watch_messenger,'Console.watch_messenger')
		else:
			messenger.toggleVerbose()
			taskMgr.remove(self.task_watch_messenger)

	def watch_messenger(self,task):
		'''
		prints out panda messenger's events traffic
		'''
		self.out(str(messenger))
		messenger.clear()
		return task.again if self._print_messenger else task.done

	print_messenger=property(get_print_messenger,set_print_messenger)

