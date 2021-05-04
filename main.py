from flask import Flask, render_template, Response, request, redirect, url_for 
from game import Game
from login import _login, register
from account import readAccountData, bet_ac, sendMoney, readAccountBalance, allaccount
from constant import *

import os
# Hi
app = Flask(__name__)
G = Game()

@app.route("/")
@app.route('/login')
def login():
	return render_template('login.html')

@app.route("/index",  methods=['POST'])
def index():
	print(G.allRunningGames())
	print(request.form)
	if "account" in request.form:
		userUid = _login(request.form['account'], request.form['pw'])

	elif "uid" in request.form:
		userUid = request.form['uid']


	if userUid == WRONG_ACCOUNT:
		return "帳號錯誤"

	elif userUid == WRONG_PW:
		return "密碼錯誤"

	else:
		userData = readAccountData(userUid)
		betHistory = G.loadAllBetByUid(userUid)

		return render_template('index.html', userName = userData["name"], balance = userData["currentAmount"],data = betHistory, uid = userUid)


@app.route("/bet", methods=["POST"])
def bet():
	gameData = []
	allGames = G.allRunningGames()
	for game in allGames:
		# players = []

		# for p in allGames[game]["betData"]:
		# 	players.append(p)

		p1Total = allGames[game]["p1Amount"]
		p2Total = allGames[game]["p2Amount"]


		# for u in allGames[game]["betData"][players[0]]:
		# 	p1Total += sum(allGames[game]["betData"][players[0]][u])

		# for u in allGames[game]["betData"][players[1]]:
		# 	p2Total += sum(allGames[game]["betData"][players[1]][u])

		print(p1Total,p2Total)
		if p1Total == 0:
			p1Ratio = "無人下注"
		else:
			p1Ratio = round((p1Total+p2Total)/p1Total*0.98,2)

		if p2Total == 0:
			p2Ratio = "無人下注"
		else:
			p2Ratio = round((p1Total+p2Total)/p2Total*0.98,2)


		g = {"gid":game,
			"title":allGames[game]["title"],
			"p1":allGames[game]["p1Names"],
			"p2":allGames[game]["p2Names"],
			"p1Ratio":p1Ratio,
			"p2Ratio":p2Ratio}
		gameData.append(g)

	print(gameData)
	b = readAccountBalance(request.form["uid"])
	return render_template('bet.html', CurrentGames = gameData, uid = request.form["uid"], balance = b)

@app.route("/settle_bet", methods=["POST"])
def settle_bet():
	try:
		totalCost =  int(request.form["num"])
	except:
		return "請輸入數字"
	accountResult = bet_ac(uuid = request.form["uid"], gid = request.form["gid"], amount = totalCost*100)
	if accountResult == WRONG_ACCOUNT:
		return "WRONG_ACCOUNT"

	elif accountResult == INSUFFICIENT:
		return "餘額不足"

	print("{} bet on {} with {}".format(request.form["uid"], request.form["side"], int(request.form["num"])*100))
	G.bet(gid = request.form["gid"], uuid = request.form["uid"], amount = int(request.form["num"])*100, side = request.form["side"])

	return "下注成功"

@app.route("/new_game", methods=["POST"])
def new_game():
	title = request.form["title"]
	names = [request.form["n1"],request.form["n2"]]
	print(title)
	print(names)
	r = G.newGame(title,names)
	return r


@app.route("/new_account", methods=["POST"])
def new_account():
	ac = request.form["ac"]
	pw = request.form["pw"]
	print("new account：")
	print(ac)
	print(pw)
	r = register(ac,pw)
	if r == NAME_USED:
		return "NAME_USED"

	else:
		return "SUCCESS"


@app.route("/manager", methods=["POST"])
def manager():
	print(request.form['account'],request.form['pw'])
	if request.form['account'] != "manager" or request.form['pw'] != "qwerasdf":
		return "Fuck off !!!!!"

	allGames = G.AllGames()
	print("all games:")
	gameData = []
	for game in allGames:

		g = {"gid":game,
			"title":allGames[game]["title"],
			"p1":allGames[game]["p1Names"],
			"p2":allGames[game]["p2Names"],
			"state":allGames[game]["state"],}
		gameData.append(g)
		print(g)
	# print(gameData)
	return render_template('manager.html',gameData = gameData)


@app.route("/endBet", methods=["POST"])
def endBet():
	gid = request.form["gid"]
	r = G.endBet(gid)
	return r

@app.route("/draw", methods=["POST"])
def draw():
	gid = request.form["gid"]
	winner = request.form["winner"]
	r = G.draw(gid,winner)
	return r

@app.route("/send_money", methods=["POST"])
def send_money():
	uid = request.form["uid"]
	amount = int(request.form["amount"])
	r = sendMoney(uid,amount)
	return "SUCCESS"

@app.route("/all_account", methods=["GET"])
def all_account():
	o = allaccount()
	output = "(uid, uuid, currentAmount, name)\n"
	for oo in o:
		output += str(oo)
		output += "\n"
	return output

@app.route("/all_bet", methods=["GET"])
def all_bet():
	o = G._allb()
	output = "(bid, uid, gid, amount, side)<br>"
	for oo in o:
		output += str(oo)
		output += "<br>"
	return output

@app.route("/all_games", methods=["GET"])
def all_games():
	o = G._allg()
	output = "(gid, title, startTime, endTime, state, winner, ratio, sideA, sideB)<br>"
	for oo in o:
		output += str(oo)
		output += "<br>"
	return output


if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
