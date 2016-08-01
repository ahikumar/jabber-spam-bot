#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль спам-бота использующего протокол xmpp для массовой рассылки
"""

import xmpppy
import config
import logging
from Queue import Queue
from multiprocessing import Process 


format = "%(asctime)s  %(filename)s  %(levelname)s:\t%(message)s"
if config.debug:
	logging.basicConfig(format=format, level=logging.DEBUG)
else:
	logging.basicConfig(format=format)


class NoSendersError(Exception):
	def __init__(self):
		logging.critical("No senders to start sending")
		exit(1)

class NoRecipientsError(Exception):
	def __init__(self):
		logging.critical("No recipients to start sending")
		exit(1)

class AuthenticationError(Exception):
	def __init__(self, user):
		logging.error("User '%s' can not authenticate the server" % user)

class ConnectError(Exception):
	def __init__(self, user):
		logging.error("User '%s' can not connect to the server" % user)






class Request(object):
	""" Класс для получения сендеров и реципиентов """

	def get_senders(self):
		""" Возвращает словарь отправителей вида {user:passwd, ...} """

		with open("senders") as file:
			text = file.read()
			lines = text.split("\n")
			values = [line.split() for line in lines if line]
			senders = [[key, value] for (key, value) in values]

			if not senders:
				NoSendersError()

		return senders


	def get_recipients(self):
		""" Возвращает список получателей [user, ...] """

		with open("recipients") as file:
			text = file.read()
			lines = text.split("\n")
			recipients = [line for line in lines if line]

			if not recipients:
				NoRecipientsError()

		return recipients




def spam_bot(user, password, recipients):
	logging.info("User '%s' started sending" % user)

	jid = xmpppy.protocol.JID(user)
	bot = xmpppy.Client(jid.getDomain(), debug=[])

	try:
		bot.connect()
	except:
		ConnectError(user)
		return

	auth = bot.auth(jid.getNode(), password)
	if not auth:
		AuthenticationError(user)
		bot.disconnect()
		return

	for recipient in recipients:
		#message = xmpppy.protocol.Message(to=recipient, body=config.message, subject=config.subject)
		message = xmpppy.protocol.Message()
		message.setTo(recipient)
		message.setSubject(config.subject)
		message.setBody(config.message)
		bot.send(message)

	logging.info("User '%s' finished sending" % user)
	bot.disconnect()





def main():
	""" Точка входа в программу """

	threads = config.threads
	senders = Request().get_senders()
	recipients = Request().get_recipients()

	queue = Queue(threads)
	while senders:
		user, password = senders.pop()
		process = Process(target=spam_bot, args=(user, password, recipients))
		process.start()

		if queue.empty() or queue.qsize() < threads:
			queue.put(process)
		else:
			old_process = queue.get()
			old_process.join()
			queue.put(process)





if __name__ == "__main__":
	main()