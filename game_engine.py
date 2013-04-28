#IMPORT CLASS-INDEPENDENT DATABASES:
from game_universal_functions import *
from scene_database import *
from enemy_database import *
from game_database_cluster import *

#CORE FUNCTIONS
def experience_per_level(level):
	if level==0: return 1 #Prevents pre-mature level-up in character construction.
	else: return 10*level+5*(level-1)

def binary_question(question): #Allows simpler binary choice questions.
	print question
	while (True):
		choice = raw_input("--")
		if choice.lower() in valid_positive_responses:
			return True
		if choice.lower() in valid_negative_responses:
			return False
		print "That is not a valid response. Try again:"

def question_consequent(question_result):
	if question_result == "inventory_add":
		player.inventory_add(scene.object_to_add, scene.object_quantity)
			
#CORE VARIABLES
race_options = ["Elf", "Orc", "Human", "Dwarf", "Gnome", "Bear", "Goblin"]
class_options = ["Fighter", "Ranger", "Wizard", "Rogue", "Bard", "Barbarian"]
stat_names = ["Strength", "Dexterity","Constitution", "Wisdom", "Intelligence", "Charisma"]
	
valid_positive_responses={"yes", "yup", "y", "yeah", "sure", "alright"} #To remain constant
valid_negative_responses={"no", "nope", "n", "nah", "never"} #To remain constant

live_enemies 			= []
dead_enemies 			= []

