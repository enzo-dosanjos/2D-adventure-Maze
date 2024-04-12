class Monster:
    """Class representing a monster in the maze game.

    Attributes:
        position (tuple): The current position of the monster in the maze.
        monster_img (tk.PhotoImage): image representing the monster.
    """

    def __init__(self, position):
        """Initialize the Monster instance.

        Args:
            position (tuple): The initial position of the monster.
        """

    def move(self):
        """Move the monster according to the shortest path"""
        

    def shortest_path(self, player_coord):
        """compute the shortest path between the monster and the player
        Args:
            player_coord (tuple): The coordinate of the player

        """
        # using BFS algorithm