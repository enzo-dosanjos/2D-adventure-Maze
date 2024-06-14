import random  # to randomly position elements
import math  # to compute euclidian dist


class GameElements:
    """
    Manages all game elements within the maze (traps and treasure)

    Attributes:
        game_state (dict): The state of the game containing all trap states and positions.
        treasure (Treasure): The treasure object
    """

    __slots__ = ['game_state', 'treasure']

    def __init__(self, game_state, nb_traps=5):
        """ Initialize every game elements in the maze

        Args:
            game_state (dict): The state of the game containing all trap states and positions
            nb_traps (int): Number of traps to initialize
        """

        self.treasure = Treasure(game_state)

        if game_state['traps'] == {}:
            for i in range(nb_traps):
                Trap(game_state)

class Trap:
    """ Class representing a trap

    Attributes:
        game_state (dict): Dictionary containing the traps states and positions
        trap_position (tuple): The coordinates of the trap within the maze
        activated (bool): Status indicating whether the trap has been activated
        type (int): Numerical identifier representing the type of trap
    """

    __slots__ = ['game_state', 'trap_position', 'activated', 'type']

    def __init__(self, game_state):
        """Initialize the Trap instance.

        Args:
            game_state (dict): Dictionary containing the traps states and positions
        """
        self.game_state = game_state

        self.trap_position = self.init_trap_position()
        self.activated = False
        self.type = random.randint(1, 3)  # Randomly assigns a type to the trap.

        self.game_state['traps'][self.trap_position] = [self.activated, self.type]

    def init_trap_position(self):
        """spawns a trap at a random position in the maze, avoiding walls, other traps, monster and player

        Return
            trap_pos (tuple): coordinates of the trap, x and y.
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
    """ Class representing the treasure in the maze game

    Attributes:
        game_state (dict): Dictionary containing the treasure position
    """

    __slots__ = ['game_state']

    def __init__(self, game_state):
        """Initialize the Treasure instance

        Args:
            game_state (dict): Dictionary containing the treasure position
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
