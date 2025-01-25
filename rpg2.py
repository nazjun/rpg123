# -*- coding: utf-8 -*- 
"""
	rpg2.py
	by N Junco
	November-December 2016
	
	This program launches a simple RPG-inspired minigame.
	This time, it's more complex than ever.
	
	MANUAL:
		Four idols stand before you. You must battle them in any order.
		Once you enter a room, you cannot exit it until a winner is decided, or unless you forfeit.
		Upon defeating an idol, you will receive their blessing. Each blessing has a unique effect on your competence. Each increases a different stat.
		If you lose to any of them, you fail the challenge.
		In battle, you have multiple options:
		"FIGHT" is your attack prompt. You will attack your enemy and they will attack back.
		"EXAMINE" allows you to look up a brief entry about your opponent's stats without losing a turn.
		"INVENTORY" will open your collection of items. You start out with four medicines that heal 50 HP each. Drinking one uses a turn.
		"FORFEIT" lets you give up fighting and ends the challenge. You will lose all progress by doing so.
		
		Here are the stats in detail:
		HP (hit points) is the health supply. Once it hits zero, the fight ends.
		Attack is the average extent of damage that can be dealt. In practice, it randomly varies by a small margin.
		Defence is the opposite of attack. The higher defence, the less damage is taken.
		Luck is the rate at which critical hits are delivered. Its base value is 15%.
		Protection is the opposite of luck. A higher level of protection means a better chance to nullify critical hits.
		Precision is the accuracy of attacks. Its base value is 85%.
		Evasion is the opposite of accuracy. Evasion yields a greater chance of avoiding attacks entirely.
"""

from graphics import *
from time import sleep
from random import randint, choice

win = GraphWin("RPG2",640,480)

# CLASSES ####################################################################################################	
	
# Box class
class Box(object):
	def __init__(self):
		self.obj = []
		for i in range(5):
			col = max(0,255-i*64)
			self.obj.append(Rectangle(Point(0+i*2,360+i*2),Point(639-i*2,479-i*2)))
			self.obj[i].draw(win)
			self.obj[i].setFill(color_rgb(col,col,col))
			
	def clear(self):
		for i in range(len(self.obj)):
			self.obj[i].undraw()
		del self.obj[:]
			
# Text message class
class Message(object):
	def __init__(self,y,size):
		self.obj = Text(Point(20,y),"")
		self.obj.config["anchor"]="nw"
		self.obj.config["justify"]="left"
		self.obj.draw(win)
		self.obj.setFace("courier")
		self.obj.setStyle("normal")
		self.obj.setSize(size)
		
	def set(self,str,r=255,g=255,b=255):
		self.obj.setFill(color_rgb(r,g,b))
		self.obj.setText("")
		sleep(0.1)
		if len(str) > 0:
			for i in range(len(str)+1):
				self.obj.setText("{}".format(str[:i]))
				sleep(0.02)	
			sleep(1)
		
# Options task
class Option(object):
	def __init__(self):
		self.txt = []
		self.box = []
		self.min = []
		self.max = []
		
	def set(self,opts):
		#Before selection
		start = 320-(len(opts)-1)*50
		for i in range(len(opts)):
			self.txt.append(Text(Point(start+i*100,430),opts[i]))
			self.txt[i].draw(win)
			self.txt[i].setSize(5)
			self.txt[i].setFill(color_rgb(255,255,255))
			self.txt[i].setFace("courier")
			self.txt[i].setStyle("bold")
			self.min.append(start-50+i*100)
			self.max.append(start+50+i*100)
			self.box.append(Rectangle(Point(self.min[i]+5,420),Point(self.max[i]-5,440)))
			self.box[i].draw(win)
			for j in range(6,11):
				self.txt[i].setSize(j)
				sleep(0.01)
			for j in range(52):
				self.box[i].setOutline(color_rgb(j*5,j*5,j*5))
				sleep(0.005)
		res = self.select()
		
		#After selection
		restxt,resbox = self.txt.pop(res),self.box.pop(res)
		for i in range(51,-1,-1):
			for j in range(len(opts)-1):
				self.txt[j].setFill(color_rgb(i*5,i*5,i*5))
				self.box[j].setOutline(color_rgb(i*5,i*5,i*5))
			resbox.setOutline(color_rgb(i*5,i*5,i*5))
			sleep(0.005)
		for i in range(len(opts)-1):
			self.txt[i].undraw()
			self.box[i].undraw()
		resbox.undraw()
		for i in range(10,19):
			restxt.setSize(i)
			sleep(0.01)
		for i in range(51,-1,-1):
			restxt.setFill(color_rgb(i*5,i*5,i*5))
			sleep(0.01)
		restxt.undraw()
		del(self.txt[:], self.box[:], self.max[:], self.min[:], restxt, resbox)
		return res
		
	def select(self):
		pick = win.getMouse()
		if pick.getY() >= 420 and pick.getY() < 440 and pick.getX() >= self.min[0] and pick.getX() < self.max[-1]:
			for i in range(len(self.txt)):
				if pick.getX() >= self.min[i] and pick.getX() < self.max[i]:
					return i
		else:
			return self.select()
			
