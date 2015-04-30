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
from itertools import chain
import random

def make_maze(w, h):
    edges = [[0 for x in range(h)] for x in range(w)]
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
    
    def endpoint():
        results = []
        for i in range(w - 7, w):
            for j in range(h - 7, h):
                if edges[i][j][1] == False :
                    results.append(edges[i][j])
        index = random.randint(0, len(results)-1)
        edges[results[index][2]][results[index][3]] = (101, False, results[index][2], results[index][3])
                    
    #all_adjacent shouldn't need any arguments and should
    #return all edge elements that are adjacent to any existing path edge
    def all_adjacent():
        results = []
        counter = 0
        for i in range(w):
            for j in range(h):
                if edges[i][j][1] == False :
                    results.append(adjacent(i, j))
                    counter += 1
        return (results, counter)
    
    edges[0][0] = (0, False, 0, 0)
    
    def path():
        adjacents = list(chain.from_iterable(all_adjacent()[0]))
        num = all_adjacent()[1]
        
        if (len(adjacents) + num) == (w * h) or num >= 200:
            return
        elif min(adjacents):
            minimum = min(adjacents)
            edges[minimum[2]][minimum[3]] = (0, False, minimum[2], minimum[3])
            #print adjacents
            path()
    path()
    endpoint()
    
    mazestring = []

    for i in range(w):
        mazestring.append("")
        for j in range(h):
            if edges[i][j][1]:
                mazestring[i] += "x"
                print "x",
            elif edges[i][j][0] == 101:
                mazestring[i] += "e"
                print "e",
            else:
                mazestring[i] += "."
                print ".",
        print ""

    topline = "............1.2.....3."
    mazestring.insert(0, topline) 
    #print mazestring
    return mazestring
    
maze = make_maze(15,22)