#Game Mechanics
class Control(object):
	def __init__(self):
		self.options	 	 = []
		self.options_results = [] #IE: list of plot_points to which self.options refers.
		self.description	 = "temp"
		self.scene			 = "temp"
		self.game_path 		 = []
		self.battle_active	 = False
		self.ask_question	 = False
		self.add_item		 = False	
	def change_to(self, plot_point):		
		self.battle_description = ""
		
		try:
			#Gather the list of information related to a specific scene.
			temp = gather_scene_info(plot_point) 
			self.description	 = temp[0]
			self.options	 	 = temp[1][:] #[:] copies the list rather than references it.
			self.options_results = temp[2][:] 
			self.scene 			 = temp[3]
		except:
			print "ERROR: KEY NOT FOUND, BUT CONTINUING."###Should not be necessary.
			pass
		
		#Scene-specific happenstances:		
		if (plot_point==1):
			if "Cardinal Directions" in player.knowledge:
				self.options += ["Travel West", "Travel East"]
			else:
				self.options += ["Travel Left", "Travel Right"]
		elif (plot_point==1.1):
			spot_check = d(20)+player.ability_modifiers[3]#Wisdom
			if (spot_check>=8):
				self.description += ("You notice your bag is still attached to your belt!\n")
			if (spot_check>=12):
				self.description += "You believe you saw something move amidst the shadows of some trees.\n"
				self.options +=["Call Out"]
			self.description += ("(Spot check of: "+str(spot_check) + ")")
		elif (plot_point==1.2):
			if "Cardinal Directions" in player.knowledge:
				self.options += ["Wander West", "Wander East"]
				self.description += ("The routes to the East and West look almost identical. The forest is very quiet.")
			else:
				self.options += ["Wander Left", "Wander Right"]
				self.description += ("To your left and right lie separate clearings in the jungle.")
		elif (plot_point==1.3):
			listen_check = d(20) + player.ability_modifiers[3]#Wisdom
			if "Cardinal Directions" in player.knowledge:
				self.options += ["Wander East", "Wander West"]
				self.description += ("There are lovely flowers growing here. They smell like fall.")
			elif (listen_check >=15) and (7 in self.game_path)==False:
				self.options += ["Wander Right", "Wander Left"]
				self.description += "\nYou believe you heard a goblinoid squeal a distance to your right."
			else:
				self.options += ["Wander"]
			self.description += ("\n(Listen check of: "+str(listen_check) + ")")
		elif (plot_point==1.4):
			#Question--Man with Red Potions
			self.question="Accept his potions?"
			self.question_response_true="You pocket the potions and the old man walks back into the forest."
			self.question_response_false="The man walks back into the forest as quietly as he came."
			self.question_result_true="inventory_add"
			self.object_to_add = "Red Potion"
			self.object_quantity = d(3)+1

			if (plot_point in self.game_path):
				if (self.game_path[self.game_path.index(plot_point)-1]=="F"):
					self.description = ("You call out again and the man humbly walks towards you.")
					self.ask_question=True
				else:
					self.description = ("There is no response...")
			else:
				self.description = ("An old man approaches you out of the forest and hands you some red potions."+
				"\n\"Take these for the road, friend.\"")
				self.ask_question=True				
		elif (plot_point==2):
			if "Cardinal Directions" in player.knowledge:
				self.options += ["Travel West", "Travel East"]
			else:
				self.options += ["Wander Left", "Wander Right"]
			if plot_point in self.game_path:
				#Generate random battle
				generate_random_encounter(10, 1, "Field")
				self.description = "You return to where you were ambushed by ROUSs. The trees creek in the dim light of the forest."
			else:
				#Generate scripted battle.
				for i in range(d(3)):
					Monster("ROUS", 1)
				self.battle_description = generate_fight_sequence("pre_battle")
				self.battle_active=True	
		elif (plot_point==2.1):
			if "Cardinal Directions" in player.knowledge:
				self.options += ["Travel West", "Travel East"]
			else:
				self.options += ["Wander Left", "Wander Right"]
		elif (plot_point==3):
			#Question -- Rusty sword on ground
			self.question="Pick up the sword?"
			self.question_response_true="You pick up the sword."
			self.question_response_false="You leave the sword on the ground."
			self.question_result_true="inventory_add"
			self.object_to_add = "Rusty Iron Sword"
			self.object_quantity = 1					
			
			if (plot_point in self.game_path):
				if (self.game_path[self.game_path.index(plot_point)-1]=="F"):
					self.description += ("The rusty sword is still lying on the ground.")
					self.ask_question=True
			else:
				self.description += ("You see a familiar-looking, rusty sword on the ground.")
				self.ask_question=True
		elif (plot_point==4):
			generate_random_encounter(10, 3, "Field")
			wisdom_check = d(20)+player.ability_modifiers[3]#Wisdom
			if "Cardinal Directions" in player.knowledge:
				self.options = ["Travel West", "Travel North", "Travel South"]
			elif wisdom_check >=14:
				self.options = ["Travel West", "Travel North", "Travel South"]
				self.description += " You think you assert the cardinal directions."
				player.knowledge = player.knowledge.union({"Cardinal Directions"})
			else:
				self.options = ["Travel Path 1", "Travel Path 2", "Travel Path 3"]
			self.description += ("\n(Wisdom check of: "+str(wisdom_check) + ")")	
		elif (plot_point==7):
			if plot_point in self.game_path:
				#Generate random battle
				generate_random_encounter(25, 5, "Field")
			else:
				#Generate scripted battle.
				for i in range(d(3)+1):
					Monster("Marauder", 2)
				self.battle_description = generate_fight_sequence("pre_battle")
				self.battle_active=True	
		elif (plot_point==7.1):
			spot_check = d(20)+player.ability_modifiers[3]#Wisdom
			item_found = random.choice(item_details.keys()) #Randomly chooses an item.
			if (spot_check>=15):
				#Find a Weapon.
				self.description += "You find a {} in one of the broken-down doors!".format(item_found)
				player.inventory_add(item_found)
			elif (15>spot_check>=10):
				#Surprise Battle.
				for i in range(d(2)+1):
					Monster("Marauder", 2)
				self.battle_description = generate_fight_sequence("pre_battle")
				self.battle_active=True					
				self.description += ("The Marauders appeared to be hiding in one of the huts. \"Threat\" terminated.")
			else:
				self.description += ("You find nothing in the camp. It seems it has already been plundered...")
			self.description += ("(Spot check of: "+str(spot_check) + ")")
		elif (plot_point==8):
			player.knowledge = player.knowledge.union({"Cardinal Directions"})
		elif (plot_point==11.1):
			spot_check = d(20)+player.ability_modifiers[3]#Wisdom
			if (spot_check>=8):
				self.description += ("You notice your bag is still attached to your belt!\n")
			if (spot_check>=12):
				self.description += "You believe you saw something move amidst the shadows of some trees.\n"
				self.options +=["Call Out"]
			self.description += ("(Spot check of: "+str(spot_check) + ")")
		elif (plot_point==16.1):
			spot_check = d(20)+player.ability_modifiers[3]#Wisdom
			if (spot_check>=14):
				self.description = ("You find a hole that you could squeeze into...")
				self.options += ["Seriously? Nope. Turn Around.", "Squeeze in..."]
			else:
				self.description = "Too bad. Just a boring, old rock that probably isn't hiding anything."
				self.options += ["Turn Around."]
			self.description += ("(Spot check of: "+str(spot_check) + ")")
		elif (plot_point==17.1):
			spot_check = d(20)+player.ability_modifiers[3]#Wisdom
			item_found = random.choice(item_details.keys()) #Randomly chooses an item.
			if (spot_check>=15):
				#Find a Weapon.
				self.description = "You pick up a {} that was lying on the ground!".format(item_found)
				player.inventory_add(item_found)
			elif (15>spot_check>=10):
				#Surprise Battle.
				for i in range(d(2)+2):
					Monster("Thug", 4)
				self.battle_description = generate_fight_sequence("pre_battle")
				self.battle_active=True					
				self.description = ("The thugs that ambushed you are no longer able to ambush you.")
			else:
				self.description += ("The smoldering fire is old -- but not... TOO... old.")
			self.description += ("(Spot check of: "+str(spot_check) + ")")
		elif (plot_point==206):
			if plot_point in self.game_path:
				#Generate random battle
				generate_random_encounter(10, 1, "Field")
				self.description += "\nYou return to where you heroically faced the Spoctiderpus. \nThe chest is still in the corner."
			else:
				Monster("Spoctiderpus", 15)
				self.battle_description = generate_fight_sequence("pre_battle")
				self.battle_active=True	
				self.description += "\nSomehow you managed to defeat the legendary Spoctiderpus! You see a treasure chest in the corner."
		elif (plot_point==206.1):
			#Question -- Rusty sword on ground
			self.question="Open the Chest?"
			self.question_response_true="You find a heroic-looking sword! You add it to your inventory."
			self.question_response_false="On second thought... You leave the chest alone."
			self.question_result_true="inventory_add"
			self.object_to_add = "Hero's Sword"
			self.object_quantity = 1					
			
			if (plot_point in self.game_path):
				if (self.game_path[self.game_path.index(plot_point)-1]=="F"):
					self.description += ("\nThe chest is innocently sitting in the corner.")
					self.ask_question=True
			else:
				self.description += ("\nYou approach the gold-trimmed chest.")
				self.ask_question=True
			
		else: #GENERAL CASES:
			if plot_point in {9, 12, 15}: generate_random_encounter(10, player.level, "Field")
			elif plot_point in {202,203,204,205}: generate_random_encounter(30, 1, "Water_Dungeon") #Water Dungeon
		
		"""GENERAL TOWN OPTIONS"""
		#Shopping Containers
		if (plot_point==102): #"54,48"
			shop.change_to("Townington Emporium")
			shop.activate()
		elif (plot_point==112): #"55,50"
			shop.change_to("Mole Forge")
			shop.activate()
		#Arena Containers
		if (plot_point==103): #"54,48"
			arena.change_to("Townington Fight Club")
			arena.activate()
		elif (plot_point==113): #"55,50"
			arena.change_to("Mole Arena of Death")
			arena.activate()
				
		#Update game log while keeping most recent events closer to the head of the list.
		self.game_path.insert(0,plot_point)

