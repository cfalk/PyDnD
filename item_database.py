from game_universal_functions import *
from game_engine import player #Allow the 'player' to be directly modified.

#TYPE FUNCTIONS:
#	(Responsible for stat/character changes.)

def weapon(item):	
	player.active_ammo  = "None"
	player.eq_ammo		= "None"
	if player.eq_weapon==item:
		player.hand_1 = "Free"
		if player.eq_shield=="None":
			player.hand_2 = "Free"
		player.eq_weapon="None"
		player.attack_bonus_weapon	= 0
		player.attack_damage_weapon = 0
		player.eq_ammo				= "None"
		player.attack_bonus_ammo 	= 0
		player.attack_damage_ammo 	= 0
		print "You unequipped the {}.".format(item)
	elif (player.hand_2=="Busy" and (item in weapons_2h)):
		print "ERROR: You need another hand free to equip your {}!".format(item)
	else:
		player.eq_weapon=item
		player.hand_1 = "Busy"
		if player.eq_shield=="None" and not (player.eq_weapon in weapons_2h):
			player.hand_2 = "Free"
		if item=="Rusty Iron Sword":
			player.attack_bonus_weapon  = 1
			player.attack_damage_weapon = 2
		elif item=="Iron Sword":
			player.attack_bonus_weapon  = 2
			player.attack_damage_weapon = 3
		elif item=="Iron Dagger":
			player.attack_bonus_weapon  = 3
			player.attack_damage_weapon = 2
		elif item=="Silver Dagger":
			player.attack_bonus_weapon  = 4
			player.attack_damage_weapon = 2
		elif item=="Rapier":
			player.attack_bonus_weapon  = 3
			player.attack_damage_weapon = 4
		elif item=="Hero's Sword":
			player.attack_bonus_weapon  = 10
			player.attack_damage_weapon = 15
		elif item=="Iron War Axe":
			player.attack_bonus_weapon  = 5
			player.attack_damage_weapon = 7
		elif item=="Short Spear":
			player.attack_bonus_weapon  = 3
			player.attack_damage_weapon = 2
		elif item=="Staff":
			player.attack_bonus_weapon  = 1
			player.attack_damage_weapon = 1
		elif item=="Sling":
			player.attack_bonus_weapon  = 0
			player.attack_damage_weapon = 1
			player.active_ammo 			= "Pebble"
		if player.hand_2=="Free":
			if item=="Iron Bastard Sword":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 3
				player.attack_damage_weapon = 9
			elif item=="Steel Bastard Sword":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 8
				player.attack_damage_weapon = 13
			elif item=="Steel Claymore":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 7
				player.attack_damage_weapon = 10
			elif item=="Iron Claymore":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 6
				player.attack_damage_weapon = 8
			elif item=="Iron Battle Axe":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 3
				player.attack_damage_weapon = 15
			elif item=="Mythril Halberd":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 10
				player.attack_damage_weapon = 25
			elif item=="Wooden Spear":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 1
				player.attack_damage_weapon = 2
			elif item=="Long Spear":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 2
				player.attack_damage_weapon = 3
				player.hand_2 				= "Busy"
			elif item=="Pitchfork":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 0
				player.attack_damage_weapon = 2
			elif item=="Cracked Wooden Bow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 2
				player.attack_damage_weapon = 1
				player.active_ammo 			= "Arrow"
			elif item=="Willow Short Bow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 6
				player.attack_damage_weapon = 5
				player.active_ammo 			= "Arrow"
			elif item=="Elm Horn Bow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 5
				player.attack_damage_weapon = 6
				player.active_ammo 			= "Arrow"
			elif item=="Maple Recurve Bow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 7
				player.attack_damage_weapon = 7
				player.active_ammo 			= "Arrow"
			elif item=="Yew Long Bow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 7
				player.attack_damage_weapon = 10
				player.active_ammo 			= "Arrow"
			elif item=="Blunderbuss":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 0
				player.attack_damage_weapon = 30
			elif item=="Wooden Crossbow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 7
				player.attack_damage_weapon = 10
				player.active_ammo 			= "Bolt"
			elif item=="Iron Crossbow":
				player.hand_2 				= "Busy"
				player.attack_bonus_weapon  = 10
				player.attack_damage_weapon = 15
				player.active_ammo 			= "Bolt"
		print "You equipped the " + item + "."
		
