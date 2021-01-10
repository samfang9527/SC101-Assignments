"""
File: boggle.py
Name:
----------------------------------------
TODO:
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
database = []
input_data = []


def main():
	"""
	TODO: input 16 alphabet and find all possible words
	"""
	read_dictionary()
	for i in range(4):
		j = str(input(f'{i+1} row of letters: '))
		strip_j = j.strip().split(' ')
		if test_input(strip_j) is False:
			break
		input_data.append(strip_j)
	searching_words(input_data)


def searching_words(lst):
	"""
	:param lst: The list of input_data
	:return: print all words founded and the total numbers
	"""
	global database
	word_lst = []
	# search the database and run the word with 4 or more alphabet
	for word in database:
		if len(word) >= 4:
			target = 0
			# i is the index of the rows and j is the index of alphabet in the row
			for i in range(len(lst)):
				for j in range(len(lst[i])):
					if word[target] == lst[i][j]:
						helper(lst, word, target+1, i, j, word_lst, '', [], [])
	print(f'There are {len(word_lst)} words in total.')


def helper(lst, target_word, target, row, ele_in_row, word_lst, cur_s, point, cur_lst):
	"""
	:param lst: the list of input data
	:param target_word: the look up word
	:param target: the look up alphabet
	:param row: row index in the lst
	:param ele_in_row: ele index in the row
	:param word_lst: word founded
	:param cur_s: current string to check if it's base case
	:param point: record the coordinate used
	:param cur_lst: record the row index and the ele index of the alphabet surround
	:return: print word founded
	"""
	cur_s += lst[row][ele_in_row]
	point.append((row, ele_in_row))
	if len(cur_s) == len(target_word):
		if cur_s not in word_lst:
			word_lst.append(cur_s)
			print(f'Found: "{cur_s}"')
	else:
		if target < len(target_word):
			for i in range(row-1, row+2):
				for j in range(ele_in_row-1, ele_in_row+2):
					if 4 > i >= 0 and 4 > j >= 0:
						if (i, j) in point:
							pass
						else:
							cur_lst.append((i, j))
			for ele in cur_lst:
				if lst[ele[0]][ele[1]] == target_word[target]:
					cur_lst = []
					helper(lst, target_word, target+1, ele[0], ele[1], word_lst, cur_s, point, cur_lst)
					point.pop()


def test_input(lst_tested):
	"""
	:param lst_tested: list
	:return: bool
	"""
	if len(lst_tested) == 4:
		for ele in lst_tested:
			ele_isalpha = ele.isalpha()
			ele_len = len(ele)
			if ele_isalpha is False or ele_len != 1:
				print('Illegal input')
				return False
		return True
	else:
		print('Illegal input')
		return False


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	global database
	with open(FILE, 'r') as f:
		for line in f:
			database.append(line.strip('\n'))


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	pass


if __name__ == '__main__':
	main()
