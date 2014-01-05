from RadiopieModule import RadiopieModule
import logging
import time
import pygst
pygst.require("0.10")
import gst
import smbus
import json

log = logging.getLogger("radiopie")

class RadioStream(RadiopieModule):

	def run(self):
		log.info("Radio started")
		self._lcd.setFirst("Radio")
		self.loadConfiguration()
		self.__position = 0
		self.__player = None
		self._lcd.setLast(self.__stations[self.__position]["name"].encode("utf-8"))
		while not self._terminate.isSet():
			if(self._ok.isSet()):
				self._ok.clear()
				self.playCurrentRadio()
			if(self._right.isSet()):
				self._right.clear()
				self.__position = (self.__position + 1) % len(self.__stations)
				self._lcd.setLast(self.__stations[self.__position]["name"].encode("utf-8"))
	
			time.sleep(1)
		self.setdown()

	def playCurrentRadio(self):
		if(self.__player == None):
			self.setup()
		else:
			self.__player.set_state(gst.STATE_NULL)
		self._lcd.setLast(self.__stations[self.__position]["name"].encode("utf-8"))
		self.__player.set_property("uri", self.__stations[self.__position]["url"].encode("utf-8"))
		self.__player.set_state(gst.STATE_PLAYING)
			
	def setup(self):
		self.__player = gst.element_factory_make("playbin2", "player")
		bus = self.__player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_status)

	def loadConfiguration(self):
		json_data = open('defaults.json')
		data = json.load(json_data)
		self.__stations = data["stations"]
		print self.__stations

	def setdown(self):
		self.__player.set_state(gst.STATE_NULL)

	def on_status(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS or t == pygst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			log.error(err)
			log.debug(debug)
			self.__player.set_state(gst.STATE_NONE)

	@staticmethod
	def getName():
		return "Radio Streams"

	def left(self):
		self._terminate.set()
