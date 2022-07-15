import keyboard
import threading
import random
import os
import time
import board
import neopixel
import RPi.GPIO as GPIO
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,GPIO.HIGH)

size=200

led_pin = board.D18
num_pixels = 200
ORDER = neopixel.GRB
leds = neopixel.NeoPixel(
    led_pin, num_leds, brightness=0.2#, auto_write=False, pixel_order=ORDER
)

global field
field = [0]*(size*2)
global mover

def printfield():
    for i in range(size):
        if field[i]==1:
            leds[i]=[0,255,0]
        elif field[i]=="X":
            leds[i]=[255,0,0]
        else:
            leds[i]=[0,0,0]
        leds.show()



def fruits(position):
    fruitposition = random.randint(0, 199)
    while fruitposition in position:
        fruitposition = random.randint(0, 199)
    field[fruitposition]="X"


def moving():
    mover=1
    while True:
        if keyboard.read_key()=="w":
            field[200] = -20
        if keyboard.read_key() == "s":
            field[200] = 20
        if keyboard.read_key() == "a":
            field[200] = -1
        if keyboard.read_key() == "d":
            field[200]=1
def endscreen(length):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Score:", (length + 1))
    with open("Highscore.txt","r") as highscore:
        score=highscore.read()
    if int(score) < (length + 1):
        with open("Highscore.txt", "w") as highscore:
            length=length+1
            highscore.write(str(length))
            print("Highscore", length)
    else:
        print("Highscoe",score)

    quit()

def positionupdate(position,length):

    if length>0:
        field[position[length]]=0
        for i in reversed(range(length)):
            position[i+1] = position[i]
    else:
        field[position[0]]=0
    if field[position[0]+field[200]]==1:
        endscreen(length)
    else:
        position[0]=position[0]+field[200]

    #for number in range(length+1):
        #position[number]=position[number]
    for number in reversed(range(length+1)):
        x=field[200]
        field[200+number]=field[200+number+1]
        field[200]=x
    return position

def bordercontrol(position,length):
    for i in range(10):
        if position[0] <0 or position[0] >199:
            endscreen(length)


        elif field[200]==1:
            for next in range(1,10):
                if position[0]==20*next:
                    endscreen(length)
        elif field[200]==-1:
            for next in range(1,10,2):
                if position[0]==10*next+9:
                    endscreen(length)



if __name__ == '__main__':


    threading.Thread(target=moving).start()
    position = []
    position.append(90)
    start=1
    length=0
    allpositions = []
    counter=1

    while True:
        if start==1 or hit==1:
            fruits(position)
            start=0
            hit=0
        bordercontrol(position,length)
        printfield()


        time.sleep(0.3)
        position=positionupdate(position,length)

        if field[position[0]]=="X":
            length+=1
            lastpos=position[length-1]
            position.append(lastpos)
            fruits(position)


        for pos in position:

            field[pos]=1
