from mazegraphics import *
from module import *
"""
from random import shuffle, randrange
 
def make_maze(w = 16, h = 8):
	vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
	ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
	hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
	def walk(x, y):
		vis[y][x] = 1
 
		d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
		shuffle(d)
		for (xx, yy) in d:
			if vis[yy][xx]: continue
			if xx == x: hor[max(y, yy)][x] = "+  "
			if yy == y: ver[y][max(x, xx)] = "   "
			walk(xx, yy)
 
	walk(randrange(w), randrange(h))
	for (a, b) in zip(hor, ver):
		print(''.join(a + ['\n'] + b))
 
make_maze()
"""

import random

def make_maze(w, h):
    edges = [[0 for x in range(w)] for x in range(h)]
    max = 100
    for col in range(w):
        for row in range(h):
            edges[col][row] = (random.randint(1,max), True, col, row)
    
    def in_grid(x, y):
        return x >= 0 and y >= 0 and x < w and y < h
    
    def adjacent(x, y):
        results = []
        if in_grid(x+1,y) and not(edges[x+1][y][0] == 0):
            results.append(edges[x+1][y])
        if in_grid(x-1,y) and not(edges[x-1][y][0] == 0):
            results.append(edges[x-1][y])
        if in_grid(x,y+1) and not(edges[x][y+1][0] == 0):
            results.append(edges[x][y+1])
        if in_grid(x,y-1) and not(edges[x][y-1][0] == 0):
            results.append(edges[x][y-1])
        return results
    
    edges[0][0] = (0, False, 0, 0)
    
    def path(x, y):
        
        adjacents = adjacent(x, y)
        if not(adjacents):
            return
        else:
            minimum = min(adjacents)
            edges[minimum[2]][minimum[3]] = (0, False, minimum[2], minimum[3])
            path(minimum[2],minimum[3])
    
    path(0,0)
    print edges
    
    for i in range(w):
        for j in range(h):
            if edges[i][j][1]:
                print "x",
            else:
                print ".",
        print ""
    
make_maze(10,10)

