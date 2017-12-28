from telegram.ext import CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from ircmefuncs import (linkedUser, getUser, getArgs, snowballText, kissText, slapText)
from bottoken import getToken

updater = getToken()
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Hello buddy! I am here to give your group chat some possibilities for more action. Just invite me to any group and then type /me and what you want to virtually do and I will do the magic.\nFor example you can type '/me invited this bot' and I will change it to 'Bob invited this bot.' (in case your name is Bob).\nJust try it out!")

def me(bot, update):
	theMe = linkedUser(getUser(update.message))
	theArgs = getArgs(update.message)
	bot.send_message(chat_id=update.message.chat_id, text=u'{0} {1}'.format(theMe, theArgs), parse_mode = 'Markdown')
	bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def snowball(bot, update):
	realText = snowballText(update.message)
	if realText is not None:
		bot.send_message(chat_id=update.message.chat_id, text=realText, parse_mode = 'Markdown')
	rmMessage(bot, update.message)

def kiss(bot, update):
	realText = kissText(update.message)
	if realText is not None:
		bot.send_message(chat_id=update.message.chat_id, text=realText, parse_mode = 'Markdown')
	rmMessage(bot, update.message)

def slap(bot, update):
	realText = slapText(update.message)
	if realText is not None:
		bot.send_message(chat_id=update.message.chat_id, text=realText, parse_mode = 'Markdown')
	rmMessage(bot, update.message)

def cmds(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = 'Available commands:\n/me [text]\n/snowball [name/mention]\n/kiss [name/mention]\n/slap [name/mention]\n\nAll commands except /me can also be triggered by replying to any other message.')

def rmMessage(bot, message):
	if  message.chat.type != "private":
		try:
			bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
		except BadRequest:
			print("There is a group I am no admin in.")


def error_callback(bot, update, error):
	try:
		raise error
	except Unauthorized:
		print ('UnauthorizedError >> ' + str(error))
		# remove update.message.chat_id from conversation list
	except BadRequest:
		print ('BadRequestError >> ' + str(error))
		# handle malformed requests - read more below!
	except TimedOut:
		print ('TimedOutError >> ' + str(error))
		# handle slow connection problems
	except NetworkError:
		print ('NetworkError >> ' + str(error))
		# handle other connection problems
	except ChatMigrated as e:
		print ('ChatMigratedError >> ' + str(error))
		# the chat_id of a group has changed, use e.new_chat_id instead
	except TelegramError:
		print ('AnotherError >> ' + str(error))
		# handle all other telegram related errors

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('me', me))
dispatcher.add_handler(CommandHandler('snowball', snowball))
dispatcher.add_handler(CommandHandler('kiss', kiss))
dispatcher.add_handler(CommandHandler('slap', slap))
dispatcher.add_handler(CommandHandler('cmds', cmds))
dispatcher.add_handler(CommandHandler('commands', cmds))
dispatcher.add_handler(CommandHandler('help', cmds))
dispatcher.add_error_handler(error_callback)
updater.start_polling()

updater.idle()

