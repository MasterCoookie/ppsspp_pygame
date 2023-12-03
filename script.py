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

GENERAL_VELOCITY = 4


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

def draw_text(screen, text, x=0, y=0):
    font.drawText(screen, x, y, text)


class GameObject(psp2d.Image):
    def __init__(self, *args):
        psp2d.Image.__init__(self, *args)
        # self.position = [width/2,height/2]
        self.velocity = [0,0]
        self.target_x = None
        self.target_y = None

        self.target_a = None
        self.target_b = None
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
        
    def is_within(self, point, target, offset=0):
        if abs(point - target) < GENERAL_VELOCITY + offset:
            return True
        return False
        
    def update(self):
        if self.target_x is not None:
            if self.is_within(self.target_x, self.position[0]):
                self.position[0] = self.target_x
                self.target_x = None

            if self.target_x > self.position[0]:
                self.velocity[0] = GENERAL_VELOCITY
            elif self.target_x < self.position[0]:
                self.velocity[0] = -GENERAL_VELOCITY
                
        if self.target_y is not None:
            if self.is_within(self.target_y, self.position[1]):
                self.position[1] = self.target_y
                self.target_y = None
            if self.target_y > self.position[1]:
                self.velocity[1] = GENERAL_VELOCITY
            elif self.target_y < self.position[1]:
                self.velocity[1] = -GENERAL_VELOCITY

        if self.target_a is not None and self.target_b is not None:
            draw_text(screen, "pos: %s, %s" % (self.position[0], self.position[1]))
            if self.is_within(self.position[0], self.target_a[0], self.size[0]) and self.is_within(self.position[1], self.target_a[1], self.size[1]):
                self.goto(self.target_b[0], self.target_b[1])
                draw_text(screen, "dupa1")
            elif self.is_within(self.position[0], self.target_b[0], self.size[0]) and self.is_within(self.position[1], self.target_b[1], self.size[1]):
                draw_text(screen, "dupa2")
                self.goto(self.target_a[0], self.target_a[1])

    def goto(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def walk_between(self, target_a, target_b):
        self.target_a = target_a
        self.target_b = target_b

        self.target_x = target_a[0]
        self.target_y = target_a[1]
    


player = GameObject('ball.png')
player.set_starting_position([width/2,height/2])

ciulik = GameObject('ball.png')
ciulik.set_starting_position([0, 0])
# ciulik.goto(width, height)
# ciulik.goto(150, 150)
ciulik.walk_between([width-5, height-5], [0, 0])

all_entities = [player, ciulik]

game_started = True
while game_started:
    pad = psp2d.Controller()
    velocity = [0,0]
    if pad.cross: #z na klawie
        game_started = False
    if pad.left:
        player.velocity[0] = -GENERAL_VELOCITY
    if pad.right:
        player.velocity[0] = GENERAL_VELOCITY
    if pad.up:
        player.velocity[1] = -GENERAL_VELOCITY
    if pad.down:
        player.velocity[1] = GENERAL_VELOCITY

    # ball_position[0] += velocity[0]
    # ball_position[1] += velocity[1]

    screen.clear(psp2d.Color(0,0,0,255))
    # screen.blit(ball, 0, 0, ball_size[0], ball_size[1], ball_position[0], ball_position[1], True)
    for entity in all_entities:
        entity.update()
        entity.move(entity.velocity)
        entity.velocity = [0,0]
        entity.draw(screen)

    if player.intersects(ciulik):
        # font.drawText(screen, 0, 0, "Hello World")
        draw_text(screen, "Hello World")
        # print "Collision detected!"

    screen.swap()
