import json
import os
from constant import *


def readAccountData(uid):
	if not os.path.exists("data/account/{}.json".format(uid)):
		return WRONG_ACCOUNT

	f = open("data/account/{}.json".format(uid))
	Data = json.loads(f.readline())
	f.close()
	return Data

def sendMoney(uid,amount):
	if not os.path.exists("data/account/{}.json".format(uid)):
		print("account sendMoney() got wrong uid WTF")
		return WRONG_ACCOUNT

	f = open("data/account/{}.json".format(uid),"r")
	Data = json.loads(f.readline())
	f.close()


	Data["currentAmount"] += amount
	f = open("data/account/{}.json".format(uid),"w")
	f.write(json.dumps(Data))
	f.close()

	return SUCCESS

def bet_ac(uid,amount,gid):
	# only add data for users
	if not os.path.exists("data/account/{}.json".format(uid)):
		print("account bet() got wrong uid WTF")
		return WRONG_ACCOUNT

	f = open("data/account/{}.json".format(uid),"r")
	Data = json.loads(f.readline())
	f.close()


	Data["currentAmount"] -= amount
	if gid not in Data["bethistory"]:
		Data["bethistory"].append(gid)

	if Data["currentAmount"] < 0:
		return INSUFFICIENT



	f = open("data/account/{}.json".format(uid),"w")
	f.write(json.dumps(Data))
	f.close()
	return SUCCESS


if __name__ == '__main__':

	# print(readAccountData("dd856101b36e56538af2203badf096729b8d63eb9d0691b35289d3d555298a8c"))

	print(sendMoney("dd856101b36e56538af2203badf096729b8d63eb9d0691b35289d3d555298a8c",10))

	# print(readAccountData("dd856101b36e56538af2203badf096729b8d63eb9d0691b35289d3d555298a8c"))
