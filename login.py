import json
import time
import hashlib
import os
from constant import *
from sqliteControl import updateById, createRow, readSQ
from share import findAccount



def _login(account, password):

	# check account ID valid
	if not findAccount(account):
		return WRONG_ACCOUNT

	# set up hashed uid
	m = hashlib.sha256()
	m.update(account.encode())
	m.update(password.encode())
	m.update(m.hexdigest().encode())
	uuid = m.hexdigest()

	accountData = readSQ("users","name",account)[0]
	if accountData[1] != uuid:
		return WRONG_PW

	return uuid


def register(account, password):
	if findAccount(account):
		return NAME_USED

	else:
		m = hashlib.sha256()
		m.update(account.encode())
		m.update(password.encode())
		m.update(m.hexdigest().encode())
		uuid = m.hexdigest()

		accountData = {	"currentAmount":2000,
						"name": account,
						"uuid":uuid}

		createRow("users",accountData)

		return SUCCESS

def caculateUid(account,password):
	m = hashlib.sha256()
	m.update(account.encode())
	m.update(password.encode())
	m.update(m.hexdigest().encode())
	uid = m.hexdigest()
	return uid


if __name__ == '__main__':
	print(_login("test","test"))
