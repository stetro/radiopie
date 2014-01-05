
from gmusicapi import Webclient
from RadiopieModule import RadiopieModule
import logging, random, json, time
import pygst
pygst.require("0.10")
import gst
import smbus


log = logging.getLogger("radiopie")

class GoogleMusic(RadiopieModule):
	def run(self):
		log.info("Google Music started")
		self._lcd.setFirst(" Google")
		self.__player = None
		self.__api = None
		self.__library = None
		self.loadConfiguration()
		self.googleMusicConnection()
		while not self._terminate.isSet():
			if(self._ok.isSet()):
				self._ok.clear()
				self.playCurrentSong()
			time.sleep(1)

	def googleMusicConnection(self):
		log.info("Login as user " + self.__user + " ...")
		self._lcd.setLast("Login..")
		self.__api = Webclient()
		self.__api.login(self.__user, self.__password)
		log.info("Loading Library")
		self._lcd.setLast(" Loading")
		self.__library = self.__api.get_all_songs()
		self._lcd.setLast("Ready")

	def playCurrentSong(self):
		log.info("Playing a song")
		if(self.__player == None):
			self.setup()
		else:
			self.__player.set_state(gst.STATE_NULL)
		self.__currentsong = self.__library[random.randint(0,len(self.__library))]
		self._lcd.setLast(self.__currentsong["title"].encode("utf-8"))
		url = self.__api.get_stream_urls(self.__currentsong["id"])
		self.__player.set_property("uri", url[0])
		self.__player.set_state(gst.STATE_PLAYING)
		log.info("Playing song " + self.__currentsong["title"] + " ... ")
	

	def setup(self):
		self.__player = gst.element_factory_make("playbin2", "player")
		bus = self.__player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_status)

	def loadConfiguration(self):
		log.info("Loading settings from json ...")
		json_data = open('defaults.json')
		data = json.load(json_data)
		self.__user = data["google-music-user"]
		self.__password = data["google-music-password"]

	def setdown(self):
		self.__player.set_state(gst.STATE_NULL)

	def on_status(self, bus, message):
		t = message.type
		if(t == gst.MESSAGE_EOS):
			log.info("Song end")
			self.playCurrentSong()
		if(t == pygst.MESSAGE_ERROR):
			err, debug = message.parse_error()
			log.error(err)
			log.debug(debug)
			self.__player.set_state(gst.STATE_NONE)


	@staticmethod
	def getName():
		return "Google Music"
