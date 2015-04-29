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
            edges[col][row] = (random.randint(1,max), True)
    print edges
    
    def in_grid(x, y):
        return x >= 0 and y >= 0 and x < w and y < h
    
    def adjacent(x, y):
        results = []
        if in_grid(x+1,y):
            results.append(edges[x+1][y])
        if in_grid(x-1,y):
            results.append(edges[x-1][y])
        if in_grid(x,y+1):
            results.append(edges[x][y+1])
        if in_grid(x,y-1):
            results.append(edges[x][y-1])
        return results

    for cur_col in range(w):
        for cur_row in range(h):
            adjacents = adjacent(cur_col, cur_row)
            minimum = min(adjacents)
            minimum[1] = False
            print adjacents
    
make_maze(5,5)