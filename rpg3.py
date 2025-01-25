# -*- coding: utf-8 -*- 
"""
	rpg3.py
	by Nazar Junco
	April-May 2018
	
	This program launches a simple (or is it, now?) RPG-styled game.
	In this installment, the complexity is through the roof.
	
	MANUAL:
		There are seven idols this time around, but you may choose not to battle all of them.
		Once you enter a room, you cannot exit it until a winner is decided, or unless you forfeit.
		If you lose to any of them, you fail the challenge.
		Upon defeating an idol, you will pick up some gold, which can be used to purchase new items, spells, and perks.

		In battle, you have multiple options:
		"FIGHT" is your attack prompt. You will attack your enemy and they will attack back.
		"MAGIC" accesses the spells menu. Casting a spell requires mana.
		"BAG" will open your collection of items. You start out with a Medicine and an Elixir.
		"FORFEIT" lets you give up fighting and ends the challenge. You will lose all progress by doing so.
		
		These are the stats in detail.
		HP (hit points) is the health supply. Once it hits zero, the fight ends.
		Attack is the average extent of damage that can be dealt. In practice, it randomly varies by a small margin.
		Defence is the opposite of attack. The higher defence, the less damage is taken.
		Luck is the rate at which critical hits are delivered. Its base value is 15%.
		Protection is the opposite of luck. A higher level of protection means a better chance to nullify critical hits.
		Precision is the accuracy of attacks. Its base value is 85%.
		Evasion is the opposite of accuracy. Evasion yields a greater chance of avoiding attacks entirely.
		
		More information can be found in the in-game manual.
"""

from graphics import * 
from time import sleep
from random import randint, choice
from math import ceil

# CLASSES ####################################################################################################	
	
# Box class
class Box(object):
	def __init__(self, pt1, pt2):
		self.obj = []
		self.hidden = True
		for i in range(5):
			self.obj.append(Rectangle(Point(pt1[0] + i * 2, pt1[1] + i * 2), Point(pt2[0] - i * 2, pt2[1] - i * 2)))
			self.obj[i].setOutline(color_rgb(0, 0, 0))
			self.obj[i].draw(win)
			self.obj[i].move(0, -480)
		self.obj[0].setFill(color_rgb(0, 0, 0))
		
	def show(self):
		if self.hidden:
			for i in range(len(self.obj)):
				self.obj[i].move(0, 480)
				for j in range(0, 255 + 51, 51):
					self.obj[i].setOutline(color_rgb(max(0, j - i * 64), max(0, j - i * 64), max(0, j - i * 64)))
					sleep(1 / 60)
			self.hidden = False
		else: pass
			
	def hide(self):
		if not self.hidden:
			for i in range(len(self.obj) - 1, - 1, - 1):
				for j in range(255, - 51, - 51):
					self.obj[i].setOutline(color_rgb(max(0, j - i * 64), max(0, j - i * 64), max(0, j - i * 64)))
					sleep(1 / 60)
				self.obj[i].move(0, -480)
			self.hidden = True
		else: pass
			
# Background effect class
class Backdrop(object):
	def __init__(self):
		self.obj = []
		self.c = [255, 255, 255]
		self.hidden = True
		for i in range(31):
			self.obj.append(Line(Point((i + 1) * 20, 0), Point(((i + 1) * 20) * 2 - 320, 360)))
			self.obj[i].setOutline(color_rgb(0, 0, 0))
			self.obj[i].setWidth(2)
			self.obj[i].draw(win)
			
		for i in range(15):
			self.obj.append(Line(Point(0, (i + 1) * (10 + i)), Point(640, (i + 1) * (10 + i))))
			self.obj[i + 31].setOutline(color_rgb(0, 0, 0))
			self.obj[i + 31].setWidth(2)
			self.obj[i + 31].draw(win)
			
	def show(self, col=[255, 255, 255]):
		self.c = col
		if self.hidden:
			for i in range(255, - 51, - 51):
				for j in range(len(self.obj)):
					self.obj[j].setOutline(color_rgb(max(0, self.c[0] - i), max(0, self.c[1] - i), max(0, self.c[2] - i)))
				sleep(1 / 60)
			self.hidden = False
		else: pass
			
	def hide(self):
		if not self.hidden:
			for i in range(0, 255 + 51, 51):
				for j in range(len(self.obj)):
					self.obj[j].setOutline(color_rgb(max(0, self.c[0] - i), max(0, self.c[1] - i), max(0, self.c[2] - i)))
				sleep(1 / 60)
			self.hidden = True
		else: pass
		
