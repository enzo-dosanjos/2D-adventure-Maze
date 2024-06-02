import random
import math

class GameElements:
    def __init__(self, game_state, nb_traps):
        """Initialize every game elements in the maze

        Attributes:
            nb_traps (int): The number of traps in the game.
        """

        self.treasure = Treasure(game_state)

        for i in range(nb_traps):
            Trap(game_state)

class Trap:
    """Class representing a trap.

    Attributes:
        trap_position (tuple): The position of the trap in the maze.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, game_state):
        """Initialize the Trap instance.

        Slots:
            activated (Boolean): the status of the trap set to disactivated.

        """
        self.game_state = game_state

        self.trap_position = self.init_trap_position()
        self.activated = False

        self.game_state['traps'][self.trap_position] = self.activated

    def init_trap_position(self):
        """spawns a trap at a random position in the maze.

        Return
            trap_pos (tuple) = Contains the position of the coordinates of the traps, x and y.
        """
        trap_pos = ()

        x = 0
        y = 0

        max_distance = math.sqrt((0.1 * self.game_state['maze_size'][0])**2 + (0.1 * self.game_state['maze_size'][1])**2)
        distance = max_distance
        while self.game_state['maze'][x][y].type != 'path' or trap_pos in self.game_state['traps'].keys() \
                or trap_pos == self.game_state['treasure_position'] or trap_pos == self.game_state['monster_position'] \
                or distance <= max_distance:   # check position to avoid overlaping objects and check distance to player to avoid putting traps to close
            x = random.randint(1, self.game_state['maze_size'][0] - 2)
            y = random.randint(1, self.game_state['maze_size'][1] - 2)
            trap_pos = (x, y)

            distance = math.sqrt((x - self.game_state['player_position'][0]) ** 2 + (y - self.game_state['player_position'][1]) ** 2)

        return trap_pos



class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        treasure_position (tuple): The position of the treasure in the maze.
    """

    def __init__(self, game_state):
        """Initialize the Treasure instance.

        Args:
            treasure_position (tuple): The position of the treasure in the maze.

        """
        self.game_state = game_state

        if game_state['treasure_position'] is None:
            game_state['treasure_position'] = self.init_treasure_position()


    def init_treasure_position(self):
        """Spawns the treasure at a random position in the maze, taking care that it doesn't appear on walls.

        Returns:
            (x,y) (tuple): position of the treasure in the maze as a tuple of x position and y position.
        """
        x = 0
        y = 0
        while self.game_state['maze'][x][y].type != 'path':
            x = random.randint(1, self.game_state['maze_size'][0] - 2)
            y = random.randint(1, self.game_state['maze_size'][1] - 2)
        return (x, y)
