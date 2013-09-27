from bases import SkypeDBusMessageBase
import re

class DBusMsgProcessor(object):

	def __init__(self, skype_dbus):
		self.skype_dbus = skype_dbus

	def process_message(self, msg, fromChecker=False):
		#trim msg
		msg = msg.strip()
		#print "The message is: %s" % msg

		#set messages
		get_connection_status = DBusConnectionStatMsg()
		get_error = DBusErrorStatMsg()
		get_user_handle = DBusUserHandleMsg()
		get_user_status = DBusUserStatMsg()
		get_chat_message = DBusChatMsg()
		eventStr = ""
		kw_args = {}

		if not fromChecker and re.search("^%s" % get_connection_status.connection_status().toStr(),msg):
			eventStr = "connection_"

			msg = msg.replace(get_connection_status.connection_status().toStr(),"").strip()
			eventStr += msg.lower()

		elif not fromChecker and re.search("^%s" % get_user_handle.user_handle().toStr(), msg):
			eventStr = "user_handle"

			kw_args['skype_username'] = msg.replace(get_user_handle.user_handle().toStr(),"").strip()

		elif not fromChecker and re.search("^%s" % get_user_status.user_status().toStr(),msg):
			eventStr = "user_status_"

			msg = msg.replace(get_user_status.user_status().toStr(),"").strip()
			eventStr += msg.lower()

		elif re.search("^%s" % get_error.error().toStr(), msg):
			eventStr = "error"

			kw_args['error_details'] = msg.replace(get_error.error().toStr(),"").strip()

		elif not fromChecker and re.search(get_chat_message.chat_message().otherParam("([0-9]+)").property_status().toStr(), msg):
			eventStr = "chat_message_"

			splittedMsg = msg.strip().split(" ")
			eventStr += splittedMsg[3].lower()

			kw_args['skype_message_id'] = splittedMsg[1]

		if eventStr != "":
			self.skype_dbus.fireEvents(eventStr, **kw_args)

		return eventStr

class DBusUserHandleMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusUserHandleMsg, self).__init__(*args, **kwargs)

	def user_handle(self):
		self.message = "CURRENTUSERHANDLE"
		return self

class DBusErrorStatMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusErrorStatMsg, self).__init__(*args, **kwargs)

	def error(self):
		self.message = "ERROR"
		return self

class DBusConnectionStatMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusConnectionStatMsg, self).__init__(*args, **kwargs)

	def connection_status(self):
		self.message += "CONNSTATUS "

		return self

	def offline(self):

		self.message += "OFFLINE "
		return self

	def connecting(self):

		self.message += "CONNECTING "

		return self

	def pausing(self):

		self.message += "PAUSING "
		return self

	def online(self):
		self.message += "ONLINE "
		return self

class DBusUserStatMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusUserStatMsg, self).__init__(*args, **kwargs)

	def user_status(self):
		self.message += "USERSTATUS "
		return self

	def unknown(self):
		self.message += "UNKNOWN "
		return self

	def online(self):
		self.message += "ONLINE "
		return self

	def offline(self):
		self.message += "OFFLINE "
		return self

	def skypeme(self):
		self.message += "SKYPEME "
		return self

	def away(self):
		self.message += "AWAY "
		return self

	def na(self):
		self.message += "NA "
		return self

	def dnd(self):
		self.message += "DND "
		return self

	def invisible(self):
		self.message += "INVISIBLE "
		return self

	def loggedout(self):
		self.message += "LOGGEDOUT "
		return self

class DBusFileTransferMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusFileTransfersMsg, self).__init__(*args, **kwargs)

	def file_transfer(self):
		self.message += "FILETRANSFER "

	def incoming(self):
		self.message += "INCOMING "

	def outgoing(self):
		self.message += "OUTGOING "

	def new(self):
		self.message += "NEW "

	def waiting_for_accept(self):
		self.message += "WAITING_FOR_ACCEPT "

	def connecting(self):
		self.message += "CONNECTING "

	def transferring(self):
		self.message += "TRANSFERRING "

	def transferring_over_relay(self):
		self.message += "TRANSFERRING_OVER_RELAY "

	def paused(self):
		self.message += "PAUSED "

	def remotely_paused(self):
		self.message += "REMOTELY_PAUSED "

	def cancelled(self):
		self.message += "CANCELLED "

	def completed(self):
		self.message += "COMPLETED "

	def failed(self):
		self.message += "FAILED "

	def failure_reason(self):
		self.message += "FAILUREREASON "

	def sender_not_authorized(self):
		self.message += "SENDER_NOT_AUTHORIZED "

	def remotely_cancelled(self):
		self.message += "REMOTELY_CANCELLED "

	def failed_read(self):
		self.message += "FAILED_READ "

	def failed_remoted_read(self):
		self.message += "FAILED_REMOTE_READ "

	def failed_write(self):
		self.message += "FAILED_WRITE "

	def failed_remote_write(self):
		self.message += "FAILED_REMOTE_WRITE "

	def remote_does_not_support_ft(self):
		self.message += "REMOTE_DOES_NOT_SUPPORT_FT "

	def remote_offline_for_too_long(self):
		self.message += "REMOTE_OFFLINE_FOR_TOO_LONG "

	def partner_handle(self):
		self.message += "PARTNER_HANDLE "

	def partner_dispname(self):
		self.message += "PARTNER_DISPNAME "

	def start_time(self):
		self.message += "STARTTIME "

	def finish_time(self):
		self.message += "FINISHTIME "

	def file_path(self):
		self.message += "FILEPATH "

	def file_name(self):
		self.message += "FILENAME "

	def file_size(self):
		self.message += "FILESIZE "

	def bytes_per_second(self):
		self.message += "BYTESPERSECOND "

	def bytes_transferred(self):
		self.message += "BYTESTRANSFERRED "

class DBusChatMsg(SkypeDBusMessageBase):

	def __init__(self, *args, **kwargs):

		super(DBusChatMsg, self).__init__(*args, **kwargs)

	def chat_message(self):
		self.message += "CHATMESSAGE "
		return self

	def property_chatname(self):
		self.message += "CHATNAME "
		return self

	def property_timestamp(self):
		self.message += "TIMESTAMP "
		return self

	def property_from_handle(self):
		self.message += "FROM_HANDLE "
		return self

	def property_from_dispname(self):
		self.message += "FROM_DISPNAME "
		return self

	def property_users(self):
		self.message += "USERS "
		return self

	def property_leavereason(self):
		self.message += "LEAVEREASON "
		return self

	def property_body(self):
		self.message += "BODY "
		return self

	def status_sending(self):
		self.message += "SENDING "
		return self

	def status_sent(self):
		self.message += "SENT "
		return self

	def status_received(self):
		self.message += "RECEIVED "
		return self

	def status_read(self):
		self.message += "READ "
		return self

	def seen(self):
		self.message += "SEEN "
		return self

class SkypeDBusFunctionsBase(object):

	def sendMessage(self, skype_dbus, chatname, msg):
		msgObject = DBusChatMsg()
		return skype_dbus.send_message(msgObject.chat_message().otherParam(chatname).otherParam(msg).toStr())

	def getChatName(self, skype_dbus, messageId):
		msgObject = DBusChatMsg()
		
		response = skype_dbus.send_message(msgObject.get().chat_message().otherParam(messageId).property_chatname().toStr())
		return response.replace(msgObject.chat_message().otherParam(messageId).property_chatname().toStr(), "").strip()

	def setToSeen(self, skype_dbus, messageId):
		msgObject = DBusChatMsg()
		return skype_dbus.send_message(msgObject.set_().chat_message().otherParam(messageId).seen().toStr())

	def editMessage(self, skype_dbus, messageId, newmsg):
		msgObject = DBusChatMsg()
		return skype_dbus.send_message(msgObject.set_().chat_message().otherParam(messageId).property_body().otherParam(newmsg).toStr())

	def getBody(self, skype_dbus, messageId):
		msgObject = DBusChatMsg()
		
		response = skype_dbus.send_message(msgObject.get().chat_message().otherParam(messageId).property_body().toStr())
		return response.replace(msgObject.chat_message().otherParam(messageId).property_body().toStr(), "").strip()