import random
import math
class Player:
    """Class representing the player in the maze game.

    Attributes:
        lives (int): The number of lives the player has.
        maze (Maze): The maze object
        position (tuple): The current position of the player in the maze.
        game_state (dictionary): dictionary containing state of the game: amount of lives, position of the different elements, ...
    """

    def __init__(self, game_state):
        """Initialize the Player instance.

        Args:
            maze (Maze): The maze object.
            maze_size (tuple): tuple containing size in x and y.
            game_state (dictionary): dictionary containing state of the game: amount of lives, position of the different elements, ...
        """
        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        game_state['player_position'] = self.init_player_pos()
        self.position = game_state['player_position']


    def init_player_pos(self):
        """ Initialise the player position inside the border of the maze, taking care of not generating an
        initial position on the walls.

        Returns:
            coord (Tuple): the initial coordinates of the player chosen randomly in the maze's border.
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

    def check_collision(self, monsters, traps, treasure):
        """Check for collision of the player with game elements (traps, walls, treasure or monsters).

        Args:
            monsters (list): List of monsters in the maze.
            traps (list): List of traps in the maze.
            treasure (tuple): Position of the treasure.

        Returns:
            object (string): The object with which a collision happened.
            collision (boolean): True if there is a collision, False if there isn't.
        """
        for monster in monsters:
            if self.position == monster.position:
                self.lose_life()
                new_monster_position = self.init_monster_pos()
                new_monster = Monster(self.game_state)
                new_monster.position = new_monster_position
                monsters.append(new_monster)
                self.game_state['monsters'] = monsters
                return 'monster', True
            
        for trap in traps:
            if self.position == trap.trap_position and not trap.activated:
                trap.activate_trap(self, self.maze_size, traps)
                self.lose_life()
                new_trap_position = self.init_trap_position()
                new_trap = Trap(traps)
                new_trap.trap_position = new_trap_position
                traps.append(new_trap)
                self.game_state['traps'] = traps
                return 'trap', True

        if self.position == treasure.treasure_position:
            return 'treasure', True

        return None, False

    def lose_life(self):
        """Decrease the player's life by one and check for game over."""
        self.game_state['life'] -= 1
        if self.game_state['life'] <= 0:
            print("Game Over!")
            self.reset_game()
            # Here you could reset the maze or end the game.
