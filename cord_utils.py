
class CordCalc:
  def __init__(self, board):
    self.snakes = board.snakes
    self.height = board.height
    self.width = board.width

 
  def get_adjacent_cells_dict(self, coordinate):
    adjacent_cells_cor = {}
    adjacent_cells_cor["up"] = self.get_up_cor(coordinate)
    adjacent_cells_cor["down"] = self.get_down_cor(coordinate)
    adjacent_cells_cor["right"] = self.get_right_cor(coordinate)
    adjacent_cells_cor["left"] = self.get_left_cor(coordinate)
    valid_cells = {}
    for direction, cor in adjacent_cells_cor.items():
       x, y = cor["x"], cor["y"]
       if 0 <= x < self.width and 0 <= y < self.height:
          valid_cells[direction] = cor
    return valid_cells
   
  def get_up_cor(self, coordinate):
     return {"x": coordinate["x"], "y": coordinate["y"] + 1}
  def get_down_cor(self, coordinate):
     return {"x": coordinate["x"], "y": coordinate["y"] - 1}
  def get_right_cor(self, coordinate):
     return {"x": coordinate["x"] + 1, "y": coordinate["y"]}
  def get_left_cor(self, coordinate):
     return {"x": coordinate["x"] - 1, "y": coordinate["y"]}
  
  def is_depth_within_bounds(self, depth):
    x, y = depth["x"], depth["y"]
    return 0 <= x < self.width and 0 <= y < self.height