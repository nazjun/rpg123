"""
	rpg.py
	by N Junco
	October 2016
	
	This program launches a simple RPG-inspired minigame.
	It demonstrates manipulation of text graphics and pseudo-random numbers.
	For the "choice" and "break" words I consulted the official documentation.
	https://docs.python.org/3.5/tutorial/controlflow.html
	https://docs.python.org/3.5/library/random.html
	
	GUIDE
		Objective:
			Defeat the enemy in turn-based combat.
		Controls:
			Mouse Click: Select option.
		Options:
			FIGHT: Directly attack the enemy. 80% chance to hit normally (55-60 damage). 10% chance to hit critically (115-120 damage). 10% chance to miss. 
			PRAY: Invoke a divine power to heal HP. 60% chance for a normal blessing(25-30 healed). 10% chance for a miraculous blessing (55-60 healed). 30% chance to have no effect.
			CRY: Start crying to derive sympathy. 60% chance for the enemy to take damage out of pity (25-30 damage). 40% to have no effect.
			RUN: Flee the fight and close the program. 100% chance of success.
		Enemy:
			The enemy's attack has an 80% chance to hit normally (10-15 damage), a 10% chance to hit critically (25-30 damage), and a 10% chance to miss.
			
	NOTE TO SELF:
		>Define global constants
		>Create objects
		>Pass parameters as lists
"""

from graphics import *
from time import sleep
from random import randint, choice

# General effect functions
def fadeaway(obj,spd):
	for i in range(51,-1,-1):
		obj.setFill(color_rgb(i*5,i*5,i*5))
		sleep(1.0/spd)
	obj.setText("")
	
# Curtain functions
def curtain_make(win):
	obj = []
	for i in range(2):
		obj.append(Rectangle(Point(i*320,0),Point(320+i*320,480)))
		obj[i].setFill(color_rgb(255,255,255))
		obj[i].draw(win)
	return obj
		
def curtain_open(obj):
	anchor = obj[0].getP2().getX()
	for i in range(160):
		obj[0].move(-2,0)
		obj[1].move(2,0)
		sleep(1.0/120)
	
def curtain_close(obj):
	anchor = obj[0].getP2().getX()
	for i in range(160):
		obj[0].move(2,0)
		obj[1].move(-2,0)
		sleep(1.0/120)

# Enemy functions
def enemy_make(win):
	obj = Text(Point(320,200),":)")
	obj.draw(win)
	obj.setFace("courier")
	obj.setFill(color_rgb(255,255,255))
	obj.setStyle("bold")
	for i in range(5,31):
		obj.setSize(i)
		sleep(1.0/30)
	return obj
	
def enemy_get(obj):
	face = obj.getText()
	return face
	
def enemy_set(obj,face):
	if enemy_get(obj) != face:
		for i in range(31,36):
			obj.setSize(i)
			sleep(1.0/30)
		obj.setText(face)
		for i in range(35,29,-1):
			obj.setSize(i)
			sleep(1.0/30)
	else:
		return
		
# Health functions	
def hp_make(win):
	obj = Text(Point(40,460),"HP:00")
	obj.draw(win)
	obj.setFace("courier")
	obj.setFill(color_rgb(255,255,255))
	obj.setStyle("normal")
	for i in range(5,13):
		obj.setSize(i)
		sleep(1.0/30)
	return obj
	
def hp_set(obj,new,spd):
	oldlist = obj.getText().split(":")
	old = int(oldlist[1])
	if new != old:
		for i in range(12,17):
			obj.setSize(i)
			sleep(1.0/30)
		if new > old:
			for i in range(old,new+1):
				if i > 99:
					obj.setText("HP:{:02d}".format(99))
					break
				obj.setText("HP:{:02d}".format(i))
				sleep(1.0/spd)
		elif new < old:
			for i in range(old,new-1,-1):
				if i < 0:
					obj.setText("HP:{:02d}".format(0))
					break
				obj.setText("HP:{:02d}".format(i))
				sleep(1.0/spd)
		for i in range(16,11,-1):
			obj.setSize(i)
			sleep(1.0/30)	
	elif new == old:
		obj.setText("HP:{:02d}".format(i))
	return new
	
def hp_get(obj):
	try:
		list = obj.getText().split(":")
		hp = int(list[1])
		return hp
	except IndexError:
		return 0
	
# Enemy-specific health functions
def ehp_make(win):
	obj = Text(Point(320,100),"BOSS:\n000")
	obj.draw(win)
	obj.setFace("courier")
	obj.setFill(color_rgb(255,255,255))
	obj.setStyle("bold")
	for i in range(5,16):
		obj.setSize(i)
		sleep(1.0/30)
	return obj
	