class Shop(object):
	def __init__(self):
		self.inventory 		= [] #Note: contains only names of items.
		self.buy_quantities = [] #How many of each item bought per purchase.
		self.prices 		= [] #Contains prices of items in shop's inventory.
		self.charisma_score = 0
		self.name 			= "temp"
		
	def change_to(self,shop_id):
		if shop_id == "Townington Emporium":
			self.inventory		=["Rusty Iron Sword", "Iron Sword", "Cracked Wooden Bow", "Stone Arrow", "Red Potion"]
			self.buy_quantities	=[1,1,1,2,1]
			self.prices			=["D","D","D","D",5]
			self.charisma_score	=15
			self.name 			= shop_id
		elif shop_id == "Mole Forge":
			#Sell all items at default price
			self.inventory		=item_details.keys()
			self.buy_quantities	=[1 for i in range(len(self.inventory))] #All items default pricing
			self.prices			=["D" for i in range(len(self.inventory))] #All items default pricing
			self.charisma_score	=20
			self.name 			= shop_id
		else:
			raise Exception("Invalid shop_id")
			
	def activate(self):		
		#Below: Import "default" price listings where requested (by presence of "D" in self.prices).
		for i in range(len(self.prices)):
			if self.prices[i] == "D":
				self.prices[i] = item_details[self.inventory[i]][1] #Look up the price of each item.
			
		effective_sell_percentage = (80+player.stats[5]-self.charisma_score)/100.0
		effective_buy_percentage  = (135-player.stats[5]+self.charisma_score)/100.0
		
		active=True
		print "__"*10
		print "Welcome to {}! Enter \"0\" to exit at any time.".format(self.name)
		while active:
			choice = raw_input("Would you like to \"buy\" or \"sell\"?\n--")
			if choice == "0":
				break
			elif choice.lower() == "buy" or choice.lower() == "b":
				while (True):
					print "\nShop's Wares:  (Your Gold: " + str(player.gold) + ")"
					for i in range(len(self.inventory)): #List the shop wares.
						if self.buy_quantities[i]>1:
							print ("     "+str(i+1) + ".) " + self.inventory[i] + " x " + str(self.buy_quantities[i]) + " -- Price: " +
							 str(int(round(self.prices[i]*effective_buy_percentage))) + " Gold")
						else:
							print ("     "+str(i+1) + ".) " + self.inventory[i] + " -- Price: " +
							 str(int(round(self.prices[i]*effective_buy_percentage))) + " Gold")		
					while (True):				
						try:
							choice = int(raw_input("--"))-1
							assert(len(self.inventory) > choice >= -1)
							break		
						except:
							print "That is not a valid response."
					if choice == -1: #IE: Choice "0" (aka "exit the shop")
						break
					else:
						item_to_buy = self.inventory[choice]
						item_price  = self.prices[choice]
						while (True):
							try:
								quantity_to_buy	= int(raw_input("How many would you like to buy?\n--"))
								assert(quantity_to_buy>=0)
								purchase_total = int(round((item_price*effective_buy_percentage)))*quantity_to_buy
								quantity_to_buy = quantity_to_buy*self.buy_quantities[choice] #For items that come in pairs, triplets, etc.
								break
							except:
								print "That is not a valid response."
						if quantity_to_buy == 0:
							print "You do not complete the purchase."
						elif (purchase_total<=player.gold):
							if quantity_to_buy>1:
								q = "Are you sure you want to buy {0} {1}s for {2} gold?".format(quantity_to_buy, item_to_buy, purchase_total)
							else:
								q = "Are you sure you want to buy the {0} for {1} gold?".format(item_to_buy, purchase_total)
							if binary_question(q):
								player.inventory_add(item_to_buy,quantity_to_buy)
								player.gold -= purchase_total
								print "You complete the purchase."
							else:
								print "You do not complete the purchase."
						else:
							print "You cannot afford that purchase!"
						raw_input("<Press \"Enter\" to continue.>")
						print "__"*5 
			elif choice.lower() == "sell" or choice.lower() == "s":
				while (True):
					if len(player.inventory)>0:
						print "__"*5+"\nYour Wares:  (Your Gold: " + str(player.gold) + ")"
						for i in range(len(player.inventory)):
							item = player.inventory[i][0]
							if player.inventory[i][1]==1:
								print "     "+str(i+1) + ".) " + item + " -- Offer: " + str(int(round(player.inventory[i][3]*effective_sell_percentage)))
							else:
								print "     "+(str(i+1) + ".) " + item + " -- Offer: " + str(int(round(player.inventory[i][3]*effective_sell_percentage))) +
									" (" + str(player.inventory[i][1]) + " in inventory)")
						while (True):
							try:
								choice = int(raw_input("--"))-1
								assert(len(player.inventory) > choice >= -1)
								break
							except:
								print "That is not a valid response."
						if choice == -1: break
						else:
							item_to_sell 	= player.inventory[choice][0]
							sell_price		= int(round(player.inventory[i][3]*effective_sell_percentage))
							quantity_sold = 0
							while (True):
								try:
									quantity_to_sell = int(raw_input("How many would you like to sell?\n--"))
									if quantity_to_sell == 0:
										print "You do not sell your {}.".format(item_to_sell)
									assert(player.inventory[choice][1]>=quantity_to_sell>=0)
									break
								except:
									print ("That is not a valid amount. Please use an amount between 1 and " + 
										str(player.inventory[choice][1]) + ".")
										
							if quantity_to_sell == 0: break
							elif quantity_to_sell >1:
								q = "Are you sure you want to sell your {0} {1}s?".format(quantity_to_sell, item_to_sell)
							else:	
								q = "Are you sure you want to sell your {}?".format(item_to_sell)
								
							if binary_question(q):
								total_sell_price = 0
								while (quantity_to_sell > 0):
									if (item_to_sell in player.eq_items) and (player.inventory[choice][1]==1):
										print "Please unequip your {} before selling it.".format(item_to_sell)
										break
									else:
										total_sell_price += sell_price
										player.inventory_remove(item_to_sell)
										quantity_sold +=1
										quantity_to_sell -= 1
								player.gold += total_sell_price
								if quantity_sold > 1:
									print "The shopkeeper hands you {0} gold for {1} {2}s.".format(str(total_sell_price), str(quantity_sold), item_to_sell)
								elif quantity_sold != 0:
									print "The shopkeeper hands you {0} gold for the {1}.".format(str(total_sell_price), item_to_sell)						
							else:
								print "You do not sell your {}.".format(item_to_sell)
							raw_input("<Press \"Enter\" to continue.>")
					else:
						print "\nYou have nothing to sell!"
						raw_input("<Press \"Enter\" to continue.>")
						print "__"*5 
						break								
			else:
				print "That is not a valid response."
				
