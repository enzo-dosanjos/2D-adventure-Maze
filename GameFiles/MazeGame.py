import tkinter as tk
import csv

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

    def generate_maze(self):
        """Generate a random maze using kruskal's MST algorithm."""

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

    def __init__(self, x, y, type):
        """Initialize the MazeCell instance.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            type (String): string indicating the type of cell (wall or path).
        """

    def get_cell_neighbors(self):
        """ Retrieve the neighbors of the cell in the maze."""