# Health HUD class
class HP(object):
	def __init__(self,name,max,x,anchor,justify):
		self.obj = Text(Point(x,460),"{0}:{1:03d}".format(name,000))
		self.obj.setFace("courier")
		self.obj.setStyle("normal")
		self.obj.setSize(5)
		self.obj.config["anchor"]=anchor
		self.obj.config["justify"]=justify
		self.obj.setFill(color_rgb(255,255,255))
		self.drawn = 0
		self.hp = 0
		self.max = max
		self.name = name
		
	def set(self,obj,value):
		if self.drawn == 0:
			self.obj.draw(win)
			for i in range(6,13):
				self.obj.setSize(i)
				sleep(0.01)
			self.drawn = 1
		self.hp = self.iterate(self.hp,value)
		obj.hp = self.hp
		
	def iterate(self,old,new):
		if new > self.max:
			new = self.max
		elif new < 0:
			new = 0
		if new != old:
			for i in range(14,17):
				self.obj.setSize(i)
				sleep(0.05)
			if new > old:
				for i in range(old,new+1):
					self.obj.setText("{0}:{1:03d}".format(self.name,i))
					sleep(0.002)
			elif new < old:
				for i in range(old,new-1,-1):
					self.obj.setText("{0}:{1:03d}".format(self.name,i))
					sleep(0.002)
			for i in range(16,11,-1):
				self.obj.setSize(i)
				sleep(0.05)
		elif new == old:
			self.obj.setText("{0}:{1:03d}".format(self.name,new))
		return new
		
	def fade(self):
		for i in range(51,-1,-1):
			self.obj.setFill(color_rgb(i*5,i*5,i*5))
			sleep(0.01)
		self.obj.undraw()
		del self.obj
		
# Coloured door class		
class Doors(object):
	def __init__(self):
		self.door = []
		self.greyed = []
		self.col = [[255,102,51],[255,204,102],[102,204,255],[51,102,255]]
		for i in range(4):
			self.door.append(Text(Point(140+120*i,200),"۩"))
			self.door[i].setFace("courier")
			self.door[i].setSize(35)
			self.door[i].setFill(color_rgb(0,0,0))
		self.drawn = 0
		
	def show(self):
		for i in range(4):
			self.door[i].draw(win)
			for j in range(255,-5,-5):
				self.door[i].setFill(color_rgb(max(0,self.col[i][0]-j),max(0,self.col[i][1]-j),max(0,self.col[i][2]-j)))
				sleep(0.01)
		self.drawn = 1
		
	def hide(self):
		for i in range(0,260,5):
			for j in range(4):
				self.door[j].setFill(color_rgb(max(0,self.col[j][0]-i),max(0,self.col[j][1]-i),max(0,self.col[j][2]-i)))
			sleep(0.01)
		for i in range(4):
			self.door[i].undraw()
		self.drawn = 0
		
	def greyout(self,index):
		self.col[index] = [153,153,153]
		self.greyed.append(index)
		
