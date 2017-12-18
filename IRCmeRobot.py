from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from random import randint

updater = Updater(token='')
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hello buddy! I am here to give your group chat some possibilities for more action. Just invite me to any group and then type /me and what you want to virtually do and I will do the magic.\nFor example you can type '/me invited this bot' and I will change it to 'Bob invited this bot.' (in case your name is Bob).\nJust try it out!")

def getUser(update):
        return update.message.from_user

def linkedUser(user):
        return '[{}](tg://user?id={})'.format(user['first_name'], user['id'])

def me(bot, update):
        theMe = linkedUser(getUser(update))
        theArgs = getArgs(update)
        bot.send_message(chat_id=update.message.chat_id, text=u'{0} {1}'.format(theMe, theArgs), parse_mode = 'Markdown')
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def snowball(bot, update):
        scenario = randint(0, 100)
        bot.send_message(chat_id=update.message.chat_id, text=snowballText(update, scenario), parse_mode = 'Markdown')
        bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

def snowballText(update, scenario):
        theArgs = getArgs(update)
        theMe = linkedUser(getUser(update))
        if scenario > 80:
                return u'{0} sees that {1} is preparing a snowball and throws first, disarming {1} again!'.format(theMe, theArgs)
        elif scenario > 50:
                return u'{0} aims carefully at {1}\'s chest, throws, and the snowball hits exactly there!'.format(theMe, theArgs)
        elif scenario > 40:
                return u'{0} throws a snowball and accidentally hits {1} in the face. Not cool!'.format(theMe, theArgs)
        elif scenario > 10:
                return u'{0} throws a snowball to {1} but it hits the ground in front of {1}!'.format(theMe, theArgs)
        elif scenario > 0:
                return u'{0} tries to throw a snowball at {1} but instead slips and lands on the butt!'.format(theMe, theArgs)
        else:
                return u'{0} throws a snowball at {1} but {1} catches and throws it back to {0}! Better be faster next time.'.format(theMe, theArgs)

def getArgs(update):
        firstElem = update.message.entities[0].length + 1
        messageText = ''
        for i in update.message.entities:
                lastElem = i.offset
                if i.user is not None:
                        messageText = messageText + update.message.text[firstElem:lastElem] + linkedUser(i.user)
                        firstElem = i.offset+i.length
        if firstElem < len(update.message.text):
                messageText = messageText + update.message.text[firstElem:]
        return messageText

def cmds(bot, update):
        bot.send_message(chat_id = update.message.chat_id, text = 'Available commands:\n/me [text]\n/snowball [name/mention]\n\nTry some things in a chat with the bot.')

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

start_handler = CommandHandler('start', start)
me_handler = CommandHandler('me', me)
snowball_handler = CommandHandler('snowball', snowball)
cmd_handler = CommandHandler('cmds', cmds)
commands_handler = CommandHandler('commands', cmds)
help_handler = CommandHandler('help', cmds)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(me_handler)
dispatcher.add_handler(snowball_handler)
dispatcher.add_handler(cmd_handler)
dispatcher.add_handler(commands_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_error_handler(error_callback)
updater.start_polling()

updater.idle()