class Arena(object):
	def __init__(self):
		self.bet_range  		= [0,0] #[Minimum Bet, Maximum Bet]
		self.chal_rating_max  = 0
		self.enemy_quantity_lim = 0
		self.name				= "temp"
		
	def change_to(self,arena_id):
		if arena_id == "Townington Fight Club":
			self.bet_range  		= [1,15] 
			self.chal_rating_max	= 5
			self.enemy_quantity_lim = 3
			self.name				= arena_id
		elif arena_id == "Mole Arena of Pain":
			self.bet_range  		= [20,100] 
			self.chal_rating_max	= 10
			self.enemy_quantity_lim = 15
			self.name				= arena_id
		else:
			raise Exception("Invalid arena_id")
			
	def activate(self):		
		arena_active=True
		
		global dead_enemies
		global live_enemies
		
		print "__"*10
		print "You enter the {}!".format(self.name)
		while arena_active:
			while True:
				try:
					choice = raw_input("Would you like to \"practice\" or \"wager\"? (Enter \"0\" to exit.)\n--").lower()
					assert choice in {"practice", "p", "wager", "w", "0"}
					if choice[0]=="p": arena_mode="p"
					if choice[0]=="w": arena_mode="w"
					break
				except:
					print "That is an invalid option. Please type \"p\",\"w\", or \"0\"."
			if choice == "0":
				break
			print "How many opponents would you like to battle?"
			while (True):
				try:
					#Enemy Count:
					choice_quantity = int(raw_input("--"))
					assert(choice_quantity>0) #Can't battle 0 enemies.
					if choice_quantity > self.enemy_quantity_lim:
						print "Our next monster shipment doesn't arrive until Morndas, leave some for other adventurers!..."
					else:	
						break
				except:
					print "That is an invalid input. Please choose an integer between 1 and {}.".format(self.enemy_quantity_lim)
			print "And how tough do you want'em?"
			while (True):
				try:
					#Enemy Difficulty:
					choice_chal_rating = int(raw_input("--"))
					if choice_chal_rating <= 0:
						print "... Sure, would you like to battle this pillow or that tree? Choose a higher number, buddy."
					elif self.chal_rating_max>=choice_chal_rating>0:
						break
					else:
						print "Yikes! We don't carry monsters that powerful! Perhaps less dangerous?..."
				except:
					print "Please choose a challenge rating between 1 and {}.".format(self.chal_rating_max)
			if arena_mode=="w": #Wager
				print "Heh... And what's y'er wager?"
				while (True):
					try:
						#Bet:
						choice_wager = int(raw_input("--"))

						if choice_wager==0:
							print "You decide not to bet your hard-earned gold."
							arena_mode = "p"
							break
						assert (self.bet_range[1]>=choice_wager>=self.bet_range[0])
						if choice_wager>player.gold:
							print "You don't have that much gold to bet!  (Gold: {})".format(str(player.gold))
						else:
							break
					except:
						if player.gold==0:
							print "You have no gold to bet!"
							arena_mode="p"
							break
						else:
							print "Please choose a bet between {} and {}.".format(self.bet_range[0],self.bet_range[1])
			
			#Generate random enemies. 
			generate_random_encounter(100,choice_chal_rating,"Arena")
			
			#Battle Protocol (mainly copied from game loop)
			if (scene.battle_active):
				while (len(live_enemies)>0 and player.hp>0):
					battle_turn()
					raw_input("<Press \"Enter\" to continue.>")
				scene.battle_active = False 
				if (player.hp <= 0):
					print "\nYou fall to the ground unconscious!"
					print "You wake up battered and defeated in a rickety bed."
					player.hp = 1 #IE: player can't die in arena.
					if arena_mode=="w": 
						print "Your coinpurse feels lighter."
						player.gold -= choice_wager
				else:
					collect_loot()
					player.refresh_stats()
					print "\nYou take your spoils and walk out of the pit."
					if arena_mode=="w":
						print "You earn {} gold from your battle!".format(choice_wager)
						player.gold += choice_wager
						

				#Reset enemies for next battle:
				scene.battle_active=False
				live_enemies = []
				dead_enemies = []
			arena_active=False
				
