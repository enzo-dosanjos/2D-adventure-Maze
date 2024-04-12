class Trap:
    """Class representing a trap .

    Attributes:
        position (tuple): The position of the trap in the maze.
        trap_activated_img (tk.PhotoImage): The image representing the trap when activated.
        trap_deactivated_img (tk.PhotoImage): The image representing the trap when deactivated.
        activated (Boolean): the status of the trap (already activated or not).

    """

    def __init__(self, position, trap_activated_img, trap_deactivated_img, activated):
        """Initialize the Trap instance.

        Args:
            position (tuple): The position of the trap.
            trap_activated_img (tk.PhotoImage): The image representing the trap when activated.
            trap_deactivated_img (tk.PhotoImage): The image representing the trap when deactivated.
            activated (Boolean): the status of the trap (already activated or not).
        """

    def activate_trap(self):
        """When the trap is activated."""
        # make the player lose a heart and change the image of the trap


class Treasure:
    """Class representing the treasure in the maze game.

    Attributes:
        position (tuple): The position of the treasure in the maze.
        treasure_close_img (tk.PhotoImage): The image representing the treasure when closed.
        treasure_open_img (tk.PhotoImage): The image representing the treasure when oppened.
    """

    def __init__(self, position, treasure_close_img, treasure_open_img):
        """Initialize the Treasure instance.

        Args:
            position (tuple): The position of the treasure.
            treasure_close_img (tk.PhotoImage): The image representing the treasure when closed.
            treasure_open_img (tk.PhotoImage): The image representing the treasure when oppened.
        """

    def treasure_reached(self):
        """When the treasure is reached."""
        # the player wins , he will be asked if he preferes to continue to the next level or exit the game