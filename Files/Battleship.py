##############################################################################################################
# Class: Programming Languages 220
# Prof: John Broere
# Date: 9/23/2015
# Program Name: Battleship Game Python
# Programmers: Bjorn Mathisen and Jacob Huss
# Description of Program: A battleship clone game, the end goal is for either the player or the AI/computer
#                         to destroy all the ships on the opposing team. They can accomplish this with a 
#                         varriety of artillary, including bombs, torpedoes, and single hit missiles. The 
#                         AI is programmed to select random coordinates and on occasion use a limited supply
#                         of artillary, the same amount is alloted to the player. For deployment purposes
#                         the player can select either manual or automatic deployment, the computers ships
#                         are always randomly automatically assigned positions. When the player places his
#                         ships he has the option to place them left, right, up or down. Error checking 
#                         validates these coordinates before placing a ship. To view the players/enemy board
#                         a algorithm was designed that would allow the programming to view the map as values
#                         and the player would see appropriate symbols depending on the ship, and the damage
#                         that each ship has sustained. A table depicting all possible values and their meaning
#                         has been constructed below, as well as a table of all the possible ships plus any 
#                         other information that might be requried either by the programmer or the player 
#                         should he so desire to see it.
#
#                        NOTE: Massive data validation on every input
##############################################################################################################

#Game Documentation

#Players
	#Human
	#Computer Opponent
	
#Ship Name			Size
#Carrier			5
#Battleship			4
#Destroyer			3
#Submarine			2


#Grid Layout Information
#Information for each point on the grid

#Function							Base String		Player View (Own Board)		Player View (Enemy Board)
#Empty space, not fired on				"0"					  " "						  "?"
#Empty space, missed shot				"1"				   	  "*"						  " "
#Carrier, not fired on					"2"					  "C"						  "?"
#Carrier, fired on, not sunk			"3"					  "X"						  "X"
#Carrier, fired on, sunk				"4"					  "X"						  "C"	
#Battleship, not fired on				"5"					  "B"						  "?"
#Battleship, fired on, not sunk		"6"					  "X"						  "X"
#Battleship, fired on, sunk			"7"					  "X"						  "B"
#Destroyer, not fired on				"8"					  "D"						  "?"
#Destroyer, fired on, not sunk		"9"					  "X"						  "X"
#Destroyer, fired on, sunk				"A"					  "X"						  "D"
#Submarine, not fired on				"B"					  "S"						  "?"
#Submarine, fired on, not sunk		"C"					  "X"						  "X"
#Submarine, fired on, sunk				"D"					  "X"						  "S"

'''
Program Prologue

'''

import os
import random
import time

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: cls()
#
#   Pre: none	
#
#   Post: decides which clear statement commands to use depending on the installed OS
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cls():
		os.system('cls' if os.name == 'nt' else 'clear')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: main()
#
#   Pre: none
#
#   Post: calls forth various functions designed to enable gameplay and menu selection/deployment of ships
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
		print "Co-created by: Bjorn & Jacob, 2014"
		print
		print "       _~  _~     ______       _   _   _      _____ _     _        "
		print "    __|=|_|=|__   | ___ \     | | | | | |    /  ___| |   (_)       "
		print "    \ o.o.o.oY/   | |_/ / __ _| |_| |_| | ___\ `--.| |__  _ _ __   "
		print "     \_______/    | ___ \/ _` | __| __| |/ _ \`--. \ '_ \| | '_ \  "
		print "   ~~~~~~~~~~~~~~ | |_/ / (_| | |_| |_| |  __/\__/ / | | | | |_) | "
		print "   ~ ~ ~ ~ ~ ~ ~  \____/ \__,_|\__|\__|_|\___\____/|_| |_|_| .__/  "
		print "  ~  ~  ~  ~  ~  ~                                         | |     "
		print "                                                           |_|     "
		print
		print
		
		raw_input("Press ENTER to view the rules.")
		Rules() #calls forth the rules function (text wall)
		cls()
		
		repeat = "Y"
		while (repeat == "Y"):
		
			#Help from stackoverflow.com
			playerBoard = [["0" for x in range(10)] for x in range(10)] #sets the playerBoard dictionary matrix with default 0 values
			enemyBoard = [["0" for x in range(10)] for x in range(10)] #same as above, only for the enemyBoard
		
			#Calls deployment phase which automates both computer and player deployment
			DeploymentPhase(playerBoard, enemyBoard)
			
			#calls gameplay phase, takes turns for both the player and the enemy, untill either one wins
			GamePhase(playerBoard, enemyBoard)
			
			# varaible for data loop
			validData = "false"
			# prompts to repeat the game, loops untill valid input is applied
			while (validData == "false"):
				cls()
				repeat = raw_input("Would you like to repeat the game? Enter Y or N: ")
				repeat = repeat.upper()
				if repeat == "Y" or repeat == "N":
					validData = "true"
			
		#end of while repeat
	#end of main()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: Rules()
#
#   Pre: none
#
#   Post: prints a solid wall of strings, displaying the rules for the game, exits with ENTER
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Rules():
		cls()
		print "                                     RULES                          "
		print
		print " Welcome to Battleship, the game where the goal is to sink your enemy's"
		print " ships before they sink yours.  To start the game, you will have the"
		print " option to either manually deploy your ships onto your 10 by 10 board"
		print " or have them randomly deployed on your map. Either way, you will have"
		print " a 5-unit long Carrier, a 4-unit long Battleship, a 3-unit long Destroyer"
		print " and a 2-unit long Submarine."
		print
		print " Once both sides have deployed their ships, the computer will randomly decide"
		print " who gets to go first. You and the enemy will the take turns firing at each"
		print " other's ships."
		print
		print " When looking at your map, each of your ships will be represented with the"
		print " capital letter of the first letter of the respective ships. Once hit, those"
		print " letters will change to an 'X' character. A ' ' character represents a blank"
		print " position and a '*' represents an enemy's missed shot." 
		print
		print " When looking at your enemy's map, uncovered grid positions"
		print " will have a '?'. Missed shots will have a ' '.  Shot ship pieces will be"
		print " represented with an 'X'.  Once a ship is completely destroyed, those ships"
		print " will be represented with the capital letter of the first letter of the ship"
		print " that has been destroyed. Once someone's ships are all destroyed, they lose."
		print
		print " Once gameplay starts, the player will have a variety of artillary to use, from"
		print " clusterbombs to torpedoes and missiles. You will have a large variety of"
		print " weapondry to rain fire down upon your enemies. However they shall have access"
		print " to this functionality as well, so plan safely Commander. Best of luck..."
		print
		raw_input("Press ENTER to begin sinkin' all y'er enemies...")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ShowBaseBoard()
