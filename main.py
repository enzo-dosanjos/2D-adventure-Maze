import tkinter as tk
import csv

class Maze(tk.Tk):
    """Main application class for the Maze Game.

    Attributes:
        maze_size (int): The size of the maze (number of cells in each dimension).
        cell_size (int): The size of each cell in pixels.
        player_position (tuple): The current position of the player in the maze.
        maze (list): A 2D list representing the maze layout.
        canvas (tk.Canvas): The canvas widget for drawing the maze.
    """

    def __init__(self, maze_size, cell_size):
        """Initialize the MazeGame instance.

        Args:
            maze_size (int): The size of the maze (number of cells in each dimension).
            cell_size (int): The size of each cell in pixels.
        """
        super().__init__()

    def generate_maze(self):
        """Generate a random maze."""

    def draw_maze(self):
        """Draw the maze on the canvas."""

    def save_game(self, filename):
        """Save the game state to a CSV file.

        Args:
            filename (str): The name of the CSV file to save.
        """

class MazeCell:
    """Class representing a cell in the maze.

    Attributes:
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.
        type (String): string indicating the type of cell (wall or path).
        path_img (tk.PhotoImage): The image representing a path.
        wall_img (tk.PhotoImage): The image representing a path.
    """

    def __init__(self, x, y, type):
        """Initialize the MazeCell instance.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            type (String): string indicating the type of cell (wall or path).
        """


class Player:
    """Class representing the player in the maze game.

    Attributes:
        position (tuple): The current position of the player in the maze.
        image (tk.PhotoImage): The image representing the player.
    """

    def __init__(self, position, image):
        """Initialize the Player instance.

        Args:
            position (tuple): The initial position of the player.
            image (tk.PhotoImage): The image representing the player.
        """

    def get_input(self):
        """get the player's input on its keyboard (up arrow, down arrow, left arrow or right arrow)

        Return:
            direction (String): direction the player clicked
        """

    def move_player(self, direction):
        """Move the player in the specified direction.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """

    def check_collision(self, x, y):
        """Check for collision at the specified position.

        Args:
            x (int): The x-coordinate of the position to check.
            y (int): The y-coordinate of the position to check.

        Returns:
            object (string): the object with which a collision happened
            collision (boolean): True if there is a collision, False otherwise.
        """

class Monster:
    """Class representing a monster in the maze game.

    Attributes:
        position (tuple): The current position of the monster in the maze.
        monster_img (tk.PhotoImage): image representing the monster.
    """

    def __init__(self, position, monster_img):
        """Initialize the Monster instance.

        Args:
            position (tuple): The initial position of the monster.
            monster_img (tk.PhotoImage): image representing the monster.
        """

    def move(self):
        """Move the monster according to the shortest path"""

    def shortest_path(self):
        """compute the shortest path between the monster and the player"""

class Trap:
    """Class representing a trap .

    Attributes:
        position (tuple): The position of the trap in the maze.
        trap_activated_img (tk.PhotoImage): The image representing the trap when activated.
        trap_deactivated_img (tk.PhotoImage): The image representing the trap when deactivated.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, position, trap_activated_img, trap_deactivated_img, activated):
        """Initialize the Trap instance.

        Args:
            position (tuple): The position of the trap.
            trap_activated_img (tk.PhotoImage): The image representing the trap when activated.
            trap_deactivated_img (tk.PhotoImage): The image representing the trap when deactivated.
            activated (Boolean): the status of the trap (already activated or not).
        """

    def activate_trap(self):
        """When the trap is activated."""
        # make the player lose a heart and change the image of the trap


class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        position (tuple): The position of the treasure in the maze.
        treasure_close_img (tk.PhotoImage): The image representing the treasure when closed.
        treasure_open_img (tk.PhotoImage): The image representing the treasure when oppened.
    """

    def __init__(self, position, treasure_close_img, treasure_open_img):
        """Initialize the Treasure instance.

        Args:
            position (tuple): The position of the treasure.
            treasure_close_img (tk.PhotoImage): The image representing the treasure when closed.
            treasure_open_img (tk.PhotoImage): The image representing the treasure when oppened.
        """

    def treasure_reached(self):
        """When the treasure is reached."""
