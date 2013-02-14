from bases import SkypeDBusEventsBase
from messages import SkypeDBusFunctionsBase
from settings import SKYPE_USER_STATUS_AWAY, SKYPE_USER_STATUS_DND
import re, urllib2
from python_simsimi import SimSimi
from python_simsimi.language_codes import LC_FILIPINO
from python_simsimi.simsimi import SimSimiException

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
			print "Set to seen is: %s" % self.setToSeen(skype_dbus, messageId)

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



class SkypeSimSimiPlugin(SkypeDBusEventsBase, SkypeDBusFunctionsBase):

	def __init__(self, *args, **kwargs):
		self.conversation_key = kwargs.get('conversation_key','')
		self.conversation_language = kwargs.get('conversation_language',LC_FILIPINO)

	def chat_message_received(self, skype_dbus, **kwargs):

		messageId = kwargs.get('skype_message_id')
		automatedMsg = "SimSimi can't talk to you right now.. :)"

		body = self.getBody(skype_dbus, messageId)
		body = body.strip()

		simSimi = SimSimi(
			conversation_language=self.conversation_language,
			conversation_key=self.conversation_key
		)

		try:
			response = simSimi.getConversation(body)
			automatedMsg = response['response']
		except SimSimiException as e:
			pass

		chatname = self.getChatName(skype_dbus, messageId)
		self.setToSeen(skype_dbus, messageId)
		self.sendMessage(skype_dbus,chatname, automatedMsg)