#
#   Pre: requires board as an argument 
#
#   Post: returns the board in a 10x10 row without formatting of any kind
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ShowBaseBoard(board):
		for list in board:
			print list
	
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: DisplayBoard(board, player)
#
#   Pre: requires board as an argument, along with the player to be printed, allowed players are enemy and player
#
#   Post: returns the board in formatted 10x10 row
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def DisplayBoard(board, player):
		print "                         " + player + "'s Board" #Board Heading
		print
		print "       0     1     2     3     4     5     6     7     8     9" #Board Heading Cont.
		rowValue = "@" #ACSII character before "A", used to keep track of row letter, loops foward
		for list in board: #for every list in the matrix
			print
			rowValue = chr(ord(rowValue) + 1); #Used to increment row letter using ASCII, with help from stackoverflow.com		
			sDisplayLine = "  " + rowValue + "  " #Display's each row's letter
			colValue = 0 #Tracks column number for current for formatting purposes
			for item in list: #Goes through each item in a row to add it to the display string for that row
				if colValue == 0:
					sDisplayLine = sDisplayLine + "  " + ConvertFromBase(item, player) + "  "
				else:
					sDisplayLine = sDisplayLine + "|  " + ConvertFromBase(item, player) + "  "
				colValue = colValue + 1
			print sDisplayLine
			
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function:  ConvertFromBase(baseString, player)
#
#   Pre: requires board and player as parameters
#
#   Post: returns a value that coordinates with the symbol required for gameplay view or enemy view
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def ConvertFromBase(baseString, player):
	if player == "Player":	#value interpitations for gameplay on playerside
		if baseString == "0":
			return " "
		elif baseString == "1":
			return "*"
		elif baseString == "2":
			return "C"
		elif baseString == "3":
			return "X"
		elif baseString == "4":
			return "X"
		elif baseString == "5":
			return "B"
		elif baseString == "6":
			return "X"
		elif baseString == "7":
			return "X"
		elif baseString == "8":
			return "D"
		elif baseString == "9":
			return "X"
		elif baseString == "A":
			return "X"
		elif baseString == "B":
			return "S"
		elif baseString == "C":
			return "X"
		else:
			return "X"
			
	else: #enemy screen viewed by player 
		if baseString == "0":
			return "?"
		elif baseString == "1":
			return " "
		elif baseString == "2":
			return "?"
		elif baseString == "3":
			return "X"
		elif baseString == "4":
			return "C"
		elif baseString == "5":
			return "?"
		elif baseString == "6":
			return "X"
		elif baseString == "7":
			return "B"
		elif baseString == "8":
			return "?"
		elif baseString == "9":
			return "X"
		elif baseString == "A":
			return "D"
		elif baseString == "B":
			return "?"
		elif baseString == "C":
			return "X"
		else:
			return "S"		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: DeploymentPhase(playerBoard, enemyBoard):
