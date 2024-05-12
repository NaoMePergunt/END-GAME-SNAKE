from colorama import Fore, Style
from flood_class import Flood
from random import choice


class Snake:
  def __init__(self, id, health, length, body, head):
   self.id = id
   self.body = body
   self.health = health
   self.length = length
   self.head = head


  def __str__(self):
     return f"Snake:id={self.id}, health={self.health}, length={self.length}, body={self.body}, head={self.head})"

  @classmethod
  def create_from_game_state(cls, game_state):
   snakes_info = game_state["board"]["snakes"]
   my_id = game_state["you"]["id"]

   snakes = [
          cls(
         id = snake_data["id"],
         health = snake_data["health"],
         body = snake_data["body"],
         length = snake_data["length"],
         head = snake_data["head"],

      )
      for  snake_data in snakes_info
   ]
   for snake in snakes:
      if my_id == snake.id:
          snakes.remove(snake)
          snakes.insert(0, snake)


   return snakes

    

  def get_body(self):
     return self.body
  
  def get_head(self):
     return self.head
   
  def get_length(self):
     return self.length
    
  def get_id(self):
     return self.id
   
  def get_health(self):
     return self.health
   
  

class Board:
   def __init__(self, height, width, food, snakes):
    self.height = height
    self.width = width
    self.food = food
    self.snakes = snakes
    self.occupied_snakes = self.create_occupied_board()
    self.occupied_food = self.create_occupied_food()
    self.snakes_length = self.get_snakes_length()
    self.flood = Flood.create(self)
    self.fills = self.flood.create_floodfill()
    self.my_flood_grid = self.create_my_flood_grid()
    self.players_food = self.find_foods_by_player()


   @classmethod
   def create_from_game_state(cls, game_state):
       width = game_state["board"]["width"]
       height = game_state["board"]["height"]
       food = game_state["board"]["food"]
       snakes = Snake.create_from_game_state(game_state)
       return cls(width, height, food, snakes)
   
   @classmethod   
   def create_empty_grid(cls, width, height):
      return [[False for x in range(width)] for y in range(height)]
   
   def create_my_flood_grid(self):
      flood_grid = self.create_empty_grid(self.height, self.width)

      my_fill = self.fills[0]
      for depth in my_fill:
         for cell in depth:
            x, y = cell
            flood_grid[y][x] = True
      return flood_grid
            
   
   def create_occupied_board(self):
      occupied_snakes_grid = self.create_empty_grid(self.height, self.width)
      for snake in self.snakes:
         for body_part in snake.body[:-1]:
          x, y = body_part["x"], body_part["y"]
          occupied_snakes_grid[y][x] = True
      return occupied_snakes_grid
              
              
   def create_occupied_food(self):
      occupied_food_grid = self.create_empty_grid(self.height, self.width)
      for cor in self.food:
         x, y = cor["x"], cor["y"]
         occupied_food_grid[y][x] = True
      return occupied_food_grid
   
   def board_display(self):
         my_snake = self.snakes[0]
         enemy_snakes = self.snakes[1:]
         colors = ['RED', 'GREEN', 'YELLOW', 'MAGENTA', 'BLACK']
         snake_colors = [Fore.BLUE] + [Style.BRIGHT + getattr(Fore, choice(colors)) for i in range(len(enemy_snakes))]
         fills = self.fills
         new_board = []

         for y in range(self.height):
            new_row = ""
            for x in range(self.width):
                  for i, snake in enumerate([my_snake] + enemy_snakes):
                     if any((x, y) == (part["x"], part["y"]) for part in snake.body[:-1]):
                        if (x, y) == (snake.head["x"], snake.head["y"]):
                              new_row += snake_colors[i] + "3" + Style.RESET_ALL
                        else:
                              new_row += snake_colors[i] + "@" + Style.RESET_ALL
                        break
                  else:
                     for i, fill in enumerate(fills):
                        if any((x, y) in depth for depth in fill):
                          if self.occupied_food[y][x]:
                               new_row += snake_colors[i] + "F" + Style.RESET_ALL
                          else: 
                               new_row += snake_colors[i] + "." + Style.RESET_ALL
                          break
                              
                     else:
                        new_row += "."
                  new_row += " "
            new_board.append(new_row)

         return new_board[::-1]
     

   def get_snakes_length(self):
     snakes_length = []
     for snake in self.snakes:
       snakes_length.append(snake.length)
     return snakes_length
   
   def find_foods_by_player(self):
    found_food_by_player = []
    for fill in self.fills:
        player_food = []
        for depth in fill:
            for cell in depth:
                x, y = cell
                if self.occupied_food[y][x]:
                    player_food.append(cell)
        found_food_by_player.append(player_food)
    return found_food_by_player
    



