import os
import telebot
import configparser
import json


BIN_LOG = []

fd = os.open('./.env',os.O_RDONLY)

API_KEY = os.read(fd,46)
API_KEY = API_KEY.decode('utf-8')

os.close(fd)


bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['bin'])
def bin(message):
	name = message.from_user.first_name + ' ' + message.from_user.last_name
	count = int(message.text[4:])
	listing = message.reply_to_message
	if listing == None:
		bot.reply_to(message, 'Please ')
		return
		

	binText = message.from_user.first_name + ' ' + message.from_user.last_name + ' ' + message.text[4:]
	BIN_LOG.append(binText)
	bot.reply_to(message, 'Bin Recorded')
	print(BIN_LOG)
	
@bot.message_handler(commands=['test'])
def test(message):
	bot.send_message(message.chat.id,'TEST ITEM\n\n$30\n\n30 available\n\neta 20 days')
	bot.send_message(message.chat.id,message.chat.id)
	bot.send_photo(message.chat.id,'https://www.akc.org/wp-content/uploads/2017/11/Shiba-Inu-standing-in-profile-outdoors.jpg','TEST ITEM\n\n$30\n\n30 available\n\neta 20 days')
bot.polling()
