import tkinter as tk
from PIL import ImageTk, Image

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

        self.cell_size = 30  # Adjust the cell size

        # Load images for game elements
        self.player_image = Image.open("../data/player.png").convert("RGBA")
        self.monster_image = Image.open("../data/monster.png").convert("RGBA")
        self.treasure_image = Image.open("../data/treasure.png").convert("RGBA")

        self.title("Maze Game")

        self.main_window()

    def crop_images(self,  img, split, nb):
        """Crop given images to a certain part

       Args:
           img : Image to crop
           split (tuple) : number of parts in the image in height and width
           nb (tuple) : number of the wanted part in width and height
        """

        w, h = img.size

        left = (nb[0] - 1) * w / split[0]
        right = nb[0] * w / split[0]
        upper = (nb[1] - 1) * h / split[1]
        lower = nb[1] * h / split[1]

        ratio = 1/(h/self.cell_size)

        crop_img = img.crop([left, upper, right, lower])
        resized_img = crop_img.resize((int(w*ratio), int(h*ratio)))

        new_w, new_h = resized_img.size

        image = ImageTk.PhotoImage(resized_img)

        return image, new_w, new_h

    def main_window(self):
        """Main game window displaying the maze, hud, ..."""
        self.canvas = tk.Canvas(self, width=self.maze.maze_size[1] * self.cell_size,
                                height=self.maze.maze_size[0] * self.cell_size)
        self.canvas.pack()

        self.draw_maze()

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

    def draw_player(self, player):
        """Draws the player character on the canvas."""
        player_position = player.position
        self.player_image, w, h = self.crop_images(self.player_image, (4, 4), (1, 1))

        x, y = player_position[1] * self.cell_size + (self.cell_size/2 - w/2), player_position[0] * self.cell_size + (self.cell_size/2 - h/2)
        self.player = self.canvas.create_image(x, y, anchor=tk.NW, image=self.player_image)

    def draw_monster(self, monster):
        """Draws the monster on the canvas.

        Args:
            position (tuple): The position of the monster in the maze (row, column).
        """
        monster_position = monster.position
        self.monster_image, w, h = self.crop_images(self.monster_image, (4, 4), (1, 1))

        x, y = monster_position[1] * self.cell_size + (self.cell_size/2 - w/2), monster_position[0] * self.cell_size + (self.cell_size/2 - h/2)
        self.monster = self.canvas.create_image(x, y, anchor=tk.NW, image=self.monster_image)

    def draw_treasure(self, position):
        """Draws the treasure on the canvas.

        Args:
            position (tuple): The position of the treasure in the maze (row, column).
        """
        x, y = position[1] * self.cell_size, position[0] * self.cell_size
        self.treasure = self.canvas.create_image(x, y, anchor=tk.NW, image=self.treasure_image)

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