#
#   Pre: requires playerBoard and enemyBoard as parameters
#
#   Post: prompts for either manual or automatic player deployment, upon completion assigns enemy ship pos
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def DeploymentPhase(playerBoard, enemyBoard):
		deployChoice = "false" #required for input data validation
			
		while (deployChoice == "false"):		
			cls()
			print "###############################################################################"
			print "#                                                                             #"
			print "#                                                                             #"
			print "#                                                                             #"
			print "#     Welcome Commander, would you like to manual or automatic deployment?    #"
			print "#                                                                             #"                   
			print "#                                                                             #"
			print "#                                                                             #"
			print "#              For optimal viewing, please maximize your window               #"
			print "###############################################################################"
			print 

			#prompts for manual or automatic deployment selection
			deploymentChoice = raw_input("Enter 'M' for manual or 'A' for automatic: ")
			deploymentChoice = deploymentChoice.upper() #converts to upper for proper data validation
		
			# data validation for deployment input
			if deploymentChoice == "M": #if manual deployment option is choosen call forth the manual function
				ManualDeploy(playerBoard)
				deployChoice = "true"
		
			elif deploymentChoice == "A": #if automatic deployment is choosen, assign randoml values to ships
				AutoDeploy(playerBoard)
				deployChoice = "true"
			else: #if inpropper input is entered, display message and restart prompt
				raw_input("I don't understand... press ENTER to try again")
			
		cls()
		#clear the screen after all ships have been deployed, print the player board and display a legend
		DisplayBoard(playerBoard, "Player")
		print
		raw_input("Press ENTER to let the enemy deploy their ships.")
		
		#calls forth the enemy ships
		cls()
		AutoDeploy(enemyBoard)
		print "Enemy deployed, Carrier, Battleship, Destroyer and Submarine."
		print "Prepare yourself commander, they are coming..."
		print
		raw_input("Press ENTER continue to the game.")
	
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ManualDeploy(board):
#
#   Pre: the board to be deployed to must be passed in as a parameter
#
#   Post: each ships coords are fully data valid, once complete exit back to game screen
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def ManualDeploy(board):

		# var pool, we know the input variables do not need to be previously declared, however we decided 
		# to add them here simply for safetys sake 
		inputCol = -1
		inputRow = -1
		inputRot = -1
		input = -1 #used for storing raw_input divided between row/col using sparse
		
		# placeholders for boolean values used to control the while statements for each ship
		addCarrier = "false"
		addBattleship = "false"
		addDestroyer = "false"
		addSubmarine= "false"
		
		# add carrier while loop
		while (addCarrier == "false"):
			
			cls()
			# displays board so the player can see the current situtation 
			DisplayBoard(board, "Player")
			
			#prompts for input coordinates
			print
			print "Please enter the row and column numbers for your Carrier (length 5)."
			print "Example: D,6"
			input = raw_input("Coordinates: ")
			
			try:	
				# parses the input into the two coordinate values
				inputRow,inputCol = input.split(",")
				
				# converts character to a numeric value
				inputRow = inputRow.upper()
				inputRow = ConvertRowToNumb(inputRow)	

				# converts the string number value to an int
				inputCol = int(inputCol)
				
				# prompts for direction of ship placement
				print
				print "Would you like your ship to face up, down, left or right?"
				inputRot = raw_input("Enter U, D, L, or R: ")
				inputRot = inputRot.upper() #converts input to uppercase
				
				#converts first letter to acceptable function parameter input
				if inputRot == "U":
					# adds the ship to the board if it fits within the alloted space 
					if 	CanAddShip(board, inputRow, inputCol, 5, "up") == "true":
						AddShip(board, inputRow, inputCol, 5, "up", "2") #2 not fired on value for carrier
						addCarrier = "true" #provides the condition to close the carrier while loop
					else:
						print #valid prompt
						raw_input("Not a valid position. Press ENTER to try again...")
				
				elif inputRot == "D":
					# adds the ship to the board if it fits within the alloted space 
					if 	CanAddShip(board, inputRow, inputCol, 5, "down") == "true":
						AddShip(board, inputRow, inputCol, 5, "down", "2") #2 not fired on value for carrier
						addCarrier = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "L":
					# adds the ship to the board if it fits within the alloted space 
					if 	CanAddShip(board, inputRow, inputCol, 5, "left") == "true":
						AddShip(board, inputRow, inputCol, 5, "left", "2") #2 not fired on value for carrier
						addCarrier = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "R":
					# adds the ship to the board if it fits within the alloted space 
					if 	CanAddShip(board, inputRow, inputCol, 5, "right") == "true":
						AddShip(board, inputRow, inputCol, 5, "right", "2") #2 not fired on value for carrier
						addCarrier = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
									
				else:
					print
					raw_input("Not a valid orientation. Press ENTER to try this again...")
			except:
				raw_input("Not a valid position. Press ENTER to try again...")
			
		#NOTE: the remaining ship while statements have not been commented because they are the exact same as above
        #      the only difference being the ship being given coordinates
		
		#battleship while loop start		
		while (addBattleship == "false"):
			
			cls()
			DisplayBoard(board, "Player")
			
			print
			print "Please enter the row and column numbers for your Battleship (length 4)."
			print "Example: D,6"
			input = raw_input("Coordinates: ")
			
			try:
				inputRow,inputCol = input.split(",")
				
				inputRow = inputRow.upper()
				inputRow = ConvertRowToNumb(inputRow)
			
				inputCol = int(inputCol)

				print
				print "Would you like your ship to face up, down, left or right?"
				inputRot = raw_input("Enter U, D, L, or R: ")
				inputRot = inputRot.upper()
				
				if inputRot == "U":
					
					if 	CanAddShip(board, inputRow, inputCol, 4, "up") == "true":
						AddShip(board, inputRow, inputCol, 4, "up", "5") 
						addBattleship = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
				
				elif inputRot == "D":
					
					if 	CanAddShip(board, inputRow, inputCol, 4, "down") == "true":
						AddShip(board, inputRow, inputCol, 4, "down", "5") 
						addBattleship = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "L":
					
					if 	CanAddShip(board, inputRow, inputCol, 4, "left") == "true":
						AddShip(board, inputRow, inputCol, 4, "left", "5") 
						addBattleship = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "R":
					
					if 	CanAddShip(board, inputRow, inputCol, 4, "right") == "true":
						AddShip(board, inputRow, inputCol, 4, "right", "5") 
						addBattleship = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
									
				else:
					print
					raw_input("Not a valid orientation. Press ENTER to try this again...")
			except:
				raw_input("Not a valid position. Press ENTER to try again...")
		#destroyer while loop start		
		while (addDestroyer == "false"):
			
			cls()
			DisplayBoard(board, "Player")
			
			print
			print "Please enter the row and column numbers for your Destroyer (length 3)."
			print "Example: D,6"
			input = raw_input("Coordinates: ")
			
			try:
				inputRow,inputCol = input.split(",")
				
				inputRow = inputRow.upper()
				inputRow = ConvertRowToNumb(inputRow)
			
				inputCol = int(inputCol)
				
				print
				print "Would you like your ship to face up, down, left or right?"
				inputRot = raw_input("Enter U, D, L, or R: ")
				inputRot = inputRot.upper()
				
				if inputRot == "U":
					
					if 	CanAddShip(board, inputRow, inputCol, 3, "up") == "true":
						AddShip(board, inputRow, inputCol, 3, "up", "8")
						addDestroyer = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
				
				elif inputRot == "D":
					
					if 	CanAddShip(board, inputRow, inputCol, 3, "down") == "true":
						AddShip(board, inputRow, inputCol, 3, "down", "8") 
						addDestroyer = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "L":
					
					if 	CanAddShip(board, inputRow, inputCol, 3, "left") == "true":
						AddShip(board, inputRow, inputCol, 3, "left", "8") 
						addDestroyer = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "R":
					
					if 	CanAddShip(board, inputRow, inputCol, 3, "right") == "true":
						AddShip(board, inputRow, inputCol, 3, "right", "8") 
						addDestroyer = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
									
				else:
					print
					raw_input("Not a valid orientation. Press ENTER to try this again...")
					
			except:		
				raw_input("Not a valid position. Press ENTER to try again...")
		#submarine while loop start		
		while (addSubmarine == "false"):
			
			cls()
			DisplayBoard(board, "Player")
			
			print
			print "Please enter the row and column numbers for your Submarine (length 2)."
			print "Example: D,6"			
			input = raw_input("Coordinates: ")
			
			try:
				inputRow,inputCol = input.split(",")
				
				inputRow = inputRow.upper()
				inputRow = ConvertRowToNumb(inputRow)
				
				inputCol = int(inputCol)
				
				print
				print "Would you like your ship to face up, down, left or right?"
				inputRot = raw_input("Enter U, D, L, or R: ")
				inputRot = inputRot.upper()

				if inputRot == "U":
					
					if 	CanAddShip(board, inputRow, inputCol, 2, "up") == "true":
						AddShip(board, inputRow, inputCol, 2, "up", "B") 
						addSubmarine = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
				
				elif inputRot == "D":
					
					if 	CanAddShip(board, inputRow, inputCol, 2, "down") == "true":
						AddShip(board, inputRow, inputCol, 2, "down", "B")
						addSubmarine = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "L":
					
					if 	CanAddShip(board, inputRow, inputCol, 2, "left") == "true":
						AddShip(board, inputRow, inputCol, 2, "left", "B") 
						addSubmarine = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")

				elif inputRot == "R":
					
					if 	CanAddShip(board, inputRow, inputCol, 2, "right") == "true":
						AddShip(board, inputRow, inputCol, 2, "right", "B") 
						addSubmarine = "true"
					else:
						print
						raw_input("Not a valid position. Press ENTER to try again...")
									
				else:
					print
					raw_input("Not a valid orientation. Press ENTER to try this again...")
			except:	
				raw_input("Not a valid position. Press ENTER to try again...")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: AutoDeploy(board)