#Character and Monster Generators:
class Character(object):
	def __init__(self):
		#Create Character
		while (True):
			print "What is your character's name?"
			self.name = raw_input("--")
			
			print "Please choose a race to play by selecting a number:"
			for i in range(len(race_options)):
				print "     ",str(i+1)+".)", race_options[i] 
			while (True):
				try:
					temp = int(raw_input("--"))
					assert(temp>0)
					self.race = race_options[temp-1]
					break
				except:
					print "That is not a valid race option. Please select a number from 1 to " +str(len(race_options))+ ".\n"
					
			print "Please choose a class to play by selecting a number:"
			for i in range (len(class_options)):
				print "     ",str(i+1)+".)", class_options[i] 
			while (True):
				try:
					temp = int(raw_input("--"))
					assert(temp>0)
					self.cclass = class_options[temp-1]
					break
				except:
					print "That is not a valid class option. Please select a number from 1 to " +str(len(class_options))+ ".\n"
			print "__"*20			
			self.erase() #Sets up/Resets character's stats. 
			print "Your randomly generated stats are as follows:"
			chosen_race_skill_mods = race_modifications(self.race)
			for i in range(len(stat_names)):
				temp = [d(6),d(6),d(6),d(6)]
				#Below: Roll 4 d6 and remove lowest. Then add racial modifier.
				self.stats[i] = sum(temp) - min(temp) + chosen_race_skill_mods[i]
				self.ability_modifiers[i] = (self.stats[i]-10)/2
				print stat_names[i] + ": " + str(self.stats[i])
				print "     Ability Modifier: " + str(self.ability_modifiers[i])
			self.level_up() #Forces level-up from 0 to 1.
			print "__"*10
			
			while (True):
				temp = raw_input("Is the character, " + self.name + " the " + self.race + " " + self.cclass + ", to your liking?\n--").lower()
				if (temp in valid_positive_responses):
					player_choice="yes"
					break
				elif (temp in valid_negative_responses):
					player_choice="no"
					break
				else:
					print "Please input either \"yes\" or \"no\".\n"
			if player_choice=="yes":
				break
			else:
				print "__"*30	
		#Inventory
		self.gold = 0
		self.inventory = [] #Contains list, [item,quant,value], for each item.
	def erase(self, full_erase="F"):
		self.stats 				= [0,0,0,0,0,0]
		self.ability_modifiers 	= [0,0,0,0,0,0]
		self.hp			= 0
		self.hp_max		= 0
		
		self.attack_bonus_ammo 	  = 0
		self.attack_damage_ammo   = 0
		self.attack_bonus_weapon  = 0
		self.attack_damage_weapon = 0
		
		self.AC_armor_bonus 	= 0
		self.AC_shield_bonus 	= 0
		
		self.hit_die 			= 0
		self.level				= 0
		self.experience			= 0
		self.knowledge			= set()
		
		if full_erase=="T":
			self.name = "TEMP"
			self.cclass = "TEMP"

		#Reset all equipped items:
		self.inventory  = []
		self.eq_armor   ="None"
		self.eq_shield  ="None"
		self.eq_weapon  ="None"
		self.eq_ammo    ="None"
		self.active_ammo	="None"
		self.hand_1			="Free"
		self.hand_2			="Free"
		self.refresh_stats()	
	def level_up(self):
		if self.level==0:
			self.hit_die 	= class_modifications(self.cclass)
			self.hp_max = self.hit_die+self.ability_modifiers[2]
			self.hp 	= self.hp_max
			self.level 		= 1
		else:
			temp			 = [d(self.hit_die), d(self.hit_die)]
			self.hp		+= max(temp)+self.ability_modifiers[2]
			self.hp_max	+= max(temp)+self.ability_modifiers[2]
			self.level		+= 1
			print "You are now level " + str(self.level) + "!"
		#Below: Ability increase every four levels.
		if (self.level%4==0):
			print ""
			for i in range(len(self.ability_modifiers)):
				print str(i+1) + ".) " + stat_names[i] + ": " + str(self.stats[i])
			print "\nPlease select an ability to increase by one."
			while (True):
				try:
					temp = int(raw_input("--"))
					assert(temp>0)
					self.stats[temp-1] = self.stats[temp-1]+1
					self.ability_modifiers[temp-1] = (self.stats[temp-1]-10)/2
					break
				except:
					print "That is not a valid option. Please select a number from 1 to " +str(len(self.stats))+ ".\n"
		print "Character Level: " + str(self.level)
		print "Hitpoints: " + str(self.hp) + "/" + str(self.hp_max)
	def view_inventory(self):
		self.eq_items = [self.eq_armor, self.eq_shield, self.eq_weapon, self.eq_ammo]
		
		print "__"*10
		if (len(self.inventory) == 0):
			print "Your inventory is empty!"
		else:
			print "Your inventory contains:"
			for i in range(len(self.inventory)):
				if self.inventory[i][0] in self.eq_items:
					item_status = "(Equipped)"
				else:
					item_status = ""
				print "     ",str(i+1)+".)",self.inventory[i][0], "x", str(self.inventory[i][1]), item_status
		print "Coin Purse: " + str(self.gold) + " gold"
		print "\nTo use/equip an item, type its number. To leave your inventory, type \"0\"." 
		while (True):
			try:
				temp = int(raw_input("--"))
				assert(temp>=0)
				if temp == 0:
					break
				else:
					player_choice = temp-1
					self.inventory_use(self.inventory[player_choice][0])
			except:
				print "That is not a valid input."
		print "__"*10
	def inventory_use(self,item):
		try:
			in_inventory = False
			for i in self.inventory:
				if item==i[0]: in_inventory=True
			assert(in_inventory==True) #IE: If item is in inventory:
			item_details[item][0](item)
			self.refresh_stats()
		except:
			print "You can't use what you don't have!"	
	def inventory_add(self,item, item_quantity=1):
		location_in_inv = -1 #IE: Must change to a possible index to be "found".
		for i in range(len(self.inventory)):
			if item==self.inventory[i][0]: location_in_inv=i
			
		if location_in_inv!=-1:
			self.inventory[location_in_inv][1] += item_quantity
		else:
			#Adds item, quantity, type, and value information to inventory.
			self.inventory +=[[item,item_quantity] + item_details[item]]			
	def inventory_remove(self,item,force_remove=False):		
		location_in_inv = -1 #IE: Must change in order to be "found"
		for i in range(len(self.inventory)):
			if item==self.inventory[i][0]: location_in_inv=i
			
		if (location_in_inv != -1):
			if (self.inventory[location_in_inv][1]>1):
				self.inventory[location_in_inv][1] -= 1
			elif (item in player.eq_items):
				print "This item is equipped and cannot be removed."
			elif (force_remove) and (item in player.eq_items):#Forced remove.
				self.inventory_use(item) #Unequip item
				self.refresh_stats()
				del self.inventory[location_in_inv]
			else:
				del self.inventory[location_in_inv]
		else:
			print "You can't remove what you don't have!"
	def refresh_stats(self):
		#Refresh Level
		while self.experience >= experience_per_level(self.level):
			self.level_up()
		#Refresh Equipment
		self.AC = 10 + self.AC_armor_bonus + self.AC_shield_bonus + self.ability_modifiers[1]
		self.attack_bonus  = 0 + self.attack_bonus_weapon + self.attack_bonus_ammo
		self.attack_damage = 3 + self.attack_damage_weapon + self.attack_damage_ammo
		self.eq_items = [self.eq_weapon, self.eq_armor, self.eq_shield, self.eq_ammo]
	def view_stats(self):		
		self.refresh_stats
		self.experience_to_level = experience_per_level(self.level)
		
		print "__"*10
		print "CHARACTER STATUS:"
		print "Name: " + self.name
		print "Race: " + self.race
		print "Class: " + self.cclass + "  (Hit Die: " + str(self.hit_die) +")"
		experience_needed = (self.experience_to_level-self.experience)
		print "Level: " + str(self.level) + "  ("+ str(experience_needed) + " Experience until level-up)"
		
		print "\nAbility Stats:"
		for i in range(len(stat_names)):
			print str("     "+stat_names[i])  + ": " + str(self.stats[i]) + " (MOD: " + str(self.ability_modifiers[i]) +")"
			
		print "\nCombat Stats:"
		print "     Health: " + str(self.hp) + "/" + str(self.hp_max)
		print "     Attack Bonus: " + str(self.attack_bonus)
		print "     Attack Damage: " + "1d"+str(self.attack_damage)
		print "     Armor Class: " + str(self.AC)
		
		print "\nTo exit stat-view, type \"0\"." 
		while (True):
			try:
				assert(int(raw_input("--"))==0)
				break
			except:
				print "That is not a valid input."
		print "__"*10
			
