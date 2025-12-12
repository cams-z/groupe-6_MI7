from random import randint

def initialise_sequence():
    return [randint(0,3)]

def add_to_sequence(s):
    s.append(randint(0,3))
    return s

def game_round(s):
    print(s)
    for e in s:
        sequence_input = int(input())
        if sequence_input != e:
            return False
    return True

def game():
    s = initialise_sequence()
    while game_round(s):

        s = add_to_sequence(s)
    return "perdu"

print(game())