# Curtain class
class Curtain(object):
	def __init__(self):
		self.obj = []
		for i in range(2):
			self.obj.append(Rectangle(Point(i*320,0),Point(319+i*320,480)))
			self.obj[i].setFill(color_rgb(255,255,255))
			self.obj[i].setOutline(color_rgb(255,255,255))
			self.obj[i].draw(win)
		sleep(0.5)
		self.open()
		
	def open(self):
		anchor = self.obj[0].getP2().getX()
		for i in range(64):
			self.obj[0].move(-5,0)
			self.obj[1].move(5,0)
			sleep(0.01)
			
	def close(self):
		for i in range(64):
			self.obj[0].move(5,0)
			self.obj[1].move(-5,0)
			sleep(0.01)
			
# Player class
class Player(object):
	def __init__(self):
		self.type = "player"
		self.maxhp = 100
		self.hp = self.maxhp
		
		# Note: Would have used a dictionary but it does not support indexing, so...
		self.stats = [["attack","defence","luck","protection","precision","evasion"],
						[50,50,50,50,50,50]]
						
		self.inventory = ["MEDICINE"]*4
		
# Boss class
class Boss(object):
	def __init__(self,dict):
		self.type = "boss"
		self.name = dict["name"]
		self.face = dict["face"]
		self.bio = dict["bio"]
		
		self.maxhp = dict["hp"]
		self.hp = self.maxhp
		self.col = [dict["r"],dict["g"],dict["b"]]
		
		#Note: Same reason as above, and to keep a consistent style.
		self.stats = [["attack","defence","luck","protection","precision","evasion"],
						[10+dict["atk"]/5, 50+dict["def"], 50+dict["lck"], 50+dict["prt"], 50+dict["prs"], 50+dict["evs"]]]
		
		self.obj = Text(Point(320,200),self.face)
		self.obj.setFace("courier")
		self.obj.setSize(35)
		self.drawn = 0
		
	def appear(self):
		self.obj.draw(win)
		for i in range(255,-5,-5):
			self.obj.setFill(color_rgb(max(0,self.col[0]-i),max(0,self.col[1]-i),max(0,self.col[2]-i)))
			sleep(0.01)
		self.drawn = 1
		
	def disappear(self):
		if self.hp > 0:
			for i in range(0,260,5):
				self.obj.setFill(color_rgb(max(0,self.col[0]-i),max(0,self.col[1]-i),max(0,self.col[2]-i)))
				sleep(0.01)
		else:
			for i in range(0,130,5):
				self.obj.setFill(color_rgb(max(0,127-i),max(0,127-i),max(0,127-i)))
				sleep(0.01)
		self.obj.undraw()
		self.drawn = 0
		
	def flicker(self,times):
		for i in range(times):
			self.obj.setFill(color_rgb(0,0,0))
			sleep(0.1)
			self.obj.setFill(color_rgb(self.col[0],self.col[1],self.col[2]))
			sleep(0.1)
		
	def flash(self):
		for i in range(2):
			self.obj.setFill(color_rgb(255,255,255))
			sleep(0.1)
			self.obj.setFill(color_rgb(0,0,0))
			sleep(0.1)
		self.obj.setFill(color_rgb(127,127,127))
		
# TASKS ####################################################################################################

# Game end task
def end(text,curt):
	text.set("")
	curt.close()
	exit()

# Attack calculation task
def fight(text,user,target):
	formula = [(user.stats[1][4]/target.stats[1][5])*85,(user.stats[1][2]/target.stats[1][3])*15,(user.stats[1][0]/target.stats[1][1])*randint(45,55)]
	rng = randint(0,100)
	if (user.type == "boss"):
		text.set("{} attacks!".format(user.name))
	else:
		text.set("You attack!")
	# Chance of hitting
	if rng <= formula[0]:
		rng = randint(0,100)
		# Chance of critical hit
		if rng <= formula[1]:
			dmg = round(formula[2])*2
			if(target.type == "boss"):
				target.flicker(4)
			target.hphud.set(target,target.hp-dmg)
			text.set("A critical hit!")
		else:
			dmg = round(formula[2])
			if(target.type == "boss"):
				target.flicker(2)
			target.hphud.set(target,target.hp-dmg)
			
	else:
		text.set("But the attack missed...")
			
