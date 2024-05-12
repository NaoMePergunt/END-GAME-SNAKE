from queue import PriorityQueue

class Pathing:
  def __init__(self, board, flood):
      self.snakes = board.snakes
      self.board = board
      self.flood = flood
      self.fills = flood.floodfill
      self.get_adjacent_cells_list = self.flood.get_adjacent_cells_list 



  @classmethod
  def create(cls, board, flood):
      return cls(board, flood)
  
  def calc_manhattan_distance(self, start, target):
     return abs(start[0] - target[0]) + abs(start[1] - target[1]) 

  def determine_direction(self, current_cell, next_cell):
    move = []
    
    if current_cell[0] == next_cell[0] - 1:
        move.append("right")
    elif current_cell[0] == next_cell[0] + 1:   
        move.append("left")
    elif current_cell[1] == next_cell[1] - 1:
        move.append("up")
    elif current_cell[1] == next_cell[1] + 1:
        move.append("down")
    return move
  
  
  def find_shortest_path_to_target(self, start, target):
    allowed_moves = self.board.my_flood_grid
    start_heuristic = self.calc_manhattan_distance(start, target) 
    queue = PriorityQueue()
    queue.put((start_heuristic, start))
    cost_so_far = {start: 0}
    came_from = {}
    while queue:
        current_heuristic, current_cell = queue.get()  
        if current_cell == target:
           return start, target, came_from
        for next_cell in self.get_adjacent_cells_list(current_cell):  
            x, y = next_cell
            if allowed_moves[y][x]:
                new_cost = cost_so_far[current_cell] + 1
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]: 
                    cost_so_far[next_cell] = new_cost 
                    came_from[next_cell] = current_cell
                    new_heuristic = new_cost + self.calc_manhattan_distance(next_cell, target)  
                    queue.put((new_heuristic, next_cell))

  

  def reconstruct_path(self, start, target):
      start, target, came_from = self.find_shortest_path_to_target(start, target)
      path = [target]
      while path[-1] != start:
          path.append(came_from[path[-1]])
      path.reverse()
      return path
  

  def get_move_towards_target(self, start, target):
     path_to_target = self.reconstruct_path(start, target)
     next_move = self.determine_direction(path_to_target[0], path_to_target[1])
     return next_move[0]
     



        
      
     
     
       

          
     
  
  
  
                    