def ehp_set(obj,new,spd):
	oldlist = obj.getText().split(":")
	old = int(oldlist[1])
	if new != old:
		for i in range(15,21):
			obj.setSize(i)
			sleep(1.0/30)	
		if new > old:
			for i in range(old,new+1):
				obj.setText("BOSS:\n{:03d}".format(i))
				sleep(1.0/spd)
		elif new < old:
			for i in range(old,new-1,-1):
				if i < 0:
					obj.setText("BOSS:\n{:03d}".format(0))
					break
				obj.setText("BOSS:\n{:03d}".format(i))
				sleep(1.0/spd)		
		for i in range(20,14,-1):
			obj.setSize(i)
			sleep(1.0/30)	
	elif new == old:
		obj.setText("BOSS:\n{:03d}".format(i))
	return new

# Dialogue functions	
def text_make(win):
	obj = Text(Point(320,320),"")
	obj.draw(win)
	obj.setFace("courier")
	obj.setFill(color_rgb(255,255,255))
	obj.setStyle("normal")
	obj.setSize(15)
	return obj

def text_set(obj,str):
	if len(str) == 0:
		obj.setText("")
	else:
		for i in range(len(str)):
			obj.setText("<{}>".format(str[:i+1]))
			sleep(1.0/30)	
		sleep(1)
	
# Option functions
def option_make(win):
	obj = []
	for i in range(4):
		obj.append(Text(Point(128+i*128,420),""))
		obj[i].draw(win)
		obj[i].setFace("courier")
		obj[i].setStyle("bold")
	return obj
	
def option_clear(obj,index):
	for i in range(12,26):
		obj[index].setSize(i)
		sleep(1.0/30)
	for i in range(51,-1,-1):
		for j in range(4):
			obj[j].setFill(color_rgb(i*5,i*5,i*5))
		sleep(1.0/60)
	for i in range(4):
		obj[i].setText("")

def option_select(obj,win):
	pick = win.getMouse()
	if pick.getY() > 320:
		if pick.getX() < 160:
			return 0
		elif pick.getX() > 160 and pick.getX() < 320:
			return 1
		elif pick.getX() > 320 and pick.getX() < 480:
			return 2
		elif pick.getX() > 480:
			return 3
		else:
			return option_select(obj,win)
	else:
		return option_select(obj,win)
		
def option_set(obj,win,a,b,c,d):
	list = [str(a),str(b),str(c),str(d)]
	for i in range(4):
		obj[i].setSize(5)
		obj[i].setFill(color_rgb(255,255,255))
		obj[i].setText(list[i])
		for j in range(5,13):
			obj[i].setSize(j)
			sleep(1.0/30)	
	res = option_select(obj,win)
	option_clear(obj,res)
	return res
	
# Damage flash function
def flash(obj,times):
	for i in range(times):
		sleep(1.0/10)
		obj.setFill(color_rgb(0,0,0))
		sleep(1.0/10)
		obj.setFill(color_rgb(255,255,255))

# Enemy event function
def enemy_event(r,e,t,h,eh,c,curt):
	if c == 1:
		remark = ["...","...?","Eh..."]
		flash(e,2)
		ehp_set(eh,hp_get(eh)-randint(25,30),30)
		text_set(t,"Your enemy takes a hit out of sympathy.")
		enemy_set(e,":S")
		text_set(t,choice(remark))
	elif c == 0:
		chance = choice(range(10))
		text_set(t,"Your enemy attacks...")
		if chance == 0:
			"""1/10 chance"""
			remark = ["Damn it.","What the heck?","Okay then."]
			text_set(t,"...but you evade it.")
			enemy_set(e,":|")
			text_set(t,choice(remark))
		elif chance >= 1 and chance <= 8:
			"""8/10 chance"""
			hp_set(h,hp_get(h)-randint(10,15),15)
			text_set(t,"...and you get hit!")
		elif chance == 9:
			"""1/10 chance"""
			remark = ["I almost pity you.","What's the matter?","Poor you."]
			hp_set(h,hp_get(h)-randint(25,30),15)
			text_set(t,"...and you get hit... hard!")
			enemy_set(e,":P")
			text_set(t,choice(remark))
	if hp_get(eh) > 0 and hp_get(h) > 0:
		return
	else:
		end(e,t,h,eh,curt)
	
