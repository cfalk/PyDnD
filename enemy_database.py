from game_universal_functions import *

possible_enemy_loot = {
	"ROUS": ["","","","ROUS Fang","ROUS Tail","ROUS, Fur"],
	"Goblin": ["","Wooden Shield", "!4", "Iron Sword", "Goblin Eye", "Leather Square"],
	"Kobold": ["","Leather Square","!4","Wooden Spear", "Sling", "3 x Pebble", "Kobold Trinkets", "Kobold Vest"],
	"Guard": ["","!10", "Iron Sword", "10 x Iron Arrow", "Rusty Chainmail"],
	"Marauder": ["","!5", "Wooden Shield", "Iron Shield", "Iron Bastard Sword", "Leather Square"],
	"Thug": ["","!5", "Leather Overcoat", "Large Wooden Shield", "Iron War Axe", "Leather Square", "Short Spear"],
	"Lycan": ["", "", "Lycan Eye", "Lycan Claw", "!50"]
	}
		
#Responsible for generation of monster stats.
def gen_enemy_stats(enemy, enemy_level): 
	try:
			#NAMING SCHEME:
			#	"name":				[name, hp, damage, AC, level]
		return { 
			"ROUS":					[enemy, (d(3)), 2, 8, enemy_level],
			"Goblin":				[enemy, (d(2)+1) + enemy_level/2, d(2)+2, 10, enemy_level],
			"Thug":					[enemy, (d(3)+2) + enemy_level/2, d(2)+2, 10+d(3), enemy_level],
			"Kobold":				[enemy, (d(enemy_level)+1), d(3)+1, 14, enemy_level],
			"Guard":				[enemy, (d(4)+4)*enemy_level, d(10)+3, 19, enemy_level],
			"Marauder":				[enemy, (d(3)+3)*enemy_level, d(12), 16, enemy_level],
			"Lycan":				[enemy, (d(5)+5)*enemy_level, d(12)+3, 17, enemy_level],
			}[enemy]
	except:
		print "\"" + str(enemy) + "\" is not a stock enemy."

#Responsible for generation of enemy loot.
def gen_enemy_loot(enemy):
	try:
		temp = d(len(possible_enemy_loot[enemy])-1)
		return possible_enemy_loot[enemy][temp]
	except:
		print "\"" + str(enemy) + "\" is not a stock enemy."
