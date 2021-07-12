import sqlite3
from ast import literal_eval

TEST = False
con = sqlite3.connect('data.db',check_same_thread=False)
cur = con.cursor()

# Here are some tools I write to use sqlite in python.

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init():	
	try:
		cur.execute('''CREATE TABLE users (uid int, uuid text, currentAmount int, name text)''')
		cur.execute('''CREATE TABLE bethistory (bid int, uid int, gid int, amount int, side text)''')
		cur.execute('''CREATE TABLE games (gid int, title text, startTime text, endTime text, state int, winner text, ratio real, sideA text, sideB text)''')
		con.commit()
		return "INIT SUCCESS"

	except:
		return "DB ALREADY EXISTS"


def tableSize(tableName):
	a = cur.execute('''select count(*) from {}'''.format(tableName)).fetchall()
	return a[0][0]

def updateById(tableName, data, _id, flag = False):
	for d in data:
		cur.execute("UPDATE {} SET {}=? WHERE {}={}".format(tableName,d,tableName[0]+"id",_id),[data[d]])
	con.commit()
	return



def createRow(tableName, data):
	new_id = tableSize(tableName)

	# create new one
	cur.execute('''INSERT into {} ({}) VALUES (?)'''.format(tableName,tableName[0]+"id"),[new_id])
	updateById(tableName,data,new_id)
	con.commit()
	return new_id

def readColumnName(tableName):
	# read all column names with specific table name
	a = cur.execute('''PRAGMA table_info({})'''.format(tableName))
	a = a.fetchall()
	output = []
	for aa in a:
		output.append(aa[1])
	return output

def readSQ(tableName,key,value):
	# read with specific key and value
	con.row_factory = dict_factory
	cur.execute("SELECT * FROM {} WHERE {} = ?".format(tableName,key),[value])
	return cur.fetchall()

def readAll(tableName):
	# read the whole table
	con.row_factory = dict_factory
	cur.execute("SELECT * FROM {}".format(tableName))
	return cur.fetchall()

def _download():
	# now sure if it works
	con.close()
	con = sqlite3.connect('data.db',check_same_thread=False)
	cur = con.cursor()


def init_from_accountData():
	# init
	# need to work with data.txt in the right form
	# can do manual update to our db
	con_ = sqlite3.connect('data_.db',check_same_thread=False)
	cur_ = con_.cursor()
	cur_.execute('''CREATE TABLE users (uid int, uuid text, currentAmount int, name text)''')
	cur_.execute('''CREATE TABLE bethistory (bid int, uid int, gid int, amount int, side text)''')
	cur_.execute('''CREATE TABLE games (gid int, title text, startTime text, endTime text, state int, winner text, ratio real, sideA text, sideB text)''')
	con_.commit()

	f = open("data.txt")
	for line in f:
		print(line[:-1])
		con_.execute("INSERT INTO users (uid, uuid, currentAmount, name) VALUES {}".format(line[:-1]))
		con_.commit()
	con_.close()



if __name__ == '__main__':
	print(init_from_accountData())
