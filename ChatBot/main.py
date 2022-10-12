import os
import telebot
import configparser
import json
import re
import datetime

#Declare Globals
global BIN_LOG 
global config_data
global WHITELIST

#Load Config
config = open('config.json')
config_data = json.load(config)

#Initialize Globals/Api Key
API_KEY = config_data['api_key']
WHITELIST = config_data['whitelist']
BIN_LOG = []

#Initialize Bot
bot = telebot.TeleBot(API_KEY)

#Helper Functions
def list_to_formatted_string(x, delim):
	formatted = ''
	if len(x) == 1:
		formatted = x[0]
	else:
		for i in range(0,len(x)-1):
			formatted += x[i] + ', '
		formatted += delim + ' ' + x[len(x)-1]		
	return formatted

#General Commands

@bot.message_handler(commands=['bin'])
def bin(message):
	global BIN_LOG
	if re.search('^\/bin \d+$',message.text) == None:
		bot.reply_to(message, 'Error: Usage "/bin #"')
		return
	if message.reply_to_message == None:
		bot.reply_to(message, 'Please submit your bin in reply to a listing')
		return
	if message.reply_to_message .text == None:
		if message.reply_to_message .caption == None:
			bot.reply_to(message, 'Please submit your bin in reply to a listing')
			return
		else:
			listing = message.reply_to_message.caption.split('\n')[0]
	else:
		listing = message.reply_to_message.text.split('\n')[0]
		
	name = message.from_user.first_name + ' ' + message.from_user.last_name
	count = message.text[4:]
	date = str(datetime.datetime.fromtimestamp(message.date))
	binText = name + ' ' + count + ' ' + listing + ' @' + date
	BIN_LOG.append(binText)
	bot.reply_to(message, 'Bin Recorded')

#Admin Commands
@bot.message_handler(commands=['getBins'])
def getBins(message):
	
	#Declare Globals
	global BIN_LOG
	global WHITELIST
	
	#Validate Parameters
	if message.from_user.id not in WHITELIST:
		bot.reply_to(message,"Error: Invalid Permissions")
		return
	if not message.from_user.id == message.chat.id:
		bot.reply_to(message,"Error: Command only available in DMs")
		return 
	if len(BIN_LOG) == 0:
		bot.send_message(message.from_user.id,'No Bins recorded',disable_notification=True)
		return
	
	#Reset Bin Log
	temp_bin_log = BIN_LOG
	BIN_LOG = []
	
	#Send Response
	for entry in temp_bin_log:
		bot.send_message(message.from_user.id,entry,disable_notification=True)

@bot.message_handler(commands=['reloadConfig'])
def reloadConfig(message):
	
	#Declare Globals
	global config_data
	global WHITELIST
	
	#Validate Parameters
	if message.from_user.id not in WHITELIST:
		bot.reply_to(message,"Error: Invalid Permissions")
		return
	if not message.from_user.id == message.chat.id:
		bot.reply_to(message,"Error: Command only available in DMs")
		return 
	
	#Reload Config JSON
	config = open('config.json')
	config_data = json.load(config)
	WHITELIST = config_data['whitelist']
	
	#Send Response
	bot.reply_to(message,'Config Reloaded',disable_notification=True)

@bot.message_handler(commands=['adminHelp'])
def adminHelp(message):

	#Declare Globals
	global WHITELIST
	
	#Validate Parameters
	if message.from_user.id not in WHITELIST:
		bot.reply_to(message,"Error: Invalid Permissions")
		return
	if not message.from_user.id == message.chat.id:
		bot.reply_to(message,"Error: Command only available in DMs")
		return 
		
	#Build Response
	response = 'Admin Commands: \n'
	response += '"/getBins" \t\t| Retrieve recorded bins\n'
	response += '"/reloadConfig" \t\t| Reload Config File\n'
	response += '"/adminHelp" \t\t| Display Admin Commands'
	
	bot.reply_to(message,response)
	
