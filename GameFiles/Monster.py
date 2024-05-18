import tkinter as tk
from collections import deque

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
        self.monster_img = tk.PhotoImage(file="../data/monster.png")  # Adjust the file path as needed

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
        """Compute the shortest path between the monster and the player using a BFS algo.

        Args:
            maze (list): The 2D list representing the maze layout.
            player_coord (tuple): The coordinate of the player.

        Returns:
            list: The shortest path from the monster to the player.
        """

        done = []
        queue = [self.position]

        while queue:
            cell = queue.pop(0)
            cell = maze[cell[0]][cell[1]]

            done.append(cell)

            neighbors = cell.get_cell_neighbors(maze, "any")
            for neighbor in neighbors:
                if neighbor.coord not in done and neighbor.coord not in queue:
                    queue.append(neighbor.coord)

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