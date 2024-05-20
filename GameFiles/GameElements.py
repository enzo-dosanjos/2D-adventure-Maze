from Player import Player
from Maze import Maze
class Trap:
    """Class representing a trap .

    Attributes:
        trap_position (tuple): The position of the trap in the maze.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, trap_position):
        """Initialize the Trap instance.

        Args:
            trap_position (tuple): The position of the trap.
        Slots:
            activated (Boolean): the status of the trap set to deactivated.

        """
        super().__init__()
        self.trap_position = trap_position
        self.activated = False

    def activate_trap(self, player, maze_size, traps):
        """When the trap is activated.
        Return:
            activated (Boolean): the status of the trap set to activated.

        """
        dist = ((player.position[0] - self.trap_position[0]) ** 2 + (player.position[1] - self.trap_position[1]) ** 2) ** 0.5
        if dist <= 5 * self.maze_size / 100:
             self.activated = True
        return self.activated



class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        treasure_position (tuple): The position of the treasure in the maze.
    """

    def __init__(self, treasure_position):
        """Initialize the Treasure instance.

        Args:
            treasure_position (tuple): The position of the treasure.
        """
        super().__init__()
        self.treasure_position = treasure_position

    def treasure_reached(self, player):
        """When the treasure is reached."""
        if player.position == self.treasure_position:
            #display he's won this level 
