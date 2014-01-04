from lcdproc.server import Server
import logging

log = logging.getLogger("radiopie")

class LCDController:
	def __init__(self):
		print "Setting up lcdproc client ..."
		self.__lcdServer = Server(hostname="localhost")
		self.__lcdServer.start_session()
		self.__screen = self.__lcdServer.add_screen("Radio")
		self.__screen.set_heartbeat("off")
		self.__first = self.__screen.add_scroller_widget("artist",text="",left=5, top=1, right=12, bottom=2,speed=5, direction="h")
		self.__last = self.__screen.add_scroller_widget("title",text="",left=5, top=2, right=12, bottom=2,speed=5, direction="h")

	def setFirst(self, text):
		self.__first.set_text(text)
		log.info("LCD - First: " + text)
	
	def setLast(self, text):
		self.__last.set_text(text)
		log.info("LCD -  Last: " + text)

