from tile import Tile  # used for modeling each tile on the tetromino
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # module for generating random values/permutations
import numpy as np  # the fundamental Python module for scientific computing

# Class used for modeling tetrominoes with 3 out of 7 different types/shapes
# as (I, O and Z)
class Tetromino:
   # Constructor for creating a tetromino with a given type (shape)
    def __init__(self, type, grid_height, grid_width):
        self.type = type
        #create height and width parameters
        self.grid_height = grid_height
        self.grid_width = grid_width
        # set the shape of the tetromino based on the given type
        self.occupied_tiles = []
        if type == 'I':
            n = 4  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino I in its initial orientation
            self.occupied_tiles.append((1, 0))  # (column_index, row_index)
            self.occupied_tiles.append((1, 1))
            self.occupied_tiles.append((1, 2))
            self.occupied_tiles.append((1, 3))
        elif type == 'O':
            n = 2  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino O in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((1, 1))
        elif type == 'Z':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
            self.occupied_tiles.append((2, 1))
        elif type == 'J':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
            self.occupied_tiles.append((1, 2))
            self.occupied_tiles.append((0, 2))
        elif type == 'L':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((0, 2))
            self.occupied_tiles.append((1, 2))
        elif type == 'T':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 0))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
        elif type == 'S':
            n = 3  # n = number of rows = number of columns in the tile matrix
            # shape of the tetromino Z in its initial orientation
            self.occupied_tiles.append((0, 1))
            self.occupied_tiles.append((2, 0))
            self.occupied_tiles.append((1, 0))
            self.occupied_tiles.append((1, 1))
            # create a matrix of numbered tiles based on the shape of the tetromino
        self.tile_matrix = np.full((n, n), None)
        # initialize the position of the tetromino (the bottom left cell in the
        # tile matrix) with a random horizontal position above the game grid
        self.bottom_left_cell = Point()
        self.bottom_left_cell.y = grid_height
        self.bottom_left_cell.x = random.randint(0, grid_width - n)
        # create the four tiles (minos) of the tetromino and place these tiles
        # into the tile matrix
        for i in range(len(self.occupied_tiles)):
            col_index, row_index = self.occupied_tiles[i][0], self.occupied_tiles[i][1]
            self.tile_matrix[row_index][col_index] = Tile(self.get_cell_position(row_index, col_index))

    def get_cell_position(self, row, col):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        position = Point()
        # horizontal position of the cell
        position.x = self.bottom_left_cell.x + col
        # vertical position of the cell
        position.y = self.bottom_left_cell.y + (n - 1) - row
        return position
    # Method for drawing the tetromino on the game grid
    def draw(self):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
        for row in range(n):
            for col in range(n):
            # draw each occupied tile (not equal to None) on the game grid
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw()

    # Method for moving the tetromino in a given direction by 1 on the game grid
    def move(self, direction, game_grid):
        n = len(self.tile_matrix)
        # check if the tetromino can be moved in the given direction by using the
        if(direction == "jump"):
            if not (self.can_be_moved("down", game_grid)):
                return False  # tetromino cannot be moved in the given direction
        else:
            if not (self.can_be_moved(direction, game_grid)):
                return False
      # the tetromino cannot be moved in the given direction
      # move the tetromino by updating the position of the bottom left cell in
      # the tile matrix
        if direction == "left":
            self.bottom_left_cell.x -= 1
        elif direction == "right":
            self.bottom_left_cell.x += 1
        elif direction == "jump":
            self.bottom_left_cell.y -= 1
        else:  # direction == "down"
            self.bottom_left_cell.y -= 1
        #move tiles in wanted firection
        for a in range(n):
            for b in range(n):
                if self.tile_matrix[a][b] != None:
                    if direction == "left":
                        self.tile_matrix[a][b].move(-1, 0)
                    elif direction == "right":
                        self.tile_matrix[a][b].move(1, 0)
                    elif direction == "jump":
                        self.tile_matrix[a][b].move(0, -1)
                    else:
                        self.tile_matrix[a][b].move(0, -1)
        #if the jump pressed call the jump function
        if (direction == "jump"):
            self.move("jump", game_grid)
        return True  # successful move in the given direction

    #change the position of the tetromino
    def move_pos(self, dx, dy):
        # select a pivot point for everys hape of tetromino
        pivot_point = Point()
        if self.type == 'I':
            pivot_point.x = self.tile_matrix[1][1].position.x
            pivot_point.y = self.tile_matrix[1][1].position.y
        elif self.type == 'O':
            pivot_point.x = self.tile_matrix[0][0].position.x
            pivot_point.y = self.tile_matrix[0][0].position.y
        elif self.type == 'Z':
            pivot_point.x = self.tile_matrix[0][0].position.x
            pivot_point.y = self.tile_matrix[0][0].position.y
        elif self.type == 'J':
            pivot_point.x = self.tile_matrix[2][1].position.x
            pivot_point.y = self.tile_matrix[2][1].position.y
        elif self.type == 'L':
            pivot_point.x = self.tile_matrix[0][0].position.x
            pivot_point.y = self.tile_matrix[0][0].position.y
        elif self.type == 'T':
            pivot_point.x = self.tile_matrix[0][0].position.x
            pivot_point.y = self.tile_matrix[0][0].position.y
        elif self.type == 'S':
            pivot_point.x = self.tile_matrix[0][1].position.x
            pivot_point.y = self.tile_matrix[0][1].position.y
        #move the tile according to the pivot point
        for m in self.tile_matrix:
            for p in m:
                if p != None:
                    p.move(dx-pivot_point.x, dy-pivot_point.y)


    # rotate tetrominos
    def rotation(self, game_grid, current_tetromino):
        n = len(self.tile_matrix)
        copy_matrix = np.copy(self.tile_matrix)
        #rotate the tetromino inside its own matrix
        for r in range(n):
            for c in range(n):
                self.tile_matrix[c][n - 1 - r] = copy_matrix[r][c]
        #rotate the matrix inside the whole game game matrix
        for r in range(n):
            for c in range(n):
                # if there is a tile move it to its new position
                if self.tile_matrix[r][c] is not None:
                    self.tile_matrix[r][c].move(-r + c, -c + (n - r))
                    #if the new rotation is out of the bounds of game matrix move it inside one step
                    if self.tile_matrix[r][c].position.x < 0:
                        for i in range(0-self.tile_matrix[r][c].position.x):
                            current_tetromino.move("right", game_grid)
                    elif self.tile_matrix[r][c].position.x >= 12:
                        for i in range(self.tile_matrix[r][c].position.x-11):
                            current_tetromino.move("left", game_grid)


    # Method to check if the tetromino can be moved in the given direction or not
    def can_be_moved(self, dir, game_grid):
        n = len(self.tile_matrix)  # n = number of rows = number of columns
      # check for moving left or right
        if dir == "left" or dir == "right":
            for row in range(n):
                for col in range(n):
                    # direction = left --> check the leftmost tile of each row
                    if dir == "left" and self.tile_matrix[row][col] is not None:
                        leftmost = self.tile_matrix[row][col].position
                        # tetromino cannot go left if any leftmost tile is at x = 0
                        if leftmost.x == 0:
                            return False
                        # skip each row whose leftmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if leftmost.y >= self.grid_height:
                            break
                  # the tetromino cannot go left if the grid cell on the left of
                  # any leftmost tile is occupied
                        if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                            return False
                        break  # end the inner for loop
                    # direction = right --> check the rightmost tile of each row
                    elif dir == "right" and self.tile_matrix[row][n - 1 - col] is not None:
                        rightmost = self.tile_matrix[row][n - 1 - col].position
                  # the tetromino cannot go right if any rightmost tile is at
                  # x = grid_width - 1
                        if rightmost.x == self.grid_width - 1:
                            return False
                        # skip each row whose rightmost tile is out of the game grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if rightmost.y >= self.grid_height:
                            break
                  # the tetromino cannot go right if the grid cell on the right
                  # of any rightmost tile is occupied
                        if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                            return False
                        break  # end the inner for loop
        # direction = down --> check the bottommost tile of each column
        else:
            for col in range(n):
                for row in range(n - 1, -1, -1):
                    if self.tile_matrix[row][col] is not None:
                        bottommost = self.tile_matrix[row][col].position
                        # skip each column whose bottommost tile is out of the grid
                        # (possible for newly entered tetrominoes to the game grid)
                        if bottommost.y > self.grid_height:
                            break
                        # tetromino cannot go down if any bottommost tile is at y = 0
                        if bottommost.y == 0:
                            return False
                            # or the grid cell below any bottommost tile is occupied
                        if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                            return False
                        break  # end the inner for loop
        return True  # tetromino can be moved in the given direction
