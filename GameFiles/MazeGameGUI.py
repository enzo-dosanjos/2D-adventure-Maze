import tkinter as tk


class MazeGUI(tk.Tk):
    """A class for creating a graphical user interface (GUI) for displaying a maze.

    Attributes:
        maze (Maze): The maze object to be displayed in the GUI.
    """

    def __init__(self, maze):
        """Initializes the MazeGUI class.

        Args:
            maze (Maze): The maze object to be displayed in the GUI.
        """

    def draw_maze(self):
        """Draws the maze based on the grid provided by the maze object."""
