class Trap:
    """Class representing a trap .

    Attributes:
        position (tuple): The position of the trap in the maze.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, position):
        """Initialize the Trap instance.

        Args:
            position (tuple): The position of the trap.
        Slots:
            activated (Boolean): the status of the trap set to deactivated.

        """

    def activate_trap(self):
        """When the trap is activated.
        Return:
            activated (Boolean): the status of the trap set to activated.

        """


class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        position (tuple): The position of the treasure in the maze.
    """

    def __init__(self, position):
        """Initialize the Treasure instance.

        Args:
            position (tuple): The position of the treasure.
        """

    def treasure_reached(self):
        """When the treasure is reached."""
