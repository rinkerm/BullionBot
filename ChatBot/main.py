from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import requests
import telebot
from telebot.types import InputFile
#Declare Globals
global BIN_LOG 
global CONFIG_DATA
global KITCO 
global WHITELIST


KITCO = 'http://www.kitco.com/market/'

#Load Config
config = open('config.json')
CONFIG_DATA = json.load(config)

#Initialize Globals/Api Key
API_KEY = CONFIG_DATA['api_key']
WHITELIST = CONFIG_DATA['whitelist']
BIN_LOG = []

#Initialize Bot
bot = telebot.TeleBot(API_KEY)

#Helper Functions
		
def get_spot():
	#Declare Globals
	global KITCO
	
	#Scrape Kitco Spot
	try:
		wr = requests.get(KITCO)
	except Exception as e:
		bot.reply_to(message, "Error: Unable to access KITCO Spot Price")
		return
	content = wr.content
	
	#Parse Data
	soup = BeautifulSoup(content, features ='lxml')
	metalList = ['GOLD','SILVER','PLATINUM','PALLADIUM']
	priceList = [soup.find('td',id="AU-ask").contents[0],
		soup.find('td',id="AG-ask").contents[0],
		soup.find('td',id="PT-ask").contents[0],
		soup.find('td',id="PD-ask").contents[0]]
			
	return metalList, priceList
	
#General Commands

def binn(message):

	global BIN_LOG
	if re.search('^\/bin \d+$',message.text) == None:
		bot.reply_to(message, 'Error: Usage "/bin #"')
		return
	if message.reply_to_message == None:
		bot.reply_to(message, 'Please submit your bin in reply to a listing')
		return
	if message.reply_to_message.text == None:
		if message.reply_to_message.caption == None:
			bot.reply_to(message, 'Please submit your bin in reply to a listing')
			return
		else:
			listing = message.reply_to_message.caption.split('\n')[0]
	else:
		listing = message.reply_to_message.text.split('\n')[0]
		
	name = message.from_user.username
	count = message.text[4:]
	date = str(datetime.fromtimestamp(message.date))
	binText = name + ', ' + count + ', ' + listing + ', ' + date + ', N/A' 
	BIN_LOG.append(binText)
	bot.reply_to(message, 'Bin Recorded')

def spot(message):
	
	metalList, priceList = get_spot()
			
	#Build Response
	now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
	response = "Kitco Spot Prices @ {0}".format(now)
	for i in range(0,len(metalList)):
		response += "\n\n {0}:\t\t${1}".format(metalList[i],priceList[i])
	bot.reply_to(message,response)

@bot.message_handler(commands=['bin','spot'])
def spotbin (message):
	global BIN_LOG
	
	if re.search('/bin',message.text) == None:
		spot(message)
	elif re.search('/spot',message.text) == None:
		binn(message)
	else:
		if re.search('^\/bin \d+ \/spot$',message.text) == None:
			bot.reply_to(message, 'Error: Usage "/bin # /spot"')
			return
		if message.reply_to_message == None:
			bot.reply_to(message, 'Please submit your bin in reply to a listing')
			return
		if message.reply_to_message.text == None:
			if message.reply_to_message.caption == None:
				bot.reply_to(message, 'Please submit your bin in reply to a listing')
				return
			else:
				listing = message.reply_to_message.caption.split('\n')[0]
		else:
			listing = message.reply_to_message.text.split('\n')[0]
			
		name = message.from_user.username
		count = message.text[4:]
		date = str(datetime.fromtimestamp(message.date))
		
		#Build Spot String
		metalList,priceList = get_spot()
		if metalList is None or priceList is None:
			return
			
		#Build Response
		now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
		spot_str = "Kitco Spot Prices @ {0}".format(now)
		for i in range(0,len(metalList)):
			spot_str += "| {0}: ${1}".format(metalList[i],priceList[i])
			
		binText = name + ', ' + count + ', ' + listing + ', ' + date + ', ' + spot_str
		BIN_LOG.append(binText)
		bot.reply_to(message, 'Spot Bin Recorded')
	

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
	
	#Write to csv
	
	now = datetime.now().strftime("%d%m%Y_%H%M%S")
	filename = 'Logs/' + now + '.csv'
	
	f = open(filename,'x')
	
	for entry in temp_bin_log:
		f.write(entry + '\n')
	f.close()
	
	bot.send_message(message.from_user.id,'Success! Output file location: ' + filename)

@bot.message_handler(commands=['reloadConfig'])
def reloadConfig(message):
	
	#Declare Globals
	global CONFIG_DATA
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
	CONFIG_DATA = json.load(config)
	WHITELIST = CONFIG_DATA['whitelist']
	
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
	response= 'Admin Commands\n==========================\n'
	response += '"/getBins" \t\t| Dump recorded bins to .csv\n'
	response += '"/reloadConfig" \t\t| Reload Config File\n'
	response += '"/adminHelp" \t\t| Display Admin Commands'
	
	bot.reply_to(message,response)
	
#Info Commands

@bot.message_handler(commands=['airtites'])
def airtites(message):
	bot.send_photo(message.chat.id,InputFile('Images/airtite.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['buyback'])
def buyback(message):
	bot.send_photo(message.chat.id,InputFile('Images/buyback.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['payments'])
def payments(message):

	bot.send_photo(message.chat.id,InputFile('Images/payments.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['policy'])
def policy(message):

	bot.send_photo(message.chat.id,InputFile('Images/policy.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['shipping'])
def shipping(message):

	bot.send_photo(message.chat.id,InputFile('Images/shipping.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['team'])
def team(message):

	bot.send_photo(message.chat.id,InputFile('Images/info.jpg'), reply_to_message_id = message.id)

@bot.message_handler(commands=['welcome'])
def welcome(message):

	global CONFIG_DATA
	
	bot.send_message(message.chat.id,'Welcome! Please see the linked message for some info on how this all works.',reply_to_message_id = CONFIG_DATA['welcome_message'])

@bot.message_handler(commands= ['help'])
def help(message):

	#Build Response
	response = 'General Commands\n==========================\n'
	response += '"/bin #" \t\t| Used to record a bin\n'
	response += '"/bin # /spot" \t\t| Used to record a bin w/spot price\n'
	response += '"/spot" \t\t| Display Kitco Spot Prices\n'
	response+= '\nInformational Commands\n==========================\n'
	response += '"/airtites" \t\t| Display Info about Airtites and Tubes\n'
	response += '"/buyback" \t\t| Display Buyback Program Info\n'
	response += '"/payments" \t\t| Display Payment Method Info\n'
	response += '"/policy" \t\t| Display Company Policy Info\n'
	response += '"/shipping" \t\t| Display Shipping and Packing Info\n'
	response += '"/team" \t\t| Display Company Info\n'
	response += '"/welcome" \t\t| Link Welcome Message\n'
	response+= '\nHelp Commands\n==========================\n'
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

@bot.message_handler(commands=['debugGetBins'])
def debugGetBins(message):
	
	#Declare Globals
	global BIN_LOG
	
	#Validate Parameters
	if len(BIN_LOG) == 0:
		bot.send_message(message.from_user.id,'No Bins recorded',disable_notification=True)
		return
	
	#Reset Bin Log
	temp_bin_log = BIN_LOG
	BIN_LOG = []
	
	#Send Response
	for entry in temp_bin_log:
		bot.send_message(message.chat.id,entry,disable_notification=True)

@bot.message_handler(commands=['get_reply_id'])
def getreplyid(message):
	print(message.reply_to_message.id)

#Listen for Commands
bot.polling()

