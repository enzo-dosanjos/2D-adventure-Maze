import random
import math
class Player:
    """Class representing the player in the maze game.

    Attributes:
        lives (int): The number of lives the player has.
        maze (Maze): The maze object
        position (tuple): The current position of the player in the maze.
        border (float): The max distance from the border of the maze for initializing position of the player
    """

    def __init__(self, maze):
        """Initialize the Player instance.

        Args:
            maze (Maze): The maze object.
        """

        self.maze = maze
        self.lives = 3
        self.border = 1/8
        self.position = self.init_player_pos()


    def init_player_pos(self):
        coord = [0, 0]
        done_x = []
        done_y = []
        while self.maze.maze[coord[0]][coord[1]].type == "wall":
            coord = []
            for j in range(2):
                posi_init = random.randint(0, int(2*(self.maze.maze_size[j]-1) * self.border) -1 )
                liste_border = []
                for i in range (1, math.ceil(self.maze.maze_size[j] * self.border)):
                    liste_border += [i]
                for i in range (math.floor(self.maze.maze_size[j] * (1-self.border)), (self.maze.maze_size[j]) - 1):
                    liste_border += [i]

                coord += [liste_border[posi_init]]

            done_y.append(coord[0])
            done_x.append(coord[1])
        return coord


    def move_player(self, event):
        """Change the player's character's coordinates depending on the player's input.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """
        x, y = self.position
        if event.keysym == 'Up':
            new_position = (x - 1, y)
        elif event.keysym == 'Down':
            new_position = (x + 1, y)
        elif event.keysym == '<Left>':
            new_position = (x, y - 1)
        elif event.keysym == '<Right>':
            new_position = (x, y + 1)
        else:
            new_position = self.position

        if self.maze.maze[new_position[0]][new_position[1]].type != 'wall':
            self.position = new_position

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
            # Here you could reset the maze or end the game.
