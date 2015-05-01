#!/usr/bin/env python
# -*- coding: utf-8 -*-
from module import *
from maze import *

def maze():

    import pygame
    import random
 
    #Initialize window, fill screen, create background, and prepare for drawing
    pygame.init()
    screen = pygame.display.set_mode((640,465)) 
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((255,255,255))
    background = background.convert()
    background0 = background.copy()
    screen.blit(background,(0,0))

    #Initializer player, set position and create sprite
    player = PlayerObject()
    start_pos = (0,40)
    player.rect.x = start_pos[0]
    player.rect.y = start_pos[1]
    playersprite = pygame.sprite.RenderPlain(player)

    ballsurface = pygame.Surface((10,10))
    ballsurface.set_colorkey((0,0,0))
    pygame.draw.circle(ballsurface,(255,0,0),(0,0),5)
    ballsurface = ballsurface.convert_alpha()
    ballrect = ballsurface.get_rect()
    background.blit(ballsurface, (5,5))

    backup_level =  [
                  "......................",
                  "..xxxxxxxxxxxxxxxxxxxx",
                  "....xxx.......x......x",
                  "x....x.....x..x......x",
                  "x.......x..x..xxxxxxxx",
                  "x......x...x...xx...3x",
                  "x..1..xxxxxx....x....x",
                  "x......x........x....x",
                  "x.xxx...x.......xx...x",
                  "x.x.x........2....x..x",                   
                  "x.x....x.......x.....x",
                  "x.x.....x...xxxxxxxxxx",
                  "x.xxxxxxxx..xx.....xxx",
                  "x.......x...x...xx.exx",
                  "x..xx..........xxxxxxx",
                  "xxxxxxxxxxxxxxxxxxxxxx"]

    #Generate string representation of levels using maze algorithm from maze.py
    first_level = make_maze(15,22)
    second_level = make_maze(15,22)
    if first_level[1] == "......................":
      first_level = backup_level

    #Draw level using string representation generated above
    def addlevel(level):
 
        lines = len(level)
        columns = len(level[0])
 
        length = screenrect.width / columns
        height = screenrect.height / lines

        wallobjects = []
        enemyobjects = []

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
                elif level[y][x] == "1": #enemy
                    enemy = BasicEnemyObject()
                    enemyobjects.append(enemy)
                    enemy.rect.x = length * x
                    enemy.rect.y = length * y
                    screen.blit(background, enemy.rect, enemy.rect)
                elif level[y][x] == "2": #fast enemy
                    enemy = FastEnemyObject()
                    enemyobjects.append(enemy)
                    enemy.rect.x = length * x
                    enemy.rect.y = length * y
                    screen.blit(background, enemy.rect, enemy.rect)
                elif level[y][x] == "3": #lockon enemy
                    enemy = LockOnEnemyObject(player)
                    enemyobjects.append(enemy)
                    enemy.rect.x = length * x
                    enemy.rect.y = length * y
                    screen.blit(background, enemy.rect, enemy.rect)
                elif level[y][x] == "e": #exit
                    exit = ExitObject()
                    exit.rect.x = length * x
                    exit.rect.y = length * y
                    screen.blit(background, exit.rect, exit.rect)

        screen.blit(background0, (0,0))
        return length, height, lines, columns, background, wallobjects, enemyobjects, exit

    all_levels = [first_level, second_level]
    my_maze = all_levels[0]
    length, height, lines, columns, background, wallobjects, enemyobjects, exitobject = addlevel(my_maze)
    
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Solve the Maze!")

    #Define custom events for collision, reaching end of level and dying
    PLAYERCOLLISION = pygame.USEREVENT + 2
    playercollisionevent = pygame.event.Event(PLAYERCOLLISION)
    REACHEXIT = pygame.USEREVENT + 3
    exitevent = pygame.event.Event(REACHEXIT)
    DEAD = pygame.USEREVENT + 4
    deadevent = pygame.event.Event(DEAD)
    cur_level = 0
 
    # Game loop
    while True:
        #set FPS
        clock.tick(60)
        #Respond to events in queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            #If player collides with wall or enemy, reset to starting position, decrement lives, and either continue with game or fire deadevent
            elif event.type == PLAYERCOLLISION:
                player.num_lives -= 1
                if player.num_lives <= 0:
                    pygame.event.post(deadevent)
                screen.fill((255,255,255))
                my_maze = all_levels[cur_level]
                length, height, lines, columns, background, wallobjects, enemyobjects, exitobject = addlevel(my_maze)
                player.rect.x = start_pos[0]
                player.rect.y = start_pos[1]
                pygame.time.wait(500)
            #If player reaches exit, load next level, reset to starting position
            elif event.type == REACHEXIT:
                print "Success!"
                cur_level += 1
                screen.fill((255,255,255))
                if cur_level < len(all_levels): my_maze = all_levels[cur_level]
                length, height, lines, columns, background, wallobjects, enemyobjects, exitobject = addlevel(my_maze)
                player.rect.x = start_pos[0]
                player.rect.y = start_pos[1]
                pygame.event.clear(REACHEXIT)
            #If player is dead, game over
            elif event.type == DEAD:
                print "Game over!"
                screen.fill((255,255,255))
                font = pygame.font.Font(None, 64)
                text = font.render("Game Over",1,(10,10,10))
                screen.blit(background, (0,0))
                screen.blit(text, text.get_rect())
                return
            #Player movement responds to keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP] and not(pressed[pygame.K_RIGHT]) and not(pressed[pygame.K_LEFT]): player.move(0,-player.speed)
                if pressed[pygame.K_DOWN] and not(pressed[pygame.K_RIGHT]) and not(pressed[pygame.K_LEFT]): player.move(0,player.speed)
                if pressed[pygame.K_RIGHT] and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_UP]): player.move(player.speed,0)
                if pressed[pygame.K_LEFT] and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_UP]): player.move(-player.speed,0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.movepos = [0,0]
        
        #Render text and sprites, draw to screen and redraw for each iteration of the game loop
        text = font.render("Level: "  + str(cur_level + 1) + "  Lives: " + str(player.num_lives),1,(10,10,10))
        screen.blit(background, (0,0))
        screen.blit(text, text.get_rect())
        if not(exitobject == None):
            exitsprite = pygame.sprite.RenderPlain(exitobject)
            exitsprite.update(player)
            exitsprite.draw(screen)
        wallsprites = pygame.sprite.RenderPlain(wallobjects)
        wallsprites.update(player)
        wallsprites.draw(screen)
        enemysprites = pygame.sprite.RenderPlain(enemyobjects)
        enemysprites.update(player)
        enemysprites.draw(screen)
        playersprite.update()
        playersprite.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    maze()