class Monster(object):
	def __init__(self, nm, lvl):
		self.name  = nm
		self.level = lvl
		
		#[enemy, hp, damage, AC, level]
		temp				= gen_enemy_stats(self.name, self.level)
		self.hp_max  		= temp[1]
		self.hp 			= self.hp_max
		self.damage			= temp[2]
		self.AC				= temp[3]
		
		self.loot			= gen_enemy_loot(self.name)
		global live_enemies #Adds enemy to list of living enemies
		live_enemies		+= [self] 		
	def been_attacked(self,damage,attack_roll):
		global dead_enemies
		global live_enemies
		
		if attack_roll>=self.AC:
			self.hp -= damage
			print "\nYou do " + str(damage) + " damage to the " + self.name + "."
		else:
			print "\n"+generate_fight_sequence(scene.fight_style).format(self.name)
		
		if self.hp <= 0:
			dead_enemies.append(self)
			print generate_fight_sequence("enemy_dead").format(self.name)
			live_enemies.remove(self)

#Gameplay Functions:
def pop_experience(enemy):
	effective_intelligence_bonus = enemy.hp_max+player.ability_modifiers[4]
	experience_earned = (enemy.level * effective_intelligence_bonus)/player.level
	if experience_earned < 1: experience_earned = 1
	return experience_earned
	
