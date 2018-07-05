import random
import itertools
from operator import itemgetter
from ..util import get_direction, get_random_direction, AStarGraph, AStarSearch, get_closest, get_closest_astar
import matplotlib.pyplot as plt


# cool_list structure
# {
#    'x_in': 1,
#    'y_in': 2,
#    'x_ut': 3,
#    'y_ut': 4
# }

class simple_dumb(object):
    def __init__(self):
        ###############################################################################
        #
        # Config Variables
        #
        ###############################################################################
        self.max_diamonds = 3 # Larger is heavy'er on the CPU
        self.min_path_cost = 50

    def get_next_step(self, start, end, enemies):
        from_ = start
        to_ = end
        #print ("Me: ", from_)
        #print ("Goal: ", to_)
        graph = AStarGraph(enemies)
        result, cost = AStarSearch(from_, to_, graph)
        #print ("Best Route: ", result)
        #print ("Steps to goal position: ", cost)
        try:
            return list(result[1])
        except:
            return [4,4]

    def create_full_list(self, combos, diamonds, my_pos, my_home):
        #print("Lenght of combos: "+str(len(combos)))
        #print("Diamonds: "+str(diamonds))
        #print("========FUN STARTS?=======")
        big_list = []
        for path in combos:
            temp = []
            temp.append(my_pos)
            for obj in path:
                temp.append(diamonds[obj])
            temp.append(my_home)
            #print(temp)
            big_list.append(temp)
        return big_list
        #print("========FUN ENDING?=======")

    def get_shortest_path(self, big_list, enemies):
        graph = AStarGraph(enemies)
        lowest_steps = None
        best_path = None
        for path in big_list:

            steps = 0
            for index, obj in enumerate(path):
                if index != len(path)-1:
                    result, cost = AStarSearch(path[index], path[index+1], graph)
                    steps += cost

            if best_path == None or steps < lowest_steps:
                lowest_steps = steps
                best_path = path

        return best_path, lowest_steps

    # Get distance between all the objects in the current order
    def get_distance(self, cool_path):
        distance = 0
        lenth = len(cool_path)-1
        for index, obj in enumerate(cool_path):

            if index == lenth:
                break
            else:
                x_dist = abs(obj["x_out"] - cool_path[index+1]["x_in"])
                y_dist = abs(obj["y_out"] - cool_path[index+1]["y_in"])
                distance += x_dist+y_dist

        return distance

    def create_cool_list(self, combos, diamonds, teleporters, my_home, my_pos, length, my_dias):
        new_list = []
        for path in combos:
            # Add two different, because of teleporters can go two ways
            # 1
            new_path = []
            amount_of_tele = 0 # NEW
            teleporter_number = 99#length-1
            teleporter_number_2 = 98#length-2 # NEW
            #print("==================================")
            #print("Path: "+str(path))
            #print("Diamonds: "+str(diamonds))
            #print("Teleport Number 1: "+str(teleporter_number)) # NEW
            #print("Teleport Number 2: "+str(teleporter_number_2)) # NEW
            # add player_pos
            new_path.append({"x_out":my_pos["x"], "x_in":my_pos["x"], "y_out":my_pos["y"], "y_in":my_pos["y"]})
            # Add all the diamonds and check for the teleporter
            for objecttt in path:
                #print("Objectt = "+str(objecttt))
                if objecttt == teleporter_number:
                    #print("Was Teleport 1")
                    amount_of_tele += 1
                    new_path.append({"x_out":teleporters[1]["position"]["x"], "x_in":teleporters[0]["position"]["x"], "y_out":teleporters[1]["position"]["y"], "y_in":teleporters[0]["position"]["y"]})
                elif objecttt == teleporter_number_2: # NEW
                    #print("Was Teleport 2")
                    amount_of_tele += 1
                    new_path.append({"x_out":teleporters[0]["position"]["x"], "x_in":teleporters[1]["position"]["x"], "y_out":teleporters[0]["position"]["y"], "y_in":teleporters[1]["position"]["y"]}) # NEW
                else:
                    #print("Was A Diamond")
                    new_path.append({"x_out":diamonds[objecttt]["x"], "x_in":diamonds[objecttt]["x"], "y_out":diamonds[objecttt]["y"], "y_in":diamonds[objecttt]["y"]})
                if len(new_path)+1 == 5-my_dias+amount_of_tele:
                    break
            # Add Home Path
            new_path.append({"x_out":my_home["x"], "x_in":my_home["x"], "y_out":my_home["y"], "y_in":my_home["y"]})
            new_list.append(new_path)

            #print("==================================")

            '''
            # 2
            new_path = []
            teleporter_number = len(combos)
            # add player_pos
            new_path.append({"x_out":my_pos["x"], "x_in":my_pos["x"], "y_out":my_pos["y"], "y_in":my_pos["y"]})
            # Add all the diamonds and check for the teleporter
            for objecttt in path:
                if objecttt == teleporter_number:
                    new_path.append({"x_out":teleporters[0]["position"]["x"], "x_in":teleporters[1]["position"]["x"], "y_out":teleporters[0]["position"]["y"], "y_in":teleporters[1]["position"]["y"]})
                else:
                    new_path.append({"x_out":diamonds[objecttt]["x"], "x_in":diamonds[objecttt]["x"], "y_out":diamonds[objecttt]["y"], "y_in":diamonds[objecttt]["y"]})
                if len(new_path) == 5:
                    break
            # Add Home Path
            new_path.append({"x_out":my_home["x"], "x_in":my_home["x"], "y_out":my_home["y"], "y_in":my_home["y"]})
            new_list.append(new_path)
            '''

        return new_list

    def get_all_combos(self, nice_list, my_dias):
        lench_of_comb = 5-my_dias
        if len(nice_list) < lench_of_comb:
            lench_of_comb = len(nice_list)
        return [list(x) for x in itertools.permutations(nice_list, lench_of_comb)]

    def get_random_direction(self, bots):
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

    def get_8_closest_diamonds(self, diamonds, my_pos, my_home, enemies):
        
        unsorted_diamonds = []

        graph = AStarGraph(enemies)

        for dia in diamonds:
            unsorted_diamonds.append([dia, AStarSearch(my_home, dia, graph)[1]])
        
        sorted_8_diamonds_with_costs = sorted(unsorted_diamonds, key=itemgetter(1))[:self.max_diamonds]

        sorted_8_diamonds_without_cost = []
        for dia in sorted_8_diamonds_with_costs:
            sorted_8_diamonds_without_cost.append(dia[0])

        return sorted_8_diamonds_without_cost

    def get_all_possible_paths(self, potensial_diamonds, my_pos, my_home, my_diamonds):

        lench_of_comb = 5-my_diamonds
        if len(potensial_diamonds) < lench_of_comb:
            lench_of_comb = len(potensial_diamonds)
        paths = [list(x) for x in itertools.permutations(potensial_diamonds, lench_of_comb)]

        for path in paths:
            path.insert(0, my_pos)
            path.append(my_home)

        return paths

    def next_move(self, board_bot, board):

        # === Variables ===
        diamonds = [] # [(x,y),(x,y),(x,y)]
        for dia in board.diamonds:
            diamonds.append((dia["x"], dia["y"]))
        teleporters = [] # [(x,y),(x,y)]
        for obj in board.gameObjects:
            teleporters.append((obj["position"]["x"], obj["position"]["y"]))
        my_diamonds = board_bot["diamonds"] # [{'x': 5, 'y': 6}, {'x': 5, 'y': 6}]
        my_pos = (board_bot["position"]["x"], board_bot["position"]["y"]) # (x,y)
        my_home = (board_bot["base"]["x"], board_bot["base"]["y"]) # (x,y)
        max_diamonds = self.max_diamonds # larger is more heavy on the cpu
        goal_position = None # {'x': 5, 'y': 6}
        enemies = []
        players = []
        portaler = []
        for bad in board.bots:
            enemies.append((bad["position"]["x"], bad["position"]["y"]))
            players.append((bad["position"]["x"], bad["position"]["y"]))
        for bad in board.gameObjects:
            enemies.append((bad["position"]["x"], bad["position"]["y"]))
            portaler.append((bad["position"]["x"], bad["position"]["y"]))

        ###############################################################################
        #
        # First. Let's check if we gott full bag and need to return to home
        #
        ###############################################################################
        if my_diamonds == 5:
            goal_position = my_home
        else:
            goal_position = get_closest_astar(diamonds, my_pos, enemies, portaler)[0]
            goal_position = get_closest(diamonds, my_pos)[0]
        
        next_step = self.get_next_step(my_pos, goal_position, enemies)

        return get_direction(my_pos[0], my_pos[1], next_step[0], next_step[1])
