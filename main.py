#    _   __            __  ___     ____                              __     
#   / | / /___ _____  /  |/  /__  / __ \___  _________ ___  ______  / /____ 
#  /  |/ / __ `/ __ \/ /|_/ / _ \/ /_/ / _ \/ ___/ __ `/ / / / __ \/ __/ _ \
# / /|  / /_/ / /_/ / /  / /  __/ ____/  __/ /  / /_/ / /_/ / / / / /_/  __/
#/_/ |_/\__,_/\____/_/  /_/\___/_/    \___/_/   \__, /\__,_/_/ /_/\__/\___/ 
#                                              /____/                       
               


import random
import typing
from board_class import Snake, Board
from flood_class import Flood
from pathing_class import Pathing
from collision_class import Collision
from cord_utils import CordCalc



def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


def start(game_state: typing.Dict):
    print("GAME START")


def end(game_state: typing.Dict):
    print("GAME OVER\n")

   

def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    snakes = Snake.create_from_game_state(game_state)
    board = Board.create_from_game_state(game_state)
    flood = Flood.create(board)
    pathing = Pathing.create(board, flood)
    cord_calc = CordCalc(board)

    players_foods = board.players_food

    my_snake = snakes[0]
    my_head_dict = my_snake.get_head()
    my_head_tuple = (snakes[0].get_head()["x"], snakes[0].get_head()["y"])
    my_foods = players_foods[0]

    adjacent_cells = cord_calc.get_adjacent_cells_dict(my_head_dict)

    potential_collision = {}
    potential_kill = {}
    

    board_display = board.board_display()
    for row in board_display:
     print(row)


    collision = Collision.create(board, is_move_safe, potential_collision, potential_kill)
    collision.check_out_of_bounds()
    collision.check_collisions()

    
    safe_moves = calculate_safe_moves(is_move_safe, adjacent_cells)
    
    priority_moves = calculate_priority_moves(my_head_tuple, my_foods, pathing, potential_kill)
    next_move = choose_next_move(game_state, priority_moves, safe_moves, potential_collision)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}



def calculate_safe_moves(is_move_safe, adjacent_cells):
    safe_moves = {}
    for move, isSafe in is_move_safe.items():
        if isSafe and move in adjacent_cells:
            safe_moves[move] = adjacent_cells[move]
    return safe_moves
    
def calculate_priority_moves(my_head_tuple, my_foods, pathing, potential_kill):
    priority_moves = []
    if len(potential_kill) > 0:
        priority_moves.extend(potential_kill.keys())
    elif len(my_foods) > 0:
        priority_moves.append(pathing.get_move_towards_target(my_head_tuple, my_foods[0]))
    return priority_moves


def choose_next_move(game_state, priority_moves, safe_moves, potential_collision):
    if len(priority_moves) > 0:
        return random.choice(priority_moves)
    elif len(safe_moves) > 0:
        return random.choice(list(safe_moves))
    elif len(potential_collision) > 0:
        print(f"MOVE {game_state['turn']}: Potential collision move detected! Moving unsafe!")
        return random.choice(list(potential_collision))
    else:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving up!")
        return {"move": "up"}
  


if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })


