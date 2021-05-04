import json
import os
import time
from constant import *
from account import *
from sqliteControl import updateById, createRow, readSQ, readColumnName, tableSize
from share import findAccount, findUuid


class Game():

	def __init__(self):
		pass

	def _allg(self):
		return readAll("games")

	def _allb(self):
		return readAll("bethistory")

	def newGame(self,title,teamNames):
		# create new game file
		# SQLite
		gameData = {"title":title,
					"startTime":time.asctime( time.localtime(time.time()) ),
					"endTime":"",
					"sideA":teamNames[0],
					"sideB":teamNames[1],
					"state":0}

		# gid = tableSize("games")

		# # count current gid
		# try:
		# 	gid = len(os.listdir("data/games"))
		# except:
		# 	gid = 0

		gid = createRow("games",gameData)

		# # write file
		# try:
		# 	f = open("data/games/{}.json".format(gid),"w")
		# except:
		# 	os.mkdir("data/games")
		# 	f = open("data/games/{}.json".format(gid),"w")

		# f.write(json.dumps(gameData))
		# f.close()
		print("create game {}".format(gid))
		print(gameData)
		return 'SUCCESS'

	def loadAllBetByUid(self, uuid):
		# SQLite
		output = []
		if not findUuid(uuid):
			print("Game.loadAllBetByUid() got wrong uid WTF")
			return []

		uid = readAccountData(uuid)["uid"]
		allBet = readSQ("bethistory","uid",uid)

		for bet in allBet:
			game = self.loadGameByGid(bet[2])
			if game["state"] == 2 and game["winner"] == bet[4]:
				output.append("您在比賽 {} 中下注 {} 點於 {} 方, 獲利 {} 點".format(game["title"],bet[3],bet[4], game["ratio"]*bet[3]))
			elif game["state"] == 2:
				output.append("您在比賽 {} 中下注 {} 點於 {} 方, 輸到脫褲".format(game["title"],bet[3],bet[4]))
			elif game["state"] == 1:
				output.append("您在比賽 {} 中下注 {} 點於 {} 方, 目前已封盤，請等待結果出爐~".format(game["title"],bet[3],bet[4]))
			elif game["state"] == 0:
				output.append("您在比賽 {} 中下注 {} 點於 {} 方".format(game["title"],bet[3],bet[4]))
			else:
				print("這裡有點問題!!!!")
				print(game)

		# f = open("data/account/{}.json".format(uid))
		# data = json.loads(f.readline())
		# f.close()

		# for gid in data["bethistory"]:
		# 	output.extend(self.loadBetByUidAndGid(uid,gid))

		return output

	def loadGameByGid(self,gid):
		# SQLite
		Data = readSQ("games","gid",gid)
		keys_list = readColumnName("games")
		zip_iterator = zip(keys_list, Data[0])
		output = dict(zip_iterator)
		return output

	# def loadBetByUidAndGid(self,uid,gid):
		output = []
		if not os.path.exists("data/games/{}.json".format(gid)):
			print("Game.loadBetByUidAndGid() got wrong gid WTF")
			return []

		f = open("data/games/{}.json".format(gid))
		data = json.loads(f.readline())
		f.close()
		betData = data["betData"]
		title = data["title"]
		if data['state'] == 2:			
			winner = data["winner"]
			ratio = data["ratio"]
			for b in betData:
				if uid in betData[b]:
					for value in betData[b][uid]:
						if b == winner:
							output.append("您在比賽 {} 中下注 {} 點於 {} 方, 獲利 {} 點".format(title,value,b, int(value)*ratio))
						else:
							output.append("您在比賽 {} 中下注 {} 點於 {} 方".format(title,value,b))

		else:
			for b in betData:
				if uid in betData[b]:
					for value in betData[b][uid]:
						output.append("您在比賽 {} 中下注 {} 點於 {} 方".format(title,value,b))

		return output

	def AllGames(self):
		# SQLite
		output = {}
		games = readSQ("games","state",0)
		for g in games:
			o = {"title":g[1],"p1Names":g[7],"p2Names":g[8],"state":g[4]}
			output[g[0]] = o

		games = readSQ("games","state",1)
		for g in games:
			o = {"title":g[1],"p1Names":g[7],"p2Names":g[8],"state":g[4]}
			output[g[0]] = o
		
		games = readSQ("games","state",2)
		for g in games:
			o = {"title":g[1],"p1Names":g[7],"p2Names":g[8],"state":g[4]}
			print(o)		

		return output		
		# try:
		# 	allFileList = os.listdir("data/games")
		# 	for gid in allFileList:
		# 		f = open("data/games/{}".format(gid))
		# 		data = json.loads(f.readline())
		# 		f.close()
		# 		output[gid] = data
		# 	return output

		# except:
		# 	return output

	def allRunningGames(self):
		# return current availabe game
		# SQLite
		output = {}
		games = readSQ("games","state",0)
		for g in games:
			o = {"title":g[1],"p1Names":g[7],"p2Names":g[8],"p1Amount":0,"p2Amount":0}
			gid = g[0]
			allbet = readSQ("bethistory","gid",gid)
			for bet in allbet:
				if bet[4] == o["p1Names"]:
					o["p1Amount"] += bet[3]
				elif bet[4] == o["p2Names"]:
					o["p2Amount"] += bet[3]
				else:
					print("someone bet on an side that's not exists")
			output[g[0]] = o
		return output

		# try:
		# 	allFileList = os.listdir("data/games")
		# 	for gid in allFileList:
		# 		f = open("data/games/{}".format(gid))
		# 		data = json.loads(f.readline())
		# 		f.close()

		# 		if data["state"] == 0:
		# 			output[gid] = data

		# 	return output

		# except:
		# 	return {}
		

	def endBet(self,gid):
		# read and write
		# SQLite

		# if not os.path.exists("data/games/{}.json".format(gid)):
		# 	print("Game.endBet() got wrong gid WTF")
		# 	return
		if len(readSQ("games","gid",gid)) == 0:
			print("Game.endBet() got wrong gid WTF")
			return "Wrong gid"

		if self.loadGameByGid(gid)["state"] == 0:
			updateById("games",{"state":1},gid)
			return "SUCCESS"

		else:
			return "endBet with wrong state, please check"

		# f = open("data/games/{}.json".format(gid))
		# data = json.loads(f.readline())
		# f.close()
		# if data["state"] == 0:
		# 	data["state"] += 1

		# 	f = open("data/games/{}.json".format(gid),"w")
		# 	f.write(json.dumps(data))
		# 	f.close()
		# 	return "SUCCESS"

		# else:
		# 	return "endBet with wrong state, please check"

	def bet(self, gid, uuid, amount, side):
		# only add data for games
		# SQLite
		uid = readAccountData(uuid)["uid"]
		createRow("bethistory",{"gid":gid,"uid":uid,"side":side,"amount":amount})
		return
		# f = open("data/games/{}.json".format(gid))
		# data = json.loads(f.readline())
		# f.close()

		# uid = str(uid)

		# if uid not in data["betData"][side]:
		# 	data["betData"][side][uid] = [amount]

		# else:
		# 	data["betData"][side][uid].append(amount)


		# f = open("data/games/{}.json".format(gid),"w")
		# f.write(json.dumps(data))
		# f.close()		

	def draw(self, gid, winner):
		# calculate the game result and send money to those we win
		# SQLite

		print("draw, gid {}, winner {}".format(gid,winner))
		data = self.loadGameByGid(gid)
		if data["state"] != 1:
			return "draw with wrong state"

		else:
			updateById("games",_id = gid, data = {"state":2})

			allbet = readSQ("bethistory","gid",gid)

			totalAmount = 0
			winnerAmount = 0
			for bet in allbet:
				totalAmount += bet[3]
				if bet[4] == winner:
					winnerAmount += bet[3]

			if winnerAmount != 0:
				ratio = round(totalAmount*1.0/winnerAmount,2)*0.98
			else:
				ratio = 0

			for bet in allbet:
				if bet[4] == winner:
					uuid = readSQ("users","uid",bet[1])[0][1]
					sendMoney(uuid,bet[3]*ratio)
					print("send {} to {}".format(bet[3]*ratio,uuid))


			updateById("games",_id = gid, data = {"endTime":time.asctime( time.localtime(time.time()))})
			updateById("games",_id = gid, data = {"winner":winner})
			updateById("games",_id = gid, data = {"ratio":ratio})

			return "SUCCESS"

		# f = open("data/games/{}.json".format(gid))
		# data = json.loads(f.readline())
		# f.close()

		# if data["state"] != 1:
		# 	return "draw with wrong state"
			
		# else:
			# data["state"] += 1

			# totalAmount = 0
			# winnerAmount = 0
			# for side in data["betData"]:
			# 	for uid in data["betData"][side]:
			# 		totalAmount += sum(data["betData"][side][uid])
			# 		if side == winner:
			# 			winnerAmount += sum(data["betData"][side][uid])

			# if winnerAmount != 0:
			# 	ratio = round(totalAmount*1.0/winnerAmount,2)*0.98


			# 	for uid in data["betData"][winner]:
			# 		betAmount = sum(data["betData"][winner][uid])
			# 		gain = int(betAmount*ratio)
			# 		sendMoney(uid,gain)

			# data["endTime"] = time.asctime( time.localtime(time.time()))
			# data["winner"] = winner
			# data["ratio"] = ratio
			# f = open("data/games/{}.json".format(gid),"w")
			# f.write(json.dumps(data))
			# f.close()





if __name__ == '__main__':
	G = Game()

	# print(G.newGame("testGame",["T1","T2"]))
	print(G.loadGameByGid(2))
