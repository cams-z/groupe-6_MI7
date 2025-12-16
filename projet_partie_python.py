from grove.gpio import GPIO
from grove.grove_button import GroveButton

from random import randint
from time import sleep
from time import time as current_time

import RPi.GPIO as GPIO2
GPIO2.setmode(GPIO2.BCM)


class GroveChainableLED: #code fournit par le prof pour les chainable LED
    def __init__(self, pin, num_leds):
        self.pin_clk = GPIO(pin, GPIO.OUT)
        self.pin_data = GPIO(pin+1 , GPIO.OUT)
        self.num_leds = num_leds
        self.reset()

    def __setitem__(self, index, val):
        offset = index * 3
        for i in range(3):
            self.buf[offset + i] = val[i]

    def __getitem__(self, index):
        offset = index * 3
        return tuple(self.buf[offset + i] for i in range(3))

    def fill(self, color):
        for i in range(self.num_leds):
            self[i] = color

    def reset(self):
        self.buf = bytearray(self.num_leds * 3)
        # Begin data frame 4 bytes
        self._frame()
        # 4 bytes for each led (checksum, blue, green, red)
        for i in range(self.num_leds):
            self._write_byte(0xC0)
            for i in range(3):
                self._write_byte(0)
        # End data frame 4 bytes
        self._frame()

    def write(self):
        # Begin data frame 4 bytes
        self._frame()

        # 4 bytes for each led (checksum, blue, green, red)
        for i in range(self.num_leds):
            self._write_color(self.buf[i * 3], self.buf[i * 3 + 1], self.buf[i * 3 + 2])

        # End data frame 4 bytes
        self._frame()

    def _frame(self):
        # Send 32x zeros
        self.pin_data.write(0)
        for i in range(32):
            self._clk()

    def _clk(self):
        self.pin_clk.write(0)
        #sleep(0.01) # works without it
        self.pin_clk.write(1)
        #sleep(0.01) # works without it


    def _write_byte(self, b):
        if b == 0:
            # Fast send 8x zeros
            self.pin_data.write(0)
            for i in range(8):
                self._clk()
        else:
            # Send each bit, MSB first
            for i in range(8):
                if ((b & 0x80) != 0):
                    self.pin_data.write(1)
                else:
                    self.pin_data.write(0)
                self._clk()

                # On to the next bit
                b <<= 1

    def _write_color(self, r, g, b):
        # Send a checksum byte with the format "1 1 ~B7 ~B6 ~G7 ~G6 ~R7 ~R6"
        # The checksum colour bits should bitwise NOT the data colour bits
        checksum = 0xC0 # 0b11000000
        checksum |= (b >> 6 & 3) << 4
        checksum |= (g >> 6 & 3) << 2
        checksum |= (r >> 6 & 3)

        self._write_byte(checksum)

        # Send the 3 colours
        self._write_byte(b)
        self._write_byte(g)
        self._write_byte(r)



#setup des boutons et des LEDS
chain = GroveChainableLED(pin=16, num_leds=4)
GPIO2.setup(22, GPIO2.IN)
GPIO2.setup(24, GPIO2.IN)
GPIO2.setup(26, GPIO2.IN)
GPIO2.setup(18, GPIO2.IN)
buttons2 = {0:  22, 1: 24, 2: 26, 3: 18} #on associ chaque couleur a un bouton

"""
GPIO2.setup(5, GPIO2.OUT)
buzz = GPIO2.PWM(5, 1047)


chords = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
    # Play sound (DO, RE, MI, etc.), pausing for 0.5 seconds between notes
for fr in chords:
    buzz.ChangeFrequency(fr)
    buzz.start(50)
    sleep(1)
    buzz.stop()
    """


def light_up_LED(index): #fonction qui allume la "index"-ieme LED pendant 1 seconde
    if index == 0:
        chain[0] = (100,44, 221)
        chain.write()
        sleep(0.5)

    if index == 1:
        chain[1] = (232, 150, 46)
        chain.write()
        sleep(0.5)

    if index == 2:
        chain[2] = (250, 75, 70)
        chain.write()
        sleep(0.5)

    if index == 3:
        chain[3] = (50, 75, 150)
        chain.write()
        sleep(0.5)
        
    chain.reset()



def GAME_OVER(): #fonction qui allume tout les LEDs en rouge pour annoncer le Game Over
    chain[0] = (250, 000, 000)
    chain[1] = (250, 000, 000)
    chain[2] = (250, 000, 000)
    chain[3] = (250, 000, 000)
    chain.write()
    sleep(1)
    chain.reset()


def initialise_sequence(): 
    return [randint(0,3)]

def add_to_sequence(s):
    s.append(randint(0,3))
    return s

def game_round(s):
    for e1 in s:
        light_up_LED(e1)
        sleep(0.2)
        print(e1)
        #a voir si on ajoute du son ou non
        

    reussite = True
    for e2 in s: #a tester
        
        buttons = {0:  22, 1: 24, 2: 26, 3: 18} 
        buttons.pop(e2)
        start = current_time() 
        while reussite:
            if GPIO2.input(buttons2[e2]):
                # si on appuie sur le bon bouton, on laisse reussite sur True
                light_up_LED(e2)
                break
            
            
            for b in buttons:
                if GPIO2.input(buttons[b]) or current_time() - start >= 7:
                    reussite = False
                    break

    return reussite


def game():
    chain.reset()
    score = 0
    s = initialise_sequence()
    while game_round(s):
        s = add_to_sequence(s)
        print(s)
        score += 50
        sleep(2)
    GAME_OVER()
    return "perdu, score final : " + str(score)


print(game())