#
#   Pre: requires board as an argument, accepts either playerBoard or enemyBoard
#
#   Post: each ship is randomly assigned a value, then the function checks to see if the ship fits within
#         the alloted coordinates, if true, then it saves the ship to the board matrix position, and proc-
#         cedes down the list of ships, untill it has archived all 4 ships values succesfully saved to the 
#         passed in board parameter (either player or enemy)
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def AutoDeploy(board):
        #var pool
		randRow = -1
		randCol = -1
		randPos = -1
		#makeshift boolean values
		addCarrier = "false"
		addBattleship = "false"
		addDestroyer = "false"
		addSubmarine= "false"
		
		#start add carrier while loop
		while (addCarrier == "false"):
		    #randomly assign values based on random library function
			randRow = random.randint(0,9)
			randCol = random.randint(0,9)
			randPos = random.randint(0,3)
			#assigns random up, down, left, or right rotation based on a numeric value
			if randPos == 0:
				randPos = "right"
			elif randPos == 1:
				randPos = "down"
			elif randPos == 2:
				randPos = "left"
			else:
				randPos = "up"				
			#if all the above randomly generated numbers allow for a ship to be properly saved to a board, then 
            #add the ship to the board using the choosen values as function parameters
			if 	CanAddShip(board, randRow, randCol, 5, randPos) == "true":
				AddShip(board, randRow, randCol, 5, randPos, "2")
				addCarrier = "true" #once the ship is added, set the loop value to a non-looping value
		
        #NOTE: the remaining ship while statements have not been commented because they are the exact same as above
        #      the only difference being the ship being given coordinates

        #start of battleship while loop randomly generated position		
		while (addBattleship == "false"):
			randRow = random.randint(0,9)
			randCol = random.randint(0,9)
			randPos = random.randint(0,1)
			if randPos == 0:
				randPos = "right"
			elif randPos == 1:
				randPos = "down"
			elif randPos == 2:
				randPos = "left"
			else:
				randPos = "up"	
			if 	CanAddShip(board, randRow, randCol, 4, randPos) == "true":
				AddShip(board, randRow, randCol, 4, randPos, "5")
				addBattleship = "true"

        #start of destroyer while loop randomly generated position						
		while (addDestroyer == "false"):
			randRow = random.randint(0,9)
			randCol = random.randint(0,9)
			randPos = random.randint(0,1)
			if randPos == 0:
				randPos = "right"
			elif randPos == 1:
				randPos = "down"
			elif randPos == 2:
				randPos = "left"
			else:
				randPos = "up"	
			if 	CanAddShip(board, randRow, randCol, 3, randPos) == "true":
				AddShip(board, randRow, randCol, 3, randPos, "8")
				addDestroyer = "true"
        #start of submarine while loop randomly generated position						
		while (addSubmarine == "false"):
			randRow = random.randint(0,9)
			randCol = random.randint(0,9)
			randPos = random.randint(0,1)
			if randPos == 0:
				randPos = "right"
			elif randPos == 1:
				randPos = "down"
			elif randPos == 2:
				randPos = "left"
			else:
				randPos = "up"	
			if 	CanAddShip(board, randRow, randCol, 2, randPos) == "true":
				AddShip(board, randRow, randCol, 2, randPos, "B")
				addSubmarine = "true"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ConvertRowToNumb(baseLetter)
#
#   Pre: a string be submitted into the function ranging from values A-J
#
#   Post: if the baseletter is withing range of A-J on the alphebet, then return a corresponding value 0-9
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
def ConvertRowToNumb(baseLetter):
	if baseLetter == "A":
		return 0
	elif baseLetter == "B":
		return 1
	elif baseLetter == "C":
		return 2
	elif baseLetter == "D":
		return 3
	elif baseLetter == "E":
		return 4
	elif baseLetter == "F":
		return 5
	elif baseLetter == "G":
		return 6
	elif baseLetter == "H":
		return 7
	elif baseLetter == "I":
		return 8
	elif baseLetter == "J":
		return 9
	else:
		return -1
				
	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: CanAddShipboard(board, row, col, shipLength, direction)
#
#   Pre: requires the board, two coordinate values, and a position string either horizontal or vertical 
#
#   Post: checks to see if the coordinates are out-of-bounds or already have
#		  a ship at that position.  Returns a string false if either of these are true.
#		  Returns string true otherwise.
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CanAddShip(board, row, col, shipLength, direction):
		if direction == "right": #direction to be checked 
			for shipPart in range(shipLength): #for each piece of the ship
				if CanAddShipPiece(board, row, col) == "false": #calls the function that checks each piece individually 
					return "false"
				col = col + 1 #increments to check the next cell over
		elif direction == "down":
			for shipPart in range(shipLength):
				if CanAddShipPiece(board, row, col) == "false":
					return "false"
				row = row + 1
		elif direction == "left":
			for shipPart in range(shipLength):
				if CanAddShipPiece(board, row, col) == "false":
					return "false"
				col = col - 1
		else:
			for shipPart in range(shipLength):
				if CanAddShipPiece(board, row, col) == "false":
					return "false"
				row = row - 1				
		return "true"
		
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: CanAddShipPiece(board, row, col)	
#
#   Pre: requires the board and two coordinates 
#
#   Post: checks to see if the coordinates are out-of-bounds or already have
#		  a ship piece at that position.  Returns false if either of these are true.
#		  Returns true otherwise.
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def CanAddShipPiece(board, row, col):
		if (row < 0) or (row > 9) or (col < 0) or (col > 9): #If index is out-of-bounds
			return "false"
		if board[row][col] == "0":
			return "true"
		return "false"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: AddShip(board, row, col, shipLength, direction, shipString):