class EndBG(object):
	def __init__(self):
		self.obj = []
		self.hidden = True
		for i in range(60):
			self.obj.append(Line(Point(0, 8 * i), Point(640, 8 * i - 60)))
			self.obj[i].setOutline(color_rgb(0, 0, 0))
			self.obj[i].setWidth(8)
			self.obj[i].draw(win)
			
	def show(self):
		if self.hidden:
			for i in range(255, -17, -17):
				for j in range(len(self.obj)):
					self.obj[j].setOutline(color_rgb(max(0, 0 - i + j * 4), max(0, - 100 - i + j * 4), max(0, 100 - i - j * 4)))
				sleep(1 / 60)
			self.hidden = False
		else: pass
			
	def hide(self):
		if not self.hidden:
			for i in range(0, 255 + 17, 17):
				for j in range(len(self.obj)):
					self.obj[j].setOutline(color_rgb(max(0, 0 - i + j * 4), max(0, - 100 - i + j * 4), max(0, 100 - i - j * 4)))
				sleep(1 / 60)
			self.hidden = True
		else: pass
			
# Terrain class
class Terrain(object):
	def __init__(self):
		self.obj = []
		self.obj.append(Oval(Point(0, 320), Point(359, 439)))
		self.obj.append(Oval(Point(320, 120), Point(639, 239)))
		self.hidden = True
		for i in range(2):
			self.obj[i].setOutline(color_rgb(0, 0, 0))
			self.obj[i].setFill(color_rgb(0, 0, 0))
			self.obj[i].setWidth(5)
			self.obj[i].draw(win)
			self.obj[i].move(0, - 480)
		
	def show(self):
		if self.hidden:
			for i in range(len(self.obj)):
				self.obj[i].move(0, 480)
				for j in range(0, 255 + 17, 17):
					self.obj[i].setOutline(color_rgb(max(0, j), max(0, j), max(0, j)))
					sleep(1 / 60)
			self.hidden = False
		else: pass
			
	def hide(self):
		if not self.hidden:
			for i in range(len(self.obj) - 1, - 1, - 1):
				for j in range(255, -17, -17):
					self.obj[i].setOutline(color_rgb(max(0, j), max(0, j), max(0, j)))
					sleep(1 / 60)
				self.obj[i].move(0, - 480)
			self.hidden = True
		else: pass
		
# Text message class
class Message(object):
	def __init__(self, y, size):
		self.obj = Text(Point(20, y), "")
		self.obj.config["anchor"]="nw"
		self.obj.config["justify"]="left"
		self.obj.draw(win)
		self.obj.setFace("courier")
		self.obj.setStyle("normal")
		self.obj.setSize(size)
		
	def set(self, str, r=255, g=255, b=255):
		spl = str.split()
		cnt = 0
		
		# Highly unorthodox way of auto-generating line breaks ahoy.
		for i in range(len(spl)):
			cnt += len(spl[i])	
			if cnt > 44:
				spl[i - 1] = spl[i - 1] + "\n"
				cnt = len(spl[i - 1])			
			else:
				spl[i - 1] = spl[i - 1] + " "
				cnt += 1	
		str = "".join(spl)
		self.obj.setFill(color_rgb(r, g, b))
		self.obj.setText("")
		sleep(1 / 30)
		if len(str) > 0:
			for i in range(len(str) + 1):
				self.obj.setText("{}".format(str[:i]))
				sleep(1 / 60)	
			sleep(1)
			
# Pre-game watermark class
class Watermark(object):
	def __init__(self):
		self.obj = Text(Point(320, 240), "Created by Nazar Junco, 2018.")
		self.obj.setFace("courier")
		self.obj.setStyle("normal")
		self.obj.setSize(16)
		
	def show(self):
		self.obj.draw(win)
		for i in range(255, -17, -17):
			self.obj.setFill(color_rgb(i, i, i))
			sleep(1 / 60)
		
	def hide(self):
		for i in range(0, 255 + 17, 17):
			self.obj.setFill(color_rgb(i, i, i))
			sleep(1 / 60)
		self.obj.undraw()
		
