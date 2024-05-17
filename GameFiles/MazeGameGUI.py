import tkinter as tk

class MazeGUI(tk.Tk):
    """Class for creating a graphical user interface (GUI) for the maze game.

    Attributes:
        maze (Maze): The maze object to be displayed in the GUI.
        cell_size (int): The size of each cell in pixels.
        canvas (tk.Canvas): The canvas to draw the maze and game elements.
        player_image (tk.PhotoImage): The image representing the player.
        monster_image (tk.PhotoImage): The image representing the monster.
        treasure_image (tk.PhotoImage): The image representing the treasure.
    """

    def __init__(self, maze):
        """Initializes the MazeGUI class.

        Args:
            maze (Maze): The maze object to be displayed in the GUI.
        """
        super().__init__()
        self.maze = maze
        self.cell_size = 20  # Adjust the cell size as needed
        self.canvas = tk.Canvas(self, width=self.maze.maze_size[1] * self.cell_size,
                                height=self.maze.maze_size[0] * self.cell_size)
        self.canvas.pack()

        # Load images for game elements
        self.player_image = tk.PhotoImage(file="../data/player.png")
        self.monster_image = tk.PhotoImage(file="../data/monster.png")
        self.treasure_image = tk.PhotoImage(file="../data/treasure.png")

    def draw_maze(self):
        """Draws the maze on the canvas."""
        for i in range(self.maze.maze_size[0]):
            for j in range(self.maze.maze_size[1]):
                cell = self.maze.maze[i][j]
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size

                if cell.type == 'wall':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif cell.type == 'path':
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")

    def draw_player(self):
        """Draws the player character on the canvas."""
        player_position = self.maze.player_position
        x, y = player_position[1] * self.cell_size, player_position[0] * self.cell_size
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)

    def draw_monster(self, position):
        """Draws the monster on the canvas.

        Args:
            position (tuple): The position of the monster in the maze (row, column).
        """
        x, y = position[1] * self.cell_size, position[0] * self.cell_size
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.monster_image)

    def draw_treasure(self, position):
        """Draws the treasure on the canvas.

        Args:
            position (tuple): The position of the treasure in the maze (row, column).
        """
        x, y = position[1] * self.cell_size, position[0] * self.cell_size
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.treasure_image)

    def clear_canvas(self):
        """Clears all elements from the canvas."""
        self.canvas.delete("all")

    def update_gui(self, player_position, monster_position, treasure_position):
        """Updates the GUI by drawing player, monster, and treasure.

        Args:
            player_position (tuple): The position of the player in the maze (row, column).
            monster_position (tuple): The position of the monster in the maze (row, column).
            treasure_position (tuple): The position of the treasure in the maze (row, column).
        """
        self.draw_player(player_position)
        self.draw_monster(monster_position)
        self.draw_treasure(treasure_position)

    def end_game_menu(self, level, time_taken):
        """Displays the end game menu with level info and buttons to quit or continue.

        Args:
            level (int): The level reached by the player.
            time_taken (float): The time taken by the player to complete the level.
        """
        # Create and display the end game menu using tkinter widgets
        pass  # Placeholder for the actual implementation
