#!/usr/bin/env python3
from random import choice, randint

class Hangman():

    WORDFILE = "words.txt"
    ALPHA = "abcdefghijklmnopqrstuvwxyz"
    with open(WORDFILE, "r") as file:
        WORDS = file.read().split("\n")[:-1]

    def __init__(self):
        self.reset()

    def reset(self):
        self.state  = 0
        self.guess  = None
        self.word   = None
        self.length = None
        self.said   = []
        self._guesswords = None
        self._chosewords = None

    def wordset(self, word = "aardvark", verify = True):
        word = word.lower()
        if verify:
            if word not in self.WORDS: return False
        self.state  = 1
        self.word   = word
        self.length = len(self.word)
        self.guess  = "_" * self.length
        self._guesswords = tuple(filter(lambda w: len(w) == self.length, self.WORDS))

    def wordbot(self, l = None):
        if self.state != 0: return False
        if l == None:
            l = randint(3, 31)
        elif type(l) != int: return False
        elif l < 3 or l > 31: return False
        self.state  = 1
        self.length = l
        self.guess  = "_" * self.length
        self._guesswords = tuple(filter(lambda w: len(w) == self.length, self.WORDS))
        self._chosewords = tuple(self._guesswords)

    def wordrandom(self):
        if self.state != 0: return False
        self.wordset(choice(self.WORDS), verify = False)

    def letterguess(self, l = "a"):
        if self.state != 1: return False
        l = l.lower()
        if l not in self.ALPHA: return None
        if l in self.said:      return None
        self.said.append(l)
        if self._chosewords != None: # Wordbot
            if len(self._chosewords) > 50: 
                self.word = self.guess
            else:
                if all(l in i for i in self._chosewords): # you must give in
                    maxn = 0
                else:
                    maxn = len(self._chosewords)
                self.word = self.guess
                for i in self._chosewords:
                    tempguess = list(self.guess)
                    for m, j in enumerate(i):
                        if m == l:
                            tempguess[m] = l
                    tempguess = sum(1 for w in self._chosewords if all(tempguess[m] == "_" or j == tempguess[m] for m, j in enumerate(w)))
                    if tempguess > maxn:
                        maxn = tempguess
                        self.word = i
        self.guess = list(self.guess)
        f = False
        for i, m in enumerate(self.word):
            if m == l:
                self.guess[i] = l
                f = True
        self.guess = "".join(self.guess)
        self._guesswords = tuple(filter(lambda w: all(self.guess[m] == "_" or j == self.guess[m] for m, j in enumerate(w)), self._guesswords))
        if self._chosewords != None: # Wordbot
            if f == False:
                self._chosewords = tuple(filter(lambda w: l not in w, self._chosewords))
            else:
                self._chosewords = tuple(filter(lambda w: (l in w) and all(self.guess[m] == "_" or j == self.guess[m] for m, j in enumerate(w)), self._chosewords))
        if "_" not in self.guess:
            self.state = 2
            return True
        return f

    def letterbot(self):
        if self.state != 1: return False
        if len(self._guesswords) == 0:
            return None
        elif len(self._guesswords) == 1:
            for i in self.ALPHA:
                if i in self.said:               continue
                if i in self.guess:              continue
                if i not in self._guesswords[0]: continue
                return i
            return None # IDK What the word is
        else:
            minl = None
            minn = 0
            for i in self.ALPHA:
                if i in self.said:  continue
                if i in self.guess: continue
                tempmatch = 0
                for m in self._guesswords:
                    if (i in m) and all(self.guess[j] == "_" or k == self.guess[j] for j, k in enumerate(m)):
                        tempmatch += 1
                if (tempmatch != 0 and tempmatch > minn):
                    minl = i
                    minn = tempmatch
            return minl
    
h = Hangman()
h.wordbot(int(input("Word len:\n >>> ")))
lives = 1
while h.state != 2:
    l = h.letterbot()
    if h.letterguess(l) == False:
        lives += 1
    print(lives, l, h.guess, len(h._guesswords) - len(h._chosewords))
