import random
import tkinter as tk
import csv
from colorama import init, Fore
init()
from MazeGameGUI import MazeGUI
from Monster import Monster

class Maze(tk.Tk):
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
        super().__init__()
        self.maze_size = maze_size
        self.maze = []
        self.walls = []
        for i in range(0, maze_size[0]):
            line = []
            for j in range(0, maze_size[1]):
                line.append(MazeCell(i, j, 'unchecked'))
            self.maze.append(line)

    def generate_maze(self):
        """Generate a random maze using Prim's MST algorithm."""
        # choose the coordinates at which the player starts randomly
        starting_coord = (random.randint(1, self.maze_size[0] - 2), random.randint(1, self.maze_size[1] - 2))
        self.maze[starting_coord[0]][starting_coord[1]] = MazeCell(starting_coord[0], starting_coord[1], 'path')

        # set the cells around to walls
        for j in range(-1, 2, 2):
            self.walls.append([starting_coord[0] + j, starting_coord[1]])
            self.maze[starting_coord[0] + j][starting_coord[1]] = MazeCell(starting_coord[0] + j, starting_coord[1], 'wall')
            self.walls.append([starting_coord[0], starting_coord[1] + j])
            self.maze[starting_coord[0]][starting_coord[1] + j] = MazeCell(starting_coord[0], starting_coord[1] + j, 'wall')

        # while there are walls still not checked
        while self.walls:
            # we select a random wall
            rand_wall = self.walls.pop(random.randint(0, len(self.walls) - 1))

            for j in range(-1, 2, 2):
                if rand_wall[1] > 0 and rand_wall[1] < self.maze_size[1] - 1:  # to avoid checking cells outside the maze
                    # we check if the 2 cells separated by the random wall are unchecked for one and a path for the other
                    if self.maze[rand_wall[0]][rand_wall[1] + j].type == 'unchecked' and self.maze[rand_wall[0]][rand_wall[1] - j].type == 'path':
                        neighbooring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self, 'path'))

                        # if the random wall have less than 2 neighbouring cell of the path type, then it becomes a path
                        if neighbooring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            # replace every neighbouring cell of unchecked type to a wall
                            for j in range(-1, 2, 2):
                                if self.maze[rand_wall[0] + j][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + j][rand_wall[1]] = MazeCell(rand_wall[0] + j, rand_wall[1],
                                                                                         'wall')
                                    self.walls.append([rand_wall[0] + j, rand_wall[1]])
                                if self.maze[rand_wall[0]][rand_wall[1] + j].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + j] = MazeCell(rand_wall[0], rand_wall[1] + j,
                                                                                         'wall')
                                    self.walls.append([rand_wall[0], rand_wall[1] + j])

                # same thing for the cell separated on the y axis
                if rand_wall[0] > 0 and rand_wall[0] < self.maze_size[0] - 1:
                    if self.maze[rand_wall[0] + j][rand_wall[1]].type == 'unchecked' and self.maze[rand_wall[0] - j][rand_wall[1]].type == 'path':
                        neighbooring_path = len(self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self, 'path'))

                        if neighbooring_path < 2:
                            self.maze[rand_wall[0]][rand_wall[1]] = MazeCell(rand_wall[0], rand_wall[1], 'path')

                            # replace every neighbouring cell of unchecked type to a wall
                            for j in range(-1, 2, 2):
                                if self.maze[rand_wall[0] + j][rand_wall[1]].type == 'unchecked':
                                    self.maze[rand_wall[0] + j][rand_wall[1]] = MazeCell(rand_wall[0] + j, rand_wall[1],
                                                                                         'wall')
                                    self.walls.append([rand_wall[0] + j, rand_wall[1]])
                                if self.maze[rand_wall[0]][rand_wall[1] + j].type == 'unchecked':
                                    self.maze[rand_wall[0]][rand_wall[1] + j] = MazeCell(rand_wall[0], rand_wall[1] + j,
                                                                                         'wall')
                                    self.walls.append([rand_wall[0], rand_wall[1] + j])

        # to remove the remaining unchecked cells
        for i in range(0, self.maze_size[0]):
            for j in range(0, self.maze_size[1]):
                if self.maze[i][j].type == 'unchecked':
                    self.maze[i][j].type = 'wall'
    def print_maze(self):
        """ make it easier to display the maze for the programmer """
        for i in range(0, len(self.maze)):
            for j in range(0, len(self.maze[0])):
                if self.maze[i][j].type == 'unchecked':
                    print(Fore.WHITE, f'{self.maze[i][j]}', end="")
                elif self.maze[i][j].type == 'path':
                    print(Fore.GREEN, f'{self.maze[i][j]}', end="")
                else:
                    print(Fore.RED, f'{self.maze[i][j]}', end="")
            print('\n')

    def save_game(self, filename):
        """Save the game state to a CSV file.

        Args:
            filename (str): The name of the CSV file to save.
        """
        #the game will be saved so that the player can continue the previous game or just start a new one

    def end_game(self):
        """ generate a new maze with a bigger size and more traps if the player wants to continue to the next level"""

    def reset_maze(self):
        """ check if the player's life is at zero and reset the maze if so"""

class MazeCell:
    """Class representing a cell in the maze.

    Attributes:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        type (String): string indicating the type of cell (wall or path).
        path_img (tk.PhotoImage): The image representing a path.
        wall_img (tk.PhotoImage): The image representing a wall.
    """

    def __init__(self, y, x, type):
        """Initialize the MazeCell instance.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            type (String): string indicating the type of cell (wall, path or unchecked).
        """
        self.coord = (y, x)
        self.type = type

    def __str__(self):
        """ make it easier to understand cell type when printing """
        if self.type == 'wall':
            return 'w'
        elif self.type == 'path':
            return 'p'
        else:
            return 'u'

    def get_cell_neighbors(self, maze, searched_type):
        """ Retrieve the neighbors of a certain type of the cell in the maze."""
        searched_cells_list = []
        if searched_type == "any":
            for j in range(-1, 2, 2):
                if 1 < self.coord[0] + j < maze.maze_size[0]:
                    searched_cells_list.append(maze.maze[self.coord[0] + j][self.coord[1]])
                if 1 < self.coord[1] + j < maze.maze_size[1]:
                    searched_cells_list.append(maze.maze[self.coord[0]][self.coord[1] + j])
        else:
            for j in range(-1, 2, 2):
                if 1 < self.coord[0] + j < maze.maze_size[0]:
                    if (maze.maze[self.coord[0] + j][self.coord[1]].type == searched_type):
                        searched_cells_list.append(maze.maze[self.coord[0] + j][self.coord[1]])
                if 1 < self.coord[1] + j < maze.maze_size[1]:
                    if (maze.maze[self.coord[0]][self.coord[1] + j].type == searched_type):
                        searched_cells_list.append(maze.maze[self.coord[0]][self.coord[1] + j])
        return searched_cells_list

def main():
    maze = Maze((27, 27))
    maze.generate_maze()
    # maze.print_maze()

    Gui = MazeGUI(maze)
    Gui.draw_maze()

    monster = Monster((25, 25))
    print(monster.shortest_path(maze, (2, 2)))

    Gui.mainloop()


if __name__ == "__main__":
    main()