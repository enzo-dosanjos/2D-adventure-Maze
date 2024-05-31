import random
import csv
import tkinter as tk
from colorama import init, Fore
init()

class MazeGame():
    """Main application class for the Maze Game.

    Attributes:
        maze_size (int): The size of the maze (number of cells in each dimension).
        player_position (tuple): The current position of the player in the maze.
        maze (list): A 2D list representing the maze layout.
    """

    def __init__(self, maze_size):
        """Initialize the MazeGame instance.

        Args:
            maze_size (int): The size of the maze (number of cells in each dimension).
        """
        # initialise dictionary to save the game state at all time
        self.game_state = {
            'life': 3,
            'score': 0,
            'maze': [],
            'maze_size': maze_size,
            'player_position': None,
            'monster_position': None,
            'traps': None,
            'treasure_position': None
        }

        self.maze = self.game_state['maze']
        self.maze_size = self.game_state['maze_size']

        # initialise the maze list
        self.walls = []
        for x in range(0, maze_size[0]):
            line = []
            for y in range(0, maze_size[1]):
                line.append(MazeCell(x, y, 'unchecked'))
            self.maze.append(line)
           

    def generate_maze(self):
        """Generate a random maze using Prim's MST algorithm."""
        # choose the coordinates at which the player starts randomly
        starting_coord = (random.randint(1, self.maze_size[0] - 2), random.randint(1, self.maze_size[1] - 2))
        self.maze[starting_coord[0]][starting_coord[1]] = MazeCell(starting_coord[0], starting_coord[1], 'path')

        # set the cells around to walls
        for offset in range(-1, 2, 2):
            self.walls.append([starting_coord[0] + offset, starting_coord[1]])
            self.maze[starting_coord[0] + offset][starting_coord[1]] = MazeCell(starting_coord[0] + offset, starting_coord[1], 'wall')
            self.walls.append([starting_coord[0], starting_coord[1] + offset])
            self.maze[starting_coord[0]][starting_coord[1] + offset] = MazeCell(starting_coord[0], starting_coord[1] + offset, 'wall')

        # while there are walls still not checked
        while self.walls:
            # we select a random wall
            rand_wall = self.walls.pop(random.randint(0, len(self.walls) - 1))

            for offset in range(-1, 2, 2):
                if 0 < rand_wall[0] < self.maze_size[0] - 1:  # to avoid checking cells outside the maze
                    # we check if the 2 cells separated by the random wall are unchecked for one and a path for the other
                    if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked' and self.maze[rand_wall[0] - offset][rand_wall[1]].type == 'path':
                        neighboring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, self.maze_size, 'path'))

                        # if the random wall have less than 2 neighbouring cell of the path type, then it becomes a path
                        if neighboring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            # replace every neighbouring cell of unchecked type to a wall
                            for offset in range(-1, 2, 2):
                                if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + offset][rand_wall[1]] = MazeCell(rand_wall[0] + offset, rand_wall[1], 'wall')
                                    self.walls.append([rand_wall[0] + offset, rand_wall[1]])
                                if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + offset] = MazeCell(rand_wall[0], rand_wall[1] + offset, 'wall')
                                    self.walls.append([rand_wall[0], rand_wall[1] + offset])

                # same thing for the cell separated on the y axis
                if 0 < rand_wall[1] < self.maze_size[1] - 1:
                    if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked' and self.maze[rand_wall[0]][rand_wall[1] - offset].type == 'path':
                        neighboring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, self.maze_size, 'path'))

                        if neighboring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            # replace every neighbouring cell of unchecked type to a wall
                            for offset in range(-1, 2, 2):
                                if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + offset] = MazeCell(rand_wall[0], rand_wall[1] + offset, 'wall')
                                    self.walls.append([rand_wall[0], rand_wall[1] + offset])
                                if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + offset][rand_wall[1]] = MazeCell(rand_wall[0] + offset, rand_wall[1], 'wall')
                                    self.walls.append([rand_wall[0] + offset, rand_wall[1]])

        # to remove the remaining unchecked cells
        for y in range(0, self.maze_size[0]):
            for x in range(0, self.maze_size[1]):
                if self.maze[y][x].type == 'unchecked':
                    self.maze[y][x].type = 'wall'

    def print_maze(self):
        """make it easier to display the maze for the programmer"""
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[0])):
                if self.maze[y][x].type == 'unchecked':
                    print(Fore.WHITE, f'{self.maze[y][x]}', end="")
                elif self.maze[y][x].type == 'path':
                    print(Fore.GREEN, f'{self.maze[y][x]}', end="")
                else:
                    print(Fore.RED, f'{self.maze[y][x]}', end="")
            print('\n')

    def save_game(self, filename = 'savegame.csv'):
        """Save the game state to a CSV file.

        Args:
            filename (str): The name of the CSV file to save.
        """
        #todo
        #the game will be saved so that the player can continue the previous game or just start a new one 
        with open(filename, mode = 'w', newline='') as file:
            writer = csv.writer(file)
            #Write header
            writer.writerow(['player_name', 'lives', 'score', 'maze_type', 'player_position'])
            #Write game state
            writer.writerow(self.game_state['player_name'],
                            self.game_state['lives'],
                            self.game_state['score'],
                            self.game_state['maze_type'],
                            self.game_state['player_position'])
                    
        print(f"Game saved to {filename}")

    def load_game(self, filename = 'savegame.csv'):
        """Load a saved game under CSV.

        Args:
            filename (str): The name of the CSV file to save.

        Return
            state (dictionary): the state of loaded file (the previously saved game)
        """
        #todo
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                #Skip header
                next(reader)
                #Read game state 
                row = next(reader)
                state = {
                    'player_name': row[0],
                    'lives': int(row[1]), 
                    'score': int(row[2]),
                    'maze_type': row[3],
                    'player_position': row[4],
                    'monster_position': row[5],
                    'Traps': row[6],
                    'Treasure': row[7]
                }
                print("Game loaded from {filename}")
                return state 
        except FileNotFoundError:
            print(f"No saved game found at {filename}")
            return None
    
    def end_game(self):
        """ generate a new maze with a bigger size and more traps if the player wants to continue to the next level"""
        print("Well done, you have completed this level!")
        print("Moving to next level...")
        print("Resetting game...")
        #todo w/ menu
        

    def reset_maze(self):
        """ check if the player's life is at zero and reset the maze if so"""
        #todo
        print("Ohhh... Sorry love, you lost, game over... Resetting game now!")
        