# Event function
def event(r,e,t,h,eh,curt):
	cry = 0
	if r == 0:
		chance = choice(range(10))
		text_set(t,"You try to attack...")
		if chance == 0:
			"""1/10 chance"""
			remark = ["Whoopsie.","How embarrassing.","You tried."]
			text_set(t,"...but you miss.")
			enemy_set(e,":3")
			text_set(t,choice(remark))
		elif chance >= 1 and chance <= 8:
			"""8/10 chance"""
			flash(e,3)
			ehp_set(eh,hp_get(eh)-randint(55,60),30)
			text_set(t,"...and you land a hit!")
		elif chance == 9:
			"""1/10 chance"""
			remark = ["That hurts...","Ouch?","Hey, watch it!"]
			flash(e,4)
			ehp_set(eh,hp_get(eh)-randint(115,120),30)
			text_set(t,"...and you hit... hard!")
			enemy_set(e,":C")
			text_set(t,choice(remark))
	elif r == 1:
		chance = choice(range(10))
		text_set(t,"You start to pray...")
		if chance <= 2:
			"""3/10 chance"""
			text_set(t,"...but nobody answers.")
		elif chance >= 3 and chance <= 8:
			"""6/10 chance"""
			if hp_get(h) < 99:
				hp_set(h,hp_get(h)+randint(25,30),15)
				text_set(t,"...and you receive a blessing!")
			else:
				text_set(t,"...and you are blessed, but your HP is full!")
		elif chance == 9:
			"""1/10 chance"""
			if hp_get(h) < 99:
				hp_set(h,hp_get(h)+randint(55,60),15)
				text_set(t,"...and you are blessed... miraculously!")
			else:
				text_set(t,"...and you are blessed, but your HP is full!")
	elif r == 2:
		chance = choice(range(10))
		text_set(t,"You start to cry...")
		if chance <= 3:
			"""4/10 chance"""
			text_set(t,"...but nobody cares.")
		elif chance >= 4:
			"""6/10 chance"""
			text_set(t,"...and your enemy feels sorry for you.")
			cry = 1
	elif r == 3:
		remark = ["What a shame.","How cowardly.","Alright, then."]
		text_set(t,"You run away!")
		enemy_set(e,":/")
		text_set(t,choice(remark))
		text_set(t,"Come back when you actually want to fight.")
		curtain_close(curt)
		exit()
	if hp_get(eh) > 0 and hp_get(h) > 0:
		enemy_event(r,e,t,h,eh,cry,curt)
	else:
		end(e,t,h,eh,curt)
	
# Ending function
def end(e,t,h,eh,curt):
	if hp_get(h) <= 0:
		fadeaway(h,60)
		text_set(t,"Uh-oh, it seems that you died.")
		enemy_set(e,":D")
		text_set(t,"I guess that means your enemy wins.")
		text_set(t,"May we meet again on the other side!")
		curtain_close(curt)
		
	elif hp_get(eh) <= 0:
		fadeaway(eh,60)
		enemy_set(e,":O")
		text_set(t,"...!?")
		text_set(t,"I... I died?")
		enemy_set(e,":(")
		text_set(t,"I guess... they were right.")
		text_set(t,"All happiness is temporary.")
		text_set(t,"And before I depart, I want to say something.")
		text_set(t,"Enjoy life as it's thrown at you.")
		text_set(t,"Leave your mark on this world...")
		text_set(t,"...because now's your only time to shine...")
		text_set(t,"...")
		fadeaway(e,30)
		text_set(t,"")
		sleep(1)
		text_set(t,"You defeated the enemy!")
		text_set(t,"You gained 666,666,666 EXP for winning.")
		text_set(t,"But there's no EXP implemented, so it's useless!")
		text_set(t,"Play again sometime!")
		curtain_close(curt)
	
# Main task
def main():
	win = GraphWin("RPG1",640,480)
	win.setBackground(color_rgb(0,0,0))
	curt = curtain_make(win)
	curtain_open(curt)
	text = text_make(win)
	text_set(text,"!?")
	boss = enemy_make(win)
	option = option_make(win)
	text_set(text,"An enemy appears!")
	
	text_set(text,"")
	ehp = ehp_make(win)
	ehp_set(ehp,666,600)
	hp = hp_make(win)
	hp_set(hp,99,60)
	while hp_get(ehp) > 0 and hp_get(hp) > 0:
		text_set(text,"What do you do?")
		result = option_set(option,win,"FIGHT","PRAY","CRY","RUN")
		event(result,boss,text,hp,ehp,curt)
	
if __name__ == "__main__":
	main()