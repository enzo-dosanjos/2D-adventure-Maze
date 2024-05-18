import random
import tkinter as tk
import csv
from colorama import init, Fore
init()
from collections import deque
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
            maze_size (tuple): The size of the maze (number of cells in each dimension).
        """
        super().__init__()
        self.maze_size = maze_size
        self.maze = []
        self.walls = []
        self.player_position = None
        for i in range(0, maze_size[0]):
            line = []
            for j in range(0, maze_size[1]):
                line.append(MazeCell(i, j, 'unchecked'))
            self.maze.append(line)

    def generate_maze(self):
        """Generate a random maze using Prim's MST algorithm."""
        # choose the coordinates at which the player starts randomly
        starting_coord = (random.randint(1, self.maze_size[0] - 2), random.randint(1, self.maze_size[1] - 2))
        self.player_position = starting_coord
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
                        neighbooring_path = self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, 'path')

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
                        neighbooring_path = self.maze[rand_wall[0]][rand_wall[1]].get_cell_neighbors(self.maze, 'path')

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

    def draw_maze(self):
        """Draw the maze on the canvas."""

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
        """Return a string representation of the cell."""
        if self.type == 'wall':
            return 'w'
        elif self.type == 'path':
            return 'p'
        else:
            return 'u'

    def get_cell_neighbors(self, maze, searched_type):
        """Retrieve the neighbors of a certain type of the cell in the maze."""
        searched_cells = 0
        for j in range(-1, 2, 2):
            if maze[self.coord[0] + j][self.coord[1]].type == searched_type:
                searched_cells += 1
            if maze[self.coord[0]][self.coord[1] + j].type == searched_type:
                searched_cells += 1
        return searched_cells

maze = Maze((11, 27))
maze.generate_maze()
maze.print_maze()



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

    def init_gui(self):
        """Initializes the GUI by drawing the maze."""
        self.clear_canvas()
        self.draw_maze()

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
        
class Monster:
    """Class representing a monster in the maze game.

    Attributes:
        position (tuple): The current position of the monster in the maze.
        monster_img (tk.PhotoImage): image representing the monster.
    """

    def __init__(self, position):
        """Initialize the Monster instance.

        Args:
            position (tuple): The initial position of the monster.
        """
        self.position = position
        self.monster_img = tk.PhotoImage(file="monster.png")  # Adjust the file path as needed

    def move(self, maze):
        """Move the monster according to the shortest path.

        Args:
            maze (list): The 2D list representing the maze layout.
        """
        player_position = maze.player_position
        path = self.shortest_path(maze.maze, player_position)
        if path:
            # Move the monster along the shortest path
            self.position = path[1]  # Move to the next position in the path

    def shortest_path(self, maze, player_coord):
        """Compute the shortest path between the monster and the player.

        Args:
            maze (list): The 2D list representing the maze layout.
            player_coord (tuple): The coordinate of the player.

        Returns:
            list: The shortest path from the monster to the player.
        """
        queue = deque([(self.position, [self.position])])
        visited = set()

        while queue:
            current_position, path = queue.popleft()
            if current_position == player_coord:
                return path
            if current_position not in visited:
                visited.add(current_position)
                neighbors = self.get_neighbors(maze, current_position)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

    def get_neighbors(self, maze, position):
        """Get neighboring positions of a given position in the maze.

        Args:
            maze (list): The 2D list representing the maze layout.
            position (tuple): The current position in the maze.

        Returns:
            list: A list of neighboring positions.
        """
        neighbors = []
        row, col = position
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + dr, col + dc
            if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != 'wall':
                neighbors.append((r, c))
        return neighbors
        
def main():
    # Create an instance of the Maze class
    maze = Maze((11, 27))
    maze.generate_maze()

    # Create an instance of the MazeGUI class
    gui = MazeGUI(maze)

    # Initialize the GUI and start the main loop
    gui.init_gui()
    gui.mainloop()


if __name__ == "__main__":
    main()