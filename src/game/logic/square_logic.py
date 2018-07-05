import random
from ..util import get_direction, get_optimal_path, get_closest_quarters_diamonds, get_closest, get_random_direction


class SquareLogic(object):
    def __init__(self):
        self.goal_position = None
        self.next_pos = None
        self.enemy_list = []

    def next_move(self, board_bot, board):

        self.enemy_list = board.bots
        self.enemy_list.extend(board.gameObjects)

        if board_bot["diamonds"] >= 5:
            # Move to base if we are full of diamonds
            base = board_bot["base"]
            self.goal_position = base
        else:

            # Variables
            current = board_bot["position"]
            home = board_bot["base"]

            #diamonds_in_quarter = get_closest_quarters_diamonds(board.diamonds, current, home, [board.gameObjects[0]["position"], board.gameObjects[1]["position"]])
            #target = get_closest(diamonds_in_quarter, current)

            target = get_closest(board.diamonds, home)

            # Returns the next good pos to go to
            self.goal_position = target #get_optimal_path(self.enemy_list, target, current)

        if self.goal_position:
            
            # Calculate move according to goal position
            current_position = board_bot["position"]
            delta_x, delta_y = get_direction(current_position["x"], current_position["y"], self.goal_position["x"], self.goal_position["y"])
            
            first_going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}
            temp_going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}

            #print("=======")
            #print(self.enemy_list)
            #print("=======")

            for bot in self.enemy_list:
                # Remove the teleporter from enemy in case we want to use it
                #for enemy in self.enemy_list:
                #    if enemy["position"]["x"] == first_going_to["x"] and enemy["position"]["y"] == first_going_to["y"]:
                #        self.enemy_list.remove(enemy)
                # Check if we are trying to walk on something nasty
                while(temp_going_to == bot["position"] and temp_going_to["x"]>0 and temp_going_to["x"]<=9 and temp_going_to["y"]>0 and temp_going_to["y"]<=9):
                    delta_x, delta_y = get_random_direction(self.enemy_list, current_position, first_going_to)
                    temp_going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}
                
                first_going_to = temp_going_to

            return temp_going_to["x"]-current_position["x"], temp_going_to["y"]-current_position["y"]

        return 0, 0
