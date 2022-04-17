import stddraw # the stddraw module is used as a basic graphics library
from color import Color # used for coloring the tile and the number on it
from point import Point # class that stores the position of tiles
import math # we'll use this for logarith funtion
import numpy as np

# Class used for modeling numbered tiles as in 2048
class Tile:
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self, reference_point = Point(0, 0)):
      # Default tiles can gate between 2 and 4
      numbers = [2, 4]
      # Color scheme for ever tile number in order
      self.colors = [Color(239, 230, 221), Color(239, 227, 205), Color(247,178,123), Color(247,150,99), Color(247,124,90),
                Color(247,93,59), Color(239,205,115), Color(239,206,99), Color(239,198,82), Color(238,198,66), Color(239,194,49), Color(60,58,51)]
      #choose a random value between 2 and 4
      self.num = int(np.random.choice(numbers, 1))
      # set the colors of the tile
      self.background_color = self.colors[int(math.log2(self.num))-1] # background (tile) color
      self.foreground_color = Color(0, 100, 200) # foreground (number) color
      self.box_color = Color(187, 173, 160) # boundary (box) color
      # put the tile in it's given coordinet
      self.position = Point(reference_point.x, reference_point.y)

   # change the position of the tile
   def move(self, dx, dy):
      self.position.translate(dx, dy)

   # Method for drawing the tile
   def draw(self, length=1):
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(self.position.x, self.position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(self.position.x, self.position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(self.position.x, self.position.y, str(self.num))

   # Updates the background of the tile according to tile's number
   def newcolor(self, num):
      self.background_color = self.colors[int(math.log2(num)) - 1]