#
#   Pre: requires the board, row and col coordinate values, the total ship length, direction of face, and the
#        ship value accordign to the numeric value chart at the top of the program
#
#   Post: adds the ship to the board using a variety of functions to check if true, add the ship to the board
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def AddShip(board, row, col, shipLength, direction, shipString):
		if direction == "right":
			for shipPart in range(shipLength):
				board[row][col] = shipString
				col = col + 1
		elif direction == "down":
			for shipPart in range(shipLength):
				board[row][col] = shipString
				row = row + 1
		elif direction == "left":
			for shipPart in range(shipLength):
				board[row][col] = shipString
				col = col - 1
		else:
			for shipPart in range(shipLength):
				board[row][col] = shipString
				row = row - 1				
		return "true"
		
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: GamePhase(playerBoard, enemyBoard):
#
#   Pre: accepts playerBoard and the enemyBoard as parameters
#
#   Post: exicutes untill either side looses, lets each player take shots at one another until exit 
#         conditions are met 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
def GamePhase(playerBoard, enemyBoard):
	cls()
	
	playerShips = [1 for x in range(4)] #number of player ships
	enemyShips = [1 for x in range(4)] #number of enemy ships
	playerWeapons = [1,2,3] #number of available weapons to be used
	enemyWeapons = [1,2,3] #number of available weapons to be used by the enemy
	
	winner = "none" #winner data variable
	turn = random.randint(0,1)  #randomly either has the player or enemy go first
	
	while (winner == "none"): #while no winner
		if turn % 2 == 0:  #player goes first
			PlayerTurn(enemyBoard, enemyShips, playerWeapons)
			if enemyShips[0] == 0 and enemyShips[1] == 0 and enemyShips[2] == 0 and enemyShips[3] == 0:
				winner = "player"
		else: #enemy goes first
			EnemyTurn(playerBoard, playerShips, enemyWeapons)
			if playerShips[0] == 0 and playerShips[1] == 0 and playerShips[2] == 0 and playerShips[3] == 0:
				winner = "enemy"
		turn = turn + 1
	
	cls()
	
	if winner == "player":
		print "Congratulations! You win!!!"
	else:
		print "I'm sorry, but you lost..."
	raw_input("Press ENTER to continue...")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PlayerTurn(playerBoard, enemyBoard):
#
#   Pre: enemyBoard, number of enemy ships, and the avialable player weapons are passed in as parameters
#
#   Post: the player, upon entering valid coordinates, is prompted which weapon he wants to fire, the cords
#         are then checked for valid data against the enemyBoard ship locations, a hit or a miss is then recorded
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
def PlayerTurn(enemyBoard, enemyShips, playerWeapons):
		outputMessage = ""
		messageArray = [0 for x in range(5)]
		
		validInput = "false" #data validation input variable
		while (validInput == "false"):
			cls()

			DisplayBoard(enemyBoard, "Enemy") #prints the board currently fired upon
			
			#prompt for cords
			print 
			print "What coordinate would you like to fire upon?"
			print "Example: G,5"
			input = raw_input("Cords: ")
		
			try:		
				inputRow, inputCol = input.split(",") #splits the input string into appriate values
				inputRow = inputRow.upper() #converts to upper each input char
				inputRow = ConvertRowToNumb(inputRow) # converts character to a numeric value readable by the map
			
				inputCol = int(inputCol) # converts the string number value to an int
				
				if (inputRow < 0) or (inputRow > 9) or (inputCol < 0) or (inputCol > 9): # if the input is within a valid map cord range
					raw_input("Invalid input. Press ENTER to try again.")
					
				else:
					if (playerWeapons[0] == 0) and (playerWeapons[1] == 0) and (playerWeapons[2] == 0): # if a weapon is available to use
						inputWeapon = "M"
						
					else: #print the following weapons and the amount of uses for each
						print
						print "You have infinite missiles (M)"
						
						if playerWeapons[0] == 1: #grammer for each weapon based on number of
							print "You have " + str(playerWeapons[0]) + " bomb (B)"
						elif playerWeapons[0] > 1:
							print "You have " + str(playerWeapons[0]) + " bombs (B)"
							
						if playerWeapons[1] == 1:
							print "You have " + str(playerWeapons[1]) + " clusterbomb (C)"
						elif playerWeapons[1] > 1:
							print "You have " + str(playerWeapons[1]) + " clusterbombs (C)"						
							
						if playerWeapons[2] == 1:
							print "You have " + str(playerWeapons[2]) + " torpedo (T)"
						elif playerWeapons[2] > 1:
							print "You have " + str(playerWeapons[2]) + " torpedoes (T)"
						
						#prompt for input for weapon select
						inputWeapon = raw_input("Input the letter of the weapon you would like to use: ")
						inputWeapon = inputWeapon.upper()
					
					#if out of special artilary, do the following 
					if (inputWeapon == "T") or (inputWeapon == "C") or (inputWeapon == "M") or (inputWeapon == "B"):
						if inputWeapon == "B":
							if playerWeapons[0] > 0: # for no bombs
								validInput = "true" 
							else:
								raw_input("You do not have any more bombs. Press ENTER to try again.")
								
						elif inputWeapon == "C":	
							if playerWeapons[1] > 0:
								validInput = "true"
							else:
								raw_input("You do not have any more clusterbombs. Press ENTER to try again.")	
								
						elif inputWeapon == "T":	
							if playerWeapons[2] > 0:
								print
								print "Would you like the torpedo to travel up, down, left, or right from this point?"
								inputDirection = raw_input("Enter U, D, L, or R: ")
								inputDirection = inputDirection.upper()
								if (inputDirection == "U") or (inputDirection == "D") or(inputDirection == "L") or (inputDirection == "R"):
									validInput = "true"
								else:
									raw_input("Invalid input. Press ENTER to try again.")
							else:
								raw_input("You do not have any more torpedoes. Press ENTER to try again.")									
						else:
							validInput = "true"
							
					else: # end of input checking
						raw_input("Invalid input. Press ENTER to try again.")
			except:
				raw_input("Invalid input. Press ENTER to try again.")
		
		cls()
		#fires each weapon based on its own specific functions
		
		if inputWeapon == "M": #misisle
			FireBullet(enemyBoard, inputRow, inputCol, messageArray)
			if messageArray[0] == 0:
				outputMessage = outputMessage + "Miss!"
			elif messageArray[0] == 1:
				outputMessage = outputMessage + "Hit! "
			else:
				outputMessage = outputMessage + "Miss... that spot was already attacked."
		
		elif inputWeapon == "B": #bomb
			playerWeapons[0] = playerWeapons[0] - 1
			numHit = [0]
			FireBomb(enemyBoard, inputRow, inputCol, numHit)
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "
				
		elif inputWeapon == "C": #clusterbomb
			playerWeapons[1] = playerWeapons[1] - 1
			numHit = [0]
			FireClusterbomb(enemyBoard, inputRow, inputCol, numHit)
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "

		elif inputWeapon == "T": #torpedo
			playerWeapons[2] = playerWeapons[2] - 1
			numHit = [0]
			cls()
			DisplayBoard(enemyBoard, "Enemy")
			FireTorpedo(enemyBoard, inputRow, inputCol, numHit, inputDirection)
			cls()
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "					
		
		#hit messages selection! :D
		DestroyBrokenShips(enemyBoard, messageArray, enemyShips)
		if messageArray[1] == 1:
			outputMessage = outputMessage + "Carrier Destroyed! "		
		if messageArray[2] == 1:
			outputMessage = outputMessage + "Battleship Destroyed! "
		if messageArray[3] == 1:
			outputMessage = outputMessage + "Destroyer Destroyed! "
		if messageArray[4] == 1:
			outputMessage = outputMessage + "Submarine Destroyed! "			
		
		DisplayBoard(enemyBoard, "Enemy") #prints the enemy board so you can see the carnage
		print
		print outputMessage	#prints the hit message
		raw_input("Press ENTER to continue to the enemy's turn...")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: EnemyTurn(playerBoard, enemyBoard):
