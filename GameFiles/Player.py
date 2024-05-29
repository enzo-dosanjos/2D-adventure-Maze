import random
import math
class Player:
    """Class representing the player in the maze game.

    Attributes:
        lives (int): The number of lives the player has.
        maze (Maze): The maze object
        position (tuple): The current position of the player in the maze.
    """

    def __init__(self, maze):
        """Initialize the Player instance.

        Args:
            maze (Maze): The maze object.
        """

        self.maze = maze
        self.lives = 3
        self.position = self.init_player_pos()


    def init_player_pos(self):
        """ Initialise the player position inside the border of the maze

        Returns:
            coord (Tuple): the initial coordinates of the player chosen randomly in the maze's border
        """
        border = 1 / 10
        coord = [0, 0]

        while self.maze.maze[coord[0]][coord[1]].type == "wall":
            coord = []

            for j in range(2):
                pos_init = random.randint(0, math.floor(2*(self.maze.maze_size[j]-1) * border) - 1)
                list_border = []

                for i in range(1, math.ceil(self.maze.maze_size[j] * border)):
                    list_border += [i]

                for i in range(math.floor(self.maze.maze_size[j] * (1 - border)), (self.maze.maze_size[j])):
                    list_border += [i]

                coord += [list_border[pos_init]]

        return tuple(coord)

    def check_collision(self, monsters, traps, treasure):
        """Check for collision of the player with game elements or the monster.

        Args:
            monsters (list): List of monsters in the maze.
            traps (list): List of traps in the maze.
            treasure (tuple): Position of the treasure.

        Returns:
            object (string): The object with which a collision happened.
            collision (boolean): True if there is a collision, False if there isnt.
        """
        for monster in monsters:
            if self.position == monster.position:
                return 'monster', True
        for trap in traps:
            if self.position == trap:
                return 'trap', True
        if self.position == treasure:
            return 'treasure', True
        return None, False

    def lose_life(self):
        """Use the check collision method with the monster or a trap to make the player lose a heart."""
        self.lives -= 1
        if self.lives <= 0:
            print("Game Over!")
            reset_game()
            # Here you could reset the maze or end the game.
