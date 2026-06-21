import random

randomnum=random.randint(1,10)
while True:
 myguess=int(input("Enter your guess\t"))

 if myguess < randomnum:
    print("Your prediction value is lower than the random number")
 elif myguess > randomnum:
    print("Your prediction value is greater than the random number")
 else:
    print("You guessed the number")
    break

