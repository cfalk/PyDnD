#NOTES ON SCENE_DATABASE:
#	x: ["description", ["options"], [option_results], "scene"]
#
#NAMING SCHEME:
#	x.y represents sub-options of scene x
#	10x represents a town, arena, or shop
#	20x represents a dungeon
scene_database = {
	0  :["You wake up to find your clothes soaked and torn.\n"+
		"Wherever you turn, the cackling of archaic voices seems to grow louder.\n"+
		"You cannot tell where you are and you cannot remember what brought you here.\n"+
		"\n[Menu Commands: Inventory(0) and Character Status(9)]\n",
		["Spot", "Sleep", "Listen"], [1.1, 1.1, 1.2, 1.3], "50,50_start"],
	1  :["You return to where you first woke up. Nothing yet seems familiar to you.",
		["Spot","Listen"], [1.1, 1.3, 3, 2], "50,50"],
	1.1:["You see sunlight perforating through the leaves above; dawn is approaching.\n",
		["Check Again","Listen", "Wander"], [1.1,1.3,2,1.4], "50,50_searched"],
	1.2:["You wake up with a throbbing headache."+
		"The trees appear to be slightly greener and the noises have ceased."+
		"You feel entirely alone.",
		["Spot"], [1.1,3,2], "50,50_slept"],
	1.3:["You hear the howling of jungle animals and the rippling sound of water. You feel truly alone.",
		["Spot","Check Again",], [1.1,1.3,2,3], "50,50_listened"],
	1.4:["N/A",
		["Sleep","Listen", "Wander"], [1.1,1.3,2], "50,50_called_out"],
	2  :["The rodents are kaput.",
		["Spot"], [1,1.1,4], "51_50"],
	2.1:["You see nothing of interest here -- except the defeated rodents of unusual size.",
		["Spot"], [1,1.1,4], "51,50_searched"],
	3  :["You have reached a dead end; the clearings become too dense to travel through.",
		["Spot","Turn Around"], [3.1,1], "49,50"],
	3.1:["There is nothing of interest here -- just your ordinary text-limitations of Casey not wanting to write unique descriptions.",
		["Turn Around"], [1], "49,50_searched"],
	4  :["You find yourself at a junction in the path. The canopy is sparse enough that you can see the sun shining down.",
		[], [2,5,8], "52,50"],
	4.1:["Large trees seem to be dazily swaying in front of you -- lulling you from your hypnopompic state. Nothing else strikes your interest.",
		["Turn Around"], [1], "52,50_searched"],
	5  :["You hear the tell-tale sounds of a marauder camp across a thicket of trees.",
		["Approach the Camp", "Follow the Other Path", "Go Back to the Junction"], [7,6,4], "52,49"],
	6  :["A beeeeautiful waterfall pours into a lake. Birds are singing and dancing.",
		["Explore the Obvious Waterfall Dungeon", "Turn Around"], [201,5], "51,49"],
	7  :["There are a few wooden huts scattered around, but the camp looks empty.",
		["Search for Loot", "Leave the Camp"], [7.1, 5], "53,49"],
	7.1:["The camp is silent -- spare the sound of the crackling fire.",
		["Leave the Camp"], [5], "53,49_looted"],
	8  :["You come across a sign: \"TOWNINGTON (EAST), BANDITS (NORTH)\".",
		["Go North", "Go East"], [4, 9], "52,51"],
	9  :["A road leads to the East; you suspect it goes to Townington. There is a clearing to the South.",
		["Go East", "Go South"], [12, 10], "53,51"],
	12  :["You come to another crossroads. To the North you can see smoke.",
		["Go North", "Go South", "Go East"], [13, 11, 9], "54,51"],
	13  :["There is a large guard tower on the eastern side of the road. You can hear guards yelling inside.",
		["Go North", "Go South", "Knock on the Tower Door"], [14, 12, 17], "54,50"],
	14  :["You arrive at the front gate of Townington. You can see a burly man arm wrestling himself outside a nearby inn.",
		["Explore the Town", "Leave Townington", "Approach the Man"], [101, 13, 18], "54,49"],
	101 :["You enter the glorious public district of Townington!",
		["Find the Arena", "Find a Shop","Leave the Public District"], [103, 102, 14], "54,48"],
}
	
def gather_scene_info(plot_point):
	return scene_database[plot_point]