class MazeCell:
    """Class representing a cell in the maze.

    Attributes:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        type (String): string indicating the type of cell (wall or path).
        path_img (tk.PhotoImage): The image representing a path.
        wall_img (tk.PhotoImage): The image representing a wall.
    """

    def __init__(self, x, y, type):
        """Initialize the MazeCell instance.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            type (String): string indicating the type of cell (wall, path or unchecked).
        """
        self.coord = (x, y)
        self.type = type

    def __str__(self):
        """ make it easier to understand cell type when printing """
        if self.type == 'wall':
            return 'w'
        elif self.type == 'path':
            return 'p'
        else:
            return 'u'

    def get_cell_neighbors(self, maze, maze_size, searched_type):
        """ Retrieve the neighbors of a certain type of the cell in the maze."""
        searched_cells_list = []
        if searched_type == "any":
            for offset in range(-1, 2, 2):
                if 0 <= self.coord[1] + offset < maze_size[1]:
                    searched_cells_list.append(maze[self.coord[0]][self.coord[1] + offset])
                if 0 <= self.coord[0] + offset < maze_size[0]:
                    searched_cells_list.append(maze[self.coord[0] + offset][self.coord[1]])
        else:
            for offset in range(-1, 2, 2):
                if 0 <= self.coord[1] + offset < maze_size[1]:
                    if maze[self.coord[0]][self.coord[1] + offset].type == searched_type:
                        searched_cells_list.append(maze[self.coord[0]][self.coord[1] + offset])
                if 0 <= self.coord[0] + offset < maze_size[0]:
                    if maze[self.coord[0] + offset][self.coord[1]].type == searched_type:
                        searched_cells_list.append(maze[self.coord[0] + offset][self.coord[1]])
        return searched_cells_list
