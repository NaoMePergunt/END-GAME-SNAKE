from board_class import Board
from cord_utils import CordCalc
from functools import partial

class Collision:
   def __init__(self, board, is_move_safe, potential_collision, potential_kill, dead_ends):
      self.snakes = board.snakes
      self.width = board.width
      self.height = board.height
      self.my_head = self.snakes[0].get_head()
      self.my_body = self.snakes[0].get_body()
      self.occupied_snakes = board.occupied_snakes
      self.is_move_safe = is_move_safe
      self.potential_collision = potential_collision
      self.potential_kill = potential_kill
      self.dead_ends = dead_ends
      self.cord_calc = CordCalc(board)
      self.get_adjacent_cells = partial(self.cord_calc.get_adjacent_cells_dict)
      self.is_depth_within_bounds = partial(self.cord_calc.is_depth_within_bounds)
    
      

   @classmethod
   def create(cls, board, is_move_safe, potential_collision, potential_kill, dead_ends):
      return cls(board, is_move_safe, potential_collision, potential_kill, dead_ends)
   
  
   def body_collision(self, move, depth1):
      x, y = depth1["x"], depth1["y"]
      if self.occupied_snakes[y][x]:
         self.is_move_safe[move] = False
          
   
   def head_on_collision(self, move, depth1, depth2):
      x, y = depth1["x"], depth1["y"]
      for snake in self.snakes[1:]:
          enemy_body = snake.get_body()
          enemy_head = enemy_body[0]
          if depth2 == enemy_head:
            if len(self.my_body) <= len(enemy_body):
               self.potential_collision[move] = True
               self.is_move_safe[move] = False
            elif len(self.my_body) > len(enemy_body):
               if not self.occupied_snakes[y][x]:
                  self.potential_kill[move] = True
          
   

   def check_collisions(self):
        for move, depth1 in self.get_adjacent_cells(self.my_head).items():
          is_next_cell_dead_end = True
          self.body_collision(move, depth1)
          for depth2 in self.get_adjacent_cells(depth1).values():
             self.head_on_collision(move, depth1, depth2)
             x2, y2 = depth2["x"], depth2["y"]
             is_depth_2_occupied = self.occupied_snakes[y2][x2]
             is_next_cell_dead_end = is_next_cell_dead_end and is_depth_2_occupied

          if is_next_cell_dead_end:
             self.is_move_safe[move] = False
             self.dead_ends[move] = True
             
                
    
 

   def check_out_of_bounds(self):
    my_head = self.my_head
    min_x = 0
    min_y = 0
    max_w = self.width - 1
    max_y = self.height - 1

    if my_head["x"] == max_w:
        self.is_move_safe["right"] = False
    if my_head["y"] == max_y:
        self.is_move_safe["up"] = False
    if my_head["x"] == min_x:
        self.is_move_safe["left"] = False
    if my_head["y"] == min_y:
        self.is_move_safe["down"] = False
