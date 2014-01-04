import threading
import logging

log = logging.getLogger("radiopie")

class RadiopieModule(threading.Thread):
	def __init__(self):
		super(RadiopieModule, self).__init__()
		

	def left(self):
		raise NotImplementedError

	def right(self):
		raise NotImplementedError

	def ok(self):
		raise NotImplementedError

	@staticmethod
	def getName():
		raise NotImplementedError
	
	def stop(self):
		super(RadiopieModule, self).stop()
