
from RadiopieModule import RadiopieModule
import logging

log = logging.getLogger("radiopie")

class RadioStream(RadiopieModule):

	def run(self):
		print "test"

	@staticmethod
	def getName():
		return "Radio Streams"