def ammo(item):	
	if player.active_ammo=="None": #No need for ammo
		print "You have no reason to equip the {}!".format(item)
		player.eq_ammo="None"
		player.attack_bonus_ammo  = 0
		player.attack_damage_ammo = 0	
			
	elif player.eq_ammo==item: #Unequip
		player.eq_ammo="None"
		player.attack_bonus_ammo	= 0
		player.attack_damage_ammo = 0
		print "You unequipped the {}.".format(item)		
	
	#Below: Equipping Ammo
	else:
		if "Bow" in player.eq_weapon:
			if item=="Stone Arrow":
				player.attack_bonus_ammo  = 0
				player.attack_damage_ammo = 0
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			elif item=="Iron Arrow":
				player.attack_bonus_ammo  = 1
				player.attack_damage_ammo = 1
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			elif item=="Steel Arrow":
				player.attack_bonus_ammo  = 2
				player.attack_damage_ammo = 1
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			else:
				print "ERROR: You cannot use the {0} with your {1}!".format(item,player.eq_weapon)
		if "Sling" in player.eq_weapon:
			if item=="Pebble":
				player.attack_bonus_ammo  = -2
				player.attack_damage_ammo = -1
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			else:
				print "ERROR: You cannot use the {0} with your {1}!".format(item,player.eq_weapon)			
		if "Crossbow" in player.eq_weapon:
			if item=="Bolt":
				player.attack_bonus_ammo  = 2
				player.attack_damage_ammo = 4
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			else:
				print "ERROR: You cannot use the {0} with your {1}!".format(item,player.eq_weapon)			
		if "Blunderbuss" in player.eq_weapon:
			if item=="Pebble":
				player.attack_bonus_ammo  = -5
				player.attack_damage_ammo = 5
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			else:
				print "ERROR: You cannot use the {0} with your {1}!".format(item,player.eq_weapon)			
			
def shield(item): #Only incorporates player.hand_2
	if player.eq_shield==item:
		player.hand_2 = "Free"
		player.eq_shield="None"
		player.AC_shield_bonus=0
		print "You unequipped the {}".format(item)
	else:
		if player.hand_2=="Free":
			player.eq_shield=item
			player.hand_2="Busy"
			if item=="Wooden Shield":
				player.AC_shield_bonus = 1
			elif item=="Large Wooden Shield":
				player.AC_shield_bonus = 2
			elif item=="Iron Shield":
				player.AC_shield_bonus = 3
			elif item=="Oversized Iron Shield":
				player.AC_shield_bonus = 5
			print "You equipped the " + item + "."
		else:
			print "ERROR: You need another hand free to equip your {}!".format(item)
	
def armor(item):
	if player.eq_armor==item:
		player.eq_armor="None"
		player.AC_armor_bonus=0
		print "You unequipped the {}".format(item)
	else:
		player.eq_shield=item
		if item=="Leather Overcoat":
			player.AC_armor_bonus = 1
		elif item=="Studded Leather Tunic":
			player.AC_armor_bonus = 2
		elif item=="Rusty Chainmail":
			player.AC_armor_bonus = 2
		elif item=="Fine Steel Chailmail":
			player.AC_armor_bonus = 4
		elif item=="Iron Platebody":
			player.AC_armor_bonus = 3
		elif item=="Steel Armor Set":
			player.AC_armor_bonus = 5
		print "You equipped the " + item + "."
	
def useable(item):
	affected = "temp"
	effect = 0
	if item=="Red Potion":
		effect = 2+d(4)
		affected="health"
		if player.hp_max == player.hp:
			print "Using a " + item + " now would have no effect."
		elif player.hp_max <= (player.hp+effect):
			print "You used the " + item + " and reached your maximum " + affected + " of " + str(player.hp_max) + "."
			player.hp = player.hp_max
			player.inventory_remove(item)
		else:
			print "You used the " + item + " and gained " + str(effect) + " " + affected + "."
			player.hp += effect
			player.inventory_remove(item)
	if item=="Large Red Potion":
		effect = 5+d(10)
		affected="health"
		if player.hp_max == player.hp:
			print "Using a " + item + " now would have no effect."
		elif player.hp_max <= (player.hp+effect):
			print "You used the " + item + " and reached your maximum " + affected + " of " + str(player.hp_max) + "."
			player.hp = player.hp_max
			player.inventory_remove(item)
		else:
			print "You used the " + item + " and gained " + str(effect) + " " + affected + "."
			player.hp += effect
			player.inventory_remove(item)
	if item=="Elixir":
		affected="health"
		if player.hp_max == player.hp:
			print "Using a " + item + " now would have no effect."
		else:
			print "You used the " + item + " and reached your maximum " + affected + " of " + str(player.hp_max) + "."
			player.hp = player.hp_max
			player.inventory_remove(item)
			
