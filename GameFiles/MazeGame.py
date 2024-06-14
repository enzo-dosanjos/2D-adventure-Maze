import random  # needed to generate the maze
import time  # needed to count the time taken to finish a level

# for file gestion
import os
import csv

# for easier to read maze display
from colorama import init, Fore
init()

from GameFiles.Observer_Observable_logic import Observable

class MazeGame(Observable):
    """
    Represents the main game logic handling the maze generation, game state, and interactions. Inherits from Observable to notify the observer when needed.

    Attributes:
    maze_size (tuple): Dimensions of the maze (width, height)
    player_position (tuple): position of the player within the maze as a tuple of integers (x, y)
    maze (list): A 2D list of MazeCell objects representing the structure and state of the maze
    game_state (dict): A dictionary containing all relevant game state variables including:
        - maze (list): Same as the class attribute 'maze'
        - maze_size (tuple): Same as the class attribute 'maze_size'
        - life (int): Number of lives the player has left
        - level (int): Current game level
        - score (float): Current score of the player
        - player_position (tuple): Same as the class attribute 'player_position'
        - monster_position (tuple): Position of the monster within the maze
        - traps (dict): Locations and states of traps within the maze
        - treasure_position (tuple): Location of the treasure within the maze
    """

    __slots__ = ['game_state', 'start_time', 'end', 'maze', 'maze_size']

    def __init__(self, maze_size=(12, 12)):
        """Initialize the MazeGame instance.

        Args:
            maze_size (tuple): Dimensions of the maze (width, height)
        """
        # initialise dictionary to save the game state at all time
        self.game_state = {
            'maze': [],
            'maze_size': maze_size,
            'life': 3,
            'level': 1,
            'score': 0,
            'player_position': None,
            'monster_position': None,
            'traps': {},
            'treasure_position': None
        }

        self.start_time = time.time()
        self.end = False

        # to access these variable more easily
        self.maze = self.game_state['maze']
        self.maze_size = self.game_state['maze_size']

    def generate_maze(self):
        """Generate a random maze layout using Prim's MST algorithm."""
        # initialise the maze list with 'unchecked cells
        walls = []
        for x in range(0, self.maze_size[0]):
            line = []
            for y in range(0, self.maze_size[1]):
                line.append(MazeCell(x, y, 'unchecked'))
            self.maze.append(line)

        # choose a random coordinate from which the algorithm will start
        starting_coord = (random.randint(1, self.maze_size[0] - 2), random.randint(1, self.maze_size[1] - 2))
        self.maze[starting_coord[0]][starting_coord[1]] = MazeCell(starting_coord[0], starting_coord[1], 'path')

        # set the cells around the randomly chosen coordinate to walls
        for offset in range(-1, 2, 2):
            walls.append([starting_coord[0] + offset, starting_coord[1]])
            self.maze[starting_coord[0] + offset][starting_coord[1]] = MazeCell(starting_coord[0] + offset, starting_coord[1], 'wall')
            walls.append([starting_coord[0], starting_coord[1] + offset])
            self.maze[starting_coord[0]][starting_coord[1] + offset] = MazeCell(starting_coord[0], starting_coord[1] + offset, 'wall')

        # while there are walls still not checked
        while walls:
            # we select a random wall
            rand_wall = walls.pop(random.randint(0, len(walls) - 1))

            for offset in range(-1, 2, 2):
                # on the x axis
                if 0 < rand_wall[0] < self.maze_size[0] - 1:  # to avoid checking cells outside the maze
                    # we check if the 2 cells separated by the random wall are unchecked for one and a path for the other
                    if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked' and self.maze[rand_wall[0] - offset][rand_wall[1]].type == 'path':
                        neighboring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, self.maze_size, 'path'))

                        # if the random wall have less than 2 neighbouring cell of the path type, then it becomes a path
                        if neighboring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            # replace every neighbouring cell of unchecked type to a wall as we did for the starting cell
                            for offset in range(-1, 2, 2):
                                if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + offset][rand_wall[1]] = MazeCell(rand_wall[0] + offset, rand_wall[1], 'wall')
                                    walls.append([rand_wall[0] + offset, rand_wall[1]])
                                if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + offset] = MazeCell(rand_wall[0], rand_wall[1] + offset, 'wall')
                                    walls.append([rand_wall[0], rand_wall[1] + offset])

                # same thing for the cell separated on the y axis
                if 0 < rand_wall[1] < self.maze_size[1] - 1:
                    if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked' and self.maze[rand_wall[0]][rand_wall[1] - offset].type == 'path':
                        neighboring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, self.maze_size, 'path'))

                        if neighboring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            for offset in range(-1, 2, 2):
                                if self.maze[rand_wall[0]][rand_wall[1] + offset].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + offset] = MazeCell(rand_wall[0], rand_wall[1] + offset, 'wall')
                                    walls.append([rand_wall[0], rand_wall[1] + offset])
                                if self.maze[rand_wall[0] + offset][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + offset][rand_wall[1]] = MazeCell(rand_wall[0] + offset, rand_wall[1], 'wall')
                                    walls.append([rand_wall[0] + offset, rand_wall[1]])

        # to remove the remaining unchecked cells, we convert them to walls
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

    def save_game(self, filename='savegame.csv'):
        """Save the current game state to a CSV file.

        Args:
            filename (str): The filename for saving the game state. Defaults to 'savegame.csv'.

        """
        # Check if the save file already exists and remove it if it does.
        if os.path.exists('./data/saves/' + filename):
            os.remove('./data/saves/' + filename)
        else:
            print("The file does not exist")

        # Open or create the CSV file and write the game state in it
        with open('./data/saves/' + filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write header
            writer.writerow(['maze', 'maze_size', 'life', 'score', 'player_position',
                             'monster_position', 'traps', 'treasure_position'])

            # write the data in the file
            writer.writerow([
                self.game_state['maze'],
                self.game_state['maze_size'],
                self.game_state['life'],
                self.game_state['level'],
                self.game_state['score'],
                self.game_state['player_position'],
                self.game_state['monster_position'],
                self.game_state['traps'],
                self.game_state['treasure_position']
            ])

    def parse_position(self, position_str):
        """
        Convert a string representation of a position back to a tuple. Used when loading game states.

        Args:
            position_str (str): The string representation of a position in the format '(x, y)'.

        Returns:
            tuple: The tuple representation of the position (x, y) or None if the input is 'None'.
        """

        if position_str == 'None':
            return None
        x, y = map(int, position_str.strip('()').split(','))
        return (x, y)

    def str_to_class(self, object_string):
        """
        Convert a string representation of an MazeCell object to an instance of the class

        Parameters:
            object_string (str): The string representation of the MazeCell object

        Returns:
            MazeCell(x, y, type): An instance of the MazeCell class initialized with the attributes extracted from the string
        """
        useful_data = object_string.strip('<>').split('=')  # to get a list of the key and values needed to recreate the object

        # get the coordinates and type of wall to recreate an instance with the same attributes
        if useful_data != [''] and useful_data != ['None']:
            x = int(useful_data[1].split(',')[0])
            y = int(useful_data[2].split(',')[0])
            type = useful_data[3]

            return MazeCell(x, y, type)


    def parse_list(self, list_str):
        """Convert a string representation of a list back to a list. Used for the maze list
        
        Args:
            list_str (string): The string representation of the maze list.

        Returns:
            new_list (list): A list of MazeCell objects.
        """
        if list_str == 'None':
            return None

        elif list_str == '[]':
            return []

        else:
            new_list = []
            for row in list_str.strip('[]').split('], ['):
                new_row = []
                for cell in row.strip('[]').split(', <'):
                    new_row.append(self.str_to_class(cell))
                new_list.append(new_row)

            return new_list

    def parse_dict(self, list_str):
        """Convert a string representation of a dictionary back to a dictionary. Used for the traps dictionary.
        
        Args:
            list_str (string): The string representation of a dictionary

        Returns:
            new_dict (dictionary): The dictionary of traps.
        """
        if list_str == 'None':
            return None

        elif list_str == '{}':
            return {}

        else:
            new_dict = {}
            for ind, row in enumerate(list_str.strip('{}').split(', (')):
                key_val = row.strip('\'').split(': ')

                val = key_val[1].strip('[]').split(',')

                # boolean
                if val[0] =='False':
                    activated = False
                else:
                    activated = True

                # tuple
                coord = key_val[0].strip('()').split(', ')

                new_dict[(int(coord[0]), int(coord[1]))] = [activated, int(val[1])]

            return new_dict

    def load_game(self, filename='savegame.csv'):
        """ Load a saved game in CSV format by restoring the state of the maze game.

        Args:
            filename (str): The name of the CSV file to load.
        """
        try:
            with open('./data/saves/' + filename, mode='r', newline='') as file:
                reader = csv.reader(file)

                next(reader)  # Skip header

                row = next(reader)
                self.game_state = {
                    'maze': self.parse_list(row[0]),  # Convert back to list of tuples
                    'maze_size': tuple(map(int, row[1].strip('()').split(','))),  # Convert back to tuple
                    'life': int(row[2]),
                    'level': int(row[3]),
                    'score': float(row[4]),
                    'player_position': self.parse_position(row[5]),  # Convert back to tuple
                    'monster_position': self.parse_position(row[6]),  # Convert back to tuple
                    'traps': self.parse_dict(row[7]),  # Convert back to list of tuples
                    'treasure_position': self.parse_position(row[8])  # Convert back to tuple
                }

        except FileNotFoundError:
            print(f"No saved game found at {'./data/saves/' + filename}")

        except StopIteration:
            print(f"File {filename} is empty or corrupted")

    def update_score(self):
        """ Function updating the player's score by taking the time that we stocked at the start of the level and removing the time at which the player loses or wins """
        self.game_state['score'] += time.time() - self.start_time

    def win_game(self):
        """ update the time taken and notify the observer to display the winning end game menu """
        self.end = True
        self.update_score()
        self.notify_observer("win")


    def lose_game(self):
        """ update the time taken and notify the observer to display the losing end game menu"""
        self.end = True
        self.update_score()
        self.notify_observer("lose")


class MazeCell:
    """Class representing a cell in the maze.

    Attributes:
        coord (tuple): The (x, y) coordinates of the cell
        type (str): The type of cell, which can be 'wall', 'path', or 'unchecked'
    """

    __slots__ = ['coord', 'type']

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
        """
        make it easier to understand cell type when printing

         Returns:
            str: A single character representing the type of the cell ('w' for wall, 'p' for path, 'u' for unchecked).
        """
        if self.type == 'wall':
            return 'w'
        elif self.type == 'path':
            return 'p'
        else:
            return 'u'

    def __repr__(self):
        """
        Custom string representation including the object's data. Needed to parse back it's data when loading a save.

        Returns:
            (string): A string representation of the object's data of the form: <x=<x coord>, y=<y coord>, type=<type>>
        """
        return f'<x={self.coord[0]}, y={self.coord[1]}, type={self.type}>'

    def get_cell_neighbors(self, maze, maze_size, searched_type):
        """ Retrieve the neighbors of a certain type of the cell in the maze.
        Args:
            maze (list): A 2D list representing the maze layout.
            maze_size (int): The size of the maze (number of cells in each dimension).
            searched_type (string): A string containing describing the type of studied object.
        
        Returns:
            searched_cells_list (list): The list of the searched cells.
        """
        searched_cells_list = []

        # if we don't look for a specific type of cell
        if searched_type == "any":
            for offset in range(-1, 2, 2):
                # add the neighbours on the y axis to the list
                if 0 <= self.coord[1] + offset < maze_size[1]:
                    searched_cells_list.append(maze[self.coord[0]][self.coord[1] + offset])
                # add the neighbours on the x axis to the list
                if 0 <= self.coord[0] + offset < maze_size[0]:
                    searched_cells_list.append(maze[self.coord[0] + offset][self.coord[1]])

        # if we look for a specific type of cell
        else:
            for offset in range(-1, 2, 2):
                # add the neighbours on the y axis to the list
                if 0 <= self.coord[1] + offset < maze_size[1]:
                    if maze[self.coord[0]][self.coord[1] + offset].type == searched_type:
                        searched_cells_list.append(maze[self.coord[0]][self.coord[1] + offset])
                # add the neighbours on the x axis to the list
                if 0 <= self.coord[0] + offset < maze_size[0]:
                    if maze[self.coord[0] + offset][self.coord[1]].type == searched_type:
                        searched_cells_list.append(maze[self.coord[0] + offset][self.coord[1]])
        return searched_cells_list
