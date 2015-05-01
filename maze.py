#maze.py contains the algorithm for generating a random maze for the user 
#to traverse. It implements something called Prim's algorithm that works like this:
#
# 1. Initialize a tree with a single starting point, chosen arbitrarily from the graph.
# 2. Grow the tree by one edge: of the edges that connect the tree to edges not 
#    yet in the tree, find the minimum-weight edge, and transfer it to the tree.
# 3. Repeat step 2 (until all edges are in the tree).

from itertools import chain
import random

def make_maze(w, h):
    
    #the two dimensional edge array contains all of the individual
    #grid coordinates for the entire map
    edges = [[0 for x in range(h)] for x in range(w)]
    
    #we want to generate random values for each coordinate from 1 to max
    #each edge element contains a value (to calculate a minimum spanning tree),
    #a boolean indicating whether or not it is a wall object or a path, and its
    #coordinates so that we can read them
    max = 100
    
    for col in range(w):
        for row in range(h):
            edges[col][row] = (random.randint(1,max), True, col, row)
    
    #in_grid takes in a coordinate pair and tells you if it is in the map
    def in_grid(x, y):
        return x >= 0 and y >= 0 and x < w and y < h
    
    #adjacent takes in a coordinate pair and returns all grid elements
    #above, below, left, and right of it if it is not already in the path
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
    
    #endpoint takes a point in the 7x7 grid block farthest from the starting
    #point and chooses a path element within the block at random to be the 
    #ending point
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
    #it also returns the number of path elements in the map
    def all_adjacent():
        results = []
        counter = 0
        for i in range(w):
            for j in range(h):
                if edges[i][j][1] == False :
                    results.append(adjacent(i, j))
                    counter += 1
        return (results, counter)
    
    #we arbitrarily choose (0,0) to be the starting point for the map
    edges[0][0] = (0, False, 0, 0)
    
    #path finds all the grid coordinates adjacent to the entire path, finds
    #the adjacent element with the smallest value, and makes it part of the path
    #it stops whenever either the path and adjacent elements have filled the map, or
    #if we already have 200 path elements in the map
    def path():
        adjacents = list(chain.from_iterable(all_adjacent()[0]))
        num = all_adjacent()[1]
        
        if (len(adjacents) + num) == (w * h) or num >= 200:
            return
        elif min(adjacents):
            minimum = min(adjacents)
            edges[minimum[2]][minimum[3]] = (0, False, minimum[2], minimum[3])
            path()
            
    #we call path and endpoint to generate the maze
    path()
    endpoint()
    
    #this code takes in our edges array and translates it into
    #a string of characters that is readable by a parsing function
    #in mazegraphics.py
    mazestring = []
    for i in range(w):
        mazestring.append("")
        for j in range(h):
            if edges[i][j][1]:
                mazestring[i] += "x"
            elif edges[i][j][0] == 101:
                mazestring[i] += "e"
            else:
                mazestring[i] += "."

    topline = "............1.2.....3."
    mazestring.insert(0, topline) 
    return mazestring
    
#we choose to make a maze with dimensions 15x22
maze = make_maze(15,22)

