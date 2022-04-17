import stddraw as stddraw  # stddraw is used as a basic graphics library
import os
from color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import pygame

# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(206, 195, 181)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(187, 173, 160)
        self.box_color = Color(187, 173, 160)
      # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.008
        self.box_thickness = 0.015
        self.score = 0
        self.pos = Point()
        # initiliaze pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

    # Method used for displaying the game grid
    def display(self):
      # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
      # draw the current/active tetromino if it is not None (the case when the
      # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
            self.next_tetromino.draw()

        # draw a box around the game grid
        self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(250)

    def block_sound (self):
        music = pygame.mixer.music.load(os.path.join('notification.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

   # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
      # for each cell of the game grid
        for row in range(12):
            for col in range(8):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] != None:
                    self.tile_matrix[row][col].draw()

        # Draws the main score on the top right of the main game screen
        stddraw.setPenRadius(150)
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.text(9.5, 11, "SCORE")
        stddraw.text(9.5, 10, str(self.score))

        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)

        # x and y ranges for the game grid
        start_x, end_x = -0.5, 8-0.5
        start_y, end_y = -0.5, self.grid_height
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.box_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.rectangle(pos_x, pos_y, 8.1, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have
      # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # change the next tetromino to the one after that
    def set_next(self, next_tetromino):
        self.next_tetromino = next_tetromino
   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock):
        # place all the tiles of the stopped tetromino onto the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
            # place each tile onto the game grid
                if tiles_to_lock[row][col] != None:
                    pos = tiles_to_lock[row][col].position
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True
        # return the game_over flag
        return self.game_over

