import json
import os
from constant import *
from sqliteControl import updateById, readSQ, readColumnName, readAll
from share import findAccount, findUuid


def allaccount():
	return readAll("users")

def readAccountData(uuid):
	if not findUuid(uuid):
		return WRONG_ACCOUNT


	Data = readSQ("users","uuid",uuid)
	keys_list = readColumnName("users")
	zip_iterator = zip(keys_list, Data[0])
	output = dict(zip_iterator)

	Allbethistory = readSQ("bethistory", "uid", Data[0][0])
	output["bethistory"] = []
	for a in Allbethistory:
		output["bethistory"].append(a[0])

	return output

def readAccountBalance(uuid):
	return readAccountData(uuid)["currentAmount"]

def sendMoney(uuid,amount):
	if not findUuid(uuid):
		print("account sendMoney() got wrong uid WTF")
		return WRONG_ACCOUNT

	data = readAccountData(uuid)
	uid = data["uid"]
	currentAmount = data["currentAmount"]

	updateById("users",{"currentAmount":int(currentAmount + amount)}, uid)

	return SUCCESS

def bet_ac(uuid,amount,gid):
	# only write and check account
	if not findUuid(uuid):
		print("account bet_ac() got wrong uid WTF")
		return WRONG_ACCOUNT


	if readAccountBalance(uuid) < amount:
		return INSUFFICIENT

	else:
		sendMoney(uuid,-amount)
		return SUCCESS



if __name__ == '__main__':

	print(readAccountData("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	print(bet_ac("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5",1000,1))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
