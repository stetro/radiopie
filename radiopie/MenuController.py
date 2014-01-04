import RPi.GPIO as GPIO
from radiopie.modules import RadiopieModule
import sys
import time
import logging

log = logging.getLogger("radiopie")

class MenuController:
	def __init__(self, lcd):
		self.__position = 0
		self.__lcd = lcd
		self.__modules = RadiopieModule.__subclasses__()

	def start(self):
		log.info("Menu Started ...")
		self.__lcd.setFirst("Welcome!")
		time.sleep(3)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(22, GPIO.IN)
		GPIO.setup(23, GPIO.IN)
		GPIO.setup(24, GPIO.IN)
		GPIO.add_event_detect(23, GPIO.RISING, callback=self.left, bouncetime=500)
		GPIO.add_event_detect(24, GPIO.RISING, callback=self.right, bouncetime=500)
		GPIO.add_event_detect(22, GPIO.RISING, callback=self.ok)
		selection = self.showMenu()
		GPIO.clearnup()

	def showMenu(self):
		log.info(str(len(self.__modules))+" Module/s found")
		self.__lcd.setFirst("Select..")
		position = -1
		while True:
			if(position != self.__position):
				self.__lcd.setLast(self.__modules[self.__position].getName())
				position = self.__position
			time.sleep(0.4)
	
	def left(self, event):
		self.__position = (self.__position - 1) % len(self.__modules)
		log.debug("Left Button Pressed")

	def right(self, event):
		self.__position = (self.__position + 1) % len(self.__modules) 	
		log.debug("Right Button Pressed")
		
	def ok(self, event):
		module = self.__modules[self.__position]()
		log.debug("OK Button Pressed")
		module.start()
		time.sleep(3)
