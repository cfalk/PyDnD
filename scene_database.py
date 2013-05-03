#NOTES ON SCENE_DATABASE:
#	x		:["description", ["options"], [option_results], "scene_name"]
#
#NAMING SCHEME:
#	x.y represents sub-options of scene x
#	1x1 represents a town center scene
#	1xy represents a town option scene (eg, arena or shop)
#	2x1 represents a dungeon entrance scene
#	2xy represents a dungeon sub-scene ('y')
scene_database = {
	#GENERAL SCENES:
	0  		:["You wake up to find your clothes soaked and torn.\n"+
				"Wherever you turn, the cackling of strange voices seems to grow louder.\n"+
				"You cannot tell where you are and you cannot remember what brought you here.\n"+
				"\n[Menu Commands: Inventory(0) and Character Status(9)]\n",
			["Spot", "Sleep", "Listen"], [1.1, 1.2, 1.3], "50,50_start"],
	1  		:["You return to where you first woke up. Nothing yet seems familiar to you.",
			["Spot","Listen"], [1.1, 1.3, 3, 2], "50,50"],
	1.1		:["You see sunlight perforating the canopy above; dawn is approaching you guess.\n",
			["Check Again","Listen", "Wander"], [1.1,1.3,2,1.4], "50,50_searched"],
	1.2		:["You wake up with a throbbing headache."+
				"The trees appear to be slightly greener and the noises have ceased."+
				"You feel entirely alone.",
			["Spot"], [1.1,3,2], "50,50_slept"],
	1.3		:["You hear the distant howling of wild animals and the rippling sound of water. It is quiet... TOO quiet...",
			["Spot","Check Again",], [1.1,1.3,2,3], "50,50_listened"],
	1.4		:["N/A",
			["Sleep","Listen", "Wander"], [1.1,1.3,2], "50,50_called_out"],
	2  		:["The rodents are kaput.",
			["Spot"], [1,1.1,4], "51_50"],
	2.1		:["You see nothing of interest here -- except the defeated Rodents of Unusual Size.",
			["Spot"], [1,1.1,4], "51,50_searched"],
	3  		:["You have reached a dead end; the clearings become too dense to travel through.",
			["Spot","Turn Around"], [3.1,1], "49,50"],
	3.1		:["There is nothing of interest here -- just your ordinary text-limitations of Casey not wanting to write unique descriptions.",
			["Turn Around"], [1], "49,50_searched"],
	4 		:["You find yourself at a junction in the path. The canopy is sparse enough that you can see the sun shining down.",
			[], [2,5,8], "52,50"],
	4.1		:["Large trees seem to be dazily swaying in front of you -- lulling you from your hypnopompic state. Nothing else strikes your interest.",
			["Turn Around"], [1], "52,50_searched"],
	5 		 :["You hear the tell-tale sounds of a marauder camp across a thicket of trees.",
			["Approach the Camp", "Follow the Other Path", "Go Back to the Junction"], [7,6,4], "52,49"],
	6 		 :["A beeeeautiful waterfall pours into a lake. Birds are singing and dancing.",
			["Explore the Obvious Waterfall Dungeon", "Leave the Peaceful Area"], [201,5], "51,49"],
	7  		:["There are a few wooden huts scattered around, but the camp looks empty.",
			["Search for Loot", "Leave the Camp"], [7.1, 5], "53,49"],
	7.1		:["The camp is silent -- spare the sound of the crackling fire.",
			["Leave the Camp"], [5], "53,49_looted"],
	8  		:["You come across a sign: \"TOWNINGTON (EAST), BANDITS (NORTH)\".",
			["Go North", "Go East"], [4, 9], "52,51"],
	9 		 :["A road leads to the East; you suspect it goes to Townington. There is a clearing to the South.",
			["Go West","Go East", "Go South"], [8, 12, 10], "53,51"],
	10  	:["It turns out the clearing is not that clear; there are trees everywhere and smoke emanating from the South.",
			["Go North", "Go South", "Go East"], [9, 17, 11], "52,53"],
	11  	:["You find a watering well. It seems to be pondering its existence -- or so the splashing from inside implies.",
			["Peer into the Well", "Go West", "Go North", "Go East"], [11.1, 10, 12, 15], "52,54"],
	11.1  	:["As you walk forward, the splashing suddenly stops.",
			["Go West","Go North", "Go East"], [10, 12, 15], "52,54"],
	12  	:["You come to another crossroads. To the North you can see smoke.",
			["Go North", "Go South", "Go West"], [13, 11, 9], "54,51"],
	13  	:["There is a large guard tower on the eastern side of the road.",
			["Go North", "Go South", "Knock on the Tower Door"], [14, 12, 18], "54,50"],
	14  	:["You arrive at the front gate of Townington. You can see a burly man arm wrestling himself outside a nearby inn.",
			["Explore the Town", "Leave Townington", "Approach the Man"], [101, 13, 14.1], "54,49"],
	14.1  	:["He mutters something about a banana and a goat... You decide it would be best to leave him alone.",
			["Explore the Town", "Leave Townington", ], [101, 13], "54,49_talked"],
	15  	:["The trees to the North seem especially dense. Perhaps the Game Master is not the most clever world designer.",
			["Go North", "Go West", "Try to Materialize a Diamond"], [16, 11, 15.1], "52,55"],
	15.1  	:["N/A",
			["Go North", "Go West", "Try Again"], [16, 11, 15.1], "52,55_diamond"],
	16  	:["Surprisingly, you find nothing interesting here, just some generic pine trees -- wait... nope. Boring.",
			["Go South", "Investigate an Obnoxious-looking Rock"], [15, 16.1], "51,55"],
	16.1	:["N/A",
			[], [16, 111], "51,55,searched"],
	17  	:["You find yourself in an abandoned camp. The silence here seems supernatural. *crash of thunder*", 
			["Explore/loot the Camp", "Leave the Camp"], [17.1, 10], "54,49"],
	17.1	:["N/A",
			["Leave the Camp"], [10], "53,49_looted"],
	18  	:["N/A",
			[], [13, 18.1, 18.2], "54,50_guard"],
	18.1  	:["The door slams in your face. That seemed strangely familiar...",
			["Knock Again", "Leave the Tower"], [18.3, 13], "54,50_guard"],
	18.2  	:["N/A",
			["Loot the Tower", "Leave the Tower"], [18.4, 13], "54,50_guard"],
	18.3  	:["There is no response.",
			["Knock Again", "Leave the Tower"], [18.3, 13], "54,50_guard"],
	18.4  	:["N/A",
			["Leave the Tower"], [13], "54,50_guard"],
	#TOWNS:
	101 	:["You enter the glorious public district of Townington!",
			["Find the Arena", "Find a Shop","Leave the Public District"], [103, 102, 14], "54,48"],
	102 	:["",#SHOP
			[], [], "54,48"],
	103 	:["",#ARENA
			[], [], "54,48"],
	111 	:["You enter the hidden underground city of the Mole People!",
			["Find an Arena", "Find a Shop","Return to the Surface"], [113, 112, 16], "50,55"],
	112 	:["",#SHOP
			[], [], "50,55"],
	113 	:["",#ARENA
			[], [], "50,55"],
	#DUNGEONS:
	201 	:["The waterfall roars next to you as you peer into the black cave.",
			["Delve Deeper into the Cave", "Leave the Scary Dungeon"], [202, 6], "51,49(D)"],
	202 	:["The ground is sloppily moist. You will need to get some new boots at Townington."+
				"\nYou see a rather large newt skeleton in a pool of water.",
			["Ignore the Faux Pas and Continue to Ruin Your Shoes", "Return to the Dungeon Entrance"], [203, 201], "51,49(D)"],
	203 	:["A strange fungus on the cave walls expels just enough light for you to see dancing shadows in the cave.",
			["Explore the Large Sublet of the Cave", "Save What's Left of Your Shoes and Leave", "Taste the Fungus"], [204, 202, 203.1], "51,49(D)"],
	203.1 	:["You start to feel dizzy. You expert opinion says that shouldn't have done that.",
			["Explore the Large Sublet of the Cave", "Save What's Left of Your Shoes and Leave",
				"Talk to the Magic Fairies that Appeared"], [204, 202, 203.2], "51,49(D)"],
	203.2 	:["They tell you: \"Don't go down the large path! There is a giant Spoctiderpus and he will eat you!\"",
			["Ignore the Unsupporting Fairies.", "Follow the Fairies' Advice and Leave"], [204, 202], "51,49(D)"],
	204 	:["You hear a low grumbling coming from deeper down the cave.",
			["Follow the Grumbling", "On Second Thought, Maybe This Wasn't a Great Idea..."], [205, 203], "51,49(D)"],
	205 	:["You see large, inhuman skeletons littering the cavern floor. Small lights are floating around the cavern like fireflies.",
			["Continue to Follow the Grumbling", "NopeNopeNopeNope. Leave."], [206, 204], "51,49(D)"],
	206 	:["The grumbling sound seems to be coming from a river passing through the cave.",
			["Approach the Chest!", "It's Probably a Trap. Turn Around."], [206.1, 205], "51,49(D)"],
	206.1 	:["The light of the fungus gives a green glow to the water all along the cave.",
			["Leave the Cave."], [205], "51,49(D)"],
}
	
def gather_scene_info(plot_point):
	return scene_database[plot_point]


