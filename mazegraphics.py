#!/usr/bin/env python
# -*- coding: utf-8 -*-
from module import *

def maze():

    import pygame
    import random
 
    pygame.init()
    screen = pygame.display.set_mode((640,465)) 
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((255,255,255))
    background = background.convert()
    background0 = background.copy()
    screen.blit(background,(0,0))
 

    player = PlayerObject()
    player.rect.x = 95
    player.rect.y = 30
    playersprite = pygame.sprite.RenderPlain(player)

    ballsurface = pygame.Surface((10,10))
    ballsurface.set_colorkey((0,0,0))
    pygame.draw.circle(ballsurface,(255,0,0),(0,0),5)
    ballsurface = ballsurface.convert_alpha()
    ballrect = ballsurface.get_rect()
    background.blit(ballsurface, (5,5))


    first_level = [
                  "......................",
                  "xxxpxxxxxxxxxxxxxxxxxx",
                  ".......x..............",
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
                  "xxxxxxxxxxxxxxxxxxxxex"]

    second_level =  [
                    "....................",
                    "xxxpxxxxxxxxxxxxxxxx",
                    "x............x.....x",
                    "x.........x..x.....x",
                    "x......x..x..xxxxxxx",
                    "x.....x...x...xx...x",
                    "x..p.xxxxxx....x...x",
                    "x.....x........x...x",
                    "x.x....x.......xx..x",
                    "x.x................x",                   
                    "x.x...x............x",
                    "x.x....x...xxxxxxxxx",
                    "x.xxxxxxx..x......xx",
                    "x......x.......xx.ex",
                    "x.............xxxxxx",
                    "xxxxxxxxxxxxxxxxxxxx"]

    third_level = [
                "................................",
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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

    def addlevel(level):
 
        lines = len(level)
        columns = len(level[0])
 
        length = screenrect.width / columns
        height = screenrect.height / lines

        wallobjects = []

        background = background0.copy()
        exit = None
 
        for y in range(lines):
            for x in range(columns):
                if level[y][x] == "x": #wall
                    wall = WallObject()
                    wallobjects.append(wall)
                    wall.rect.x = length * x
                    wall.rect.y = length * y
                    screen.blit(background, wall.rect, wall.rect)
                elif level[y][x] == "e": #exit
                    exit = ExitObject()
                    exit.rect.x = length * x
                    exit.rect.y = length * y
                    screen.blit(background, exit.rect, exit.rect)

        screen.blit(background0, (0,0))
        return length, height, lines, columns, background, wallobjects, exit
 
    all_levels = [first_level, second_level, third_level]  
    max_levels = len(all_levels)        
    my_maze = all_levels[0]
    length, height, lines, columns, background, wallobjects, exitobject = addlevel(my_maze)
    
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Get Going!!!!")

    #Define custom events
    COLLISION = pygame.USEREVENT + 2
    collisionevent = pygame.event.Event(COLLISION)
    REACHEXIT = pygame.USEREVENT + 3
    exitevent = pygame.event.Event(REACHEXIT)
    DEAD = pygame.USEREVENT + 4
    deadevent = pygame.event.Event(DEAD)
 
    # Game loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == COLLISION:
                player.num_lives -= 1
                if player.num_lives <= 0:
                    pygame.event.post(deadevent)
                player.rect.x = 95
                player.rect.y = 30
                pygame.time.wait(500)
            elif event.type == REACHEXIT:
                print "Success!"
                screen.fill((255,255,255))
                my_maze = all_levels[1]
                length, height, lines, columns, background, wallobjects, exitobject = addlevel(my_maze)
                player.rect.x = 95
                player.rect.y = 30
            elif event.type == DEAD:
                print "Game over!"
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
                """pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]: player.move(.7 * player.speed,-.7 * player.speed)
                if pressed[pygame.K_UP] and pressed[pygame.K_LEFT]: player.move(-.7 * player.speed,-.7 * player.speed)
                if pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT]: player.move(-.7 * player.speed,.7 * player.speed)
                if pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT]: player.move(.7 * player.speed,.7 * player.speed)
                if pressed[pygame.K_UP] and not(pressed[pygame.K_RIGHT]) and not(pressed[pygame.K_LEFT]): player.move(0,-player.speed)
                if pressed[pygame.K_DOWN] and not(pressed[pygame.K_RIGHT]) and not(pressed[pygame.K_LEFT]): player.move(0,player.speed)
                if pressed[pygame.K_RIGHT] and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_UP]): player.move(player.speed,0)
                if pressed[pygame.K_LEFT] and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_UP]): player.move(-player.speed,0)"""
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.movepos = [0,0]
        
        text = font.render("Lives: " + str(player.num_lives),1,(10,10,10))
        screen.blit(background, (0,0))
        screen.blit(text, text.get_rect())
        if not(exitobject == None):
            exitsprite = pygame.sprite.RenderPlain(exitobject)
            exitsprite.update(player)
            exitsprite.draw(screen)
        wallsprites = pygame.sprite.RenderPlain(wallobjects)
        wallsprites.update(player)
        wallsprites.draw(screen)
        playersprite.update()
        playersprite.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    maze()