# Boss room task
def bossroom(index,text,opt,door,curt,you):
	bosses = [ 	{"name":"Akua Ahi",		"face": "火",	"r":255,"g":102,"b":51,	"hp":500,	"atk":20,	"def":-20,	"prs":-10,	"evs":0,	"lck":10,	"prt":0,
					"bio":["\"Entry I:\"",
							"\"Akua Ahi, the idol of fire...\"",
							"\"They have immense power, however their\ndefences are lacking.\"",
							"\"They also tend to be very reckless and\nmiss their targets.\""]},
				{"name":"Akua Lepo",	"face": "土",	"r":255,"g":204,"b":102,"hp":500,	"atk":-20,	"def":20,	"prs":0,	"evs":-10,	"lck":0,	"prt":10,
					"bio":["\"Entry II:\"",
							"\"Akua Lepo, the idol of earth...\"",
							"\"Their defence is unbreakable, however they\nare very sluggish in attacking.\"",
							"\"They are so placid and confident that\nthey will not even try to dodge attacks.\""]},
				{"name":"Akua Makani",	"face": "气",	"r":102,"g":204,"b":255,"hp":500,	"atk":0,	"def":-10,	"prs":10, 	"evs":-5,	"lck":20,	"prt":-5,
					"bio":["\"Entry III:\"",
							"\"Akua Makani, the idol of wind...\"",
							"\"They rely solely on their luck, as they\ndo not have very much stamina.\"",
							"\"They are the most anxious of the idols\nand prioritise having perfect accuracy.\""]},
				{"name":"Akua Wai",		"face": "水",	"r":51,	"g":102,"b":255,"hp":500,	"atk":-10,	"def":0,	"prs":-5,	"evs":10,	"lck":-5,	"prt":20,
					"bio":["\"Entry IV:\"",
							"\"Akua Wai, the idol of water...\"",
							"\"They are both resilient and evasive, but they\ndo not attack very forcefully.\"",
							"\"They are a trickster. Not only are they hard\nto hit, they can also take many hits.\""]},
				{"name":"Akua Lani",	"face": "大天王","r":153,"g":102,"b":153,"hp":750,	"atk":5,	"def":5,	"prs":5,	"evs":5,	"lck":5,	"prt":5,
					"bio":["\"Entry V:\"",
							"\"Akua Lani, the supreme god of the idols...\"",
							"\"They are very adept in all areas. Please\ntake extreme caution.\"",
							"\"They have all of the other idols' skills,\nplus a whopping health pool.\"",
							"\"They are so self-absorbed, they have three\ncharacters in their body rather than one.\""]}]
	sleep(0.5)
	curt.open()
	boss = Boss(bosses[index])
	boss.appear()
	text.set("{} challenges you!".format(boss.name))
	boss.hphud = HP(boss.name.upper(),boss.maxhp,620,"e","right")
	boss.hphud.set(boss,boss.hp)
	while you.hp > 0 and boss.hp > 0:
		text.set("What will you do?")
		res = opt.set(["FIGHT","EXAMINE","INVENTORY","FORFEIT"])
		if res == 0:
			fight(text,you,boss)
			
		elif res == 1:
			for i in boss.bio:
				text.set(i)
			continue
		elif res == 2:
			if len(you.inventory) > 0:
				text.set("Use an item?")
				itemsandexit = you.inventory + ["EXIT"]
				item = opt.set(itemsandexit)
				if itemsandexit[item] == "MEDICINE":
					you.inventory.pop(item)
					text.set("You used the Medicine...")
					you.hphud.set(you,you.hp+50)
					text.set("You restored 50 HP!")
				elif itemsandexit[item] == "NECTAR":
					you.inventory.pop(item)
					text.set("You used the Nectar...")
					you.hphud.set(you,you.hp+100)
					text.set("You restored all of your HP! Amazing!")
				else:	
					continue
			else:
				text.set("You have no items...")
				continue
		elif res == 3:
			text.set("Farewell, then...")
			boss.disappear()
			end(text,curt)
		if boss.hp > 0:
			fight(text,boss,you)
	
	if boss.hp == 0:
		boss.hphud.fade()	
		boss.flash()
		sleep(0.5)
		text.set("You defeated {}!".format(boss.name))
		if index == 4:
			you.hphud.fade()
			boss.disappear()
			text.set("")
			curt.close()
			sleep(0.5)
		else:
			you.stats[1][index]+=10
			text.set("You were blessed! Your {} rose!".format(you.stats[0][index]))
			boss.disappear()
			text.set("")
			curt.close()
			sleep(0.5)
			curt.open()
			door.greyout(index)
			lobby(text,opt,door,curt,you)
		
	
	elif you.hp == 0:
		you.hphud.fade()
		text.set("You were defeated!")
		text.set("See you on the other side, then...")
		boss.disappear()
		end(text,curt)
			
