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
            image (tk.PhotoImage): The image representing the player.
        """

    def get_input(self):
        """get the player's input on its keyboard (up arrow, down arrow, left arrow or right arrow)

        Return:
            direction (String): direction the player clicked
        """

    def move_player(self, direction):
        """Move the player in the specified direction.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """

    def check_collision(self, x, y):
        """Check for collision at the specified position.

        Args:
            x (int): The x-coordinate of the position to check.
            y (int): The y-coordinate of the position to check.

        Returns:
            object (string): the object with which a collision happened
            collision (boolean): True if there is a collision, False otherwise.
        """