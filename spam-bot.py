#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль спам-бота использующего протокол xmpp для массовой рассылки
"""

import xmpppy
import config





class Request(object):
	""" Класс для получения сендеров и реципиентов """

	def get_senders(self):
		""" Возвращает словарь отправителей вида {user:passwd, ...} """

		with open("senders") as file:
			text = file.read()
			lines = text.split("\n")
			values = [line.split() for line in lines if line]
			senders = {key:value for (key, value) in values}

		return senders


	def get_recipients(self):
		""" Возвращает список получателей [user, ...] """

		with open("recipients") as file:
			text = file.read()
			lines = text.split("\n")
			recipients = [line for line in lines if line]

		return recipients




class Bot(object):
	""" Основной класс спам-бота """

	def __init__(self, user, password, server):
		self.bot = xmpppy.Client(server, debug=[])

		try:
			self.bot.connect()
		except AttributeError:
			print ("Пользователя '%s' нет на сервере %s" % (user, server))
			return
		print ("Пользователь '%s' подключился к серверу" % user)

		self.bot.auth(user, password)
		print ("Пользователь '%s' авторизован" % user)

		self.bot.online = True
		self.bot.sendInitPresence()


	def send_message(self, recipient):

		print ("Отправка соощения '%s'" % recipient)
		self.bot.send(xmpppy.protocol.Message(recipient, config.message))


	def __del__(self):

		self.bot.online = False

		self.bot.disconnect()





def main():
	""" Точка входа в программу """

	senders = Request().get_senders()
	recipients = Request().get_recipients()

	for (sender, password) in senders.items():
		server = sender.split("@")[-1]
		bot = Bot(sender, password, server)
		for recipient in recipients:
			bot.send_message(recipient)





if __name__ == "__main__":
	main()