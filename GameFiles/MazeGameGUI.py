import tkinter as tk


class MazeGUI(tk.Tk):
    """class for creating a graphical user interface (GUI).

    Attributes:
        maze (Maze): The maze object to be displayed in the GUI.
    """

    def __init__(self, maze):
        """Initializes the MazeGUI class.

        Args:
            maze (Maze): The maze object to be displayed in the GUI.
        """

    def draw_maze(self):
        """use the draw_cell method to draw every cells that forms the maze."""

    def draw_cell(self):
        """ draw a maze cell (a wall or a path) using canvas.draw_rectangle"""

    def init_gui(self):
        """put the health, level and time spent on a level on the player's screen
        using canvas.create_image for the hearth and simple create_text for the rest"""

    def update_gui(self):
        """ will update the number of hearth displayed when the player take damage"""

    def draw_player(self):
        """ draw the player's character on the canva using canva.create_image"""

    def player_move(self):
        """ animate the player's move using the player's sprite"""

    def player_attacked(self):
        """ animate the player when it is on the same cell as the monster"""
    def draw_GameElements(self):
        """ draw the treasure and traps using canvas.create_image"""

    def update_GameElements(self):
        """ change the game elements' picture when the player goes on their cell"""

    def draw_monster(self):
        """ draw the monster using canva.create_image"""

    def monster_move(self):
        """ animate the monster's move"""

    def monster_atack(self):
        """ animate the monster when it is on the same cell as the player"""

    def end_game(self):
        """ display a menu when the player reach the treasure displaying the level, time taken
        and one button to quit and one button to continue to the next level"""
