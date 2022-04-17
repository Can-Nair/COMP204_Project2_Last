'''
Authors: Can Nair, Bilge Kılıç, Yaşar Koray Keskin
Date: 12.04.2022
'''
# We shall use the numpy class for calculations
import numpy as np
# we use stddraw module as a substitude graphics library
import stddraw
# This class is used in order to create different and random tetrominos
import random
# This Class is used to create the game grid
from game_grid import GameGrid
from tetromino import Tetromino  # This class contains the various bluprints for our tetrominos
# We use this class for holding our game
import os  # We use this for file and directory operations
# color the game menu
from color import Color
from picture import Picture  # used representing images to display
# This class holds the function calls that are used to create the game
class Game:

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
    def start(self):
        grid_h, grid_w =12, 12 # We set the dimensions of the game grid
        game_w = 8 # These could have been different
   # set the size of the drawing canvas
        canvas_h, canvas_w = 55 * grid_h, (55 * grid_w)
        stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
        stddraw.setXscale(-0.5, grid_w - 0.5)
        stddraw.setYscale(-0.5, grid_h - 0.5)
        # An empty list used to store terominos
        self.tetrominos = list()
        self.round_count = 0  # Keeping the round count of the game
        # Creates 10 tetrominos and assigns them inside the self.tetrominos array
        self.create_tetromino(grid_h, game_w)

        # next tetromino to show on the side of the panel
        self.next_type = self.tetrominos[self.round_count + 1]
        # Moves the next tetromino rightside area to show the player
        self.next_type.move_pos(9, 5)

        # create the game grid
        grid = GameGrid(grid_h, grid_w)

        # create the first tetromino to enter the game grid
        # by using the create_tetromino function defined below
        current_tetromino = self.tetrominos[self.round_count]
        grid.current_tetromino = current_tetromino

        #variables to check what stage is game in
        self.restart = False
        self.is_paused = False
        self.is_finished = False
        self.game_over = False

        # display a simple menu before opening the game
        # by using the display_game_menu function defined below
        self.display_game_menu(grid_h, grid_w, grid)

        # the main game loop (keyboard interaction for moving the tetromino)
        while True:
            # print the next tetromino on the side of the screen
            grid.set_next(self.tetrominos[self.round_count + 1])
            # check user interactions via the keyboard
            if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
                key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
                # if the left arrow key has been pressed
                if key_typed == "left":
            # move the active tetromino left by one
                    current_tetromino.move(key_typed, grid)
                # if the right arrow key has been pressed
                elif key_typed == "right":
            # move the active tetromino right by one
                    current_tetromino.move(key_typed, grid)
                # if the down arrow key has been pressed
                elif key_typed == "down":
            # move the whole tetromino down immedietly
                    current_tetromino.move("jump", grid)
                elif key_typed == "up":
                    # rotate the tetromino
                    current_tetromino.rotation(grid, current_tetromino)
                # Check if user paused the game used keyboard by pressed 'p'
                elif key_typed == "escape":
                    # Pauses the game
                    self.is_paused = True
                    self.display_game_menu(grid_h, grid_w, grid)
         # clear the queue of the pressed keys for a smoother interaction
                stddraw.clearKeysTyped()

        # move the active tetromino down by one at each iteration (auto fall)
            not_placed = current_tetromino.move("down", grid)

      # place the active tetromino on the grid when it cannot go down anymore
            if not not_placed:
                #if the tetromino is placed play the block sound
                grid.block_sound()
                # update the game grid by locking the tiles of the landed tetromino
                self.game_over = grid.update_grid(current_tetromino.tile_matrix)
                # merge the matrix untill there is no tile to merge
                merge = 1
                while merge:
                    merge = self.check_merging(grid)

                    row_count = [0 for a in range(12)]
                    score = 0
                    for a in range(12):
                        temp = 0
                        for b in range(8):
                            if grid.tile_matrix[a][b] != None:
                                temp = temp + 1
                            else:
                                break
                        # If row is full, calculates total score in this row
                        if temp == 8:
                            score = 0
                            for b in range(8):
                                score += grid.tile_matrix[a][b].num
                                grid.tile_matrix[a][b] = None
                                row_count[a] = 1

                    for a in range(1, 12):
                        for b in range(8):
                            if a < 11 and b < 7 and a > 0:
                                if grid.tile_matrix[a][b + 1] == None:
                                    if grid.tile_matrix[a][b - 1] == None:
                                        if grid.tile_matrix[a + 1][b] == None:
                                            if grid.tile_matrix[a - 1][b] == None:
                                                if grid.tile_matrix[a][b] != None:
                                                    grid.tile_matrix[a][b].move(0, -1)
                                                    grid.tile_matrix[a - 1][b] = grid.tile_matrix[a][b]
                                                    grid.tile_matrix[a][b] = None
                                                    b -= 1
                    merge = self.check_merging(grid)
                    grid.score += score

                self.round_count += 1

                # print the current tetromino
                current_tetromino = self.tetrominos[self.round_count]
                grid.current_tetromino = current_tetromino
                # randomize the position the next tetromino will fall down
                current_tetromino.move_pos(random.randint(0,5), 12)
                #create a new tetromino
                self.create_tetromino(grid_h, game_w)
                # print the new tetromino on thr side
                self.tetrominos[self.round_count+1].move_pos(9, 5)
            #if the game is over show the restart menu
            if self.game_over:
                self.is_finished = True
                self.display_game_menu(grid_h, grid_w, grid)
            # if the restart is pressed clear the matrix and star over
            if self.restart:
                for a in range(0, 12):
                    for b in range(8):
                        grid.tile_matrix[a][b] = None
                self.restart = False
                grid.game_over = False
                current_tetromino = self.tetrominos[self.round_count]
                grid.current_tetromino = current_tetromino
                current_tetromino.move_pos(random.randint(0,5), 12)

      # display the game grid and the current tetromino
            grid.display()


    #check the whole matrix if there is a tile to merge
    def check_merging(self, grid):
        merged = False
        for a in range(0, 11):
            for b in range(8):
                if grid.tile_matrix[a][b] != None :
                    if grid.tile_matrix[a + 1][b] != None and grid.tile_matrix[a][b].num == grid.tile_matrix[a + 1][b].num:
                        # multiply the two tiles
                        grid.tile_matrix[a][b].num = grid.tile_matrix[a + 1][b].num  * grid.tile_matrix[a][b].num
                        # add the num of the tile that dissapeared to the score
                        grid.score += grid.tile_matrix[a+1][b].num
                        #delete the tile
                        grid.tile_matrix[a + 1][b] = None
                        # change the tile color
                        grid.tile_matrix[a][b].newcolor(grid.tile_matrix[a][b].num)
                        merged = True
        return merged


    # Function for creating random shaped tetrominoes to enter the game grid
    def create_tetromino(self, grid_height, grid_width):
        # type (shape) of the tetromino is determined randomly
        tetromino_types = ['I', 'O', 'Z', 'J', 'L', 'T', 'S']
        for i in range(3):
            random_index = random.randint(0, len(tetromino_types) - 1)
            self.random_type = tetromino_types[random_index]
            # create and return the tetromino
            tetromino = Tetromino(self.random_type, grid_height, grid_width)
            self.tetrominos.append(tetromino)

    # Function for displaying a simple menu before starting the game
    def display_game_menu(self, grid_height, grid_width, grid):
        # colors used for the menu
        background_color = Color(42, 69, 99)
        button_color = Color(25, 255, 228)
        text_color = Color(31, 160, 239)
        # clear the background canvas to background_color
        stddraw.clear(background_color)
        # get the directory in which this python code file is placed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # path of the image file
        img_file = current_dir + "/images/menu_image.png"
        # center coordinates to display the image
        img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
        # image is represented using the Picture class
        image_to_display = Picture(img_file)
        # display the image
        stddraw.picture(image_to_display, img_center_x, img_center_y)
        # dimensions of the start game button
        button_w, button_h = grid_width - 1.5, 2
        # coordinates of the bottom left corner of the start game button
        button_x, button_y = img_center_x - button_w / 2, 4
        # display the start game button as a filled rectangle
        stddraw.setPenColor(button_color)
        stddraw.filledRectangle(button_x, button_y, button_w, button_h)
        # display the text on the start game button
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(25)
        stddraw.setPenColor(text_color)

        #if the game is paused show the pause menuz
        if not self.is_finished and self.is_paused:
            stddraw.setPenColor(button_color)
            stddraw.filledRectangle(button_x, button_y - 3, button_w, button_h)
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(50)
            stddraw.setPenColor(text_color)


            stddraw.text(img_center_x, 5, "Continue")

            text1_to_display = "Restart"
            stddraw.text(img_center_x, 2, text1_to_display)
            # Displays restart-continue buttons
            while True:
                stddraw.show(50)
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    # Closes the menu end continue to game
                    if mouse_x >= button_x and mouse_x <= button_x + button_w:
                        if mouse_y >= button_y and mouse_y <= button_y + button_h:
                            self.is_paused = False
                            break
                        # Restarts the game
                        elif mouse_y >= button_y and mouse_y <= button_y + button_h:
                            self.is_paused = False
                            grid.score = 0
                            self.restart = True
                            break

        # if the game is finished show the restart menu
        elif self.is_finished:
            stddraw.setPenColor(Color(255, 255, 255))
            stddraw.text(img_center_x, 8, "Game Over")
            text1_to_display = "Restart"
            stddraw.text(img_center_x, 5, text1_to_display)
            while True:
                stddraw.show(50)
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    if mouse_x >= 0.26 and mouse_x <= 10.6:
                        if mouse_y >= 4.04 and mouse_y <=5.9 :
                            print(mouse_x, mouse_y)
                            self.is_paused = False
                            grid.score = 0
                            self.is_finished = False
                            self.game_over = False
                            self.restart = True
                            break

                            # resets the score
        else:
            stddraw.text(img_center_x, 5, "Start Game")
            # menu interaction loop
            while True:
                # display the menu and wait for a short time (50 ms)
                stddraw.show(50)
                # check if the mouse has been left-clicked
                if stddraw.mousePressed():
                    # get the x and y coordinates of the location at which the mouse has
                    # most recently been left-clicked
                    mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                    if mouse_x >= button_x and mouse_x <= button_x + button_w:
                        if mouse_y >= button_y and mouse_y <= button_y + button_h:
                            text1_to_display = "Start Game"
                            stddraw.text(img_center_x, 5, text1_to_display)
                            break
game = Game()
game.start()
