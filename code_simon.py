from grove.gpio import GPIO
from grove.grove_button import GroveButton
from random import randint
from time import sleep, time as current_time
import RPi.GPIO as GPIO2

GPIO2.setmode(GPIO2.BCM)

# variable partager avec flask
current_score = 0
game_status = "En attente"


class GroveChainableLED:
    def __init__(self, pin, num_leds):
        self.pin_clk = GPIO(pin, GPIO.OUT)
        self.pin_data = GPIO(pin+1 , GPIO.OUT)
        self.num_leds = num_leds
        self.reset()

    def __setitem__(self, index, val):
        offset = index * 3
        for i in range(3):
            self.buf[offset + i] = val[i]

    def fill(self, color):
        for i in range(self.num_leds):
            self[i] = color

    def reset(self):
        self.buf = bytearray(self.num_leds * 3)
        self._frame()
        for i in range(self.num_leds):
            self._write_byte(0xC0)
            for i in range(3):
                self._write_byte(0)
        self._frame()

    def write(self):
        self._frame()
        for i in range(self.num_leds):
            self._write_color(self.buf[i * 3], self.buf[i * 3 + 1], self.buf[i * 3 + 2])
        self._frame()

    def _frame(self):
        self.pin_data.write(0)
        for _ in range(32):
            self._clk()

    def _clk(self):
        self.pin_clk.write(0)
        self.pin_clk.write(1)

    def _write_byte(self, b):
        for i in range(8):
            self.pin_data.write((b & 0x80) != 0)
            self._clk()
            b <<= 1

    def _write_color(self, r, g, b):
        checksum = 0xC0
        checksum |= (b >> 6 & 3) << 4
        checksum |= (g >> 6 & 3) << 2
        checksum |= (r >> 6 & 3)
        self._write_byte(checksum)
        self._write_byte(b)
        self._write_byte(g)
        self._write_byte(r)



chain = GroveChainableLED(pin=16, num_leds=4)
buttons2 = {0: 22, 1: 24, 2: 26, 3: 18}

for pin in buttons2.values():
    GPIO2.setup(pin, GPIO2.IN)


def light_up_LED(index):
    colors = [
        (100, 44, 221),
        (232, 150, 46),
        (250, 75, 70),
        (50, 75, 150)
    ]
    chain[index] = colors[index]
    chain.write()
    sleep(0.5)
    chain.reset()


def GAME_OVER():
    chain.fill((250, 0, 0))
    chain.write()
    sleep(1)
    chain.reset()


def initialise_sequence():
    return [randint(0,3)]


def add_to_sequence(s):
    s.append(randint(0,3))
    return s


def game_round(s):
    for e in s:
        light_up_LED(e)
        sleep(0.2)

    for e in s:
        start = current_time()
        while True:
            if GPIO2.input(buttons2[e]):
                light_up_LED(e)
                break

            if current_time() - start >= 7:
                return False

            for wrong in buttons2:
                if wrong != e and GPIO2.input(buttons2[wrong]):
                    return False

    return True


def game():
    global current_score, game_status

    current_score = 0
    game_status = "Jeu en cours"
    chain.reset()

    s = initialise_sequence()

    while game_round(s):
        s = add_to_sequence(s)
        current_score += 50
        sleep(1)

    GAME_OVER()
    game_status = "PERDU"
    return current_score
