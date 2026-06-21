# Task - 3
#
# 1. Guess the Number:
print("1. Guess the Number:\n")

import random

randomnum=random.randint(1,10)
while True:
 myguess=int(input("Enter your guess\t"))

 if myguess < randomnum:
    print("Your prediction value is lower than the random number")
 elif myguess > randomnum:
    print("Your prediction value is greater than the random number")
 else:
    print("You guessed the number\n")
    break

# -----------------------------------------------------
# 2. Word Scramble:
print("2. Word Scramble:\n")

from random import shuffle

words = ['python', 'javascript', 'guvi', 'java', 'automation', 'pytest', 'selenium']
print("Available words:", words)

# Ask user to pick a word
phrase = input("Enter the word from the given list to scramble: ")

# Convert to list of characters
scrambled_list = list(phrase)

# Shuffle the list in place
shuffle(scrambled_list)

# Join back into a string
scrambled_word = ''.join(scrambled_list)

print("Scrambled word:", scrambled_word)


#sort the input phrase from user and compare with the sorted words in the list

sorted_phrase = sorted(scrambled_word)
#print("sorted_phrase is ",sorted_phrase)

match=False
for i in words:
    # sort the word in the list and compare with the sorted input phrase

    if sorted(i) == sorted_phrase:
        print("The unscrambled word is:", i)
        match=True
        break

# when not matched
if sorted(i) != sorted_phrase:
    print("Entered word not exist in the given list.")




