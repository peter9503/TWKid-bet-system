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

	# f = open("data/account/{}.json".format(uid))
	# Data = json.loads(f.readline())
	# f.close()

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

	# f = open("data/account/{}.json".format(uid),"r")
	# Data = json.loads(f.readline())
	# f.close()


	# Data["currentAmount"] += amount
	# f = open("data/account/{}.json".format(uid),"w")
	# f.write(json.dumps(Data))
	# f.close()

	return SUCCESS

def bet_ac(uuid,amount,gid):
	# only write and check account
	if not findUuid(uuid):
		print("account bet_ac() got wrong uid WTF")
		return WRONG_ACCOUNT

	# f = open("data/account/{}.json".format(uid),"r")
	# Data = json.loads(f.readline())
	# f.close()


	# Data["currentAmount"] -= amount
	# if gid not in Data["bethistory"]:
	# 	Data["bethistory"].append(gid)


	if readAccountBalance(uuid) < amount:
		return INSUFFICIENT
	# if Data["currentAmount"] < 0:
	# 	return INSUFFICIENT
	else:
		sendMoney(uuid,-amount)
		return SUCCESS


	# f = open("data/account/{}.json".format(uid),"w")
	# f.write(json.dumps(Data))
	# f.close()


if __name__ == '__main__':

	print(readAccountData("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	# print(sendMoney("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5",1024))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))
	print(bet_ac("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5",1000,1))
	print(readAccountBalance("2e605ac51ccff4980ae3a5c247ad381b777c1e39e82215c25ed10e92372fc0c5"))

	# print(sendMoney("dd856101b36e56538af2203badf096729b8d63eb9d0691b35289d3d555298a8c",10))

	# print(readAccountData("dd856101b36e56538af2203badf096729b8d63eb9d0691b35289d3d555298a8c"))