#
#   Pre: takes in playerBoard, the number of playerships and available enemy weapons
#
#   Post: based on random variables, selects a cord, and a random weapon to fire upon that cord location
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def EnemyTurn(playerBoard, playerShips, enemyWeapons):
		outputMessage = ""
		messageArray = [0 for x in range(5)]
		
		validInput = "false" #input valid var
		while (validInput == "false"): #variable dependend while loop start		
			if PartiallyDestroyedPieceCount(playerBoard) == 0: #if no player pieces are destroyed, then fire upon random coordinates
				inputRow = random.randint(0,9) #randomly generated values
				inputCol = random.randint(0,9)
			else: #if a enemy ship location is known, then fire upon the surrounding area
				inputCountFind = PartiallyDestroyedPieceCount(playerBoard)
				inputCoords = GetPartiallyDestroyedPiece(playerBoard, random.randint(1, inputCountFind))
				
				#var pool
				inputCoords
				inputRow = inputCoords[0]
				inputCol = inputCoords[1]
				directionToLook = "none"
				
				#for each ship cord, check if ship
				if (inputCol + 1 <= 9) and IsPartiallyBroken(playerBoard, inputRow, inputCol + 1) == "true":
					directionToLook = "horizontal"
				elif (inputCol - 1 >= 0) and IsPartiallyBroken(playerBoard, inputRow, inputCol - 1) == "true":
					directionToLook = "horizontal"
				elif (inputRow + 1 <= 9) and IsPartiallyBroken(playerBoard, inputRow + 1, inputCol) == "true":
					directionToLook = "vertical"
				elif (inputRow - 1 >= 0) and IsPartiallyBroken(playerBoard, inputRow - 1, inputCol) == "true":
					directionToLook = "vertical"					
				elif random.randint(0,1) == 0:
					directionToLook = "horizonal"
				else:
					directionToLook = "vertical"
					
				if directionToLook == "vertical":
					inputRow = inputRow + random.randint(-1,1)
				else:
					inputCol = inputCol + random.randint(-1,1)
			
				#two nested ifs, first range check then has the cord been fired upon before
			if (inputRow >= 0) and (inputRow <= 9) and (inputCol >= 0) and (inputCol <= 9):			
				if HasBeenFiredAt(playerBoard, inputRow, inputCol) == "false":

					inputWeapon = random.randint(0,19)
				#assigns a random weapon to be fired if available
					if inputWeapon == 0:
						if enemyWeapons[0] > 0:
							inputWeapon = "B" #bomb
							validInput = "true"

					elif inputWeapon == 1 or inputWeapon == 2:	
						if enemyWeapons[1] > 0:
							inputWeapon = "C" #clusterbomb
							validInput = "true"
							
					#direction of travel if weapon requires it
					elif inputWeapon == 3 or inputWeapon == 4 or inputWeapon == 5:	
						if enemyWeapons[2] > 0:
							inputWeapon = "T"
							inputDirection = random.randint(0,3)
							if inputDirection == 0:
								inputDirection = "U"
							elif inputDirection == 1:
								inputDirection = "D"
							elif inputDirection == 2:
								inputDirection = "L"
							else:
								inputDirection = "R"							
							validInput = "true"							
					else: #if none of the weapons is selected, use the defaut missile
						inputWeapon = "M"
						validInput = "true"
		
		
		cls()
		#message section of enemy player, all of these are responces to be sent into the arraymessage depending on the value parameter
		if inputWeapon == "M":
			FireBullet(playerBoard, inputRow, inputCol, messageArray)
			if messageArray[0] == 0:
				outputMessage = outputMessage + "Miss!"
			elif messageArray[0] == 1:
				outputMessage = outputMessage + "Hit! "
			else:
				outputMessage = outputMessage + "Miss... that spot was already attacked."
		
		elif inputWeapon == "B":
			enemyWeapons[0] = enemyWeapons[0] - 1
			numHit = [0]
			FireBomb(playerBoard, inputRow, inputCol, numHit)
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "
				
		elif inputWeapon == "C":
			enemyWeapons[1] = enemyWeapons[1] - 1
			numHit = [0]
			FireClusterbomb(playerBoard, inputRow, inputCol, numHit)
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "

		elif inputWeapon == "T":
			enemyWeapons[2] = enemyWeapons[2] - 1
			numHit = [0]
			FireTorpedo(playerBoard, inputRow, inputCol, numHit, inputDirection)
			if numHit[0] == 1:
				outputMessage = outputMessage + "1 hit! "
			else:
				outputMessage = outputMessage + str(numHit[0]) + " hits! "					
		
		DestroyBrokenShips(playerBoard, messageArray, playerShips)
		if messageArray[1] == 1:
			outputMessage = outputMessage + "Carrier Destroyed! "		
		if messageArray[2] == 1:
			outputMessage = outputMessage + "Battleship Destroyed! "
		if messageArray[3] == 1:
			outputMessage = outputMessage + "Destroyer Destroyed! "
		if messageArray[4] == 1:
			outputMessage = outputMessage + "Submarine Destroyed! "			
		
		DisplayBoard(playerBoard, "Player")
		print

		
		## AI PORTION SAVE TO STORAGE DICTIONARY ## 
		
		inputCol = str(inputCol) #convert to string
		
		if inputWeapon == "M":
			print "The enemy fired a basic missile on " + ConvertNumbToLet(inputRow) + "," + inputCol #prints message to player displaying the fired upon cords
		elif inputWeapon == "T": #weapon selection direction
			if inputDirection == "U":
				print "The enemy fired a torpedo on " + ConvertNumbToLet(inputRow) + "," + inputCol + " heading upwards"
			elif inputDirection == "D":
				print "The enemy fired a torpedo on " + ConvertNumbToLet(inputRow) + "," + inputCol + " heading downwards"
			elif inputDirection == "R":
				print "The enemy fired a torpedo on " + ConvertNumbToLet(inputRow) + "," + inputCol + " heading to the right"
			else:
				print "The enemy fired a torpedo on " + ConvertNumbToLet(inputRow) + "," + inputCol + " heading to the left"
		elif inputWeapon == "C":
			print "The enemy fired a clusterbomb on " + ConvertNumbToLet(inputRow) + "," + inputCol
		else:
			print "The enemy fired a bomb on " + ConvertNumbToLet(inputRow) + "," + inputCol
			
		print outputMessage	
		raw_input("Press ENTER to continue to the enemy's turn...")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: DestroyBrokenShips(board):