def junk(item):
	print "{} doesn't have a use.".format(item)
	
#ITEM_DATABASE:
#	Responsible for values and type identification. 
#"ITEM" :[type, value] 
item_details = {
	"Rusty Iron Sword"		:[weapon,5],
	"Iron Sword"			:[weapon,50],
	"Iron Dagger"			:[weapon,5],
	"Silver Dagger"			:[weapon,350],
	"Rapier"				:[weapon,20],
	"Iron Bastard Sword"	:[weapon,300],
	"Steel Bastard Sword"	:[weapon,550],
	"Iron Claymore"			:[weapon,200],
	"Steel Claymore"		:[weapon,400],
	"Iron War Axe"			:[weapon,55],
	"Iron Battle Axe"		:[weapon,45],
	"Mythryl Halberd"		:[weapon,4500],
	"Hero's Sword"			:[weapon,3500],
	"Wooden Spear"			:[weapon,3],
	"Long Spear"			:[weapon,9],
	"Short Spear"			:[weapon,15],
	"Staff"					:[weapon,1],
	"Pitchfork"				:[weapon,2],
	
	"Cracked Wooden Bow"	:[weapon,5],
	"Willow Short Bow"		:[weapon,390],
	"Yew Long Bow"			:[weapon,450],
	"Maple Recurve Bow"		:[weapon,400],
	"Elm Horn Bow"			:[weapon,375],
	"Sling"					:[weapon,2],
	"Blunderbuss"			:[weapon,500],
	"Wooden Crossbow"		:[weapon,100],
	"Iron Crossbow"			:[weapon,350],
	
	"Red Potion"			:[useable,15],
	"Large Red Potion"		:[useable,30],
	"Elixir"				:[useable,100],
	
	"Wooden Shield"			:[shield,75],
	"Large Wooden Shield"	:[shield,50],
	"Iron Shield"			:[shield,400],
	"Oversized Iron Shield"	:[shield,800],
	
	"Leather Overcoat"		:[armor,100],
	"Studded Leather Tunic"	:[armor,600],
	"Rusty Chainmail"		:[armor,800],
	"Fine  Steel Chainmail"	:[armor,1000],
	"Iron Platebody"		:[armor,1200],
	"Steel Armor Set"		:[armor,1500],
	
	"Stone Arrow"			:[ammo,5/4.0],		#Recommended quantity 
	"Iron Arrow"			:[ammo,7/3.0],		# per purchase included
	"Steel Arrow"			:[ammo,9/3.0],		# as a fractionized price.
	"Pebble"				:[ammo,1/5.0],		#
	"Gunpowder and Ball"	:[ammo,15/2.0],		#
	"Bolt"					:[ammo,10/3.0],		#
	
	"ROUS Fang"				:[junk,5],
	"ROUS Fur"				:[junk,10],
	"ROUS Tail"				:[junk,3],
	"NOUS Tail"				:[junk,8],
	"NOUS Scales"			:[junk,15],
	"Leather Square"		:[junk,7],
	"Goblin Eye"			:[junk,15],
	"Kobold Trinkets"		:[junk,20],
	"Kobold Vest"			:[junk,10],
	"Lycan Claw"			:[junk,350],
	"Lycan Eye"				:[junk,400],
	"Spoctiderpus Beak"		:[junk,1350],
	"Spoctiderpus Venom"	:[junk,1000],
	"Lobster Meat"			:[junk,15],
	"Rock Lobster Shell"	:[junk,25],
	"Diamond"				:[junk,500],
	"Dwarven Ale"			:[junk,6],
	"Troll Grog"			:[junk,3],
	}

#Two-hand weapons (can't double with a shield)
weapons_2h = {
	#Swords:
	"Iron Bastard Sword",
	"Steel Bastard Sword",
	"Iron Claymore",
	"Steel Claymore",
	
	#Axes:
	"Iron Battle Axe",
	"Mythryl Halberd",
	
	#Spears:
	"Wooden Spear",
	"Long Spear",
	
	#Ranged:
	"Cracked Wooden Bow",
	"Willow Short Bow"
	"Maple Long Bow",
	"Yew Recurve Bow",
	"Elm Horn Bow",
	"Blunderbuss",
	"Wooden Crossbow",
	"Iron Crossbow",
	
	#Misc.:
	"Pitchfork",
	}	
