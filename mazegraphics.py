#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Wanna try escape the maze???
"""   
from Tkinter import *
from module import *

def maze():

    import pygame
    import random
 
    pygame.init()
    screen=pygame.display.set_mode((640,480)) 
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((255,255,255))
    background = background.convert()
    background0 = background.copy()
    screen.blit(background,(0,0))
 

    player = PlayerObject()
    playersprite = pygame.sprite.RenderPlain(player)

    ballsurface = pygame.Surface((10,10))
    ballsurface.set_colorkey((0,0,0))
    pygame.draw.circle(ballsurface,(255,0,0),(0,0),5)
    ballsurface = ballsurface.convert_alpha()
    ballrect = ballsurface.get_rect()
    background.blit(ballsurface, (5,5))


    first_level = ["xxx.xxxxxxxxxxxxxxxxxx",
                  ".s.....x..............",
                  "xxxx.........xx......x",
                  "x......x....x.x......x",
                  "x......x......x......x",
                  "x......x......x......x",
                  "x...xxxxxx....x......x",
                  "x......x.............x",
                  "x......x......xxxxxxxx",
                  "xxxxxx.x.............x",
                  "x......x.............x",
                  "x......x.............x",
                  "x..........xxxx...xxxx",
                  "x..........x.........x",
                  "xxxxxxxxxxxxxxxxx.xxnx"]

    second_level =  ["xxxxxxxxxxxxxxx",
                    "xs............x",
                    "x.........x...x",
                    "x.........x...x",
                    "x......x..x...x",
                    "x.....x...x...x",
                    "x..p.xxxxxx...x",
                    "x.....x.......x",
                    "x.x....x......x",
                    "x.x...........x",                   
                    "x.x...x.......x",
                    "x.x....x......x",
                    "x.xxxxxxx..n..x",
                    "x......x......x",
                    "x.....x.......x",
                    "xxxxxxxxxxxxxxx"]

    third_level = ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "xs.............................x",
                "x..............................x",
                "x..............................x",
                "x............xxx....xxx........x",
                "x...........xx.xx..xx.xx.......x",
                "x............xxx....xxx........x",
                "x..............................x",
                "x................x.............x",
                "x................x.............x",
                "x................x.............x",
                "x..............................x",
                "x................r.............x",
                "x............xx....xxx.........x",
                "x.............xxxxxxx..........x",
                "x..............................x",
                "x..............................x",
                "xxxxxxpxxxxxxxxxxxnxxxxxxxxxxxex"]
 
 
    def createblock(length, height, color):
        tempblock = pygame.Surface((length, height))
        tempblock.fill(color)
        tempblock.convert()
        return tempblock
        
    """def detect_collision(other):
        player.rect.colliderect(other.rect)"""

    def addlevel(level):
 
        lines = len(level)
        columns = len(level[0])
 
        length = screenrect.width / columns
        height = screenrect.height / lines

        #wallblock = createblock(length, height,(0,0,0))

        background = background0.copy()
 
        for y in range(lines):
            for x in range(columns):
                if level[y][x] == "x": # wall
                    #background.blit(wallblock, (length * x, height * y))
                    ballx = length * x
                    bally = height * y
        screen.blit(background0, (0,0))
 
        return length, height, ballx, bally , lines, columns, background
 
    all_levels = [first_level, second_level, third_level]  
    max_levels = len(all_levels)        
    my_maze = all_levels[0]
    length, height,  ballx, bally, lines, columns, background = addlevel(my_maze)
    
    clock = pygame.time.Clock()
    pygame.display.set_caption("Get Going!!!!")
 
    # Game loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    player.move(0,-player.speed)
                if event.key == pygame.K_DOWN:
                    player.move(0,player.speed)
                if event.key == pygame.K_RIGHT:
                    player.move(player.speed,0)
                if event.key == pygame.K_LEFT:
                    player.move(-player.speed,0)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.movepos = [0,0]
                    player.state = "still"

        wall = WallObject()
        wallsprite = pygame.sprite.RenderPlain(wall)
        wall.rect.x = 0
        wall.rect.y = 0

        screen.blit(background, (0,0))
        screen.blit(background, wall.rect, wall.rect)
        playersprite.update()
        playersprite.draw(screen)
        wallsprite.update(player)
        wallsprite.draw(screen)
        pygame.display.flip() 

if __name__ == "__main__":
    maze()