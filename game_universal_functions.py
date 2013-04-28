import math
import random

def d(x):
	try:
		assert x>0
		return int(round((x-1)*random.random())+1)
	except Exception:
		print "ERROR: Dice must have positive whole number of sides."
