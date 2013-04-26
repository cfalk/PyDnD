#MINI-DATABASES
#
def	race_modifications(race):
	#"race" = [Strength, Dexterity, Constitution, Wisdom, Intelligence, Charisma]
	return {
	"Elf": [-2,0,-1,1,2,0],
	"Orc": [3,0,2,-1,-1,-2],
	"Human": [0,0,0,0,0,0],
	"Dwarf": [2,0,2,0,0,-1],
	"Gnome": [-2,2,-2,0,1,0],
	"Bear": [5,-2,2,-1,-2,-4],
	"Goblin": [1,1,0,-1,0,1],
	}[race]

def	class_modifications(cclass): #Class only modifies hit-die.
	return {
	"Fighter": 10,
	"Ranger": 8,
	"Wizard": 4,
	"Rogue": 6,
	"Bard": 6,
	"Barbarian": 12,
	}[cclass]		
