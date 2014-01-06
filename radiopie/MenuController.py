import RPi.GPIO as GPIO
from radiopie.modules import RadiopieModule
import sys
import time
import logging

log = logging.getLogger("radiopie")

class MenuController:
	def __init__(self, lcd):
		self.__position = 0
		self.__menuposition = -1
		self.__lcd = lcd
		self.__modules = RadiopieModule.__subclasses__()
		self.__module = None
		self.__terminate = False

	def start(self):
		log.info("Menu Started ...")
		self.__lcd.setFirst("Welcome!")
		time.sleep(3)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(23, GPIO.FALLING, callback=self.left, bouncetime=200)
		GPIO.add_event_detect(24, GPIO.FALLING, callback=self.right, bouncetime=200)
		GPIO.add_event_detect(22, GPIO.FALLING, callback=self.ok, bouncetime=200)
		self.showMenu()
		GPIO.cleanup()

	def showMenu(self):
		log.info(str(len(self.__modules))+" Module/s found")
		self.__lcd.setFirst("Select..")
		while not self.__terminate:
			if(self.__menuposition != self.__position):
				self.__lcd.setLast(self.__modules[self.__position].getName())
				self.__menuposition = self.__position
			time.sleep(1)
	
	def left(self, event):
		log.debug("Left Button Pressed")
		if(self.__module != None and self.__module.isAlive()):
			self.__module.left()
		else:
			self.__terminate = True

	def right(self, event):
		log.debug("Right Button Pressed")
		if(self.__module != None and self.__module.isAlive()):
			self.__module.right()
		else:
			self.__position = (self.__position + 1) % len(self.__modules) 	
		
	def ok(self, event):
		log.debug("OK Button Pressed")
		if(self.__module != None and self.__module.isAlive()):
			self.__module.ok()
		else:
			self.__module = self.__modules[self.__position](self.__lcd)
			self.__module.start()
			time.sleep(1)
			self.__module.join()
			self.__lcd.setFirst("Select..")
			self.__menuposition = -1
		