# Options task
class Option(object):
	def __init__(self):
		self.txt = []
		self.box = []
		self.min = []
		self.max = []
		
	def set(self, opts):
		#Before selection
		start = 320 - (len(opts) - 1) * 50
		for i in range(len(opts)):
			self.txt.append(Text(Point(start + i * 100, 440), opts[i]))
			self.txt[i].draw(win)
			self.txt[i].setSize(5)
			self.txt[i].setFill(color_rgb(255, 255, 255))
			self.txt[i].setFace("courier")
			self.txt[i].setStyle("bold")
			self.min.append(start - 50 + i * 100)
			self.max.append(start + 50 + i * 100)
			self.box.append(Polygon(Point(self.min[i] + 10, 420), Point(self.max[i] - 10, 420), Point(self.max[i] - 5, 440), Point(self.max[i] - 10, 460), Point(self.min[i] + 10, 460), Point(self.min[i] + 5, 440)))
			self.box[i].draw(win)
		for j in range(6, 11):
			for i in range(len(opts)):
				self.txt[i].setSize(j)
			sleep(1 / 60)
		for j in range(0, 255 + 51, 51):
			for i in range(len(opts)):
				self.box[i].setOutline(color_rgb(j, j, j))
			sleep(1 / 60)
		res = self.select()
		
		#After selection
		restxt, resbox = self.txt.pop(res), self.box.pop(res)
		for i in range(255, -51, -51):
			for j in range(len(opts) - 1):
				self.txt[j].setFill(color_rgb(i, i, i))
				self.box[j].setOutline(color_rgb(i, i, i))
			resbox.setOutline(color_rgb(i, i, i))
			sleep(1 / 60)
		for i in range(len(opts) - 1):
			self.txt[i].undraw()
			self.box[i].undraw()
		resbox.undraw()
		for i in range(10, 19):
			restxt.setSize(i)
			sleep(1 / 60)
		sleep(1 / 6)
		for i in range(255, -51, -51):
			restxt.setFill(color_rgb(i, i, i))
			sleep(1 / 60)
		restxt.undraw()
		del(self.txt[:], self.box[:], self.max[:], self.min[:], restxt, resbox)
		return res
		
	def select(self):
		pick = win.getMouse()
		if pick.getY() >= 420 and pick.getY() < 460 and pick.getX() >= self.min[0] and pick.getX() < self.max[ - 1]:
			for i in range(len(self.txt)):
				if pick.getX() >= self.min[i] and pick.getX() < self.max[i]:
					return i
		else:
			return self.select()
			
# Health/Mana/Gold HUD class
class Stat(object):
	def __init__(self, name, max, x, y, anchor, justify, string = "{0}:{1}"):
		self.string = string
		self.obj = Text(Point(x, y), self.string.format(name, 0, max))
		self.obj.setFace("courier")
		self.obj.setStyle("bold")
		self.obj.setSize(5)
		self.obj.config["anchor"]=anchor
		self.obj.config["justify"]=justify
		self.obj.setFill(color_rgb(255, 255, 255))
		self.drawn = 0
		self.value = 0
		self.max = max
		self.name = name
		
	def set(self, value):
		if self.drawn == 0:
			self.obj.draw(win)
			for i in range(6, 13):
				self.obj.setSize(i)
				sleep(1 / 60)
			self.drawn = 1
		self.value = self.iterate(self.value, value)
		
	def remax(self, value):
		self.max = self.iterate(self.max, value, True)
		
	def iterate(self, old, new, remax = False):
		if new > self.max and not remax:
			new = self.max
		elif new < 0:
			new = 0
		if new != old:
			for i in range(14, 17):
				self.obj.setSize(i)
				sleep(1 / 60)
			if new > old:
				for i in range(old, new + 1):
					if remax:
						self.obj.setText(self.string.format(self.name, self.value, i))
					else:
						self.obj.setText(self.string.format(self.name, i, self.max))
					if (old + i) % 10 == 0:
						sleep(1 / 60)
						pass
			elif new < old:
				for i in range(old, new - 1, -1):
					if remax:
						self.obj.setText(self.string.format(self.name, self.value, i))
					else:
						self.obj.setText(self.string.format(self.name, i, self.max))
					if (old + i) % 10 == 0:
						sleep(1 / 60)
						pass
			sleep(1 / 6)
			for i in range(16, 11, -1):
				self.obj.setSize(i)
				sleep(1 / 60)
		elif new == old:
			self.obj.setText(self.string.format(self.name, new, self.max))
		return new
		
	def fade(self):
		if self.obj:
			for i in range(255, -51, -51):
				self.obj.setFill(color_rgb(i, i, i))
				sleep(1 / 60)
			self.obj.undraw()
			del self.obj

