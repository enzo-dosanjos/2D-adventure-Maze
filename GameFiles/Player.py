import random
import math
from GameFiles.Monster import Monster
class Player:
    """Class representing the player in the maze game.

    Attributes:
        lives (int): The number of lives the player has.
        maze (Maze): The maze object
        position (tuple): The current position of the player in the maze.
    """

    def __init__(self, game_state):
        """Initialize the Player instance.

        Args:
            maze (Maze): The maze object.
        """
        self.game_state = game_state

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        game_state['player_position'] = self.init_player_pos()


    def init_player_pos(self):
        """ Initialise the player position inside the border of the maze

        Returns:
            coord (Tuple): the initial coordinates of the player chosen randomly in the maze's border
        """
        border = 1 / 10
        coord = [0, 0]

        while self.maze[coord[0]][coord[1]].type == "wall":
            coord = []

            for j in range(2):
                pos_init = random.randint(0, math.floor(2*(self.maze_size[j]-1) * border) - 1)
                list_border = []

                for i in range(1, math.ceil(self.maze_size[j] * border)):
                    list_border += [i]

                for i in range(math.floor(self.maze_size[j] * (1 - border)), (self.maze_size[j])):
                    list_border += [i]

                coord += [list_border[pos_init]]

        return tuple(coord)

    def check_collision(self):
        """Check for collision of the player with game elements or the monster.

        Returns:
            object (string): The object with which a collision happened.
            collision (boolean): True if there is a collision, False if there isnt.
        """
        if self.game_state['player_position'] == self.game_state['monster_position']:
            self.lose_life()
            new_monster = Monster(self.game_state)
            self.game_state['monster_position'] = new_monster.init_monster_pos()
            print(self.game_state)
            return 'monster', True
            
        # for trap in traps:
        #     if self.position == trap.trap_position and not trap.activated:
        #         trap.activate_trap(self, self.maze_size, traps)
        #         self.lose_life()
        #         new_trap_position = self.init_trap_position()
        #         new_trap = Trap(traps)
        #         new_trap.trap_position = new_trap_position
        #         traps.append(new_trap)
        #         self.game_state['traps'] = traps
        #         return 'trap', True

        if self.game_state['player_position'] == self.game_state['treasure_position']:
            return 'treasure', True

        return None, False

    def lose_life(self):
        """Decrease the player's life by one and check for game over."""
        self.game_state['life'] -= 1
        if self.game_state['life'] <= 0:
            print("Game Over!")
            self.reset_game()
            # Here you could reset the maze or end the game.
