from sqliteControl import readSQ

def findAccount(account):
	return len(readSQ("users","name",account)) != 0

def findUuid(uuid):
	return len(readSQ("users","uuid",uuid)) != 0
	