# Coloured door class		
class Doors(object):
	def __init__(self):
		self.door = []
		self.won = []
		self.col = []
		for i in range(8):
			self.col.append(bosses[i]["col"])
			self.door.append(Text(Point(320, 200), "۩"))
			self.door[i].setFace("courier")
			self.door[i].setSize(64)
			self.door[i].setFill(color_rgb(0, 0, 0))
		self.drawn = []
		self.options = []
		
	def show(self):
		self.determine()
		inds = self.options
		for i in range(len(inds)):
			self.door[inds[i]].move(120 * i - 60 * (len(inds) - 1), 0)
			self.door[inds[i]].draw(win)
			for j in range(255, -17, -17):
				self.door[inds[i]].setFill(color_rgb(max(0, self.col[inds[i]][0] - j), max(0, self.col[inds[i]][1] - j), max(0, self.col[inds[i]][2] - j)))
				sleep(1 / 60)
		self.drawn = inds
		
	def hide(self):
		inds = self.options
		for i in range(0, 255 + 17, 17):
			for j in self.drawn:
				self.door[j].setFill(color_rgb(max(0, self.col[j][0] - i), max(0, self.col[j][1] - i), max(0, self.col[j][2] - i)))
			sleep(1 / 60)
		for i in range(len(inds)):
			self.door[inds[i]].move((120 * i - 60 * (len(inds) - 1)) * - 1, 0)
			self.door[inds[i]].undraw()
		self.drawn = []
		
	def win(self, index):
		if index not in self.won:
			self.won.append(index)
		
	# Convoluted method to determine door appearances almost gave me depression trying to debug
	def determine(self):
		doors = []
		if 0 not in self.won or 1 not in self.won:
			if 2 not in self.won and 3 not in self.won:
				doors.extend([0, 1])
		if 0 in self.won or 1 in self.won:
			if 4 not in self.won and 5 not in self.won:
				doors.extend([2, 3])
		if 2 in self.won or 3 in self.won:
			if 6 not in self.won:
				doors.extend([4, 5])
		if 4 in self.won or 5 in self.won:
			doors.append(6)
		if len(self.won) == 7:
			doors.append(7)
		for i in self.won:
			if i in doors:
				doors.remove(i)
		self.options = doors
		
# Curtain class
class Curtain(object):
	def __init__(self):
		self.obj = []
		for i in range(2):
			self.obj.append(Rectangle(Point(i * 320, 0), Point(319 + i * 320, 480)))
			self.obj[i].setFill(color_rgb(255, 255, 255))
			self.obj[i].setOutline(color_rgb(255, 255, 255))
			self.obj[i].draw(win)
		
	def open(self):
		anchor = self.obj[0].getP2().getX()
		for i in range(32):
			self.obj[0].move(-10, 0)
			self.obj[1].move(10, 0)
			sleep(1 / 60)
			
	def close(self):
		for i in range(32):
			self.obj[0].move(10, 0)
			self.obj[1].move(-10, 0)
			sleep(1 / 60)
			
# Player class
class Player(object):
	def __init__(self):
		self.type = "player"
		self.hp = Stat("LIFE", 100, 20, 300, "w", "left", "{0}:{1:03d}/{2}")
		self.mp = Stat("MANA", 10, 20, 320, "w", "left", "{0}:{1:02d}/{2}")
		self.gd = Stat("GOLD", 999, 20, 340, "w", "left", "{0}:{1}G")
		# Note: Would have used a dictionary but it does not support indexing, so...
		self.stats = [["attack", "defence", "luck", "protection", "precision", "evasion"], 
						[50, 50, 50, 50, 50, 50]]
		self.bag = ["MEDICINE", "ELIXIR"]
		self.perks = []
		self.maxbag = 5
		self.magic = [["ZAP", 5]]
		self.lasthit = []
		
	def fadeall(self):
		self.hp.fade()
		self.mp.fade()
		self.gd.fade()
		
# Boss class
class Boss(object):
	def __init__(self, dict):
		self.type = "boss"
		self.name = dict["name"]
		self.face = dict["face"]
		self.hp = Stat("BOSS", dict["hp"], 580, 20, "c", "right", "{0}:{1:03d}")
		self.col = dict["col"]
		#Note: Same reason as above, and to keep a consistent style.
		self.stats = [["attack", "defence", "luck", "protection", "precision", "evasion"], 
						[(dict["atk"]) / 5, dict["def"], dict["lck"], dict["prt"], dict["prs"], dict["evs"]]]
		self.lasthit = []
		self.status = []
		self.god = False
		self.obj = Text(Point(480, 160), self.face)
		self.obj.setFace("courier")
		self.obj.setSize(96 if dict["name"] == "Akua Hala" else 64)
		self.drawn = 0
	def appear(self):
		self.obj.draw(win)
		for i in range(255, -5, -5):
			self.obj.setFill(color_rgb(max(0, self.col[0] - i), max(0, self.col[1] - i), max(0, self.col[2] - i)))
			sleep(1 / 120)
		self.drawn = 1	
	def disappear(self):
		if self.hp.value > 0:
			for i in range(0, 260, 5):
				self.obj.setFill(color_rgb(max(0, self.col[0] - i), max(0, self.col[1] - i), max(0, self.col[2] - i)))
				sleep(1 / 120)
		else:
			for i in range(0, 130, 5):
				self.obj.setFill(color_rgb(max(0, 127 - i), max(0, 127 - i), max(0, 127 - i)))
				sleep(1 / 120)
		self.obj.undraw()
		self.drawn = 0
	def flicker(self, times, col=[0, 0, 0]):
		for i in range(times):
			self.obj.setFill(color_rgb(col[0], col[1], col[2]))
			sleep(1/12)
			self.obj.setFill(color_rgb(self.col[0], self.col[1], self.col[2]))
			sleep(1/12)
	def flash(self):
		for i in range(2):
			self.obj.setFill(color_rgb(255, 255, 255))
			sleep(1/12)
			self.obj.setFill(color_rgb(0, 0, 0))
			sleep(1/12)
		self.obj.setFill(color_rgb(127, 127, 127))
		
