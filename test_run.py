from skype_dbus import SkypeDBus
from skype_dbus.skype_dbus_exceptions import SkypeDBusException
from skype_dbus.plugins import SkypeAutoResponderPlugin, SkypeUrlToTiny
import sys
	
plugins = [SkypeAutoResponderPlugin(), SkypeUrlToTiny()]

if __name__ == "__main__":

	try:
		skypeDBus = SkypeDBus(plugins=plugins)
		skypeDBus.start()
	except SkypeDBusException as e:
		print "SkypeDBus Error: %s" % e
		sys.exit()