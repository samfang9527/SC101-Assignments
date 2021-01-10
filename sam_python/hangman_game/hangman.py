"""
File: hangman.py
-------------------------------
This file demonstrates a Python Console hangman game.
At the beginning of the game, users are asked to input
one letter at a time to guess out a dashed vocabulary (answer).
If the letter is in the answer, the Console updates the
dashed word to its current status. 7 wrong guesses end the game.
"""

import random

# Constant
N_TURNS = 7


def main():
    """
    TODO:
    """
    w = random_word()
    life = N_TURNS
    print("The word looks like: "+"_"*len(w))
    print("You have "+str(N_TURNS)+" guesses left.")
    rf = "_"*len(w)
    rfs = ""
    n = str.upper(input())
    while life > 0:
        if len(n) != 1 or not n.isalpha():
            print("You idiot, type something else")
            n = str.upper(input())
        else:
            if n in w:
                for i in range(len(w)):
                    if w[i] == n:
                        rfs += w[i]
                    else:
                        rfs += rf[i]
                print(rfs)
                print("You have " + str(life) + " guesses left.")
                rf = rfs
                rfs = ""
                if rf.isalpha():
                    print("YMCA")
                n = str.upper(input())
            else:
                life -= 1
                if life > 0:
                    print("ohho")
                    print("You have " + str(life) + " guesses left.")
                    n = str.upper(input())
                else:
                    print("You are completely hung :(")
    print("You suck!")


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"

#####  DO NOT EDIT THE CODE BELOW THIS LINE  #####

if __name__ == '__main__':
    main()
