

class Flood:
  def __init__(self, board):
    self.snakes = board.snakes
    self.occupied_snakes = board.occupied_snakes
    self.occupied_food = board.occupied_food
    self.width = board.width
    self.height = board.height
    self.snakes_length = board.snakes_length
    self.floodfill = self.create_floodfill()

  @classmethod
  def create(cls, board):
    return cls(board)

  def is_cell_valid(self, cell):
    x, y = cell
    return 0 <= x < self.width and 0 <= y < self.height and not self.occupied_snakes[y][x]
    
  def get_adjacent_cells_list(self, start):
   x, y = start
   adjacent_cells = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
   return [cell for cell in adjacent_cells if self.is_cell_valid(cell)]

  def process_new_cell(self, cell, id, new_fill):
    self.visited[cell] = id
    new_fill.append(cell)
    return True

  def process_contested_cell(self, cell, id, other_id, new_fill):
    length = self.snakes_length[id] 
    other_length = self.snakes_length[other_id] 

    other_fill = self.fills[other_id][-1] 

    if cell in other_fill:
        if length > other_length: 
            other_fill.remove(cell) 
            return self.process_new_cell(cell, id, new_fill) 

        if length == other_length:
            other_fill.remove(cell) 
            return False

        return False

      

  def create_floodfill(self):
    self.visited = {}
    self.fills = [[[(snake.head["x"], snake.head["y"])]] for snake in self.snakes]
    current_depth_cells = set()
    has_new_cells = True
    while has_new_cells:
        has_new_cells = False
        
        for id, fill in enumerate(self.fills):
          if id == 0:
             current_depth_cells.clear()
          previous_fill = fill[-1]
          new_fill = []
          for previous_cell in previous_fill:
              adjacent_cells = self.get_adjacent_cells_list(previous_cell)
              for cell in adjacent_cells:
                if cell not in self.visited:
                    current_depth_cells.add(cell)
                    new_cell_found = self.process_new_cell(cell, id, new_fill)
                    has_new_cells = has_new_cells or new_cell_found
                else:
                    other_id = self.visited[cell]
                    if id != other_id and cell in current_depth_cells:
                      new_cell_found = self.process_contested_cell(cell, id, other_id, new_fill)
                      has_new_cells = has_new_cells or new_cell_found

          if new_fill:
             self.fills[id].append(new_fill)


    return self.fills
  



  
 
          
  
          