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
# ball=psp2d.Image('ball.png')
# ball_size=9,9
# ball_position=[width/2,height/2]
# ball_velocity=[0,0]

class GameObject(psp2d.Image):
    def __init__(self, *args):
        psp2d.Image.__init__(self, *args)
        # self.position = [width/2,height/2]
        self.velocity = [0,0]
        # self.size = [9, 9]

    def move(self, velocity):
        self.position[0] += velocity[0]
        self.position[1] += velocity[1]

    def set_starting_position(self, position):
        self.position = position

    def draw(self, screen):
        screen.blit(self, 0, 0, self.size[0], self.size[1], self.position[0], self.position[1], True)

    def intersects(self, other):
        if self.position[0] < other.position[0] + other.size[0] and \
           self.position[0] + self.size[0] > other.position[0] and \
           self.position[1] < other.position[1] + other.size[1] and \
           self.position[1] + self.size[1] > other.position[1]:
            return True
        else:
            return False


player = GameObject('ball.png')
player.set_starting_position([width/2,height/2])

ciulik = GameObject('ball.png')
ciulik.set_starting_position([width/3,height/3])

all_entities = [player, ciulik]

game_started = True
while game_started:
    pad = psp2d.Controller()
    velocity = [0,0]
    if pad.cross: #z na klawie
        game_started = False
    if pad.left:
        player.velocity[0] = -4
    if pad.right:
        player.velocity[0] = 4
    if pad.up:
        player.velocity[1] = -4
    if pad.down:
        player.velocity[1] = 4

    # ball_position[0] += velocity[0]
    # ball_position[1] += velocity[1]

    screen.clear(psp2d.Color(0,0,0,255))
    # screen.blit(ball, 0, 0, ball_size[0], ball_size[1], ball_position[0], ball_position[1], True)
    for entity in all_entities:
        entity.move(entity.velocity)
        entity.velocity = [0,0]
        entity.draw(screen)
    screen.swap()