# TASKS ####################################################################################################

# Game end task
def end():
	text.set("")
	floor.hide()
	ebg.hide()
	bg.hide()
	you.fadeall()
	pbox.hide()
	box.hide()
	curt.close()
	exit()

# Attack calculation task
def fight(user, target, usetext = True, spell = False, spldmg=0):
	# Precision/Evasion, Luck/Protection, Attack/Defence
	formula = [(user.stats[1][4] / target.stats[1][5]) * 90, (user.stats[1][2] / target.stats[1][3]) * 10, (user.stats[1][0] / target.stats[1][1]) * randint(45, 55)]
	rng = randint(0, 100)
	summary = []
	if usetext:
		if (user.type == "boss"):
			text.set("{} attacks!".format(user.name))
		else:
			text.set("You attack!")
	# Exceptional attacks
	if spell:
		dmg = spldmg
		target.hp.set(target.hp.value - dmg)
		summary.extend((dmg, "HIT", "SPELL"))
	else:
		# Chance of hitting
		if rng <= formula[0]:
			rng = randint(0, 100)
			# Chance of critical hit
			if rng <= formula[1]:
				dmg = ceil(formula[2]) * 2
				if(target.type == "boss"):
					target.flicker(4)
				target.hp.set(target.hp.value - dmg)
				text.set("A critical hit!")
				summary.extend((dmg, "HIT", "CRIT"))
			else:
				dmg = ceil(formula[2])
				if(target.type == "boss"):
					target.flicker(2)
				target.hp.set(target.hp.value - dmg)
				summary.extend((dmg, "HIT"))
		else:
			text.set("But the attack missed...")
			summary.extend((0, "MISS"))
	user.lasthit = summary
			
