import json
import os
import time
from constant import *
from account import *

class Game():

	def __init__(self):
		self.runningGame = {}
		self.loadAllRunningGames()


	def newGame(self,title,teamNames):
		# create new game file
		gameData = {"title":title,
					"startTime":time.asctime( time.localtime(time.time()) ),
					"endTime":"",
					"betData":{teamNames[0]:{},teamNames[1]:{}},
					"state":0}

		# count current gid
		gid = len(os.listdir("data/games"))

		# write file
		f = open("data/games/{}.json".format(gid),"w")
		f.write(json.dumps(gameData))
		f.close()

		return 'SUCCESS'


	def loadAllBetByUid(self, uid):
		output = []
		if not os.path.exists("data/account/{}.json".format(uid)):
			print("Game.loadAllBetByUid() got wrong uid WTF")
			return []

		f = open("data/account/{}.json".format(uid))
		data = json.loads(f.readline())
		f.close()

		for gid in data["bethistory"]:
			output.extend(self.loadBetByUidAndGid(uid,gid))

		return output

	def loadBetByUidAndGid(self,uid,gid):
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


	def loadAllRunningGames(self):
		# only load games that are open for betting
		self.runningGame = {}
		try:
			allFileList = os.listdir("data/games")
			for gid in allFileList:
				f = open("data/games/{}".format(gid))
				data = json.loads(f.readline())
				f.close()

				if data["state"] == 0:
					self.runningGame[gid] = data
		return

	def AllGames(self):
		output = {}
		allFileList = os.listdir("data/games")
		for gid in allFileList:
			f = open("data/games/{}".format(gid))
			data = json.loads(f.readline())
			f.close()
			output[gid] = data
		return output

	def allRunningGames(self):
		# return current availabe game
		self.loadAllRunningGames()
		return self.runningGame


	def endBet(self,gid):
		# read and write
		if not os.path.exists("data/games/{}.json".format(gid)):
			print("Game.endBet() got wrong gid WTF")
			return

		f = open("data/games/{}.json".format(gid))
		data = json.loads(f.readline())
		f.close()
		if data["state"] == 0:
			data["state"] += 1

			f = open("data/games/{}.json".format(gid),"w")
			f.write(json.dumps(data))
			f.close()
			return "SUCCESS"

		else:
			return "endBet with wrong state, please check"


	def bet(self, gid, uid, amount, side):
		# only add data for games
		f = open("data/games/{}.json".format(gid))
		data = json.loads(f.readline())
		f.close()

		uid = str(uid)

		if uid not in data["betData"][side]:
			data["betData"][side][uid] = [amount]

		else:
			data["betData"][side][uid].append(amount)


		f = open("data/games/{}.json".format(gid),"w")
		f.write(json.dumps(data))
		f.close()		

	def draw(self, gid, winner):
		# calculate the game result and send money to those we win
		f = open("data/games/{}.json".format(gid))
		data = json.loads(f.readline())
		f.close()

		if data["state"] != 1:
			return "draw with wrong state"
			
		else:
			data["state"] += 1

			totalAmount = 0
			winnerAmount = 0
			for side in data["betData"]:
				for uid in data["betData"][side]:
					totalAmount += sum(data["betData"][side][uid])
					if side == winner:
						winnerAmount += sum(data["betData"][side][uid])

			if winnerAmount != 0:
				ratio = round(totalAmount*1.0/winnerAmount,2)*0.98


				for uid in data["betData"][winner]:
					betAmount = sum(data["betData"][winner][uid])
					gain = int(betAmount*ratio)
					sendMoney(uid,gain)

			data["endTime"] = time.asctime( time.localtime(time.time()))
			data["winner"] = winner
			data["ratio"] = ratio
			f = open("data/games/{}.json".format(gid),"w")
			f.write(json.dumps(data))
			f.close()

			return "SUCCESS"



if __name__ == '__main__':
	G = Game()
	# G.bet(0,1234,231,"TeamName B")
	a = G.allRunningGames()
	for aa in a:
		print(a[aa])

