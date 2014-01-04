
from RadiopieModule import RadiopieModule
import logging

log = logging.getLogger("radiopie")

class GoogleMusic(RadiopieModule):
	@staticmethod
	def getName():
		return "Google Music"