# Boss room task
def bossroom(index):
	bg.show([max(0, i - 102) for i in bosses[index]["col"]])
	boss = Boss(bosses[index])
	floor.show()
	boss.appear()
	text.set("{} challenges you!".format(boss.name))
	bbox.show()
	boss.hp.set(bosses[index]["hp"])
	while you.hp.value > 0 and boss.hp.value > 0:
		you.lasthit = []
		boss.lasthit = []
		# Your turn
		text.set("What will you do?")
		res = opt.set(["FIGHT", "MAGIC", "BAG", "FORFEIT"])
		if res == 0:
			fight(you, boss)
		elif res == 1:
			text.set("Cast a spell?")
			spellsandexit = ["{0}\n{1} MANA".format(you.magic[i][0], you.magic[i][1]) for i in range(len(you.magic))] + ["(EXIT)"]
			spell = opt.set(spellsandexit)
			if spellsandexit[spell] == "(EXIT)":	
				continue	
			elif you.mp.value >= you.magic[spell][1]:
				text.set("You cast {}...".format(you.magic[spell][0].lower().capitalize()))
				you.mp.set(you.mp.value - you.magic[spell][1])
				if you.magic[spell][0] == "ZAP":
					boss.flicker(4, [255, 255, 0])
					fight(you, boss, False, True, randint(95, 105))
					text.set("You landed a powerful strike on the enemy!")
				elif you.magic[spell][0] == "IGNITE":
					boss.flicker(4, [255, 0, 0])
					boss.status = ["BURN", 5]
					text.set("You set the enemy ablaze!")
				elif you.magic[spell][0] == "CONGEAL":
					boss.flicker(4, [0, 255, 255])
					boss.status = ["FREEZE", 4]
					text.set("You froze the enemy solid!")
			else:
				text.set("You don't have enough mana for that spell!")
				continue	
		elif res == 2:
			if len(you.bag) > 0:
				text.set("Use an item?")
				itemsandexit = you.bag + ["(EXIT)"]
				item = opt.set(itemsandexit)
				if itemsandexit[item] == "(EXIT)":
					continue
				else:
					you.bag.pop(item)
					text.set("You used the {}...".format(itemsandexit[item].capitalize()))
					if itemsandexit[item] == "MEDICINE":
						you.hp.set(you.hp.value + 50)
						text.set("You restored 50 life points!")
					elif itemsandexit[item] == "ELIXIR":
						you.mp.set(you.mp.max)
						text.set("You restored your mana points!")
					elif itemsandexit[item] == "NECTAR":
						you.hp.set(you.hp.max)
						text.set("You restored your life to the max! Amazing!")
			else:
				text.set("You have no items...")
				continue
		elif res == 3:
			text.set("Farewell, then...")
			boss.hp.fade()
			bbox.hide()
			boss.disappear()
			end()
		# Boss's turn
		if boss.hp.value > 0:
			rng = randint(0, 99) # All-purpose random integer for dealing with probabilities		
			if boss.status:
				boss.status[1] -= 1
				if boss.status[1] > 0:
					if boss.status[0] == "FREEZE":
						text.set("{} is frozen in place!".format(boss.name))
						continue
					elif boss.status[0] == "BURN":
						text.set("{} is on fire!".format(boss.name))
						boss.hp.set(boss.hp.value - randint(25, 35))
						if boss.hp.value == 0:
							continue
				elif boss.status[0] == "CHARGE":
					text.set("{} released a hellish shockwave!".format(boss.name))
					fight(boss, you, False, True, randint(65, 75))
					boss.status = []
					continue
				else:
					text.set("{}'s status returned to normal.".format(boss.name))
					boss.status = []			
			if index == 0: # Sloth
				if rng > boss.hp.value / 3:
					fight(boss, you)
				else:
					text.set("Akua Moe is lazing around...")						
			elif index == 1: # Gluttony
				if rng < 100 - boss.hp.value / 3:
					fight(boss, you)
				else:
					text.set("Akua Pehu is chewing on its rations...")
					boss.hp.set(boss.hp.value + randint(50, 100))				
			elif index == 2: # Lust
				if "HIT" in you.lasthit:
					text.set("Akua Kuko shares their pain!")
					you.hp.set(you.hp.value - ceil(you.lasthit[0] / 10))
				fight(boss, you)					
			elif index == 3: # Wrath		
				if "HIT" in you.lasthit:
					text.set("Akua Manini's rage is building...")
					boss.stats[1][0] += ceil(you.lasthit[0] / 20)
				fight(boss, you)				
			elif index == 4: # Envy
				fight(boss, you)
				if "HIT" in boss.lasthit:
					text.set("Akua Lili feeds on your pain...")
					boss.hp.set(boss.hp.value + ceil(boss.lasthit[0] / 5))
			elif index == 5: # Greed
				fight(boss, you)
				if "HIT" in boss.lasthit and rng < 50:
					text.set("Akua Nunu snatches your spare change!")
					you.gd.set(you.gd.value - randint(1, 3))
			elif index == 6: # Pride
				fight(boss, you)
				if "CRIT" in boss.lasthit:
					text.set("Akua Kei attacks twice out of hubris!")
					fight(boss, you, False)
			elif index == 7: # Original Sin	
				if boss.hp.value <= 300 and not boss.god:
					text.set("...?!")
					ebg.show()
					text.set("Akua Hala ignited the flames of Hell!")
					text.set("Their attacks will be more potent!")
					boss.god = True
					for i in range(len(boss.stats[0])):
						boss.stats[1][i] += 10
				elif rng < 100 - boss.hp.value / 5 and boss.god:		
					boss.flicker(4, [255, 0, 255])
					text.set("Akua Hala is charging power...")
					boss.status = ["CHARGE", 1]
				else:
					fight(boss, you)		
			# Energiser's end-of-turn effects phase
			if "ENERGISER" in you.perks:
				you.mp.set(you.mp.value + 1)
	if boss.hp.value == 0: # Boss defeat scene
		boss.hp.fade()
		bbox.hide()
		boss.flash()
		sleep(1 / 2)
		text.set("You defeated {}!".format(boss.name))
		if index == 7: # Final boss
			boss.disappear()
			text.set("")
			floor.hide()
			ebg.hide()
			bg.hide()
			door.win(index)
		else: # Other bosses
			text.set("You found {}G!".format(bosses[index]["gold"]))
			you.gd.set(you.gd.value + bosses[index]["gold"])
			boss.disappear()
			text.set("")
			floor.hide()
			bg.hide()
			door.win(index)
			lobby()	
	elif you.hp.value == 0:
		text.set("You were defeated!")
		text.set("See you on the other side, then...")
		boss.hp.fade()
		bbox.hide()
		boss.disappear()
		end()
	
