# -*- coding: iso-8859-1 -*-


import psp2d, pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import sys
import stackless, random

# Set processor and bus speed
pspos.setclocks(333,166)

print "Localtime: ", localtime()
print "Datetime: ", datetime.datetime.now()


width, height = 480, 272

# Creates the screen and its background color (Black)
screen = psp2d.Screen()
screen.clear(psp2d.Color(0,0,0,255))

# Loads the font
font = psp2d.Font('font.png')
ball=psp2d.Image('ball.png')
ball_size=9,9
ball_position=[width/2,height/2]
ball_velocity=[0,0]

game_started = True
while game_started:
    pad = psp2d.Controller()
    velocity = [0,0]
    if pad.cross:
        game_started = False
    if pad.left:
        velocity[0] = -4
    if pad.right:
        velocity[0] = 4
    if pad.up:
        velocity[1] = -4
    if pad.down:
        velocity[1] = 4

    ball_position[0] += velocity[0]
    ball_position[1] += velocity[1]

    screen.clear(psp2d.Color(0,0,0,255))
    screen.blit(ball, 0, 0, ball_size[0], ball_size[1], ball_position[0], ball_position[1], True)
    screen.swap()


