from game_engine import *
from Tkinter import *

"""###NEEDS WORK
#GUI Setup
root = Tk()

text_to_display = StringVar()
description="TEST"
text_to_display.set(description)

label = Label(root, textvariable = text_to_display, width=100, bg="black",
	fg="white", wraplength=400, anchor="n", font="helvetica")
label.pack(side=TOP)

entry = Entry(root, width=80)
entry.pack(side=LEFT)

def enter():
	description = entry.get()
	text_to_display.set(description)
	root.update_idletasks()
	
button = Button(root, text="ENTER",command=enter, width=20)
button.pack(side=RIGHT)
"""

#Game Initiation
game_status = "Play"
scene.change_to(0)
#Objects (player, arena, shop, scene) are initiated at the end of game_engine.py

#Game Loop
while (game_status=="Play"):
	#Battle Protocol
	if (scene.battle_active):
		while (len(live_enemies)>0 and player.hp>0):
			battle_turn()
			raw_input("<Press \"Enter\" to continue.>")
		scene.battle_active = False 
		if (player.hp <= 0):
			game_status="Lost"
			print "\nYou fall to the ground unconscious!"
			break
		collect_loot()
		player.refresh_stats()
	print "__"*30	
	print scene.description
	
	#Question Protocol
	if (scene.ask_question): 
		response = binary_question(scene.question)
		if response==True:
			print scene.question_response_true,"\n"
			question_consequent(scene.question_result_true)			
			scene.game_path.insert(0,"T")	
		if response==False:
			print scene.question_response_false,"\n"
			scene.game_path.insert(0,"F")
		scene.ask_question=False
	
	#Inventory Protocol
	if (scene.add_item == True):
		player.inventory_add(scene.object_to_add, scene.object_quantity)
		scene.add_item = False
		
	print "Please select an action:"
	for i in range(len(scene.options)):
		print "     ",str(i+1)+".)", scene.options[i] 
	while (True):
		print "Choice:"
		try:
			choice = int(raw_input("--"))
			if not (choice==9 or choice==0):
				assert(scene.options[choice-1])
			break
		except:
			print "That is not a valid choice."
	if (choice==0):
		player.view_inventory()
		continue
	if (choice==9):
		player.view_stats()
		continue
		
	scene.change_to(scene.options_results[choice-1])

if game_status == "Lost":
	print "__"*40 + "\nGame over!"
	
if game_status == "Win":
	print "You beat the game! Congrats!"
