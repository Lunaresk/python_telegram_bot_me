from random import randint

def getUser(message):
        return message.from_user

def linkedUser(user):
        return u'[{}](tg://user?id={})'.format(user['first_name'], user['id'])

def snowballText(message):
	scenario = randint(0,100)
	theMe = linkedUser(getUser(message))
	theArgs = checkMessage(message)
	if theArgs is "":
		return None
	if scenario > 80:
		return u'{0} sees that {1} is preparing a snowball and throws first, disarming {1} again!'.format(theMe, theArgs)
	if scenario > 50:
		return u'{0} aims carefully at {1}\'s chest, throws, and the snowball hits exactly there!'.format(theMe, theArgs)
	if scenario > 40:
		return u'{0} throws a snowball and accidentally hits {1} in the face. Not cool!'.format(theMe, theArgs)
	if scenario > 10:
		return u'{0} throws a snowball to {1} but it hits the ground in front of {1}!'.format(theMe, theArgs)
	if scenario > 0:
		return u'{0} tries to throw a snowball at {1} but instead slips and lands on the butt!'.format(theMe, theArgs)
	return u'{0} throws a snowball at {1} but {1} catches and throws it back to {0}! Better be faster next time.'.format(theMe, theArgs)

def kissText(message):
	scenario = randint(0,100)
	theMe = linkedUser(getUser(message))
	theArgs = checkMessage(message)
	if theArgs is "":
		return None
	if scenario > 75:
		return u'{0} pushes {1} softly on the wall and they start kissing long and wild.'.format(theMe, theArgs)
	if scenario > 50:
		return u'{0} looks into {1} eyes deeply and they kiss each other softly.'.format(theMe, theArgs)
	if scenario > 25:
		return u'{1} sees that {0} is coming closer and blushes when {0} kisses {1}.'.format(theMe, theArgs)
	if scenario > 10:
		return u'{0} sees {1} smiling and decides to give {1} a quick kiss.'.format(theMe, theArgs)
	return u'{0} gives {1} a sweet kiss on the cheek.'.format(theMe, theArgs)

def slapText(message):
	scenario = randint(0,100)
	theMe = linkedUser(getUser(message))
	theArgs = checkMessage(message)
	if theArgs is "":
		return None
	if scenario > 75:
		return u'{0} is enraged about {1} and punches {1} in the face, flying into the next wall.'.format(theMe, theArgs)
	if scenario > 50:
		return u'{0} slaps {1} as hard as possible in the face. The handprint is still visible on the cheek.'.format(theMe, theArgs)
	if scenario > 25:
		return u'{0} is angry about {1} and slaps {1} in the face.'.format(theMe, theArgs)
	if scenario > 10:
		return u'{0} shoves {1} angrily against the wall.'.format(theMe, theArgs)
	return u'{0} tries to slap {1} but {1} predicted it and turns it into a high-five.'.format(theMe, theArgs)

def getArgs(message):
	firstElem = message.entities[0].length + 1
	messageText = ''
	for i in message.entities:
		lastElem = i.offset
		if i.user is not None:
			messageText = messageText + message.text[firstElem:lastElem] + linkedUser(i.user)
			firstElem = i.offset+i.length
	if firstElem < len(message.text):
		messageText = messageText + message.text[firstElem:]
	return messageText

def getMention(message):
	for i in message.entities:
		if i.type == 'text_mention':
			return linkedUser(i.user)
		if i.type == 'mention':
			return message.text[i.offset:i.offset+i.length]
	return None

def checkMessage(message):
	if message.reply_to_message is not None:
		return linkedUser(getUser(message.reply_to_message))
	elif getMention(message) is not None:
		return getMention(message)
	return getArgs(message)
