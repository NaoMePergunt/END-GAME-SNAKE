#    _   __            __  ___     ____                              __     
#   / | / /___ _____  /  |/  /__  / __ \___  _________ ___  ______  / /____ 
#  /  |/ / __ `/ __ \/ /|_/ / _ \/ /_/ / _ \/ ___/ __ `/ / / / __ \/ __/ _ \
# / /|  / /_/ / /_/ / /  / /  __/ ____/  __/ /  / /_/ / /_/ / / / / /_/  __/
#/_/ |_/\__,_/\____/_/  /_/\___/_/    \___/_/   \__, /\__,_/_/ /_/\__/\___/ 
#                                              /____/                       
               


# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    my_head = game_state["you"]["body"][0]  # Coordinates of snake head
    my_neck = game_state["you"]["body"][1]  # Coordinates of snake neck
    

    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    ## gets the correct board border width and height coordinates and stores them in variables.
    max_w = board_width - 1
    max_y = board_height - 1
    min_x = 0
    min_y = 0


    ## prevents snake from going out of bounds by comparing my_head coordinates with the board coordinates.
    ## if coordinates match it means snake is at the border of the map, then updates is_move_safe to False.
    if my_head["x"] == max_w:
        is_move_safe["right"] = False
    if my_head["y"] == max_y:
        is_move_safe["up"] = False
    if my_head["x"] == min_x:
        is_move_safe["left"] = False
    if my_head["y"] == min_y:
        is_move_safe["down"] = False
    
    
    my_body = game_state['you']['body']
  
 
    #Prevent your Battlesnake from colliding with other Battlesnakes
    players = game_state['board']['snakes']
    all_players_bodys = [player_body["body"] for player_body in players]
    

    ## loops through each body in all players bodys.
    ## the function then loops through each body part and check if there is collision between my snake.
    ## if there is a collision it updates the is_move_safe dictionary accordingly.
    for body in all_players_bodys:
      check_collision(my_head, body, is_move_safe)
    
       


     ## loops through each key/move in is_move_safe.
     ## if the key returns True, it assigns the move and its coordinates to safe_move dictionary.
    adjacent_cells = get_adjcent_cells_cor(my_head)
    safe_moves = {}
    for move, isSafe in is_move_safe.items():
        if isSafe and move in adjacent_cells:
          safe_moves[move] = adjacent_cells[move]


    ## if there are no safe moves, snake moves down.
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    food = game_state['board']['food']

    priority_moves = []
    next_move = None

    ## loops through food coordinates and safe moves coordinates, then it compares if both coordinates match.
    for food_cor in food:
      for move, safe_cor in safe_moves.items():
       if food_cor["x"] == safe_cor["x"] and food_cor["y"] == safe_cor["y"]:
         
        ## If coordinates match, appends the corresponding move to priority_move list
         if my_head["x"] == food_cor["x"] + 1:
            priority_moves.append("left")
         elif my_head["x"] == food_cor["x"] - 1:   
            priority_moves.append("right")
         elif my_head["y"] == food_cor["y"] + 1:
            priority_moves.append("down")
         elif my_head["y"] == food_cor["y"] - 1:
            priority_moves.append("up")
    
        
    
         

    ## if there is a priority move, it chooses one randomly, if there inst, it chooses randomly from safe_moves.
    if len(priority_moves) > 0:
       next_move = random.choice(priority_moves)
    else:
       next_move = random.choice(list(safe_moves))
      



    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    



## a function that loops through each body_part. it checks if the body_parts collides with the head.
def check_collision(my_head, body, is_move_safe):
    enemy_head = body[0]
    adjacent_cells = get_adjcent_cells_cor(my_head)
    adjacent_cells_further = {
    "further_up": get_adjcent_cells_cor({"x": my_head["x"], "y": my_head["y"] + 1}),
    "further_down": get_adjcent_cells_cor({"x": my_head["x"], "y": my_head["y"] - 1}),
    "further_right": get_adjcent_cells_cor({"x": my_head["x"] + 1, "y": my_head["y"]}),
    "further_left": get_adjcent_cells_cor({"x": my_head["x"] - 1, "y": my_head["y"]})
    }
    for body_part in body[:-1]:
       for move, cor in adjacent_cells.items():
          if cor["x"] == body_part["x"] and body_part["y"] == cor["y"]:
             is_move_safe[move] = False

       

    for direction, moves in adjacent_cells_further.items():
      for move, cor in moves.items():
          if enemy_head["x"] == my_head["x"] and enemy_head["y"] == my_head["y"]:
            continue
          if cor["x"] == enemy_head["x"] and cor["y"] == enemy_head["y"]:
            is_move_safe[move] = False
        
        
     


      

                        


        
        
        
def get_adjcent_cells_cor(my_head):
  adjacent_cells_cor = {}
  adjacent_cells_cor["up"] = get_up_cor(my_head)
  adjacent_cells_cor["down"] = get_down_cor(my_head)
  adjacent_cells_cor["right"] = get_right_cor(my_head)
  adjacent_cells_cor["left"] = get_left_cor(my_head)
  return adjacent_cells_cor
  


def get_up_cor(my_head):
    return {"x": my_head["x"], "y": my_head["y"] + 1}

def get_down_cor(my_head):
   return {"x": my_head["x"], "y": my_head["y"] - 1}

def get_right_cor(my_head):
   return {"x": my_head["x"] + 1, "y": my_head["y"]}

def get_left_cor(my_head):
   return {"x": my_head["x"] - 1, "y": my_head["y"]}


  

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
