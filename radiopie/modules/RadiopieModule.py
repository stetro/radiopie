import threading
import logging

log = logging.getLogger("radiopie")

class RadiopieModule(threading.Thread):
	def __init__(self, lcd):
		super(RadiopieModule, self).__init__()
		self._lcd = lcd
		self._terminate = threading.Event()
		self._ok = threading.Event()
		self._right = threading.Event()
		

	def left(self):
		raise NotImplementedError

	def right(self):
		self._right.set()

	def ok(self):
		self._ok.set()

	@staticmethod
	def getName():
		raise NotImplementedError