#Info Commands
@bot.message_handler(commands=['payments'])
def payments(message):

	#Declare Globals
	global config_data
	
	#Build Response
	response = 'Payment Methods:\n\n'
	response += 'Zelle: ' + config_data['messages']['payments']['Zelle'][0] + ' (' + config_data['messages']['payments']['Zelle'][1] + ')\n\n'
	response += 'Venmo: ' + config_data['messages']['payments']['Venmo'] + ' +1.9% GS Added to total\n\n'
	response += 'Paypal: ' + config_data['messages']['payments']['Paypal'] + ' +3.5% GS Added to total\n\n'
	response += 'Credit Card: Visa/Mastercard/Amex/Discover +3.5% GS Added to total\n\n'
	response += 'Money Order, Wire, & Check: Direct Message For Details\n\n'
	response += 'Deluxe eCheck: ' + config_data['messages']['payments']['Check'][0] + ' ' + config_data['messages']['payments']['Check'][1]  + '\n\n'
	response += 'Mobile Check: Front/Back Picture (In Focus on Dark Background)\nTo: ' + config_data['messages']['payments']['Check'][0] + '\nEmail to: ' + config_data['messages']['payments']['Check'][1]
	
	bot.reply_to(message,response)

@bot.message_handler(commands=['shipping'])
def shipping(message):

	#Declare Globals
	global config_data
	
	#Build Response
	response = 'Shipping and Packing: \n\n'
	response += 'USPS: \n $5 First Class (Less Than 8oz)\n $9 Flat Rate Small (No Weight Limit)*\n $15 Flat Rate Medium\n $20 Flat Rate Large\n -*USPS Weight Limits are determined by Tetris Skills. For Reference can usually fit a very large Amount (150+oz) in the $9 Priority Box.\n\n'
	response += 'UPS: \n $12 Flat Rate Small\n $18 Flat Rate Medium\n +$6 Signature Verification\n\n'
	response += 'Fedex: \n Available by Request\n\n'
	response += 'Note: \n First Class Packages Are Insured for $100 until marked delivered.\n Priority USPS and UPS are insured fully until marked delivered.\n Any package valued at $10,000+ MUST be shipped UPS or Fedex'
	
	bot.reply_to(message,response)

@bot.message_handler(commands=['team'])
def team(message):

	#Declare Globals
	global config_data
	
	#Build Response
	response = 'Company Info: \n\n'
	response+= 'Sales Posts: \n -Only Posted By: ' + list_to_formatted_string(config_data['messages']['general']['Sales'], 'and')+ '\n\n'
	response+= 'Any Requests: \n -Tag Or DM ' + list_to_formatted_string(config_data['messages']['general']['Requests'], '') + '\n\n'
	response+= 'Invoices: \n -Come From ' + list_to_formatted_string(config_data['messages']['general']['Invoices'], 'and')+ '\n -Roughly 1 Day After Processing Bins\n -Please Pay Promptly, Keeps Inventory Fresh\n -Indicate Keep Box Open/Close\n -Send Pay Screenshots to Invoicer' + '\n\n'
	response+= 'Admins: \n -Veteran Members of the Community\n -Help Newcomers and Keep Chat Clean\n\n'
	response+= 'CAUTION: \n if you receive Purchase Offers or Invoice Requests From Anyone Besides ' + list_to_formatted_string(config_data['messages']['general']['Team'], 'or') + ' Contact an Admin/Employee Immediately Please!'
	
	bot.reply_to(message, response)

@bot.message_handler(commands= ['help'])
def help(message):

	#Build Response
	response = 'Bot Commands:\n'
	response += '"/bin #" \t\t| Used to record a bin\n'
	response += '"/team" \t\t| Display Company Info\n'
	response += '"/shipping" \t\t| Display Shipping and Packing Info\n'
	response += '"/payments" \t\t| Display Payment Method Info\n'
	response += '"/adminHelp \t\t| Display Admin Commands\n'
	response += '"/help" \t\t| Display Commands'
	bot.reply_to(message, response)

#Debug Commands
@bot.message_handler(commands=['test'])
def test(message):
	if message.from_user.id not in WHITELIST:
		bot.reply_to(message,"Error: Invalid Permissions")
		return
	bot.send_message(message.chat.id,'TEST ITEM\n\n$30\n\n30 available\n\neta 20 days')
	bot.send_photo(message.chat.id,'https://www.akc.org/wp-content/uploads/2017/11/Shiba-Inu-standing-in-profile-outdoors.jpg','TEST ITEM\n\n$30\n\n30 available\n\neta 20 days')

@bot.message_handler(commands=['auth'])
def auth(message):
	#Print username and id to console
	#Intended to grab id for adding to whitelist
	print(message.from_user.username,message.from_user.id)

#Listen for Commands
bot.polling()

