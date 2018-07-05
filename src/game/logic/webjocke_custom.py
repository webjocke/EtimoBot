import random
import time
import itertools
from time import sleep
import numpy as np
from operator import itemgetter
import operator
from ..util import get_direction, get_random_direction, AStarGraph, AStarSearch, get_closest, get_closest_astar
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# cool_list structure
# {
#    'x_in': 1,
#    'y_in': 2,
#    'x_ut': 3,
#    'y_ut': 4
# }

class Webjocke_Custom(object):
    def __init__(self):
        ###############################################################################
        #
        # Config Variables
        #
        ###############################################################################
        self.max_diamonds = 3 # Larger is heavy'er on the CPU
        self.min_path_cost = 50
        #plt.ion()
        #lt.show()
        

    def get_next_step(self, start, end, enemies, portals):
        from_ = start
        to_ = end
        #print ("Me: ", from_)
        #print ("Goal: ", to_)
        graph = AStarGraph(enemies)

        best_result = None
        best_cost = None

        # Without teleporters
        best_result, best_cost = AStarSearch(from_, to_, graph)

        # With teleportes, one way
        result, tempstep  = AStarSearch(from_, portals[0], graph)
        tempstep += AStarSearch(portals[1], to_, graph)[1]
        if tempstep < best_cost:
            best_cost = tempstep
            best_result = result
            print("Portal is shorter one way!")
        #print(tempstep)
        
        # With teleportes, other way
        result, tempstep  = AStarSearch(from_, portals[1], graph)
        tempstep += AStarSearch(portals[0], to_, graph)[1]
        if tempstep < best_cost:
            best_cost = tempstep
            best_result = result
            print("Portal is shorter other way!")
        #print(tempstep)

        #print ("Best Route: ", result)
        #print ("Steps to goal position: ", cost)
        try:
            return list(best_result[1]), best_result, graph
        except:
            return [4,4], [(4,4), (4,4)], graph

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

    def get_shortest_path(self, big_list, enemies, portals):
        graph = AStarGraph(enemies)
        lowest_steps = None
        best_path = None
        for path in big_list:

            steps = 0
            for index, obj in enumerate(path):
                if index != len(path)-1:
                    think_cost = 0
                    # Without teleporters
                    result, cost = AStarSearch(path[index], path[index+1], graph)
                    think_cost = cost
                    #print(think_cost)

                    # With teleportes, one way
                    tempstep  = AStarSearch(path[index], portals[0], graph)[1]
                    tempstep += AStarSearch(portals[1], path[index+1], graph)[1]
                    if tempstep < think_cost:
                        think_cost = tempstep
                        print("Portal is shorter one way!")
                    #print(tempstep)
                    
                    # With teleportes, other way
                    tempstep  = AStarSearch(path[index], portals[1], graph)[1]
                    tempstep += AStarSearch(portals[0], path[index+1], graph)[1]
                    if tempstep < think_cost:
                        think_cost = tempstep
                        print("Portal is shorter other way!")
                    #print(tempstep)

                    #print("===============")

                    steps += think_cost

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

    def get_8_closest_diamonds(self, diamonds, my_pos, my_home, enemies, portals):
        
        unsorted_diamonds = []

        graph = AStarGraph(enemies)

        for dia in diamonds:
            # Without teleporters
            cost = AStarSearch(my_home, dia, graph)[1]

            # With teleportes, one way
            tempstep  = AStarSearch(my_pos, portals[0], graph)[1]
            tempstep += AStarSearch(portals[1], dia, graph)[1]
            if tempstep < cost:
                cost = tempstep
                print("Portal is shorter one way!")
            #print(tempstep)
            
            # With teleportes, other way
            tempstep  = AStarSearch(my_pos, portals[1], graph)[1]
            tempstep += AStarSearch(portals[0], dia, graph)[1]
            if tempstep < cost:
                cost = tempstep
                print("Portal is shorter other way!")
            #print(tempstep)

            unsorted_diamonds.append([dia, cost])
        
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

    def diamonds_weight_method(self, board, diamonds):
        awesome_list = []
        '''
        List with all players and their paths and costs to all diamonds
        [
            ["botname", {
                # dia  cost  path
                1: (4, [(3,5), (2,6), (2,6)]),
                2: (4, [(3,5), (2,6), (2,6)])
            }]
        ]
        '''
        all_players = board.bots
        for player in all_players:
            if player["diamonds"] == 5:
                continue
            player_pos = (player["position"]["x"], player["position"]["y"])
            cool_list = []
            cool_list.append(player["name"])
            cool_list.append({})
            for index, dia in enumerate(diamonds):
                graph = AStarGraph(all_players+board.gameObjects)
                best_result, best_cost = AStarSearch(player_pos, dia, graph)
                cool_list[1][index] = (best_cost, best_result)
            awesome_list.append(cool_list)

        # List of all diamonds and their weight
        diamonds_weight = {}
        '''
        {
            # dia_index, weight
            1: 37,
            2: 37
        }
        '''
        # Fill with all the diamonds
        for index, dia in enumerate(diamonds):
                diamonds_weight[index] = 0
        # Modify the weight variable
        for player_info in awesome_list:
            multiplyer = -1
            if player_info[0] == "webjocke":
                multiplyer = 1
            for index, dia in enumerate(diamonds_weight):
                diamonds_weight[index] += multiplyer / (1+player_info[1][index][0])
        return diamonds_weight

    def other_players_closest(self, players, diamonds, enemies, portals):
        cool_lst = []
        for player in players:
            #cool_lst.append(get_closest_astar(diamonds, player, enemies, portals)[0])
            cool_lst.append(get_closest(diamonds, player))
        #print(cool_lst)
        return cool_lst

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
        portals = []
        for bad in board.bots:
            if bad["name"] != "webjocke":
                enemies.append((bad["position"]["x"], bad["position"]["y"]))
                players.append((bad["position"]["x"], bad["position"]["y"]))
        for bad in board.gameObjects:
            enemies.append((bad["position"]["x"], bad["position"]["y"]))
            portals.append((bad["position"]["x"], bad["position"]["y"]))


        ###############################################################################
        #
        # Diamond Weight Method
        #
        ###############################################################################
        #diamonds_weight = self.diamonds_weight_method(board, diamonds)
        #sorted_list = sorted(diamonds_weight.items(), key=operator.itemgetter(1), reverse=True)
        #goal_diamonds_index = sorted_list[0][0]

        ###############################################################################
        #
        # Get closest if not other players is closer - Method
        #
        ###############################################################################
        #not_to_go_to = self.other_players_closest(players, diamonds, enemies, portals)
        #my_closest = get_closest_astar(diamonds, my_pos, enemies, portals)[0]
        #while my_closest in not_to_go_to:
        #    diamonds.remove(my_closest)
        #    my_closest = get_closest_astar(diamonds, my_pos, enemies, portals)[0]
        #    #print("Someone else is closer then me...")
        #if my_closest != None:
        #    goal_diamonds_index = my_closest
        #else:
        #    goal_diamonds_index = my_home

        ###############################################################################
        #
        # First Diamond Method
        #
        ###############################################################################
        goal_diamonds_index = get_closest_astar(diamonds, my_pos, enemies, portals)[0]

        ###############################################################################
        #
        # First. Let's check if we gott full bag and need to return to home
        #
        ###############################################################################
        
        if my_diamonds == 5:
            goal_position = my_home
        #elif my_diamonds == 0:
        #    goal_position = get_closest_astar(diamonds, my_pos, enemies, portals)
        else:

            # If diamonds is to far away, go home instead
            #if get_closest_astar([goal_diamonds_index], my_pos, enemies, portals)[1] > 10 and len(players) > 2 and len(diamonds) < 3:
            #    goal_position = my_home
            #    print("To Long Away, going home")
            #else:
            goal_position = goal_diamonds_index
            
            #goal_position = get_closest_astar(diamonds, my_pos, enemies, portals)
        
        next_step, result, graph = self.get_next_step((my_pos[0], my_pos[1]), (goal_position[0], goal_position[1]), enemies, portals)


        ###############################################################################
        #
        # Show the plot
        #
        ###############################################################################
        '''
        list_to_show = []
        for row in range(0,10):
            col_list = []
            for col in range(0, 10):
                col_list.append((0,0,0))
            list_to_show.append(col_list)
            
        list_to_show[my_pos[1]][my_pos[0]] = (255,255,0)
        list_to_show[my_home[1]][my_home[0]] = (255,255,255)
        list_to_show[goal_position[1]][goal_position[0]] = (0,0,255)
        for index, dia in enumerate(diamonds):
            list_to_show[dia[1]][dia[0]] = (0,max(10, int(100+diamonds_weight[index]*155)),0)
        for dia in enemies:
            list_to_show[dia[1]][dia[0]] = (255,0,0)
        '''

        ###############################################################################
        #
        # Teleporter check
        #
        ###############################################################################
        '''
        list_to_show = []
        for row in range(0,10):
            col_list = []
            for col in range(0, 10):
                cord = (col, row)
                cost = get_closest_astar([cord], my_pos, [], portals)[1]
                col_list.append((0,255-cost*12,0))
            list_to_show.append(col_list)
        list_to_show[portals[0][1]][portals[0][0]] = (0,0,255)
        list_to_show[portals[1][1]][portals[1][0]] = (0,0,255)
        list_to_show[my_pos[1]][my_pos[0]] = (255,255,0)

        plt.clf()
        plt.imshow(np.array(list_to_show))
        plt.xlim(-0.5,9.5)
        plt.ylim(9.5,-0.5)
        plt.draw()
        plt.pause(0.001)
        '''
        

        return get_direction(my_pos[0], my_pos[1], next_step[0], next_step[1])
        #else:     
        
        '''
        elif my_diamonds >= 2:
            # Sorting out the closest 8
            potensial_diamonds = self.get_8_closest_diamonds(diamonds, my_pos, my_home, enemies, portals)
            # Get all combos of the diamonds, and add my position and the home position
            all_paths = self.get_all_possible_paths(potensial_diamonds, my_pos, my_home, my_diamonds)
            # Get shortest paths of them
            path_to_take, cost = self.get_shortest_path(all_paths, enemies, portals)
            #print(path_to_take, cost)
            goal_position = path_to_take[1]
            #goal_position = get_closest_astar(diamonds, my_pos, enemies)
            '''                                                                                           

        ###############################################################################
        #
        # Let's figure out what diamond to hunt
        #
        ###############################################################################

        ###############################################################################
        #
        # Let's generate a list of all combinations of paths between diamonds
        #
        ###############################################################################

        # Create list with all combos of 5 diamonds (using <=19 dia)
        #lengh_of_diamonds = len(diamonds) #+2 # +1 to have space for one teleporter                             <-------------------
        #if lengh_of_diamonds > max_diamonds:                                                                               <-------------------
        #    lengh_of_diamonds = max_diamonds                                                                           <-------------------
        #list_of_diamond_indexes = range(0, lengh_of_diamonds)                                          <-------------------
        #combos = self.get_all_combos(list_of_diamond_indexes, my_diamonds)                            <-------------------
        
        #print("==== Creating Combos =====")
        #print(combos)
        #print("Amount of combos: "+str(len(combos)))
        #print("Total Diamonds: "+str(len(diamonds)))
        #print("Only using "+str(self.max_diamonds)+" Diamonds")

        ###############################################################################
        #
        # Insert diamond cordinates into list and add me_pos and_home pos for each path
        #
        ###############################################################################

        # Generates big list, with me pos, home pos and all the diamonds pos
        #big_list = self.create_full_list(combos, diamonds, my_pos, my_home)                            <-------------------
        #print("==== Creating Big List =====")
        #print("Amount of combos: "+str(len(big_list)))
        #print(big_list)


        '''
        elif my_diamonds == 0:
        players_and_shortest = []
        for player in players:
        if(len(players) < len(diamonds)):
        players_and_shortest.append(get_closest_astar(diamonds, player, enemies))
        for dia in players_and_shortest:
        if dia in diamonds:
        diamonds.remove(dia)
        goal_position = get_closest_astar(diamonds, my_pos, enemies)'''
        ###############################################################################
        #
        # Let's calculate the shortest path of them all
        #
        ###############################################################################

        #shortest_path, steps = self.get_shortest_path(big_list, enemies)                            <-------------------
        #print("==== Getting the shortest path =====")
        #print("Amount of Steps: "+str(steps))
        #print(shortest_path)

        ###############################################################################
        #
        # Run to the first obj on the shortest path
        #
        ###############################################################################

        #goal_position = shortest_path[1]                                                                                                        <-------------------
        
        ''' Skipping cool_list
        # Create the cool list using create_cool_list()
        cool_list = self.create_cool_list(combos, diamonds, teleporters, my_home, my_pos, lengh_of_diamonds, board_bot["diamonds"])
        #print("==== cool_list =====")
        #print(cool_list)
        #print(len(cool_list))
        #print("==== cool_list =====")

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

        


### TODO
# Fixa så att man går ett random håll ifall man fastnar vid en annan bot --- Förbättra!
# Unvida Portaler (ifall man inte vill gå in i dem just i detta steg)
# Räkna ms ifrån start på mainloopen och kör sen direkt ifall det har gått minUpdateTime eller något
