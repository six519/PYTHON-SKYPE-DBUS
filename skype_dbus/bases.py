class SkypeDBusMessageBase(object):

	def __init__(self, *args, **kwargs):
		self.message = ""

	def get(self):
		self.message = "GET "

		return self

	def set_(self):
		self.message = "SET "
		return self

	def otherParam(self, param):
		self.message += param + " "
		return self

	def toStr(self):

		return str(self)

	def __str__(self):

		ret = self.message.strip()
		self.clear()
		return ret

	def clear(self):
		self.message = ""
		return self

class SkypeDBusEventsBase(object):

	def connection_offline(self,*args,**kwargs):
		pass

	def connection_online(self,*args,**kwargs):
		pass

	def connection_connecting(self,*args,**kwargs):
		pass

	def connection_pausing(self,*args,**kwargs):
		pass

	def error(self, *args,**kwargs):
		pass

	def user_handle(self, *args, **kwargs):
		pass

	def user_status_unknown(self, *args, **kwargs):
		pass

	def user_status_online(self, *args, **kwargs):
		pass

	def user_status_offline(self, *args, **kwargs):
		pass

	def user_status_skypeme(self, *args, **kwargs):
		pass

	def user_status_away(self, *args, **kwargs):
		pass

	def user_status_na(self, *args, **kwargs):
		pass

	def user_status_dnd(self, *args, **kwargs):
		pass

	def user_status_invisible(self, *args, **kwargs):
		pass

	def user_status_loggedout(self, *args, **kwargs):
		pass

	def chat_message_sending(self, *args, **kwargs):
		pass

	def chat_message_sent(self, *args, **kwargs):
		pass

	def chat_message_received(self, *args, **kwargs):
		pass

	def chat_message_read(self, *args, **kwargs):
		pass