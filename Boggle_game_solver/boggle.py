"""
File: boggle.py
Name: Sam Fang
This is a boggle game solver that can quickly find all answer of a random boggle board.
----------------------------------------
"""

import time


# CONSTANT
FILE = 'dictionary.txt'		# This is the dictionary txt file, we will be checking if a word exists by searching through it
BOARD_SIZE = 4				# Determine how large is your boggle board, default size is 4x4
EXIT = '-1'					# Type '-1' to stop input and end this program


class TrieNode:

	def __init__(self):
		self.d = {}
		self.end = False


def main():
	print(f"Welcome to Sam's boggle game solver")
	print(f'Please input a boggle board to start or -1 to stop input and leave the game')
	while True:
		board, uni = input_ch()				# input
		if not board:
			break
		start = time.time()
		root = read_dictionary(uni)			# load file and create tree
		boggle_game_solver(board, root)		# searching
		end = time.time()
		print('----------------------------------')
		print(f'The speed of your boggle algorithm: {end - start} seconds.')


def input_ch():
	"""
	returns:
		board (list): A list stored the alphabets of each rows.
		uni (list): A list stored all the distinct alphabet of the input board.
	"""
	while True:
		board = []
		uni = []
		wrong_format = False

		# input words
		for i in range(BOARD_SIZE):
			row = str(input(f'{i + 1} row of letters: ')).lower()
			if row == EXIT:
				print(f'Goodbye, hope to see you soon!')
				return None
			row_lst = row.strip().split()

			# check the input format
			def check():
				if len(row_lst) != BOARD_SIZE:
					return False
				for ele in row_lst:
					if len(ele) != 1 or not ele.isalpha():
						return False
				return True

			if not check():
				print(f'Illegal input, please input {BOARD_SIZE} characters in each row')
				wrong_format = True
				break

			board.append(row_lst)
			for ch in row_lst:
				if ch not in uni:
					uni.append(ch)

		if not wrong_format:
			return board, uni


def insert(root, word):
	"""
	A function that can insert words to the Trie
	param root (TrieNode): Root of the Tire that stored possible words.
	param word (str): The word insert to the Trie.
	"""
	for ch in word:
		if ch not in root.d:
			root.d[ch] = TrieNode()
		root = root.d[ch]
	root.end = True


def prefix_and_search(root, word):
	"""
	A function that can check if the input word is in the Trie and still have further possibility.
	param root (TrieNode): root of the Tire that stored possible words.
	param word (str): the word to check.
	"""
	for ch in word:
		if ch not in root.d:
			return False
		root = root.d[ch]
	return word if root.end else True


def read_dictionary(uni):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	param uni (list): A list stored all the distinct alphabet of the recent boggle board.
	"""
	root = TrieNode()
	with open(FILE, 'r') as f:
		for line in f:
			word = line.strip()

			def check():
				for ch in word:
					if ch not in uni:
						return False
				return True

			if len(word) >= 4 and check():
				insert(root, word)
	return root


def boggle_game_solver(board, root):
	"""
	param board (list): A list stored the alphabets of each rows.
	param root (TrieNode): Root of the Tire that stored possible words.
	"""
	word_found = []
	for i in range(BOARD_SIZE):
		for j in range(BOARD_SIZE):
			start = (i, j)
			path = [(i, j)]
			ch = board[i][j]
			boggle_game_solver_helper(board, root, start, ch, path, word_found)
	print(f'{len(word_found)} words found')


def boggle_game_solver_helper(board, root, index, cur_s, path, word_found):
	"""
	param board (list): A list stored the alphabets of each rows.
	param root (TrieNode): Root of the Tire that stored possible words.
	param index (tuple): A tuple (row, col) stored the current position on the board.
	param cur_s (str): Possible words to check.
	param path (list): To remember the position that already used.
	param word_found (list): To remember the words found.
	"""
	x, y = index
	for i in range(-1, 2):
		for j in range(-1, 2):
			new_index = (x+i, y+j)
			if new_index not in path and 0 <= new_index[0] < BOARD_SIZE and 0 <= new_index[1] < BOARD_SIZE:
				cur_s += board[new_index[0]][new_index[1]]
				path.append(new_index)
				prefix_or_find = prefix_and_search(root, cur_s)
				if prefix_or_find:
					if prefix_or_find == cur_s and prefix_or_find not in word_found:
						word_found.append(cur_s)
						print(f'Found: {cur_s}')
					boggle_game_solver_helper(board, root, new_index, cur_s, path, word_found)
				cur_s = cur_s[:-1]
				path.pop()


if __name__ == '__main__':
	main()
