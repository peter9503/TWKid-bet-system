import json
import time
import hashlib
import os
from constant import *


def findId(account):
	f = open("data/account/idTable.txt","r")
	for line in f:
		if account == line[:-1]:
			f.close()
			return True
	f.close()
	return False


def _login(account, password):

	# check account ID valid
	if not findId(account):
		return WRONG_ACCOUNT

	# set up hashed uid
	m = hashlib.sha256()
	m.update(account.encode())
	m.update(password.encode())
	m.update(m.hexdigest().encode())
	uid = m.hexdigest()

	if not os.path.exists("data/account/{}.json".format(uid)):
		return WRONG_PW

	return uid


def register(account, password):
	if findId(account):
		return NAME_USED

	else:
		m = hashlib.sha256()
		m.update(account.encode())
		m.update(password.encode())
		m.update(m.hexdigest().encode())
		uid = m.hexdigest()

		accountData = {"bethistory":[],
						"currentAmount":2000,
						"name": account}

		f = open("data/account/{}.json".format(uid),"w")
		f.write(json.dumps(accountData))
		f.close()

		f = open("data/account/idTable.txt","a")
		f.write(account + "\n")
		f.close()
		return SUCCESS

def caculateUid(account,password):
	m = hashlib.sha256()
	m.update(account.encode())
	m.update(password.encode())
	m.update(m.hexdigest().encode())
	uid = m.hexdigest()
	return uid


if __name__ == '__main__':
	# print(login("我","tp"))
	account = input()
	password = input()
	print(caculateUid(account,password))


