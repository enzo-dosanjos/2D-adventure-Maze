class GameElements:
    def __init__(self, nb_traps):
        """Initialize every game elements in the maze"""

        self.nb_traps = nb_traps

        self.traps = []
        for i in range(nb_traps):
            self.traps.append(Trap(self.traps))

        self.treasure = Treasure()

class Trap:
    """Class representing a trap .

    Attributes:
        trap_position (tuple): The position of the trap in the maze.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, list_traps):
        """Initialize the Trap instance.

        Slots:
            activated (Boolean): the status of the trap set to deactivated.

        """
        super().__init__()
        self.traps = list_traps
        self.trap_position = self.init_trap_position()
        self.activated = False

    def init_trap_position(self):
        """spawns a trap at a random position in the maze"""
        # todo and take into acount the coordinates of th already existing traps in self.traps

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

    def __init__(self):
        """Initialize the Treasure instance.

        Args:
            treasure_position (tuple): The position of the treasure.
        """
        super().__init__()
        self.treasure_position = self.init_treasure_position()

    def init_treasure_position(self):
        """spawns the treasure at a random position in the maze"""
        #todo by simply generating 2 random numbers

    def treasure_reached(self, player, gui):
        """When the treasure is reached."""
        if player.position == self.treasure_position:
            gui.draw_win_state()