#
#   Pre: passed in a board(player or enemy) a message and the ship total
#
#   Post: for each ships corisponding map value, have a message, ship health and total number of pieces to check
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def DestroyBrokenShips(board, messageArray, ships):
	#var pool for broken ships
	brokenCarrierPieces = 0
	brokenBattleshipPieces = 0
	brokenDestroyerPieces = 0
	brokenSubmarinePieces = 0
	
	#board range check
	for row in range(10):
		for col in range(10): #checks for numeric broken ship value representations 
			if board[row][col] == "3":
				brokenCarrierPieces = brokenCarrierPieces + 1
			elif board[row][col] == "6":
				brokenBattleshipPieces = brokenBattleshipPieces + 1
			elif board[row][col] == "9":
				brokenDestroyerPieces = brokenDestroyerPieces + 1
			elif board[row][col] == "C":
				brokenSubmarinePieces = brokenSubmarinePieces + 1
	#all carrier broken pieces			
	if brokenCarrierPieces == 5:
		messageArray[1] = 1
		ships[0] = 0
		for row in range(10):
			for col in range(10):
				if board[row][col] == "3":
					board[row][col] = "4"
	# all battleship broken pieces				
	if brokenBattleshipPieces == 4:
		messageArray[2] = 1
		ships[1] = 0
		for row in range(10):
			for col in range(10):
				if board[row][col] == "6":
					board[row][col] = "7"
					
	#all destroyer broken pieces
	if brokenDestroyerPieces == 3:
		messageArray[3] = 1
		ships[2] = 0
		for row in range(10):
			for col in range(10):
				if board[row][col] == "9":
					board[row][col] = "A"

	# all broken submarine pieces				
	if brokenSubmarinePieces == 2:
		messageArray[4] = 1
		ships[3] = 0
		for row in range(10):
			for col in range(10):
				if board[row][col] == "C":
					board[row][col] = "D"
					
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: FireBullet(playerBoard, row, col):
#
#   Pre: accepts a board, row/col values and a message to display from the map
#
#   Post: checks the map piece, if the coorisponding map has a value other than blank, change it to its hit value
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def FireBullet(board, row, col, messageArray):
		# fires bullet at cords submited, previous data validation not required in function
		if board[row][col] == "0":
			board[row][col] = "1" #ship broken piece number
			messageArray[0] = 0 #display appropriate message coorisponding to the ship piece
		elif board[row][col] == "2": #repeat for each ship number value
			board[row][col] = "3"
			messageArray[0] = 1
		elif board[row][col] == "5":
			board[row][col] = "6"
			messageArray[0] = 1
		elif board[row][col] == "8":
			board[row][col] = "9"
			messageArray[0] = 1
		elif board[row][col] == "B":
			board[row][col] = "C"
			messageArray[0] = 1
		else:
			messageArray[0] = 2

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: FireBomb(board, row, col, numHit):
#
#   Pre: accepts a board, row/col and the number of hit results
#
#   Post: fires a bullet in the cords surrounding the cords choosen by the user, returns the number of hits in 
#         the area for the board
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def FireBomb(board, row, col, numHit):
		messageArray = [0]
		FireBullet(board, row, col, messageArray)
		if messageArray[0] == 1:
			numHit[0] = numHit[0] + 1
	
		#checks each row in a surrounding 3x3 box surrounding the center cord
		if (row - 1 >= 0) and (row - 1 <= 9) and (col >= 0) and (col <= 9):
			messageArray = [0]
			FireBullet(board, row - 1, col, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1
		#next cord over		
		if (row + 1 >= 0) and (row + 1 <= 9) and (col >= 0) and (col <= 9):
			messageArray = [0]
			FireBullet(board, row + 1, col, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over						
		if (row >= 0) and (row <= 9) and (col - 1 >= 0) and (col - 1 <= 9):
			messageArray = [0]
			FireBullet(board, row, col - 1, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over		
		if (row >= 0) and (row <= 9) and (col + 1 >= 0) and (col + 1 <= 9):
			messageArray = [0]
			FireBullet(board, row, col + 1, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over		
		if (row - 1 >= 0) and (row - 1 <= 9) and (col - 1 >= 0) and (col - 1 <= 9):
			messageArray = [0]
			FireBullet(board, row - 1, col - 1 , messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over		
		if (row - 1 >= 0) and (row - 1 <= 9) and (col + 1 >= 0) and (col + 1 <= 9):
			messageArray = [0]
			FireBullet(board, row - 1, col + 1, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over		
		if (row + 1 >= 0) and (row + 1 <= 9) and (col - 1 >= 0) and (col - 1 <= 9):
			messageArray = [0]
			FireBullet(board, row + 1, col - 1, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
		#next cord over		
		if (row + 1 >= 0) and (row + 1 <= 9) and (col + 1 >= 0) and (col + 1 <= 9):
			messageArray = [0]
			FireBullet(board, row + 1, col + 1, messageArray)
			if messageArray[0] == 1:
				numHit[0] = numHit[0] + 1	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: FireClusterbomb(board, row, col, numHit):
#
#   Pre: accepts a board, row/col and the number of hit results
#
#   Post: fires bullets in randomly choosen surrounding the cords choosen by the user, returns the number of  
#         hits in the area for the board
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def FireClusterbomb(board, row, col, numHit):
		messageArray = [0]
		FireBullet(board, row, col, messageArray)
		if messageArray[0] == 1:
			numHit[0] = numHit[0] + 1
		#range check 
		for x in range(4):
			randRow = random.randint(-3,3) #randomly assign cords to be hit for each bullet in the target area
			randCol = random.randint(-3,3)
			if (row + randRow >= 0) and (row + randRow <= 9) and (col + randCol >= 0) and (col + randCol <= 9):
				messageArray = [0]
				FireBullet(board, row + randRow, col + randCol, messageArray)
				if messageArray[0] == 1:
					numHit[0] = numHit[0] + 1
					
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: FireTorpedo(board, row, col, numHit):
#
#   Pre: takes in a board & row/col and the number of ships hit during the run
#
#   Post: checks for ships in a 4 unit line, records the total number of hits the torpedo results in
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def FireTorpedo(board, row, col, numHit, direction):
		if direction == "U": #depending on direction of fire
			for x in range(4): #check each cord in 4 direction space
				if (row - x >= 0) and (row - x <= 9) and (col >= 0) and (col <= 9): 
					messageArray = [0]
					FireBullet(board, row - x, col, messageArray) # fire an individual bullet at the piece
					if messageArray[0] == 1: #select message array if hit
						numHit[0] = numHit[0] + 1 # update the hit counter
		# repeat for each direction below
		elif direction == "D":
			for x in range(4):
				if (row + x >= 0) and (row + x <= 9) and (col >= 0) and (col <= 9):
					messageArray = [0]
					FireBullet(board, row + x, col, messageArray)
					if messageArray[0] == 1:
						numHit[0] = numHit[0] + 1	

		elif direction == "L":
			for x in range(4):
				if (row >= 0) and (row <= 9) and (col - x >= 0) and (col - x <= 9):
					messageArray = [0]
					FireBullet(board, row, col - x, messageArray)
					if messageArray[0] == 1:
						numHit[0] = numHit[0] + 1	

		elif direction == "R":
			for x in range(4):
				if (row >= 0) and (row <= 9) and (col + x >= 0) and (col + x <= 9):
					messageArray = [0]
					FireBullet(board, row, col + x, messageArray)
					if messageArray[0] == 1:
						numHit[0] = numHit[0] + 1							

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: HasBeenFiredAt(board, row, col):
#
#   Pre: takes in a board & row/col
#
#   Post: checks to see if the cord has been fired upon yet
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def HasBeenFiredAt(board, row, col):
	if (board[row][col] == "0") or (board[row][col] == "2") or (board[row][col] == "5") or (board[row][col] == "8") or (board[row][col] == "B"):
		return "false" #if the board cord has a ship fired upon value or destroyed value, then return false, otherwise return true
	else:
		return "true"
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: ConvertNumbToLet(BaseNumb):
#
#   Pre: accepts a number ranging 0-9
#
#   Post: returns the coorisponding A-J letter value from the parameter int
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		

def ConvertNumbToLet(baseNumb):
	if baseNumb == 0: #numberic integer	
		return "A" #alphebet representation to be returned
	elif baseNumb == 1:
		return "B"
	elif baseNumb == 2:
		return "C"
	elif baseNumb == 3:
		return "D"
	elif baseNumb == 4:
		return "E"
	elif baseNumb == 5:
		return "F"
	elif baseNumb == 6:
		return "G"
	elif baseNumb == 7:
		return "H"
	elif baseNumb == 8:
		return "I"
	elif baseNumb == 9:
		return "J"
	else:
		return -1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: PartiallyDestroyedPieceCount(board):
#
#   Pre: requires board (player or enemy) as parameters
#
#   Post: checks each baord pos for destroyed ships, returns the total count upon completion of for statements
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def PartiallyDestroyedPieceCount(board):
	partiallyDestroyedPieces = 0
	for row in range(10): #range for the entire board 
		for col in range(10): #range for the entire board
			if IsPartiallyBroken(board, row, col) == "true": # if there is a partially broken ship there
				partiallyDestroyedPieces = partiallyDestroyedPieces + 1 #add one to the total count of pieces
	return partiallyDestroyedPieces #upon completion of the entire board, return the total broken pieces value
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: GetPartiallyDestroyedPiece(board, count):
#
#   Pre: requires the board and a count of the number of ships found (ie hit marks)
#
#   Post: allows the AI to distinquish between destroyed and partially destroyed ships, only firing upon the 
#         partially destroyed ones 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def GetPartiallyDestroyedPiece(board, inputCountFind):
	countSearch = 0
	outputPos = [0,0]
	for row in range(10):
		for col in range(10):
			if IsPartiallyBroken(board, row, col) == "true":
				countSearch = countSearch + 1
				if countSearch == inputCountFind:
					outputPos = [row, col]
					return outputPos
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Function: IsPraticiallyBroken(board, row, col):
#
#   Pre: requires board, (either player or enemy) and cords to check for ship
#
#   Post: checks the condition of the ship piece in the cord if any is selected 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
def IsPartiallyBroken(board, row, col):
		if (board[row][col] == "3") or (board[row][col] == "6") or (board[row][col] == "9") or (board[row][col] == "C"):
			return "true"
		else:
			return "false"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Call to run the main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__=='__main__':
		random.seed(time.time())
		cls()
		main()
		cls()