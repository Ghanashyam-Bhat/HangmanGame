from time import sleep
from tcp_client import client
domain = input("Enter the domain name: ").lower()
def hangman(word):
    wrong = 0
    stages =["",
            "________      ", 
            "|      |      ", 
            "|      0      ", 
            "|     /|\     ", 
            "|     / \     ", 
            "|"]
    word = word.lower()
    temp = list("-"*len(word))
    to_be = list(word)
    g = ' '
    while g  in to_be:
        i = to_be.index(g)
        temp[i] = g
        to_be[i] = '*'
    while to_be.count('*')!=len(word) and wrong!=7:
        print("".join(temp))
        g = input("Guess a letter: ").lower()
        if g=='quit':
            break
        elif len(g)>1:
            print("You can guess only 1 word at a time")
        elif g in temp:
            print("Word already guessed")
        elif g in to_be:
            print("Right Guess")
            while g  in to_be:
                i = to_be.index(g)
                temp[i] = g
                to_be[i] = '*'
        else:
            print("Wrong Guess")
            wrong+=1
            print("\n".join(stages[:wrong+1]))
            print(f"{7-wrong} wrong guesses allowed")
    if to_be.count('*')==len(word):
        print("".join(temp))
        print("You won")
        return 1
    elif wrong==7:
        print("You Lost")
        print(f"The word was : {word}")
        return 0
    if g=='quit':
        print("You have quit the game")
        return 0

def feed():
    try:
        fd = open(f"{domain}.txt","r")
    except:
        client(domain)
        sleep(1)
        fd = open(f"{domain}.txt","r")
    repo = list()
    rd = fd.readlines()
    for i in range(len(rd)):
        repo.append(rd[i][:(len(rd[i])-1)])
    import random
    i = random.randint(0,len(repo))
    #print(repo)
    hangman(repo[i])
    fd.close()

feed()