def collect_loot():
	global dead_enemies
	
	total_loot = []
	experience_earned = 0
	
	#Create Loot and Experience
	for i in range(len(dead_enemies)):
		total_loot		+= [dead_enemies[i].loot]
		experience_earned	+= pop_experience(dead_enemies[i])
	dead_enemies = [] #IE: delete all enemies. 
	
	#Translate Loot
	if len(total_loot)>0:
		looted_gold = 0
		#Empty loot translation (Remove "" from total_loot)
		i=0
		while i<len(total_loot):
			if total_loot[i]=="":
				del total_loot[i]
			else:
				i+=1
		#Gold loot translation (! --> Gold:)
		i=0
		while (i<len(total_loot)):
			if total_loot[i][0]=="!":
				looted_gold += d(int(total_loot[i][1:]))
				del total_loot[i]
			else:
				i+=1
		#Ammo translation ("A x B" --> A of B)
		i=0
		while (i<len(total_loot)):
			try:
				temp = total_loot[i]
				ammo_to_collect 		= temp[temp.index(" x ")+3:] #("5 x Arrow" --> "Arrow")
				quantity_ammo_gathered 	= int(temp[:temp.index(" x ")]) #("5 x Arrow" --> 5)
				j=i+1
				while (j<len(total_loot)): #Check for repeats of the same loot.
					try:
						temp = total_loot[j]
						assert(temp[temp.index(" x ")+3:]==ammo_to_collect)
						quantity_ammo_gathered += int(temp[:temp.index(" x ")])
						del total_loot[j]
					except:
						j+=1
				total_loot[i] = str(quantity_ammo_gathered) + " x " + ammo_to_collect 
				i+=1
			except:
				i+=1
		#Item translation and collection process
		if len(total_loot)>0:
			print "__"*3 + "\nSelect any loot you wish to collect (\"N\": abandon rest; \"A\": collect all)."
			while (True):
				if len(total_loot)==0:
					print "All loot collected!"
					break
				#Print the available loot each iteration.
				print "The following loot remains: "
				for i in range(len(total_loot)):
					print "     " + str(i+1) + ".) " + total_loot[i]
				
				#Collect/test input
				choice = raw_input("--").lower()
				if choice in {str(i+1) for i in range(len(total_loot))}:
					choice = int(choice)
				elif not choice in {"a","n"}:
					if len(total_loot)==1:
						print "That is not a valid value. The only option is \"1\"."
					else:
						print "That is not a valid value. Please choose a number between 1 and {}.".format(len(total_loot))				
					continue
						
				#Collect loot
				if choice=="n":
					print "You leave the remaining loot."
					break
				elif choice=="a":
					while len(total_loot)>0:
						temp = total_loot.pop() #Repeatedly collect the last item.
						try:
							item_to_add = temp[temp.index(" x ")+3:]
							quantity_to_add = int(temp[:temp.index(" x ")])
							player.inventory_add(item_to_add, quantity_to_add)
						except:
							item_to_add=temp
							player.inventory_add(item_to_add, 1)
				else:
					temp = total_loot.pop(choice-1)
					try:
						item_to_add = temp[temp.index(" x ")+3:]
						quantity_to_add = int(temp[:temp.index(" x ")])
						player.inventory_add(item_to_add, quantity_to_add)
						print "You add the " + str(quantity_to_add) + " " + item_to_add + "s to your inventory."
					except:
						item_to_add=temp
						player.inventory_add(item_to_add, 1)
						print "You add the " + item_to_add + " to your inventory."

		print ""#Empty Line
		if (looted_gold>0):
			print "You add " + str(looted_gold) + " gold to your inventory!"
			player.gold += looted_gold
		if (experience_earned>0):
			print "You earned " + str(experience_earned) + " experience!"
			player.experience += experience_earned
		temp = raw_input("<Press \"Enter\" to continue.>")
				
			
	else:
		print "You search your enemies but find nothing of value."

def battle_turn():
	global live_enemies
	
	#Player turn	
	print "__"*8
	print scene.battle_description
	for i in range(len(live_enemies)):
		print str(i+1) + ".) " + live_enemies[i].name + " (Health: "+str(live_enemies[i].hp)+")"
	print "\nHealth: " + str(player.hp) + "/" + str(player.hp_max) + "\n\"Attack\" or \"inventory\"?"
	while (True):
		unparsed_choice = raw_input("--")
		unparsed_choice = unparsed_choice.split()
		try:
			choice = str(unparsed_choice[0]).lower()
			assert choice in {"attack", "a", "inventory", "i", "0"}
		except:
			print "Invalid input: please choose \"attack\" or \"inventory\"."
			continue
		
		if choice == "inventory" or choice == "i" or choice == "0":
			player.view_inventory()
			#Reprint enemy list.
			print "You return to battle..."
			for i in range(len(live_enemies)):
				print str(i+1) + ".) " + live_enemies[i].name + " (Health: "+str(live_enemies[i].hp)+")"
			print "\nHealth: " + str(player.hp) + "/" + str(player.hp_max) + "\n\"Attack\" or \"inventory\"?"
			continue			
		else: #if choice == "attack" or choice == "a":
			#Make sure that the player is able to attack.
			if player.active_ammo != "None":
				try:
					#If player needs ammo, make sure it is equipped.
					assert(player.eq_ammo!="None")
				except:
					print "You must equip have {}s to use your {}!".format(player.active_ammo, player.eq_weapon)
					continue
					
			#Gather and insanity-check information.
			try:
				#Shortcut Method ("a 2" for "attack enemy #2")
				attack_choice = int(unparsed_choice[1])-1
				assert 0 <= attack_choice < len(live_enemies)
			except:
				while (True):
					try:
						if len(unparsed_choice)>1:
							print "(Invalid enemy number.)"
							unparsed_choice = [] #Prevents repeats if user re-enters bad input.
						
						#Traditional Method:
						print "\nSelect the opponent you wish to attack."
						attack_choice = int(raw_input("--"))-1
						assert 0 <= attack_choice < len(live_enemies)
						break
					except:
						if len(live_enemies)>1:
							print "That is not a valid response. Please choose a number between \"1\" and \"{}\".".format(str(len(live_enemies)))
						else:
							print "That is not a valid response. The only option is \"1\"."
				
			#Update fight style (and remove arrow per attack if applicable).
			if player.active_ammo != "None": 
				for i in player.inventory:
					if player.eq_ammo==i[0]: location_in_inv = i
				if player.inventory[location_in_inv][1]==1:
					print "You used your last {}!".format(player.eq_ammo)
					temp = player.eq_ammo
					player.inventory_remove(temp,True)
				else:
					player.inventory_remove(player.eq_ammo)
				scene.fight_style = "char_ranged"
			else:
				scene.fight_style = "char_melee"
			
			#Attack/damage the enemy.
			attack_roll = d(20) + player.ability_modifiers[0]+player.attack_bonus

			damage_to_perform = d(player.attack_damage) + player.ability_modifiers[0]
			if (damage_to_perform<1): damage_to_perform=1
		
			live_enemies[attack_choice].been_attacked(damage_to_perform, attack_roll)
			break
			
	#Enemy turn
	for i in range(len(live_enemies)):
		enemy_attack_roll = d(20)
		if (enemy_attack_roll >= player.AC):
			enemy_damage_roll = d(live_enemies[i].damage)
			print "-The " + live_enemies[i].name + " hits you for " + str(enemy_damage_roll) + " damage!"
			player.hp -= enemy_damage_roll
		else:
			print generate_fight_sequence("enemy").format(live_enemies[i].name)

	#Prepare for next round
	if (len(live_enemies)>0 and player.hp>0):
		battle_description = generate_fight_sequence("mid_battle")
	
