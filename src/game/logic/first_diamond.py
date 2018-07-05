import random
from ..util import get_direction


class FirstDiamondLogic(object):
    def __init__(self):
        self.goal_position = None
        self.next_pos = None

    def get_random_direction(self, bots):
        me = None
        new_cords = ()
        for bot in bots:
            if bot["name"] == "webjocke":
                me = bot
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

        if self.next_pos:
            current_position = board_bot["position"]
            self.goal_position = {"x":current_position["x"]+self.next_pos[0],"y":current_position["y"]+self.next_pos[1]}
            self.next_pos = None
        # Analyze new state
        elif board_bot["diamonds"] == 5:
            # Move to base if we are full of diamonds
            base = board_bot["base"]
            self.goal_position = base
        else:
            me = board_bot["position"]
            lowest_dist = None
            best_dia = None
            for dia in board.diamonds:
                if best_dia == None:
                    x_len = abs(me["x"]-dia["x"])
                    y_len = abs(me["y"]-dia["y"])
                    dist = x_len+y_len
                    lowest_dist = dist
                    best_dia = dia
                else:
                    x_len = abs(me["x"]-dia["x"])
                    y_len = abs(me["y"]-dia["y"])
                    dist = x_len+y_len
                    if dist < lowest_dist:
                        lowest_dist = dist
                        best_dia = dia

            # Move towards first diamond on board
            self.goal_position = best_dia

        '''
        else:
            # Move towards first diamond on board
            self.goal_position = board.diamonds[0]
        '''

        if self.goal_position:
            # Calculate move according to goal position
            current_position = board_bot["position"]
            delta_x_1, delta_y_1 = get_direction(current_position["x"], current_position["y"], self.goal_position["x"], self.goal_position["y"])
            delta_x, delta_y = 0, 0
            
            going_to = {"x":current_position["x"]+delta_x_1,"y":current_position["y"]+delta_y_1}
            list_of_bad = board.bots
            list_of_bad.extend(board.gameObjects)
            for bot in list_of_bad:
                while(going_to == bot["position"] or going_to["x"] < 0 or going_to["y"] < 0):
                    temp = board.bots
                    print("================ TEMP =================")
                    print(temp)
                    print("================ TEMP =================")
                    delta_x, delta_y = self.get_random_direction(temp)
                    going_to = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}

            #self.next_pos = [delta_x_1, delta_y_1]
            going_to_second = {"x":current_position["x"]+delta_x,"y":current_position["y"]+delta_y}

            return delta_x, delta_y

        return 0, 0
