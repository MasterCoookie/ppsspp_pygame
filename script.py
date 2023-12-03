# -*- coding: iso-8859-1 -*-


import psp2d, pspos
import pspnet
import pspmp3
import pspogg
from time import time, localtime
import datetime
import sys
import stackless, random
import time
import random

# Set processor and bus speed
pspos.setclocks(333,166)

print "Localtime: ", localtime()
print "Datetime: ", datetime.datetime.now()

GENERAL_VELOCITY = 2


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
        self.removed = False
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
            # draw_text(screen, "pos: %s, %s" % (self.position[0], self.position[1]))
            if self.is_within(self.position[0], self.target_a[0], self.size[0]) and self.is_within(self.position[1], self.target_a[1], self.size[1]):
                self.goto(self.target_b[0], self.target_b[1])
            elif self.is_within(self.position[0], self.target_b[0], self.size[0]) and self.is_within(self.position[1], self.target_b[1], self.size[1]):
                self.goto(self.target_a[0], self.target_a[1])

    def goto(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y

    def walk_between(self, target_a, target_b):
        self.target_a = target_a
        self.target_b = target_b

        self.target_x = target_a[0]
        self.target_y = target_a[1]
    
class Player(GameObject):
    def __init__(self, *args):
        GameObject.__init__(self, *args)

    def update(self):
        return GameObject.update(self)
    
    def move(self, velocity):
        if self.position[0] + self.velocity[0] > 0 and self.position[0] + self.velocity[0] < width - self.size[0]:
            return GameObject.move(self, velocity)
    
class Alien(GameObject):
    def __init__(self, *args):
        GameObject.__init__(self, *args)

    def update(self):
        return GameObject.update(self)

player = Player('wajchadlowiec2.png')
player.set_starting_position([width/2,height - player.size[1]])

all_entities = [player]
bullets = []
enemies = []
powerups = []
game_started = True

last_shot = time.time() - 3
shot_cooldown = 1
score = 0

now = time.time()

while game_started:
    pad = psp2d.Controller()
    velocity = [0,0]
    if pad.cross and abs(last_shot - time.time()) > shot_cooldown: #z na klawie
        bullet = GameObject('BURAK_0.png')
        bullet.set_starting_position([player.position[0] + player.size[0]/2, player.position[1] - 15])
        bullet.goto(bullet.position[0], -20)
        bullets.append(bullet)
        all_entities.append(bullet)
        last_shot = time.time()
        
    if pad.left:
        player.velocity[0] = -GENERAL_VELOCITY
    if pad.right:
        player.velocity[0] = GENERAL_VELOCITY

    screen.clear(psp2d.Color(0,0,0,255))
    # screen.blit(ball, 0, 0, ball_size[0], ball_size[1], ball_position[0], ball_position[1], True)
    for entity in all_entities:
        if entity.removed:
            all_entities.remove(entity)
            continue
        entity.update()
        entity.move(entity.velocity)
        entity.velocity = [0,0]
        entity.draw(screen)

    for bullet in bullets:
        if bullet.position[1] < 0 or bullet.position[1] > height:
            bullet.removed = True
        if bullet.removed:
            bullets.remove(bullet)
            continue
    
    for enemy in enemies:
        if random.randint(0, 150) == 0:
            bullet = GameObject('bullet_enemy.png')
            bullet.set_starting_position([enemy.position[0] + enemy.size[0]/2, enemy.position[1] + enemy.size[1] + 5])
            bullet.goto(bullet.position[0], height + 20)
            bullets.append(bullet)
            all_entities.append(bullet)
        for bullet in bullets:
            if bullet.intersects(enemy):
                enemy.removed = True
                bullet.removed = True
                score += 1
                if random.randint(0, 2) == 0:
                    powerup = GameObject('rsz_1bonus_3.png')
                    powerup.set_starting_position([enemy.position[0] + enemy.size[0]/2, enemy.position[1] + enemy.size[1] + 5])
                    powerup.goto(powerup.position[0], height + 20)
                    all_entities.append(powerup)
                    powerups.append(powerup)
                continue
            if bullet.intersects(player):
                player.removed = True
                bullet.removed = True
                game_started = False
                continue

    for powerup in powerups:
        if powerup.intersects(player):
            powerup.removed = True
            powerups.remove(powerup)
            if shot_cooldown > 0.1:
                shot_cooldown -= 0.1
            continue
        
    if time.time() - now > 5:
        # draw_text(screen, "spawning")
        for _ in range(random.randint(1, 5)):
            ciulik = GameObject('ufo.png')
            ciulik.set_starting_position([random.randint(0, width - 10), ciulik.size[1]])
            rand_x_a = random.randint(0, width - 10)
            rand_x_b = random.randint(0, width - 10)
            ciulik.walk_between([rand_x_a, ciulik.size[1]], [rand_x_b, ciulik.size[1]])
            all_entities.append(ciulik)
            enemies.append(ciulik)
        now = time.time()

    # draw_text(screen, "elapsed: " + str(time.time() - now))
    # draw_text(screen, "entities: " + str(len(all_entities)), 50)
    # draw_text(screen, "bullets: " + str(len(bullets)), 200)
    draw_text(screen, "score: " + str(score))

    screen.swap()
