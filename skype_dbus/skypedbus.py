import dbus, sys, gobject, subprocess
from dbus.mainloop.glib import DBusGMainLoop
from dbus.exceptions import DBusException
from dbus.service import Object, method
from time import sleep
from threading import Thread
from messages import DBusMsgProcessor, DBusConnectionStatMsg
from bases import SkypeDBusEventsBase
from skype_dbus_exceptions import SkypeDBusException
from settings import SKYPE_API, SKYPE_API_PATH, SKYPE_CLIENT, SKYPE_CLIENT_PATH, \
SKYPE_PROTOCOL, DBUS, DBUS_PATH, SKYPE_DBUS_APP_NAME, SKYPE_USER_STATUS_UNKNOWN, \
SKYPE_USER_STATUS_ONLINE, SKYPE_USER_STATUS_OFFLINE, SKYPE_USER_STATUS_SKYPEME, \
SKYPE_USER_STATUS_AWAY, SKYPE_USER_STATUS_NA, SKYPE_USER_STATUS_DND, \
SKYPE_USER_STATUS_INVISIBLE, SKYPE_USER_STATUS_LOGGEDOUT

class SkypeDBus(Thread):

	def __init__(self, *args, **kwargs):

		self.dbus_loop = DBusGMainLoop(set_as_default=True)
		self.dbus_session = dbus.SessionBus(mainloop=self.dbus_loop)
		self.dbus_skype_events = []
		self.addEventHandler([SkypeDBusDefaultEvent()])
		self.skype_user_status = SKYPE_USER_STATUS_UNKNOWN

		plugins = kwargs.pop('plugins', None)

		if plugins:
			if type(plugins) == type([]):
				self.addEventHandler(plugins)

		self.quit_now = False

		self.skype_process = None
		#self.skype_msg = DBusMsgProcessor(self)
		self.skype_username = ""
		#Check if Skype API Service is running
		#if not self.is_service_running:
		self.checkIfConnectedCtr = 0

		try:
			self.skype_process = subprocess.Popen(['skype'])
		except OSError:
			raise SkypeDBusException('Skype is not yet installed on your machine.')

		while True:

			try:
				sleep(2) #pause for 2 seconds
				self.skype_object = self.dbus_session.get_object(SKYPE_API, SKYPE_API_PATH)
				break
			except DBusException:
				pass

		response = self.send_message("NAME %s" % SKYPE_DBUS_APP_NAME)

		if response != "OK":
			raise SkypeDBusException("Can't bind %s to Skype Client (%s)." % (SKYPE_DBUS_APP_NAME, response))

		response = self.send_message("PROTOCOL %s" % SKYPE_PROTOCOL)

		if response != "PROTOCOL %s" % SKYPE_PROTOCOL:
			raise SkypeDBusException("%s only supports Skype API protocol version %s." % (SKYPE_DBUS_APP_NAME, PROTOCOL))

		self.skype_notification = SkypeDBusNotification(skype_dbus=self)
		gobject.threads_init()

		super(SkypeDBus, self).__init__(*args, **kwargs)
		#self.daemon = True

	def send_message(self, msg):
		service_response = self.skype_object.Invoke(msg)
		return service_response

	@property
	def is_service_running(self):

		try:

			services_list = self.dbus_session.get_object(DBUS, DBUS_PATH).ListNames()
			self.checkIfConnectedCtr += 1

			for service in services_list:
				if service == SKYPE_API:

					if self.checkIfConnectedCtr == 5:
						self.checkIfConnectedCtr = 0
						get_connection_status = DBusConnectionStatMsg()
						response = self.send_message(get_connection_status.get().connection_status().toStr())
						msg_processor = DBusMsgProcessor(self)
						msg_processor.process_message(response, True)

						if self.quit_now:
							return False
					return True
					break
		except DBusException:
			pass

		return False


	def run(self):
		self.dbus_gobject_loop = gobject.MainLoop()
		context = self.dbus_gobject_loop.get_context()
		#self.dbus_gobject_loop.run()

		while self.is_service_running:
			context.iteration()
			#sleep(1)

	def addEventHandler(self, handlers=[]):
		for handler in handlers:
			self.dbus_skype_events.append(handler)

	def fireEvents(self, event, **kwargs):

		for skype_evt in self.dbus_skype_events:
			#print skype_evt
			if hasattr(skype_evt, event):
				#fire event
				getattr(skype_evt, event)(self, **kwargs)

class SkypeDBusNotification(Object):

	def __init__(self,*args,**kwargs):
		self.recent_message = ""
		self.skype_dbus = kwargs.pop('skype_dbus')
		super(SkypeDBusNotification, self).__init__(self.skype_dbus.dbus_session, SKYPE_CLIENT_PATH)

	@method(dbus_interface=SKYPE_CLIENT)
	def Notify(self, skype_cmd):
		firedEvent = ""
		#recent_message is used to ignore duplicate message
		if self.recent_message != skype_cmd:
			#print "Skype returns: %s" % skype_cmd
			msg_processor = DBusMsgProcessor(self.skype_dbus)
			firedEvent = msg_processor.process_message(skype_cmd)

			if firedEvent:
				print "Event fired: %s" % firedEvent
			else:
				print "Skype command: %s" % skype_cmd
		
		self.recent_message = skype_cmd

class SkypeDBusDefaultEvent(SkypeDBusEventsBase):

	def error(self, skype_dbus, **kwargs):
		
		error_details = kwargs.get('error_details')
		if error_details == "68":
			#Disconnected to BUS and need to quit
			skype_dbus.quit_now = True

	def user_handle(self, skype_dbus, **kwargs):

		skype_username = kwargs.get('skype_username')
		skype_dbus.skype_username = skype_username

	def user_status_unknown(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_UNKNOWN

	def user_status_online(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_ONLINE

	def user_status_offline(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_OFFLINE

	def user_status_skypeme(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_SKYPEME

	def user_status_away(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_AWAY

	def user_status_na(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_NA

	def user_status_dnd(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_DND

	def user_status_invisible(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_INVISIBLE

	def user_status_loggedout(self, skype_dbus, **kwargs):
		skype_dbus.skype_user_status = SKYPE_USER_STATUS_LOGGEDOUT