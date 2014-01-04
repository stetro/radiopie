from radiopie import *
import logging

def main():
	lcd = LCDController()
	menu = MenuController(lcd)
	menu.start()

def setupLogger():
	logging.basicConfig()
	log = logging.getLogger("radiopie")
	log.setLevel(logging.DEBUG)

if __name__ == "__main__":
	setupLogger()
	main()