# Shop task
def shop():
	while True:
		text.set("What'cha want? I don't have all day.")
		saleandexit = ["{0}\n{1}:{2}G".format(sale[i][0], sale[i][1], sale[i][2]) for i in range(min(len(sale), 5))] + ["(EXIT)"]
		res = opt.set(saleandexit)
		if saleandexit[res] == "(EXIT)":
			break
		else:
			if you.gd.value >= sale[res][2]:
				you.gd.set(you.gd.value - sale[res][2])
				if sale[res][1] == "ITEM":
					if len(you.bag) == you.maxbag:
						text.set("Yer bag is too full, mate.")
						continue
					text.set("Here's yer {}. Use it wisely, ya hear?".format(sale[res][0].lower().capitalize()))
					you.bag.append(sale[res][0])
				elif sale[res][1] == "SPELL":
					text.set("Now ya can cast {}. Be careful, ya hear?".format(sale[res][0].lower().capitalize()))
					you.magic.append([sale[res][0], sale[res][3]])
					sale.pop(res)
			
				elif sale[res][1] == "PERK":
					text.set("Here's yer {}. Hope it does ya well.".format(sale[res][0].lower().capitalize()))
					you.perks.append(sale[res][0])
					if sale[res][0] == "HEARTSTONE":
						you.hp.remax(200)
					sale.pop(res)			
			else:
				text.set("Ya don't have enough money for that, mate.")
	lobby()

# Lobby task
def lobby():
	if 6 in door.won and len(door.won) != 7:
		return
	bg.show([51, 51, 51])
	if not door.drawn:
		text.set("")
		door.show()
		if len(door.won) == 7:
			text.set("...")
			text.set("A hidden door makes itself known to you.")
		elif len(door.options) == 1:
			text.set("A single door stands before you.")
		elif len(door.options) == 2:
			text.set("A pair of doors stands before you.")
		elif len(door.options) >= 3:
			text.set("Several doors stand before you.")
	if len(door.options) == 1:
		text.set("Enter when you are ready.")
	else:
		text.set("Enter the door that piques your interest.")
	res = opt.set(["DOOR #{0}\n{1}".format(i+1, bosses[i]["colname"]) for i in door.options] + ["SHOP!"])
	if res == len(door.options):
		shop()
	else:
		text.set("")
		door.hide()
		bg.hide()
		bossroom(door.options[res])

# Information task
def info():
	while True:
		text.set("What would you like to read about?")
		res = opt.set(["PREMISE", "SPELLS", "ITEMS", "PERKS", "TIPS", "(EXIT)"])
		if res == 0:
			text.set("This game is a continuation of two previous installments, retaining the turn-based system while elaborating upon it.")
			text.set("The player will battle through several rooms, each with its own boss (technically known as an \"idol\").")
			text.set("There are seven unique idols to battle this time around, themed around the seven deadly sins (cliché, I know).")
		elif res == 1:
			text.set("Spells are one the more major additions to this series. They were put in place to give the player more options in battle.")
			text.set("There are three spells the player can use in total, and are as follows:")
			text.set("ZAP: An electric spell that immediately deals around 100 points of damage.")
			text.set("IGNITE: A fire spell that gradually deals about 30 damage each turn for 4 turns.")
			text.set("CONGEAL: An ice spell that prevents the enemy from moving for 3 turns.")
			text.set("Each spell has a unique mana cost, as well.")
		elif res == 2:
			text.set("Items return from the previous installment and are expanded upon.")
			text.set("The available items are as follows:")
			text.set("MEDICINE: A basic item that restores 50 life points.")
			text.set("ELIXIR: An item that restores the player's mana, allowing more spells to be used.")
			text.set("NECTAR: A highly useful item that fully restores the player's life.")
			text.set("The player can hold up to 5 items at a time.")
		elif res == 3:
			text.set("Another minor yet significant addition to this game is the perk system.")
			text.set("Perks are a pair of (rather expensive) upgrades that can turn the tables in the player's favour.")
			text.set("There are only two perks in game, and are as follows:")
			text.set("ENERGISER: A perk that increases the player's mana points by 1 at the end of each turn.")
			text.set("HEARTSTONE: A vital upgrade that doubles the player's max life. The player's health will not be restored, however.")
			text.set("For most players, it is suggested to purchase both as soon as possible.")
		elif res == 4:
			text.set("There are some tips worth mentioning for this game.")
			text.set("For starters, the more rooms you clear, the more gold you will receive. Clearing all seven rooms will get you a special prize.")
			text.set("Gold is good to have, but if you can spend it, it's best to do so. The idol of the yellow room is a notorious pickpocket.")
			text.set("Furthermore, if you wish to battle all seven idols, enter the doors with lower numbers and you will achieve your goal.")
		else:
			break

# Intro task
def intro():
	while True:
		text.set("Welcome!")
		res = opt.set(["START", "MANUAL", "QUIT"])
		if res == 0:
			text.set("Prepare yourself...")
			break
		elif res == 1:
			info()
		elif res == 2:
			text.set("Farewell.")
			end()
			
