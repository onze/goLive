import widget

class HLayout:
	@staticmethod
	def validate(container):
		'''c the container'''
		if len(container.children)==0:return
#		print '================'
#		print 'HLayout.validate(',container,')'
		#set size
		#stat about content
		shared=0.
		requested=0.
		for child in container.children:
			if child.pref_w==widget.Widget.SHARED:
				shared+=1
			else:
				requested+=child.pref_w
		left=container.w-requested
		#enough room for everyone
		if left>=0:
			for child in container.children:
				if child.pref_w==widget.Widget.SHARED:
					child.size=left/shared,container.h
				else:
					child.size=child.pref_w,container.h
		#set pos (relative to the container)
		curr_x=0
		curr_y=0
		for child in container.children:
			child.pos=curr_x,curr_y
			curr_x+=child.w
		#debug
#		for child in container.children:
#			print child

class VLayout:
	@staticmethod
	def validate(container):
		'''c the container'''
		if len(container.children)==0:return
#		print '================'
#		print 'VLayout.validate(',container,')'
		#set size
		#stat about content
		shared=0.
		requested=0.
		for child in container.children:
			if child.pref_h==widget.Widget.SHARED:
				shared+=1
			else:
				requested+=child.pref_h
		left=container.h-requested
		#enough room for everyone
		if left>=0:
			for child in container.children:
				if child.pref_h==widget.Widget.SHARED:
					child.size=container.w,left/shared
				else:
					child.size=container.w,child.pref_h
		#set pos (relative to the container)
		curr_x=0
		curr_y=0
		for child in container.children:
			child.pos=curr_x,curr_y
			curr_y+=child.h
		#debug
#		for child in container.children:
#			print child