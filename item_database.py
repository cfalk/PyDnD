#TYPE FUNCTIONS:
#	Responsible for stat changes.
def weapon(item):	
	player.active_ammo = "None"
	player.eq_ammo	= "None"
	
	if player.eq_weapon==item:
		player.hand_1 = "Free"
		if player.eq_shield=="None":
			player.hand_2 = "Free"
		player.eq_weapon="None"
		player.attack_bonus_weapon	= 0
		player.attack_damage_weapon 	= 0
		player.eq_ammo				= "None"
		player.attack_bonus_ammo 		= 0
		player.attack_damage_ammo 	= 0
		print "You unequipped the {}.".format(item)
	elif (player.hand_2=="Busy" and (item in weapons_2h)):
		print "You need another hand free to equip your {}!".format(item)
	else:
		player.eq_weapon=item
		player.hand_1 = "Busy"
		if player.eq_shield=="None" and not (player.eq_weapon in weapons_2h):
			player.hand_2 = "Free"
		if item=="Rusty Iron Sword":
			player.attack_bonus_weapon  = 1
			player.attack_damage_weapon = 4
		if item=="Iron Sword":
			player.attack_bonus_weapon  = 2
			player.attack_damage_weapon = 6
		if player.hand_2=="Free":
			if item=="Iron Bastard Sword":
				player.hand_2 = "Busy"
				player.attack_bonus_weapon  = 3
				player.attack_damage_weapon = 9
			if item=="Cracked Wooden Bow":
				player.hand_2 = "Busy"
				player.attack_bonus_weapon  = 2
				player.attack_damage_weapon = 3
				player.active_ammo = "Arrow"
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
			else:
				print "You cannot use the {0} with your {1}!".format(item,player.eq_weapon)
		if "Sling" in player.eq_weapon:
			if item=="Pebble":
				player.attack_bonus_ammo  = -2
				player.attack_damage_ammo = -1
				player.eq_ammo=item
				print "You equipped the {}.".format(item)
			else:
				print "You cannot use the {0} with your {1}!".format(item,player.eq_weapon)			
			
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
			if item=="Large Wooden Shield":
				player.AC_shield_bonus = 2
			print "You equipped the " + item + "."
		else:
			print "You need another hand free to equip your {}!".format(item)
	
def armor(item):
	if player.eq_armor==item:
		player.eq_armor="None"
		player.AC_armor_bonus=0
		print "You unequipped the {}".format(item)
	else:
		player.eq_shield=item
		if item=="Leather Overcoat":
			player.AC_armor_bonus = 1
		if item=="Studded Leather Tunic":
			player.AC_armor_bonus = 2
		if item=="Rusty Chainmail":
			player.AC_armor_bonus = 2
		if item=="Iron Platebody":
			player.AC_armor_bonus = 3
		if item=="Steel Armor Set":
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
			
#ITEM_DATABASE:
#	Responsible for values and type identification. 
#"ITEM" :[type, value] 
item_details = {
	"Rusty Iron Sword"		:[weapon,5],
	"Iron Sword"			:[weapon,101],
	"Iron Dagger"			:[weapon,5],
	"Silver Dagger"			:[weapon,350],
	"Rapier"				:[weapon,20],
	"Iron Bastard Sword"	:[weapon,300],
	"Steel Bastard Sword"	:[weapon,550],
	"Iron Claymore"			:[weapon,200],
	"Steel Claymore"		:[weapon,400],
	"Iron War Axe"			:[weapon,55],
	"Iron Battle Axe"		:[weapon,45],
	"Steel Halberd"			:[weapon,4101],
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
	"Wooden Crossbow"		:[weapon,1010],
	"Iron Crossbow"			:[weapon,350],
	
	"Red Potion"			:[useable,15],
	
	"Wooden Shield"			:[shield,75],
	"Large Wooden Shield"	:[shield,50],
	"Iron Shield"			:[shield,1010],
	"Oversized Iron Shield"	:[shield,4101],
	
	"Leather Overcoat"		:[armor,100],
	"Studded Leather Tunic"	:[armor,750],
	"Rusty Chainmail"		:[armor,1010],
	"Fine  Steel Chainmail"	:[armor,1000],
	"Iron Platebody"		:[armor,1500],
	"Steel Armor Set"		:[armor,10100],
	
	"Stone Arrow"			:[ammo,5/4.0],		#Recommended quantity 
	"Iron Arrow"			:[ammo,7/3.0],		# per purchase included
	"Steel Arrow"			:[ammo,9/3.0],		# as a fractionized price.
	"Pebble"				:[ammo,1/5.0],		#
	"Gunpowder and Ball"	:[ammo,15/2.0],		#
	"Bolt"					:[ammo,10/3.0],		#
	}

#Two-hand weapons (can't double with a shield)
weapons_2h = {
	#Swords:
	"Iron Bastard Sword",
	"Steel Bastard Sword",
	"Iron Claymore",
	"Steel Claymore",
	
	#Axes:
	"Iron War Axe",
	"Steel Halberd",
	
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