# Epilogue task
def epilogue():
	if len(door.won) == 8:
		text.set("Wow.")
		text.set("You actually defeated the end boss.")
		text.set("Congratulations on your victory; you put up with another (hopefully less so) RNG hell.")
		text.set("I devised this challenge to be more skill based than before, so I hope your victory feels more deserved.")
		text.set("Anyways, fluff and flattery aside, thank you for playing!")
		text.set("Please, play again whenever you like.")
		text.set("")
	else:
		text.set("Congrats. You defeated the worst of the seven vices.")
		text.set("Do you think that's worthy of applause?")
		text.set("It would be, if there weren't unfinished business.")
		text.set("Here's a hint: The first six doors are shown in pairs.")
		text.set("Remember which is which, then defeat the vice from each door of a pair before advancing to the next.")
		text.set("Thereafter, you'll see the truth.")
		text.set("Best wishes to you.")
		text.set("")
	curt.close()
	exit()

# Main task
def main():
	win.setBackground(color_rgb(0, 0, 0))
	me.show()
	sleep(1)
	me.hide()
	curt.open()
	box.show()
	intro()
	pbox.show()
	you.hp.set(100)
	you.mp.set(10)
	you.gd.set(50)
	lobby()
	# Returns here when all bosses are defeated
	you.fadeall()
	pbox.hide()
	box.hide()
	etext = Message(240, 18)
	epilogue()
	
	
# GLOBALS ####################################################################################################
# Defined in the order that they are drawn (if applicable); first to last.
# Don't kill me for using global objects; I need them to be accessible from all functions and methods.
bosses = [  # Sloth: frequently skips turns
			{"name":"Akua Moe", "face": "怠", "col":[102, 204, 255], "hp":150, "atk":40, "def":60, "prs":40, "evs":40, "lck":40, "prt":40, "gold":30, "colname":"BLUE"}, 
			# Gluttony: frequently skips and heals self
			{"name":"Akua Pehu", "face": "貪", "col":[255, 153, 102], "hp":150, "atk":40, "def":40, "prs":40, "evs":40, "lck":40, "prt":60, "gold":30, "colname":"ORANGE"}, 
			# Lust: takes damage when dealing damage
			{"name":"Akua Kuko", "face": "色", "col":[204, 102, 255], "hp":200, "atk":60, "def":40, "prs":60, "evs":40, "lck":40, "prt":40, "gold":50, "colname":"VIOLET"}, 
			# Wrath: deals higher damage the more hits taken
			{"name":"Akua Manini", "face": "憤", "col":[255, 102, 155], "hp":200, "atk":40, "def":60, "prs":40, "evs":40, "lck":60, "prt":60, "gold":50, "colname":"RED"}, 
			# Envy: leeches life upon landing hits
			{"name":"Akua Lili", "face": "妬", "col":[153, 255, 102], "hp":250, "atk":40, "def":60, "prs":40, "evs":60, "lck":40, "prt":60, "gold":80, "colname":"GREEN"}, 
			# Greed: steals gold upon landing hits
			{"name":"Akua Nunu", "face": "欲", "col":[255, 204, 102], "hp":250, "atk":60, "def":40, "prs":60, "evs":40, "lck":60, "prt":40, "gold":80, "colname":"YELLOW"}, 
			# Pride: attacks twice upon landing critical hits
			{"name":"Akua Kei", "face": "慢", "col":[102, 153, 255], "hp":300, "atk":60, "def":50, "prs":60, "evs":50, "lck":60, "prt":50, "gold":120, "colname":"INDIGO"}, 
			# Original Sin: gains a charged attack half-way through the battle
			{"name":"Akua Hala", "face": "罪", "col":[204, 204, 204], "hp":500, "atk":60, "def":60, "prs":60, "evs":60, "lck":60, "prt":60, "gold":0, "colname":"GREY"}] 

sale = [	["MEDICINE", "ITEM", 20], 
			["ELIXIR", "ITEM", 30], 
			["IGNITE", "SPELL", 50, 7], 
			["CONGEAL", "SPELL", 70, 8], 
			["ENERGISER", "PERK", 100], 
			["HEARTSTONE", "PERK", 150], 
			["NECTAR", "ITEM", 80]]

win = GraphWin("RPGIII", 640, 480)
ebg = EndBG()
bg = Backdrop()
floor = Terrain()
pbox = Box([0, 280], [180, 360])
bbox = Box([520, 0], [639, 40])
box = Box([0, 360], [639, 479])
text = Message(384, 16)
opt = Option()
door = Doors()
you = Player()
curt = Curtain()
me = Watermark()

if __name__ == "__main__":
	main()