#! /usr/bin/env python

import sys
import math
import random

# X_PLYR - X - Player 1 - MAX
# O_PLYR - O - Player 2 - MIN

O_PLYR = "O"
X_PLYR = "X"
N_PLYR = "."

PLAYER_ID = { X_PLYR: 1, O_PLYR: 2 }

def get_human_move(board, player):
	""" Asks the human player to make the next move """

	move = -1
	legal_moves = actions(board)

	# Prompt for a move until the player enters a valid one
	while True:
		print "enter move for player " + str(PLAYER_ID[player]) + ":",
		try:
			move = int(raw_input()) - 1
			if move in range(0, 9):
				if move in legal_moves:
					break
				else:
					print "illegal move!"
			else:
				print "must enter a value in the range [1, 9]!"
		except ValueError:
			print "couldn't understand input!"
		except KeyboardInterrupt:
			sys.exit(1)

	# Add the player's token to the board
	board[move] = player

def get_agent_move(board, player):
	""" Asks the AI to determine the next move """
	moves = {}
	if player == X_PLYR:
		best = max_value(board, float("-inf"), float("inf"), moves)
	else:
		best = min_value(board, float("-inf"), float("inf"), moves)

	best_moves = [m for m in moves.keys() if moves[m] == best]
	#print best
	#print moves
	#print best_moves
	move = best_moves[0]
	print "enter move for player " + str(PLAYER_ID[player]) + ": " + str(move + 1)
	board[move] = player


def max_value(board, alpha, beta, moves):
	""" Returns the minimax value for a given max node """
	util = utility(board)
	if util is not None:
		return util

	val = float("-inf")
	for a in actions(board):
		next = min_value(place_token(board, a, X_PLYR), alpha, beta, None)
		if isinstance(moves, dict):
			moves[a] = next

		val = max(val, next)
	#	if val >= beta:
	#		return val
		alpha = max(alpha, val)
	return val

def min_value(board, alpha, beta, moves):
	""" Returns the minimax value for a given min node """
	util = utility(board)
	if util is not None:
		return util

	val = float("inf")
	for a in actions(board):
		next = max_value(place_token(board, a, O_PLYR), alpha, beta, None)
		if isinstance(moves, dict):
			moves[a] = next

		val = min(val, next)
	#	if val <= alpha:
	#		return val
		beta = min(beta, val)
	return val

def place_token(board, move, player):
	""" Returns a copy of the board with an additional token placed """
	board_cpy = board[:]
	board_cpy[move] = player
	return board_cpy

def actions(board):
	""" Returns a list of all open board positions """
	return [i for i in xrange(0, 9) if board[i] == N_PLYR];

def winner(board):
	""" Returns O_PLYR, X_PLYR, or N_PLYR """
	win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
	(0, 3, 6), (1, 4, 7), (2, 5, 8), 
	(0, 4, 8), (2, 4, 6)]

	x_win = X_PLYR * 3    # 'xxx'
	o_win = O_PLYR * 3    # 'ooo'

	for combo in win_combos:
		seq = board[combo[0]] + board[combo[1]] + board[combo[2]]
		if seq == x_win:
			return X_PLYR
		elif seq == o_win:
			return O_PLYR 

	return N_PLYR

def utility(board):
	""" Returns +1 if X wins, -1 if O wins and 0 for a tie
	Returns None if game is not over. 
	Serves as a utility function and a terminal-test. """

	w = winner(board)
	if w == X_PLYR:
		return 1
	elif w == O_PLYR:
		return -1
	elif not actions(board):
		return 0

	return None
	
def print_board(board):
	""" Prints the board to stdout """
	for y in xrange(0, 3): 
		for x in xrange(0, 3):
			print board[y * 3 + x],
		print

def main():
	""" Entry point for the application """
	# Create a blank board, initialize game state
	board = [N_PLYR] * 9
	moves = 1 
	is_human = {X_PLYR: True, O_PLYR: False}
	next_player = {X_PLYR: O_PLYR, O_PLYR: X_PLYR}
	current_player = X_PLYR

	# Start gameplay
	board_util = None
	while board_util == None:
		print_board(board)
		print "Move " + str(moves) + ": "
		if is_human[current_player]:
			get_human_move(board, current_player)
		else:
			get_agent_move(board, current_player)
		moves += 1
		board_util = utility(board)
		current_player = next_player[current_player]

	print_board(board)
	# Game's over, who won?
	print ["Player 2 has won.", "The game is a tie.", "Player 1 has won."][board_util + 1]
	return
		

if __name__ == "__main__":
	main()
