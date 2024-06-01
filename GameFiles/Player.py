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
        self.game_state = game_state
        self.gui = None
        self.monster = None
        self.mazeGame = None

        self.maze = game_state['maze']
        self.maze_size = game_state['maze_size']

        game_state['player_position'] = self.init_player_pos()


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

    def move_player(self, event):   #todo: change name and description
        """Change the player's character's coordinates depending on the player's input.

        Args:
            event: The pressed key on the tkinter window.
        """
        self.check_collision()  # check collision with the current position of the player

        # get the new position corresponding to the pushed key
        x, y = self.game_state['player_position']
        if event.keysym == 'Up':
            new_position = (x, y - 1)
        elif event.keysym == 'Down':
            new_position = (x, y + 1)
        elif event.keysym == 'Left':
            new_position = (x - 1, y)
        elif event.keysym == 'Right':
            new_position = (x + 1, y)
        else:
            new_position = self.game_state['player_position']

        if self.maze[new_position[0]][new_position[1]].type != 'wall':
            self.game_state['player_position'] = new_position

        self.check_collision()  # check collision with the future position of the player

        self.gui.update_player(event.keysym)
        self.monster.move()

    def check_collision(self):
        """Check for collision of the player with game elements (traps, treasure or monsters).

        Args:
            future_position (tuple): position the player will be
        """
        if self.game_state['player_position'] == self.game_state['monster_position']:
            self.lose_life()

            self.game_state['monster_position'] = self.monster.init_monster_pos()

        #todo when traps are done using self.game_state['player_position']

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
        #
        if self.game_state['player_position'] == self.game_state['treasure_position']:
            self.mazeGame.end_game()

    def lose_life(self):
        """Decrease the player's life by one and check for game over."""
        self.game_state['life'] -= 1
        self.gui.update_life(0)
        if self.game_state['life'] <= 0:
            print("Game Over!")
            self.mazeGame.reset_maze()
