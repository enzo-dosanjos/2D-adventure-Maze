import math   # to compute euclidian distance
from GameFiles.Observer_Observable_logic import Observable

class Monster(Observable):
    """Class representing a monster in the maze game.

    Attributes:
        game_state (dict): Dictionary containing all necessary game state information
        maze (list): 2D list representing the maze
        maze_size (tuple): Dimensions of the maze
    """

    __slots__ = ['game_state', 'maze', 'maze_size']

    def __init__(self, game_state):
        """Initialize the Monster instance.

        Args:
            game_state (dict): Dictionary containing all necessary game state information
        """
        super().__init__()
        self.game_state = game_state

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        if game_state['monster_position'] is None:
            game_state['monster_position'] = self.init_monster_pos()

    def init_monster_pos(self):
        """initialise position of the monster, taking care that it doesn't choose wall coordinates.

        Returns:
            max_position (tuple): The initial position of the monster.
        """
        max_distance = 0
        max_position = None
        player_position = self.game_state['player_position']
    
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                # monster position inside maze 
                if self.maze[i][j].type != 'wall':
                    # find randomly genrated position in maze not on walls!
                    distance = math.sqrt((i - player_position[0]) ** 2 + (j - player_position[1]) ** 2)
                    if distance > max_distance:
                        max_distance = distance
                        max_position = (i, j)

        return max_position

    def reset_position(self):
        """ Reset monster position """
        self.game_state['monster_position'] = self.init_monster_pos()
    
    def move(self):  
        """ Determines the movement direction of the monster based on its new position relative to the previous one """
        path = self.shortest_path()
        prev_pos = self.game_state['monster_position']
        if len(path) > 1:
            # Move the monster along the shortest path
            self.game_state['monster_position'] = path[1]  # Move to the next position in the path

        if prev_pos[0] < self.game_state['monster_position'][0]:
            direction = 'Right'
        elif prev_pos[0] > self.game_state['monster_position'][0]:
            direction = 'Left'
        elif prev_pos[1] > self.game_state['monster_position'][1]:
            direction = 'Up'
        else:
            direction = 'Down'
        self.notify_observer("monster", direction)

    def shortest_path(self):
        """Compute the shortest path between the monster and the player using a BFS algo.

        Returns:
            path (list): The shortest path from the monster to the player.
        """

        done = set()  # use a set to get a O(1) time complexity in average for lookups
        queue = [self.game_state['monster_position']]
        parents = {self.game_state['monster_position']: self.game_state['monster_position']}

        while self.game_state['player_position'] not in done:
            cell = queue.pop(0)
            cell_obj = self.maze[cell[0]][cell[1]]

            done.add(cell)

            neighbors = cell_obj.get_cell_neighbors(self.maze, self.maze_size, "path")
            for neighbor in neighbors:
                if neighbor.coord not in done and neighbor.coord not in queue:
                    queue.append(neighbor.coord)
                    parents[neighbor.coord] = cell

        # Reconstruct the path from the player to the monster
        path = []
        cell = self.game_state['player_position']
        while cell != self.game_state['monster_position']:
            path.append(cell)
            cell = parents[cell]
        path.append(self.game_state['monster_position'])

        # reverse to get from the monster to the player
        path.reverse()

        return path