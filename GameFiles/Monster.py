import tkinter as tk
from collections import deque

class Monster:
    """Class representing a monster in the maze game.

    Attributes:
        position (tuple): The current position of the monster in the maze.
        maze (Maze): The maze object
    """

    def __init__(self, maze):
        """Initialize the Monster instance.

        Args:
            position (tuple): The initial position of the monster.
        """
        self.maze = maze
        self.position = self.init_monster_pos()

    def init_monster_pos(self):
        #todo using an eucledian distance to the player
        return (25, 25)
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
            maze : Maze object
            player_coord (tuple): The coordinate of the player.

        Returns:
            list: The shortest path from the monster to the player.
        """

        done = []
        queue = [self.position]
        parents = {self.position: self.position}

        while player_coord not in done:
            cell = queue.pop(0)
            cell_obj = maze.maze[cell[0]][cell[1]]

            done.append(cell)

            neighbors = cell_obj.get_cell_neighbors(maze, "path")
            for neighbor in neighbors:
                if neighbor.coord not in done and neighbor.coord not in queue:
                    queue.append(neighbor.coord)
                    parents[neighbor.coord] = cell

        path = [player_coord]
        while cell != self.position:
            cell = parents[cell]
            path.append(cell)

        return path