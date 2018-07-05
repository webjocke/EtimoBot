from __future__ import print_function
import random
import matplotlib.pyplot as plt

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def get_direction(current_x, current_y, dest_x, dest_y):

    delta_y = 0
    delta_x = 0

    # Skaffa avståndet på de två axlarna
    dif_x = current_x - dest_x
    dif_y = current_y - dest_y

    if abs(dif_x) > abs(dif_y):
        if dif_x >= 0:
            delta_x = -1
        else:
            delta_x = 1
    else:
        if dif_y >= 0:
            delta_y = -1
        else:
            delta_y = 1

    return (delta_x, delta_y)

def get_optimal_path(enemy_list, target, current):

    list_of_ways_to_go = [[-1, 0], [0, -1]]
    good_comp = []

    x_max = max(target["x"], current["x"])
    x_min = min(target["x"], current["x"])
    x_dis = x_max - x_min
    y_max = max(target["y"], current["y"])
    y_min = min(target["y"], current["y"])
    y_dis = y_max - y_min

    total_steps = x_dis + y_dis
    
    all_combos = [list(x) for x in itertools.permutations(list_of_ways_to_go, total_steps)]
    for comb in all_combos:
        x = 0
        y = 0
        for way in comb:
            if way == list_of_ways_to_go[0]:
                x += 1
            else:
                y += 1
        if x == x_dis and y == y_dis:
            good_comp.append(comb)

    # NOW WE HAVE SOME GOOD COMBINATIONS


            
    return True

def get_closest_quarters_diamonds(diamonds, me, home, teleporters):
    saved_diamonds = []
    
    # Find diamonds in your current standing quater
    if me["x"] <=4 and me["y"] <= 4:
        for dia in diamonds:
            if dia["x"] <=4 and dia["y"] <= 4:
                saved_diamonds.append(dia)
    elif me["x"] >=5 and me["y"] <= 4:
        for dia in diamonds:
            if dia["x"] >=5 and dia["y"] <= 4:
                saved_diamonds.append(dia)
    elif me["x"] <=4 and me["y"] >= 5:
        for dia in diamonds:
            if dia["x"] <=4 and dia["y"] >= 5:
                saved_diamonds.append(dia)
    elif me["x"] >= 5 and me["y"] >= 5:
        for dia in diamonds:
            if dia["x"] >= 5 and dia["y"] >= 5:
                saved_diamonds.append(dia)

    if len(saved_diamonds) == 0:
        if home["x"] <=4 and home["y"] <= 4:
            for dia in diamonds:
                if dia["x"] <=4 and dia["y"] <= 4:
                    saved_diamonds.append(dia)
        elif home["x"] >=5 and home["y"] <= 4:
            for dia in diamonds:
                if dia["x"] >=5 and dia["y"] <= 4:
                    saved_diamonds.append(dia)
        elif home["x"] <=4 and home["y"] >= 5:
            for dia in diamonds:
                if dia["x"] <=4 and dia["y"] >= 5:
                    saved_diamonds.append(dia)
        elif home["x"] >= 5 and home["y"] >= 5:
            for dia in diamonds:
                if dia["x"] >= 5 and dia["y"] >= 5:
                    saved_diamonds.append(dia)

    if len(saved_diamonds) == 0:
        saved_diamonds.append(get_closest(diamonds, home))

    return saved_diamonds

def get_closest(objs, me):
    closest_space = None
    closest_obs = None

    for obj in objs:
        if closest_space == None:
            x_dist = abs(obj[0] - me[0])
            y_dist = abs(obj[1] - me[1])
            distance = x_dist+y_dist
            closest_space = distance
            closest_obs = obj
        else:
            x_dist = abs(obj[0] - me[0])
            y_dist = abs(obj[1] - me[1])
            distance = x_dist + y_dist
            if distance < closest_space:
                closest_space = distance
                closest_obs = obj

    return closest_obs

def get_closest_astar(objs, me, enemies, portals):

    closest_space = None
    closest_obs = None
    graph = AStarGraph(enemies)

    for obj in objs:

        # Without teleporters
        steps = AStarSearch(me, obj, graph)[1]

        # With teleportes, one way
        tempstep  = AStarSearch(me, portals[0], graph)[1]
        tempstep += AStarSearch(portals[1], obj, graph)[1]
        if tempstep < steps:
            steps = tempstep
            #print("Portal is shorter one way!")
        #print(tempstep)
        
        # With teleportes, other way
        tempstep  = AStarSearch(me, portals[1], graph)[1]
        tempstep += AStarSearch(portals[0], obj, graph)[1]
        if tempstep < steps:
            steps = tempstep
            #print("Portal is shorter other way!")
        #print(tempstep)

        if closest_space == None or steps < closest_space:
            closest_space = steps
            closest_obs = obj


    return closest_obs, closest_space

def get_closest_with_banned(objs, me, banned):
    closest_space = None
    closest_obs = None

    for obj in objs:
        if obj != banned["webjocke"] and obj != banned["Multiboten1"] and obj != banned["Multiboten2"] and obj != banned["Multiboten3"]:
            if closest_space == None:
                x_dist = abs(obj[0] - me["x"])
                y_dist = abs(obj[1] - me["y"])
                distance = x_dist+y_dist
                closest_space = distance
                closest_obs = obj
            else:
                x_dist = abs(obj[0] - me["x"])
                y_dist = abs(obj[1] - me["y"])
                distance = x_dist + y_dist
                if distance < closest_space:
                    closest_space = distance
                    closest_obs = obj

    return closest_obs

def position_equals(a, b):
    return a["x"] == b["x"] and a["y"] == b["y"]

def get_random_direction(enemys, me, target):
        new_cords = ()

        my_random = random.randint(1, 4)
        if my_random == 1:
            new_cords = (-1, 0)
        elif my_random == 2:
            new_cords = (1, 0)
        elif my_random == 3:
            new_cords = (0, -1)
        elif my_random == 4:
            new_cords = (0, 1)
        return new_cords


# A* Algorithm Section
class AStarGraph(object):
    #Define a class board like grid with two barriers
 
    def __init__(self, enemies):
        self.barriers = []
        #self.barriers.append([(2,4),(2,5),(2,6),(3,6),(4,6),(5,6),(5,5),(5,4),(5,3),(5,2),(4,2),(3,2)])
        self.barriers.append(enemies)
        #print(enemies)

    def heuristic(self, start, goal):
        #Use Chebyshev distance heuristic if we can move one square either
        #adjacent or diagonal
        D = 1
        D2 = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
 
    def get_vertex_neighbours(self, pos):
        n = []
        #Moves allow link a chess king
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 < 0 or x2 > 9 or y2 < 0 or y2 > 9:
                continue
            n.append((x2, y2))
        return n
 
    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier:
                return 100 #Extremely high cost to enter barrier squares
        return 1 #Normal movement cost
 
def AStarSearch(start, end, graph):
 
    G = {} #Actual movement cost to each position from the start position
    F = {} #Estimated movement cost of start to end going via this position
 
    #Initialize starting values
    G[start] = 0 
    F[start] = graph.heuristic(start, end)
 
    closedVertices = set([start])
    openVertices = set([start])
    cameFrom = {}
 
    while len(openVertices) > 0:
        #Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos
 
        #Check if we have reached the goal
        if current == end:
            #Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[end] #Done!
 
        #Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)
 
        #Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices: 
                continue #We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)
 
            if neighbour not in openVertices:
                openVertices.add(neighbour) #Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue #This G score is worse than previously found
 
            #Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H
 
    #raise RuntimeError("A* failed to find a solution")
    return ([(4, 4), (4, 4)], 4)