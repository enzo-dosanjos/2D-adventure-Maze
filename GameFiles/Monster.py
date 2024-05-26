import math

class Monster:
    """Class representing a monster in the maze game.

    Attributes:
        position (tuple): The current position of the monster in the maze.
        maze (Maze): The maze object
        player (Player): The player object.
    """

    def __init__(self, maze, player):
        """Initialize the Monster instance.

        Args:
            position (tuple): The initial position of the monster.
        """
        self.maze = maze
        self.player = player
        self.position = self.init_monster_pos()

    def init_monster_pos(self):
        #initialise position of the monster 
        max_distance = 0
        max_position = None
        player_position = self.player.position
    
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[0])):
                # monster position inside maze 
                if self.maze.maze[i][j].type != 'wall':
                    # find randomly genrated position in maze not on walls!
                    distance = math.sqrt((i - player_position[0]) ** 2 + (j - player_position[1]) ** 2)
                    if distance > max_distance:
                        max_distance = distance
                        max_position = (i, j)

        return max_position
    
    def move(self):  
        """Move the monster according to the shortest path.

        Returns:
            prev_pos: tuple with the coordinates of the previous position of the monster (x, y)
        """
        path = self.shortest_path()
        prev_pos = self.position
        if len(path) > 1:
            # Move the monster along the shortest path
            self.position = path[1]  # Move to the next position in the path
        return prev_pos

    def shortest_path(self):
        """Compute the shortest path between the monster and the player using a BFS algo.

        Returns:
            list: The shortest path from the monster to the player.
        """

        done = set()  # use a set to get a O(1) time complexity in average for lookups
        queue = [self.position]
        parents = {self.position: self.position}

        while self.player.position not in done:
            cell = queue.pop(0)
            cell_obj = self.maze.maze[cell[0]][cell[1]]

            done.add(cell)

            neighbors = cell_obj.get_cell_neighbors(self.maze, "path")
            for neighbor in neighbors:
                if neighbor.coord not in done and neighbor.coord not in queue:
                    queue.append(neighbor.coord)
                    parents[neighbor.coord] = cell

        # Reconstruct the path from the player to the monster
        path = []
        cell = self.player.position
        while cell != self.position:
            path.append(cell)
            cell = parents[cell]
        path.append(self.position)

        # reverse to get from the monster to the player
        path.reverse()

        return path