def generate_fight_sequence(mode):
	global live_enemies
	if (mode == "enemy"):
		temp = d(5)
		return {
		1:"-You dodge {0}'s attack!",
		2:"-The {0} knicks you, but it's only a flesh wound.",
		3:"-You jump out of the {0}'s blow!",
		4:"-The {0} misses!",
		5:"-The {0}'s attack falls short!",
		}[temp]
	if (mode == "char_melee"):
		temp = d(5)
		return {
		1:"-Your attack misses!",
		2:"-The {0} dodges your attack!",
		3:"-Your attack is blocked by the {0}!",
		4:"-The {0} jumps out of your line of attack.",
		5:"-The {0} side-steps!",
		}[temp]
	if (mode == "char_ranged"):
		temp = d(6)
		return {
		1:"-Your attack misses!",
		2:"-The {0} dodges your attack!",
		3:"-Your shot flies over the {0}'s head!",
		4:"-The {0} jumps out of your line of fire.",
		5:"-The {0} side-steps and your shot misses!",
		6:"Your attack lands on the ground a few feet from the {0}.",
		}[temp]
	if (mode == "enemy_dead"):
		temp = d(4)
		return {
		1:"-You fatally wound the {0}",
		2:"-The {0} falls to the ground.",
		3:"-The {0} collapses under your blow!",
		4:"-The {0} clutches his wound and dies.",
		} [temp]
	if (mode == "pre_battle"):
		if (len(live_enemies)==1):
			temp = d(3)
			return {
			1:"-A {0} runs at you!".format(live_enemies[0].name),
			2:"-You encounter a wild {0}!".format(live_enemies[0].name),
			3:"-A {0} approaches you -- weapon drawn!".format(live_enemies[0].name),
			}[temp]
		if (len(live_enemies)>1):
			temp = d(3)
			temp2 = d(len(live_enemies)-1)-1
			return {
			1:"-You encounter some {0}s!".format(live_enemies[temp2].name),
			2:"-{0}s surround you!".format(live_enemies[temp2].name),
			3:"-{0}s ambush you!".format(live_enemies[temp2].name),
			}[temp]			
	if (mode == "mid_battle"):
		temp = d(6)
		temp2 = d(len(live_enemies)-1)-1
		return {
		1:"-The {0} runs at you!".format(live_enemies[temp2].name),
		2:"-The {0} eyes you menacingly...".format(live_enemies[temp2].name),
		3:"-You throw a mean look at the {0}.".format(live_enemies[temp2].name),
		4:"-The {0} tries to flank you!".format(live_enemies[temp2].name),
		5:"-You manage to catch the {0} off guard!".format(live_enemies[temp2].name),
		6:"-The {0} lunges!".format(live_enemies[temp2].name),
		}[temp]
		
def generate_random_encounter(chance_to_occur, max_challenge_rating, environment):
	if d(100) <= chance_to_occur:
		if environment=="Field":
			if max_challenge_rating == 10:
				possible_encounters = ["Marauder", "Goblin", "Lycan"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]
				max_enemy_level   = d(player.level)+4
				number_of_enemies = d(1+player.level/5)
			elif max_challenge_rating >=8:
				possible_encounters = ["Marauder", "Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]	
				max_enemy_level   = d(player.level)+2
				number_of_enemies = d(2+player.level/2)		
			elif max_challenge_rating >=5:
				possible_encounters = ["Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]	
				max_enemy_level   = d(player.level/2)+2
				number_of_enemies = d(2+player.level/3)+d(max_challenge_rating)	
			else: #max_challenge_rating < 5:	
				possible_encounters = ["ROUS", "Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]
				max_enemy_level   = d(player.level/4)+2
				number_of_enemies = d(player.level/4+max_challenge_rating+1)
		elif environment=="Water_Dungeon":
				#Could add different challenge_ratings, but not necessary.
				possible_encounters = ["NOUS", "Rock Lobster"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]
				max_enemy_level   = d(player.level/3)+2
				number_of_enemies = d(player.level/3+1)
		elif environment=="Arena":
			if max_challenge_rating == 10:
				possible_encounters = ["Marauder", "Goblin", "Lycan"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]
				max_enemy_level   = d(player.level)+4
				number_of_enemies = d(1+player.level/5)
			elif max_challenge_rating >=8:
				possible_encounters = ["Marauder", "Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]	
				max_enemy_level   = d(player.level)+2
				number_of_enemies = d(2+player.level/2)		
			elif max_challenge_rating >=5:
				possible_encounters = ["Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]	
				max_enemy_level   = d(player.level/2)+2
				number_of_enemies = d(2+player.level/3)+d(max_challenge_rating)	
			else: #max_challenge_rating < 5:	
				possible_encounters = ["ROUS", "Goblin", "Kobold"]
				specific_enemy = possible_encounters[d(len(possible_encounters))-1]
				max_enemy_level   = d(player.level/4)+2
				number_of_enemies = d(player.level/4+max_challenge_rating+1)
		while number_of_enemies > 0:
			Monster(specific_enemy, max_enemy_level)
			number_of_enemies -= 1
		#Initiate Battle
		scene.battle_active = True
		scene.battle_description += generate_fight_sequence("pre_battle")

#Object Initiation
player = Character()
scene = Control()
shop = Shop()
arena = Arena()

#IMPORT CLASS-DEPENDENT DATABASES:
from item_database import *

###DEVELOPMENT MODIFICATIONS
for i in range(19):
	player.level_up()
