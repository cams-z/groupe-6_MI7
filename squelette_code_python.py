from random import randint
import time

def initialise_sequence():
    return [randint(0,3)]

def add_to_sequence(s):
    s.append(randint(0,3))
    return s

def game_round(s):
    print("-------------------")
    for e1 in s:
        print(e1)
        time.sleep(1)
    print("à vous de jouer")
    for e2 in s:
        sequence_input = int(input())
        if sequence_input != e2:
            return False
    return True

def game():
    score = 0
    s = initialise_sequence()
    while game_round(s):
        s = add_to_sequence(s)
        score += 50
    return "perdu, score final : " + str(score)

print(game())
