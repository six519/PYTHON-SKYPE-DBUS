from bases import SkypeDBusEventsBase
from messages import SkypeDBusFunctionsBase
from settings import SKYPE_USER_STATUS_AWAY, SKYPE_USER_STATUS_DND
import re, urllib2

class SkypeAutoResponderPlugin(SkypeDBusEventsBase, SkypeDBusFunctionsBase):

	def __init__(self, *args, **kwargs):
		self.away_message = kwargs.get('away_message','')
		self.busy_message = kwargs.get('busy_message','')

	def chat_message_received(self, skype_dbus, **kwargs):

		messageId = kwargs.get('skype_message_id')
		automatedMsg = ""

		if skype_dbus.skype_user_status == SKYPE_USER_STATUS_DND:

			automatedMsg = self.busy_message if self.busy_message else "I'm busy right now. I can't reply to your message."

		elif skype_dbus.skype_user_status == SKYPE_USER_STATUS_AWAY:
			automatedMsg = self.away_message if self.away_message else "I'm away right now. I'll reply to your message later."

		if automatedMsg != "":
			chatname = self.getChatName(skype_dbus, messageId)
			self.setToSeen(skype_dbus, chatname)

			self.sendMessage(skype_dbus,chatname, automatedMsg)


class SkypeUrlToTiny(SkypeDBusEventsBase, SkypeDBusFunctionsBase):

	def autoEdit(self, skype_dbus, **kwargs):
		messageId = kwargs.get('skype_message_id')

		body = self.getBody(skype_dbus, messageId)
		body = body.strip()

		if re.search('^http([s]{0,1}):\/\/', body):
			if not re.search('tinyurl', body):
				httpResponse = urllib2.urlopen('http://tinyurl.com/api-create.php?url=%s' % body)
				newBody = str(httpResponse.read())
				self.editMessage(skype_dbus, messageId, newBody.strip())

	def chat_message_sending(self, skype_dbus, **kwargs):
		self.autoEdit(skype_dbus, **kwargs)

	def chat_message_sent(self, skype_dbus, **kwargs):
		self.autoEdit(skype_dbus, **kwargs)