import random

def game():
    print("Hello! What is your name?")
    name=input()
    
    print(f"\nWell, {name} , I am thinking of a number between 1 and 20.")
    number=random.randint(1,20)
    guesses=0
    
    while True:
        print("Take a guess.")
        guess=int(input())
        
        if guess < 1 or guess > 20:
            print("Please enter a number between 1 and 20!")
            continue
        
        guesses+=1
        
        if number > 20:
            print("error")
        elif guess < number:
            print("Your guess is too low.")
        elif guess > number:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses} guesses!")
            break

game()