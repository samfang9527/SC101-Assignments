"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop
word_list = []


def main():
    read_dictionary()
    print(f'Welcome to stanCode "Anagram Generator" (or {EXIT} to quit)')
    while True:
        enter = str(input('Find anagrams for: '))
        if enter == EXIT:
            break
        else:
            print('Searching...')
            find_anagrams(enter)


def read_dictionary():
    global word_list
    with open(FILE, 'r') as f:
        for line in f:
            word_list.append(line.strip('\n'))


def find_anagrams(s):
    """
    :param s: string input by user
    :return: volume and value of all anagrams
    """
    anagram_lst = []
    helper(s, anagram_lst, '')
    print(f'{len(anagram_lst)} anagrams: {anagram_lst}')


def helper(s, anagram_lst, cur_s):
    if len(s) == len(cur_s):
        if cur_s in word_list:
            if cur_s not in anagram_lst:
                anagram_lst.append(cur_s)
                print(f'Found: {cur_s}')
                print('Searching...')
    else:
        for ele in s:
            if s.count(ele) > cur_s.count(ele):
                cur_s += ele
                if has_prefix(cur_s) is True:
                    helper(s, anagram_lst, cur_s)
                    cur_s = cur_s[:-1]
                else:
                    cur_s = cur_s[:-1]


def has_prefix(sub_s):
    """
    :param sub_s: strings
    :return: bool
    """
    global word_list
    for word in word_list:
        if word.startswith(sub_s) is True:
            return True
        else:
            pass


if __name__ == '__main__':
    main()
