# -*- coding: utf-8 -*-
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
        #todo with a random position in the border of the maze
        return (1, 1)

    def get_input(self, event):
        """Get the player's input on its keyboard (up arrow, down arrow, left arrow, or right arrow).

        Args:
            event (tk.Event): The event object containing key press information.
        """
        direction = None
        if event.keysym == 'Up':
            direction = 'up'
        elif event.keysym == 'Down':
            direction = 'down'
        elif event.keysym == 'Left':
            direction = 'left'
        elif event.keysym == 'Right':
            direction = 'right'
        return direction

    def move_player(self, direction):
        """Change the player's character's coordinates depending on the player's input.

        Args:
            direction (str): The direction to move ('up', 'down', 'left', or 'right').
        """
        x, y = self.position
        if direction == 'up':
            new_position = (x - 1, y)
        elif direction == 'down':
            new_position = (x + 1, y)
        elif direction == 'left':
            new_position = (x, y - 1)
        elif direction == 'right':
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
            collision (boolean): True if there is a collision, False otherwise.
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