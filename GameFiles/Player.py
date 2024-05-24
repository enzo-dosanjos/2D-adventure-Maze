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
        self.border = 1/10

    def init_player_pos(self):
        #todo with a random position in the border of the maze
        posi_init = random.randint(0, 2*self.maze.maze_size*self.border)
        liste_border = []
        for i in range (0, self.maze.maze_size * self.border):
            liste_border += i
        for i in range (self.maze.maze_size - self.border, self.maze.maze_size):
            liste_border += i

        return (liste_border[posi_init], liste_border[posi_init])


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