# Lobby task
def lobby(text,opt,door,curt,you):
	if len(door.greyed) == 4:
		text.set("...")
		text.set("Incredible.")
		text.set("You defeated the four idols with minimal\neffort.")
		text.set("However... there is, in fact, one more.")
		text.set("This idol is far stronger than the others.")
		text.set("Prepare yourself, now...")
		text.set("")
		curt.close()
		bossroom(4,text,opt,door,curt,you)
	else:
		if len(door.greyed) == 3:
			text.set("How are you managing?")
			text.set("Since you defeated three idols thus far, it\nwould only be fair to give you a small boost.")
			you.inventory.append("NECTAR")
			text.set("This item is Nectar, the beverage of the gods.\nOne bottle of this sacred fluid will heal you\nentirely.")
			text.set("Use it wisely...")
		if door.drawn == 0:
			text.set("")
			door.show()
			text.set("Four doors stand in your path.")
		text.set("Enter the door that piques your interest.")
		res = opt.set(["RED","YELLOW","CYAN","BLUE"])
		if res in door.greyed:
			text.set("It seems to be sealed...")
			lobby(text,opt,door,curt,you)
		else:
			text.set("")
			door.hide()
			curt.close()
			bossroom(res,text,opt,door,curt,you)

# Information task
def info(text,opt):
	text.set("Four idols stand before you. You must do\nbattle with each of them in the order of your\nchoosing.")
	text.set("Once you enter a room, you cannot exit it\nuntil either a winner is decided, or you\nforfeit.")
	text.set("Upon defeating an idol, you will receive their\nblessing. Each blessing has a unique effect on\nyour competence.")
	text.set("However, If you lose to any of them, you fail.")
	text.set("In battle, you have multiple options:")
	text.set("\"FIGHT\" is your attack prompt. You will attack\nyour enemy and they will attack back.")
	text.set("\"EXAMINE\" allows you to look up a brief entry\nabout your opponent's stats without losing a\nturn.")
	text.set("\"INVENTORY\" will open your collection of\nitems. You start out with four medicines that\nheal 50 HP each. Drinking one uses a turn.")
	text.set("\"FORFEIT\" lets you give up fighting and ends\nthe challenge. You will lose all progress by\ndoing so.")
	text.set("May fortune smile upon you.")

# Intro task
def intro(text,opt,curt):
	while True:
		text.set("... Welcome.")
		res = opt.set(["START","MANUAL","QUIT"])
		if res == 0:
			text.set("Prepare yourself...")
			break
		elif res == 1:
			info(text,opt)
		elif res == 2:
			text.set("Farewell.")
			end(text,curt)
			
# Epilogue task
def epilogue(text):
	text.set("So, it appears that you have defeated\neven the god of the idols...")
	text.set("I applaud you. You have survived a hellion\nof RNG that not many would tolerate.")
	text.set("I thank you, as well. I hope that you\nfound this challenging and engaging.")
	text.set("Thank you for playing!")
	text.set("")

# Main task
def main():
	win.setBackground(color_rgb(0,0,0))
	box = Box()
	curt = Curtain()
	text = Message(380,16)
	opt = Option()
	door = Doors()
	you = Player()
	intro(text,opt,curt)
	you.hphud = HP("PLAYER",100,20,"w","left")
	you.hphud.set(you,you.hp)
	lobby(text,opt,door,curt,you)
	
	# Returns here when all bosses are defeated
	box.clear()
	
	curt.open()
	etext = Message(240,18)
	epilogue(etext)
	end(text,curt)

if __name__ == "__main__":
	main()