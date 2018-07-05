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

class Multibot(object):
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

        if board_bot["diamonds"] == 5:
            goal_position = my_home
        else:

            ###############################################################################
            #
            # Figure out what quarter is yours
            #
            ###############################################################################

            corners = [(0,0), (9,0), (9,9), (0,9)]
            assignments =       {"webjocke":0,    "Multiboten1":0,    "Multiboten2":0,    "Multiboten3":0}
            bases =             {"webjocke":None, "Multiboten1":None, "Multiboten2":None, "Multiboten3":None}
            quarter_corner =    {"webjocke":None, "Multiboten1":None, "Multiboten2":None, "Multiboten3":None}

            for bot in board.bots:
                if bot["name"] == "webjocke":
                    bases["webjocke"] = bot["base"]
                elif bot["name"] == "Multiboten1":
                    bases["Multiboten1"] = bot["base"]
                elif bot["name"] == "Multiboten2":
                    bases["Multiboten2"] = bot["base"]
                elif bot["name"] == "Multiboten3":
                    bases["Multiboten3"] = bot["base"]
            
            if bases["webjocke"] != None:
                assignments["webjocke"] = get_closest_with_banned(corners, bases["webjocke"], assignments)
            if bases["Multiboten1"] != None:
                assignments["Multiboten1"] = get_closest_with_banned(corners, bases["Multiboten1"], assignments)
            if bases["Multiboten2"] != None:
                assignments["Multiboten2"] = get_closest_with_banned(corners, bases["Multiboten2"], assignments)
            if bases["Multiboten3"] != None:
                assignments["Multiboten3"] = get_closest_with_banned(corners, bases["Multiboten3"], assignments)
            
            print("===============================================")
            print("Corners: "+str(assignments))
            print("Bases: "+str(bases))
            print("===============================================")

            ###############################################################################
            #
            # Get all diamonds in your quarter
            #
            ###############################################################################

            diamonds_for_me = []
            for dia in diamonds:
                if assignments[my_name] == (0,0):
                    if dia[0] >= 0 and dia[0] <= 4 and dia[1] >= 0 and dia[1] <= 4:
                        diamonds_for_me.append(dia)
                elif assignments[my_name] == (0,9):
                    if dia[0] >= 0 and dia[0] <= 4 and dia[1] >= 5 and dia[1] <= 9:
                        diamonds_for_me.append(dia)
                elif assignments[my_name] == (9,0):
                    if dia[0] >= 5 and dia[0] <= 9 and dia[1] >= 0 and dia[1] <= 4:
                        diamonds_for_me.append(dia)
                elif assignments[my_name] == (9,9):
                    if dia[0] >= 5 and dia[0] <= 9 and dia[1] >= 5 and dia[1] <= 9:
                        diamonds_for_me.append(dia)

            ###############################################################################
            #
            # Get the closest diamond in my quarter
            #
            ###############################################################################

            if len(diamonds_for_me)>0:
                closest_dia = get_closest(diamonds_for_me, my_pos)
            else:
                closest_dia = my_home

            ###############################################################################
            #
            # Run to the first obj on the shortest path
            #
            ###############################################################################

            goal_position = closest_dia

            ''' Skipping cool_list
            # Create the cool list using create_cool_list()
            cool_list = self.create_cool_list(combos, diamonds, teleporters, my_home, my_pos, lengh_of_diamonds, board_bot["diamonds"])
            #print("==== cool_list =====")
            #print(cool_list)
            #print(len(cool_list))
            #print("==== cool_list =====")
            '''

            ''' START COMMENT

            # Move towards the next object in the perfect path on the board
            self.goal_position = {"x":best_path[1]["x_in"], "y":best_path[1]["y_in"]}
            if best_path[1]["x_in"] != best_path[1]["x_out"] or best_path[1]["y_in"] != best_path[1]["y_out"]:
                self.is_teleporter = True
            
            END COMMENT'''

            #temp = get_closest(board.diamonds, board_bot["position"]) #board.diamonds[0]
            #goal_position = (temp["x"], temp["y"])
            #print("Closest Diamonds: "+str(goal_position))


        ###############################################################################
        #
        # Let's figure out the shortest path to that goal_position (usually a diamond)
        #
        ###############################################################################

        # Calculate move according to goal position
        #delta_x, delta_y = get_direction(my_pos[0], my_pos[1], goal_position[0], goal_position[1])

        #going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}
        #first_going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}
        #temp_going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}

        next_step = self.get_next_step((my_pos[0], my_pos[1]), (goal_position[0], goal_position[1]), enemies)

        return get_direction(my_pos[0], my_pos[1], next_step[0], next_step[1])
        

### TODO
# Fixa så att man går ett random håll ifall man fastnar vid en annan bot --- Förbättra!
# Unvida Portaler (ifall man inte vill gå in i dem just i detta steg)
# Räkna ms ifrån start på mainloopen och kör sen direkt ifall det har gått minUpdateTime eller något


'''
# ========== OLD BUT STILL RUNNING BOT ===========
# Analyze new state
if board_bot["diamonds"] == 5:
    # Move to base if we are full of diamonds
    base = board_bot["base"]
    self.goal_position = base
else:
    # Move towards first diamond on board
    self.goal_position = board.diamonds[0]

if self.goal_position:
    # Calculate move according to goal position
    current_position = board_bot["position"]
    delta_x, delta_y = get_direction(current_position["x"], current_position["y"], self.goal_position["x"], self.goal_position["y"])
    return delta_x, delta_y

return 0, 0
'''