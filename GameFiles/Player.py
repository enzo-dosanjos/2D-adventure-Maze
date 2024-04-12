class Player:
    """Class representing the player in the maze game.

    Attributes:
        position (tuple): The current position of the player in the maze.
        image (tk.PhotoImage): The image representing the player.
    """

    def __init__(self, position, image):
        """Initialize the Player instance.

        Args:
            position (tuple): The initial position of the player.
        """

    def get_input(self):
        """get the player's input on its keyboard (up arrow, down arrow, left arrow or right arrow)

        Return:
            direction (String): direction the player clicked
        """

    def move_player(self, direction):
        """change the player's character's coordinates depending on the player's input

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """

    def check_collision(self):
        """Check for collision of the player with game elements or the monster.

        Returns:
            object (string): the object with which a collision happened
            collision (boolean): True if there is a collision, False otherwise.
        """

    def lose_life(self):
        """ use the check collision method with the monster or a trap to make the player lose a hearth"""