#!/bin/python

import sys
import getopt
import random

class Dice(object):
	"""docstring for Dice"""
	def __init__(self):
		super(Dice, self).__init__()

	def roll(self):
		return random.randint(1,6)

class Dealer(object):
	"""docstring for Dealer"""
	def __init__(self):
		super(Dealer, self).__init__()

		def init_dice():
			die1 = Dice()
			die2 = Dice()
			return [die1,die2]

		self.dice = init_dice()
		self.pass_line = (1,1)
		self.dont_pass = (1,1)
		self.come = (1,1)
		self.dont_come = (1,1)
		self.field = [(2,1),(1,1),(1,1),(1,1),(1,1),(1,1),(3,1)] #2,3,4,9,10,11,12
		self.big_6 = (1,1)
		self.big_8 = (1,1)
		self.place_to_win = [(9,5),(7,5),(7,6),(7,6),(7,5),(9,5)] #4,5,6,8,9,10
		self.place_against = [(5,11),(5,8),(4,5),(4,5),(5,8),(5,11)] #4,5,6,8,9,10
		self.buy = [(2,1),(3,2),(6,5),(6,5),(3,2),(2,1)] #4,5,6,8,9,10 + 5% vigorish
		

	def roll(self):
		combination = [self.dice[1].roll(),self.dice[1].roll()]
		return combination

class Player(object):
	"""docstring for Player"""
	def __init__(self):
		super(Player, self).__init__()
		self.money = 1000

	def getMoney(self):
		return self.money

	def roll(self, dealer):
		return dealer.roll()

	def knowledge(self, value):
		#Value must be 2 - 12
		if value == 2 or value == 12:
			return 1
		elif value == 3 or value == 11:
			return 2
		elif value == 4 or value ==  10:
			return 3
		elif value == 5 or value == 9:
			return 4
		elif value == 6 or value == 8:
			return 5
		elif value == 7:
			return 6
		else:
			return 0

class Game(object):
	def __init__(self, num_players):
		super(Game, self).__init__()
		#off if 0, on if 4-10
		self.on_off = 0
		self.num_players = num_players
		self.players = []
		self.dealer = Dealer()
		for i in range(num_players):
			self.players.append(Player())
			print("Player "+ str(i+1) + " has joined the table with $" + str(self.players[i].getMoney()) +".")

	def addPlayer(self):
		if self.num_players >= 8:
			print("Maximum for table has been reached.")
			return 1
		self.num_players += 1
		self.players.append(Player())
		print("Player "+ str(i+1) + " has joined the table with $" + str(self.players[i].getMoney()) +".")
		return 0

	def setOnOff(self,value):
		if value < 4 or value > 10:
			self.on_off = 0
		else:
			self.on_off = value

	def run(self):
		def point_round():
			response = raw_input("Player " + str(current_player) + " please roll for point round ")
			if response == "q":
				return 0
			result = self.players[current_player].roll(self.dealer)
			print(str((result,sum(result))))
			if sum(result) == 7:
				print"Seven-out Occurred!"
			elif sum(result) == self.on_off:
				print("Winning " + str(sum(result)) + " rolled. Round Ends!")
			else:
				point_round()

		current_player = 0
		reset = False
		while(1):

			#Select Player to roll
			if reset == True:
				if self.num_players - 1 <= current_player:
					current_player = 0
				else:
					current_player += 1
				reset = False
				self.setOnOff(0)
			print("\n\nPlayer " + str(current_player+1) + " is about to roll, place bets.\n")			

			#take bets
			print("All bets placed, player rolling.\n")
			response = raw_input("Hit Enter to roll. ")
			if response == "q":
				return 0
			#Come out roll
			result = self.players[current_player].roll(self.dealer)
			print(result,sum(result))
		
			#if crap occurred
			##2,3,7,11,12
			if sum(result) in [2,3,12]:
				reset = True
				print("\n\nCraps Occurred!\n")
			elif sum(result) in [7,11]:
				reset = True
				print("\n\nPass Line Wins!\n")
			#else take bets, point on
			#loop through rolls until 7 is rolled
			else:
				self.setOnOff(sum(result))
				point_round()
				reset = True

def usage():
	print("python craps_simulator.py [-p,num_players (1-8)]")

def get_arguments():
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hp:",["help","num_players="])
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)
	num_players = None
	for p, a in opts:
		if p in ("-h", "--help"):
			usage()
			sys.exit()
		elif p in ("-p", "--num_players"):
			num_players = a
			return num_players
		else:
			assert False, "Unhandled option"
			sys.exit(2)
	return None

def main():

	#get number of players by commandline or through user input
	num_players = get_arguments()
	print(chr(27) + "[2J")
	try:
		print("WELCOME TO MY CRAPS SIMULATOR.\nTo exit at any time press 'q' followed by the enter button.\n\n")
		if num_players == None:	
			num_players = raw_input("How many players are there (max 8)? ")
			if num_players == "q":
				return 0
		
		num_players = int(num_players)
		if num_players > 8 or num_players < 1:
			print("Invalid Number of Players. Exiting.\n")
			return 1
	except ValueError:
		print("Invalid Entry. Exiting.\n")
		return 1
	table = Game(num_players)
	table.run()

	return 0

if __name__ == '__main__':
	sys.exit(main())