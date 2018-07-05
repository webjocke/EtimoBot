import random
import itertools
from ..util import get_direction, get_random_direction, AStarGraph, AStarSearch, get_closest, get_closest_with_banned
import matplotlib.pyplot as plt


# cool_list structure
# {
#    'x_in': 1,
#    'y_in': 2,
#    'x_ut': 3,
#    'y_ut': 4
# }

class swarm(object):
    def __init__(self):

        ###############################################################################
        #
        # Config Variables
        #
        ###############################################################################
        self.max_diamonds = 7 # Larger is heavy'er on the CPU

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
            if best_path == None:
                steps = 0
                for index, obj in enumerate(path):
                    if index != len(path)-1:
                        result, cost = AStarSearch(path[index], path[index+1], graph)
                        steps += cost
                lowest_steps = steps
                best_path = path
            else:
                steps = 0
                for index, obj in enumerate(path):
                    if index != len(path)-1:
                        result, cost = AStarSearch(path[index], path[index+1], graph)
                        steps += cost
                if steps < lowest_steps:
                    lowest_steps = steps
                    best_path = path
        return best_path, lowest_steps

    def am_I_in_my_home_quarter():
        return True

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

    def next_move(self, board_bot, board):

        my_pos = (board_bot["position"]["x"], board_bot["position"]["y"]) # (x,y)

        if board_bot["diamonds"] == 5:
            goal_position = board_bot["base"]
        else:

            # === Variables ===
            diamonds = [] # [(x,y),(x,y),(x,y)]
            for dia in board.diamonds:
                diamonds.append((dia["x"], dia["y"]))
            teleporters = [] # [(x,y),(x,y)]
            for obj in board.gameObjects:
                teleporters.append((obj["position"]["x"], obj["position"]["y"]))
            my_diamonds = board_bot["diamonds"] # [{'x': 5, 'y': 6}, {'x': 5, 'y': 6}]
            
            my_home = (board_bot["base"]["x"], board_bot["base"]["y"]) # (x,y)
            max_diamonds = self.max_diamonds # larger is more heavy on the cpu
            my_name = board_bot["name"] # bots username
            goal_position = None # {'x': 5, 'y': 6}
            enemies = []
            for bad in board.bots:
                enemies.append((bad["position"]["x"], bad["position"]["y"]))
            for bad in board.gameObjects:
                enemies.append((bad["position"]["x"], bad["position"]["y"]))
            #print("Enemies: "+str(enemies))

            ###############################################################################
            #
            # First. Let's check if we gott full bag and need to return to home
            #
            ###############################################################################

            
            ###############################################################################
            #
            # Figure out what quarter is yours
            #
            ###############################################################################

            heighest_score = 0
            target_pos = None
            target_name = None
            for bot in board.bots:
                if bot["name"] == "webjocke":
                    continue
                elif heighest_score == 0:
                    heighest_score = bot["score"]
                    target_pos = bot["position"]
                    target_name = bot["name"]
                elif bot["score"] > heighest_score:
                    heighest_score = bot["score"]
                    target_pos = bot["position"]
                    target_name = bot["name"]
            
            #print("===============================================")
            #print("Target: "+target_name)
            #print("===============================================")

            ###############################################################################
            #
            # Get the closest diamond in my quarter
            #
            ###############################################################################

            goal_position = target_pos

        next_step = self.get_next_step((my_pos[0], my_pos[1]), (goal_position["x"], goal_position["y"]), enemies)

        return get_direction(my_pos[0], my_pos[1], next_step[0], next_step[1])
        