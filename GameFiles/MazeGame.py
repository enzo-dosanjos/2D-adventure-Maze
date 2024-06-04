import random
import csv
import time

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
            'maze': [],
            'maze_size': maze_size,
            'life': 3,
            'score': 0,
            'player_position': None,
            'monster_position': None,
            'traps': {},
            'treasure_position': None
        }

        self.start_time = time.time()

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

    def save_game(self, filename='savegame.csv'):
        """Save the game state to a CSV file.

        Args:
            filename (str): The name of the CSV file to save.
        """
        with open('./data/saves/' + filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write header
            writer.writerow(['maze', 'maze_size', 'life', 'score', 'player_position',
                             'monster_position', 'traps', 'treasure_position'])

            # write the data in the file necessary
            writer.writerow([
                self.game_state['maze'],
                self.game_state['maze_size'],
                self.game_state['life'],
                self.game_state['score'],
                self.game_state['player_position'],
                self.game_state['monster_position'],
                self.game_state['traps'],
                self.game_state['treasure_position']
            ])

        print(f"Game saved to {filename}")

    def parse_position(self, position_str):
        """Convert a string representation of a position back to a tuple."""
        if position_str == 'None':
            return None
        x, y = map(int, position_str.strip('()').split(','))
        return (x, y)

    def str_to_class(self, object_string):
        """
        Convert a string representation of an MazeCell object to an instance of the class.

        Parameters:
            object_string (str): The string representation of the object.

        Returns:
            MazeCell(x, y, type) (...): An instance of the MazeCell class.
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
            list_str (string): The string representation of a list.

        Returns:
            new_list (list): List containing that initial string.
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
            list_str (string): The string representation of a dictionary back to a dictionary.

        Returns:
            new_dict (dictionary): The dictionary containing this initial string. 
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
        """Load a saved game under CSV.

        Args:
            filename (str): The name of the CSV file to save.
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
                    'score': float(row[3]),
                    'player_position': self.parse_position(row[4]),  # Convert back to tuple
                    'monster_position': self.parse_position(row[5]),  # Convert back to tuple
                    'traps': self.parse_dict(row[6]),  # Convert back to list of tuples
                    'treasure_position': self.parse_position(row[7])  # Convert back to tuple
                }

                print(f"Game loaded from {filename}")

        except FileNotFoundError:
            print(f"No saved game found at {'./data/saves/' + filename}")

        except StopIteration:
            print(f"File {filename} is empty or corrupted")

    def update_score(self):
        """ Function updating the player's score.""" 
        self.game_state['score'] += time.time() - self.start_time
    
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

    def __repr__(self):
        """Custom string representation including the object's data. Needed to parse back it's data when loading a save.
        Returns:
            ...
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
